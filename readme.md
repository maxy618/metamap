# MetaMap 📍

A simple Python utility for extracting GPS coordinates from image EXIF metadata and generating a Google Maps link.

---

## Features

* Extracts GPS coordinates (latitude and longitude) from image EXIF metadata
* Converts DMS (degrees, minutes, seconds) format to decimal
* Generates a direct Google Maps link for the location
* Colorful console output using `termcolor`
* ASCII logo on startup

---

## Example

```bash
python metamap.py path/to/image.jpg
```

Example output:

```
[+] Found coordinates: Latitude: 23.7558, Longitude: 45.6173
[+] Google maps: https://www.google.com/maps?q=23.7558,45.6173
```

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/metamap.git
cd metamap
```

2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

---

## Requirements

* Python 3.8+
* Packages listed in `requirements.txt`:

  * `exif`
  * `termcolor`

---

## How It Works

The program reads the EXIF metadata of an image, extracts GPS coordinates (if available), converts them to decimal format, and generates a direct Google Maps link for the location.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Author

Made with ❤️ by [maxy618](https://github.com/maxy618)
