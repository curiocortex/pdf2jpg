"""
pdf_to_jpg_converter.py

A Python script that converts PDF files in a specified directory to a series of JPG images.

Usage:
    1. Replace 'input_folder' with the path to the directory containing PDF files.
    2. Set 'output_folder' to the desired location where you want to save the JPG images.
    3. Run the script.

Requirements:
    - pdf2image
    - Pillow

Installation:
    pip install pdf2image Pillow
"""

from pdf2image import convert_from_path
import os
from utils import MyLogger

logger = MyLogger()


class PDFtoJPGConverter:
    def __init__(self, input_directory, output_directory):
        """
        Initialize the PDFtoJPGConverter instance.

        Parameters:
            input_directory (str): Path to the directory containing PDF files.
            output_directory (str): Path to the directory where JPG images will be saved.
        """
        self.input_directory = input_directory
        self.output_directory = output_directory

    def convert_pdfs_to_jpg(self):
        """
        Convert PDF files in the input directory to JPG images and save them in the output directory.
        """
        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

        # Get a list of existing PDF file names (excluding index) in the output directory
        existing_pdfs = [folder_name.split('_', 1)[1] for folder_name in os.listdir(self.output_directory)]

        # Get the highest existing number in the output directory
        existing_numbers = [int(folder_name.split('_')[0]) for folder_name in os.listdir(self.output_directory) if
                            folder_name.split('_')[0].isdigit()]  # Filter out non-integer folder names
        highest_existing_number = max(existing_numbers, default=0)

        # Iterate through PDF files in the input directory
        for index, pdf_file_name in enumerate(os.listdir(self.input_directory), start=highest_existing_number + 1):
            if pdf_file_name.lower().endswith('.pdf'):
                pdf_file_path = os.path.join(self.input_directory, pdf_file_name)

                # Skip conversion if PDF already converted
                if os.path.splitext(pdf_file_name)[0] not in existing_pdfs:
                    output_directory = os.path.join(self.output_directory,
                                                    f"{index}_{os.path.splitext(pdf_file_name)[0]}")

                    # Convert PDF to images
                    images = convert_from_path(pdf_file_path)

                    # Create output folder for the current PDF file
                    if not os.path.exists(output_directory):
                        os.makedirs(output_directory)

                    # Save each image as a JPG file
                    for i, image in enumerate(images):
                        jpg_path = os.path.join(output_directory, f'page_{i + 1}.jpg')
                        image.save(jpg_path, 'JPEG')

                    logger.info(
                        f'Conversion complete for {pdf_file_name}. {len(images)} JPG images saved in {output_directory}')
                else:
                    logger.info(f'Skipping {pdf_file_name}. Already converted in a previous run.')



