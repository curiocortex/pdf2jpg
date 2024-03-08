import logging
from minio.error import S3Error
from pdf_to_jpg_converter import PDFtoJPGConverter
from utils import PDFImageUploader


def convert_pdfs_to_jpg(input_folder_path, output_folder_path):
    pdf_converter = PDFtoJPGConverter(input_folder_path, output_folder_path)
    pdf_converter.convert_pdfs_to_jpg()


def main():
    try:
        pdf_folder_path = '../pdffiles'
        image_folder_path = '../imagefiles'
        minio_server = "storage.smartixai.com"
        access_key = "u42yUSysaBLdGsksUTNp"
        secret_key = "v0yENLvTeevWxuqVIexVYEib3PJpJ9kzbsd40XO5"
        bucket_name = "ocr"
        folder_name = "pdf_images"

        # Convert PDFs to JPGs
        convert_pdfs_to_jpg(pdf_folder_path, image_folder_path)

        # Upload PDFs' images to MinIO with specified folder and subfolders
        uploader = PDFImageUploader(minio_server, access_key, secret_key, bucket_name, folder_name)
        uploader.create_bucket()
        uploader.upload_folder_to_minio(image_folder_path)

    except S3Error as exc:
        logging.error("Error occurred. %s", exc)


if __name__ == "__main__":
    main()
