import os
import argparse

from termcolor import colored
from exif import Image


def parse_args():
    parser = argparse.ArgumentParser(description='Extract GPS coordinates from image EXIF data.')
    parser.add_argument('image_path', type=str, help='Path to the image file')
    return parser.parse_args()


def console_log(type, text):
    prefixes = {
        'error': '[-]',
        'warning': '[!]',
        'success': '[+]'
    }
    colors = {
        'error': 'red',
        'warning': 'yellow',
        'success': 'green'
    }
    
    if type in prefixes and type in colors:
        formatted_text = f"{prefixes[type]} {text}"
        print(colored(formatted_text, colors[type], attrs=['bold']))


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def display_logo():
    clear_screen()
    logo = r'''
                __                                
  _____   _____/  |______    _____ _____  ______  
 /     \_/ __ \   __\__  \  /     \\__  \ \____ \ 
|  Y Y  \  ___/|  |  / __ \|  Y Y  \/ __ \|  |_> >
|__|_|  /\___  >__| (____  /__|_|  (____  /   __/ 
      \/     \/          \/      \/     \/|__|    
'''
    print(colored(f"{logo}\n", color='cyan', attrs=['bold']))


def convert_to_decimal(coords, reference):
    degrees, minutes, seconds = coords
    decimal = degrees + (minutes / 60) + (seconds / 3600)
    if reference in ['S', 'W']:
        decimal *= -1
    return decimal


def get_coords(image_path):
    if not os.path.exists(image_path):
        console_log('error', 'File does not exist')
        return None
    
    try:
        with open(image_path, 'rb') as image_file:
            img = Image(image_file)
            if not img.has_exif:
                console_log('error', 'EXIF metadata not found')
                return None
            
            if img.gps_latitude and img.gps_longitude:
                latitude = convert_to_decimal(img.gps_latitude, img.gps_latitude_ref)
                longitude = convert_to_decimal(img.gps_longitude, img.gps_longitude_ref)
                return latitude, longitude
            
            console_log('error', 'Coordinates not found')
            return None
    except Exception as e:
        console_log('error', f"Error processing image: {e}")
        return None
    

def create_gmaps_link(coords):
    latitude, longitude = coords
    return f"https://www.google.com/maps?q={latitude},{longitude}"


def main():
    args = parse_args()
    display_logo()
    
    coords = get_coords(args.image_path)
    if coords:
        link = create_gmaps_link(coords)
        console_log('success', f"Found coordinates: Latitude: {coords[0]}, Longitude: {coords[1]}")
        console_log('success', f"Google maps: {link}")


if __name__ == '__main__':
    main()
