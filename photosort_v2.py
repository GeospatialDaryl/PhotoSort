import os
import sys
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS

# Function to extract the date from the image's EXIF data
def get_image_date(image_path):
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()

        if exif_data:
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                if tag_name == "DateTimeOriginal":
                    date_taken = value
                    date_format = datetime.strptime(date_taken, "%Y:%m:%d %H:%M:%S")
                    return date_format.strftime('%Y-%m-%d')
        
        # If EXIF data is not available, fall back to file's modification date
        mod_time = os.path.getmtime(image_path)
        return datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d')

    except Exception as e:
        print(f"Error getting date for {image_path}: {e}")
        return None

# Function to create folders and move images and videos
def sort_files(directory):
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.heic', '.mp4', '.mov', '.avi', '.mkv')):
            file_path = os.path.join(directory, filename)
            
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.heic')):
                date_folder = get_image_date(file_path)
            else:
                # Use modification date for videos
                mod_time = os.path.getmtime(file_path)
                date_folder = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d')

            if date_folder:
                folder_path = os.path.join(directory, date_folder)
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)

                # Move the file to the folder
                new_path = os.path.join(folder_path, filename)
                os.rename(file_path, new_path)
                print(f"Moved {filename} to {date_folder}")

# Main function to handle the argument
def main():
    if len(sys.argv) < 2:
        print("Please provide the directory path containing the images and videos.")
        sys.exit(1)

    image_directory = sys.argv[1]

    if not os.path.isdir(image_directory):
        print("The provided path is not a valid directory.")
        sys.exit(1)

    # Sort the images and videos
    sort_files(image_directory)

if __name__ == "__main__":
    main()
