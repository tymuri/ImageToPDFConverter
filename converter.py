import os
import subprocess
from PIL import Image
import tempfile
from PyPDF2 import PdfMerger


def convert_heic_to_jpeg(heic_path, jpeg_path):
    # Convert HEIC to JPEG
    subprocess.run(['sips', '-s', 'format', 'jpeg', heic_path, '--out', jpeg_path], check=True)


def convert_jpeg_to_pdf(jpeg_path, pdf_path):
    # Convert JPEG to PDF
    with Image.open(jpeg_path) as img:
        img = img.convert("RGB")
        img.save(pdf_path, "PDF", resolution=100.0)


def merge_pdfs(paths, output):
    # Merge PDFs
    merger = PdfMerger()
    for pdf in paths:
        merger.append(pdf)
    merger.write(output)
    merger.close()


def convert_and_merge(source_folder, output_folder, merged_pdf_name):
    temp_dir = tempfile.TemporaryDirectory()
    pdf_paths = []

    for filename in os.listdir(source_folder):
        if filename.lower().endswith(".heic"):
            source_path = os.path.join(source_folder, filename)
            temp_jpeg_path = os.path.join(temp_dir.name, f"{filename[:-5]}.jpg")
            pdf_path = os.path.join(output_folder, f"{filename[:-5]}.pdf")
            convert_heic_to_jpeg(source_path, temp_jpeg_path)
            convert_jpeg_to_pdf(temp_jpeg_path, pdf_path)
            pdf_paths.append(pdf_path)
            print(f"Converted '{filename}' to PDF.")

    # Merge all PDFs into one
    merged_pdf_path = os.path.join(output_folder, merged_pdf_name)
    merge_pdfs(pdf_paths, merged_pdf_path)
    print(f"All PDF files have been merged into '{merged_pdf_path}'.")

    # Cleanup temporary directory
    temp_dir.cleanup()


source_folder = '/Users/tim/repos/img_to_pdf/source_images'
output_folder = '/Users/tim/repos/img_to_pdf/output_pdf'
merged_pdf_name = 'merged.pdf'
convert_and_merge(source_folder, output_folder, merged_pdf_name)