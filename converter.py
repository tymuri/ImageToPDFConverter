import os
import subprocess
from PIL import Image
import tempfile


def convert_heic_to_jpeg(heic_path, jpeg_path):
    # Convert HEIC to JPEG using the sips command
    subprocess.run(['sips', '-s', 'format', 'jpeg', heic_path, '--out', jpeg_path], check=True)


def convert_jpeg_to_pdf(jpeg_path, pdf_path):
    # Open the JPEG file
    with Image.open(jpeg_path) as img:
        # Convert image to RGB (necessary for some image formats)
        img = img.convert("RGB")
        # Create a PDF file for the image
        img.save(pdf_path, "PDF", resolution=100.0)


def convert_heic_to_pdf(source_folder, output_folder):
    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Use a temporary directory for intermediate JPEG files
    with tempfile.TemporaryDirectory() as temp_dir:
        for filename in os.listdir(source_folder):
            if filename.lower().endswith(".heic"):
                source_path = os.path.join(source_folder, filename)
                temp_jpeg_path = os.path.join(temp_dir, f"{filename[:-5]}.jpg")
                output_path = os.path.join(output_folder, f"{filename[:-5]}.pdf")

                try:
                    # Convert HEIC to JPEG
                    convert_heic_to_jpeg(source_path, temp_jpeg_path)
                    # Convert JPEG to PDF
                    convert_jpeg_to_pdf(temp_jpeg_path, output_path)
                    print(f"Converted '{filename}' to PDF.")
                except Exception as e:
                    print(f"Failed to convert '{filename}': {e}")


source_folder = '/Users/tim/repos/img_to_pdf/source_images'
output_folder = '/Users/tim/repos/img_to_pdf/output_pdf'
convert_heic_to_pdf(source_folder, output_folder)