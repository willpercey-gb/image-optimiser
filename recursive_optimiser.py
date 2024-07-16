from PIL import Image, ImageOps
import os
import sys

# Pretty exception handling in the terminal
import traceback

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    print("".join(traceback.format_exception(exc_type, exc_value, exc_traceback)))

sys.excepthook = handle_exception

def process_images(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_path = os.path.join(root, file)
                try:
                    img = Image.open(file_path)
                    img = ImageOps.exif_transpose(img)  # orientate

                    # Get original dimensions
                    original_width, original_height = img.size

                    # Determine new dimensions
                    new_width = 1000
                    new_height = int((original_height * new_width) / original_width)

                    # Resize only if the original width is greater than 1000px
                    if original_width > new_width:
                        img = img.resize((new_width, new_height), Image.LANCZOS)

                    # Strip EXIF data
                    data = list(img.getdata())
                    img_without_exif = Image.new(img.mode, img.size)
                    img_without_exif.putdata(data)

                    # Save as JPEG
                    if file.lower().endswith('.png'):
                        new_file_path = os.path.splitext(file_path)[0] + '.jpg'
                    else:
                        new_file_path = file_path

                    img_without_exif = img_without_exif.convert('RGB')
                    img_without_exif.save(new_file_path, format='JPEG', quality=85, optimize=True)

                    # Remove original PNG file if converted
                    if file.lower().endswith('.png'):
                        os.remove(file_path)

                except Exception as e:
                    print(f"Failed to process {file_path}: {e}")

if __name__ == "__main__":
    directory = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))
    print (f"Processing images in {directory}")
    process_images(directory)
