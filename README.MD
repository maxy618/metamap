# MetaMap 📍

A simple Python utility for extracting GPS coordinates from image EXIF metadata, displaying full EXIF tags for a single image, and generating Google Maps links.

---

## Features

* **GPS Extraction:** Extracts GPS coordinates (latitude and longitude) from image EXIF metadata.
* **DMS to Decimal:** Converts DMS (degrees, minutes, seconds) format to decimal.
* **Google Maps Link:** Generates a direct Google Maps link for the extracted location.
* **Full EXIF Dump:** When using the `--full` flag with a single image, prints all available EXIF tags in a readable, sorted list.
* **Batch Processing:** Process multiple images at once; coordinates are grouped by unique location, and files without GPS data are listed separately.

---

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/maxy618/metamap.git
   cd metamap
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

```bash
python metamap.py [image_paths...] [--full]
```

* `image_paths`: One or more paths to image files (separated by spaces).
* `--full`: Optional flag. When provided, prints all EXIF metadata **only if exactly one** image path is given. If used with multiple images, the program will exit with an error.

### Examples

* **Extract GPS from a single image:**

  ```bash
  python metamap.py photo1.jpg
  ```

  Output:

  ```
  [+] Unique GPS coordinates found:
  [i] Coordinates: 48.8584, 2.2945
  [i] Google Maps: https://www.google.com/maps?q=48.8584,2.2945
  ```

* **Full EXIF for one image:**

  ```bash
  python metamap.py photo1.jpg --full
  ```

  Output:

  ```
  [i] EXIF metadata for photo1.jpg:
    ApertureValue: 2.8
    DateTimeOriginal: 2025-05-10 14:23:11
    GPSLatitude: (48, 51, 29.04)
    GPSLatitudeRef: N
    GPSLongitude: (2, 17, 39.6)
    GPSLongitudeRef: E
    ...
  ```

* **Batch processing multiple images:**

  ```bash
  python metamap.py img1.jpg img2.jpg img3.jpg
  ```

  * Groups images by identical coordinates
  * Lists files without GPS data separately

---

## Requirements

* **Python:** 3.8 or higher
* **Dependencies:** Listed in `requirements.txt`:

  * `exif`
  * `termcolor`

---

## How It Works

1. **Load EXIF:** Opens each image in binary mode and reads EXIF metadata using the `exif` library.
2. **GPS Parsing:** Safely retrieves GPS tags (latitude, longitude, and their references) via `getattr`, avoiding errors if tags are missing.
3. **Conversion:** Converts DMS tuples into decimal degrees, applying negative signs for S/W references.
4. **Output:**

   * If `--full` is provided for a single image, lists all EXIF tags (sorted alphabetically).
   * Otherwise, aggregates GPS coordinates across images, prints unique locations with Google Maps links, and reports files without GPS data.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Author

Made with ❤️ by [maxy618](https://github.com/maxy618)
