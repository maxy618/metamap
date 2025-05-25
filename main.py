import os
import sys
import argparse

from termcolor import colored
from exif import Image


def parse_args():
    parser = argparse.ArgumentParser(description='Extract GPS coordinates from image EXIF data.')
    parser.add_argument('image_paths', nargs='+', type=str, 
                      help='Path(s) to one or more image files separated with spaces')
    parser.add_argument('--full', action='store_true', 
                      help='Show all EXIF metadata (only allowed with a single image)')
    return parser.parse_args()


def console_log(type, text):
    prefixes = {
        'error': '[-]',
        'warning': '[!]',
        'success': '[+]',
        'info': '[i]'
    }
    colors = {
        'error': 'red',
        'warning': 'yellow',
        'success': 'green',
        'info': 'blue'
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


def get_exif_data(image_path):
    if not os.path.exists(image_path):
        console_log('error', f'File does not exist: {image_path}')
        return None
    
    try:
        with open(image_path, 'rb') as image_file:
            img = Image(image_file)
            if not getattr(img, 'has_exif', False):
                console_log('warning', f'EXIF metadata not found in: {image_path}')
                return None
            return img
    except Exception as e:
        console_log('error', f"Error processing image {image_path}: {e}")
        return None


def get_coords(img):
    try:
        lat = getattr(img, 'gps_latitude', None)
        lat_ref = getattr(img, 'gps_latitude_ref', None)
        lon = getattr(img, 'gps_longitude', None)
        lon_ref = getattr(img, 'gps_longitude_ref', None)
        if lat and lon and lat_ref and lon_ref:
            latitude = convert_to_decimal(lat, lat_ref)
            longitude = convert_to_decimal(lon, lon_ref)
            return (latitude, longitude)
    except Exception:
        pass
    return None


def create_gmaps_link(coords):
    latitude, longitude = coords
    return f"https://www.google.com/maps?q={latitude},{longitude}"


def print_all_exif(img, image_path):
    console_log('info', f"\nEXIF metadata for {image_path}:")
    tags = sorted(img.list_all()) if hasattr(img, 'list_all') else []
    if not tags:
        console_log('warning', 'No EXIF tags found.')
        return
    for tag in tags:
        try:
            value = getattr(img, tag)
            print(f"  {tag}: {value}")
        except Exception:
            continue


def main():
    args = parse_args()
    display_logo()
    if args.full and len(args.image_paths) != 1:
        console_log('error', "The --full option can only be used with exactly one image.")
        sys.exit(1)

    coords_to_files = {}
    files_without_coords = []

    for image_path in args.image_paths:
        img = get_exif_data(image_path)
        if img is None:
            continue
            
        if args.full:
            print_all_exif(img, image_path)

        coords = get_coords(img)
        if coords:
            coords_to_files.setdefault(coords, []).append(image_path)
        else:
            files_without_coords.append(image_path)

    if coords_to_files:
        console_log('success', "\nUnique GPS coordinates found:")
        for coords, files in coords_to_files.items():
            console_log('info', f"Coordinates: {coords[0]}, {coords[1]}")
            console_log('info', f"Google Maps: {create_gmaps_link(coords)}")
            console_log('info', f"Files with these coordinates ({len(files)}):")
            for file in files:
                print(f"    {file}")
    else:
        console_log('warning', "No GPS data found in any of the files.")

    if files_without_coords:
        console_log('warning', f"\nFiles without GPS data ({len(files_without_coords)}):")
        for file in files_without_coords:
            print(f"    {file}")


if __name__ == '__main__':
    main()