import io
import logging
import os

from minio import Minio, S3Error


class MyLogger:
    _instance = None

    def __new__(cls, log_file_name="my_log.log", log_level=logging.DEBUG):
        if cls._instance is None:
            cls._instance = super(MyLogger, cls).__new__(cls)
            cls._instance.logger = logging.getLogger(__name__)
            cls._instance.logger.setLevel(log_level)
            cls._instance.logger.propagate = False

            # Create a formatter
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

            # Create a file handler and set the formatter
            log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), log_file_name)
            file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
            file_handler.setFormatter(formatter)

            # Create a stream handler and set the formatter
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)

            # Add the handlers to the logger
            cls._instance.logger.addHandler(file_handler)
            cls._instance.logger.addHandler(stream_handler)

        return cls._instance.logger


class PDFImageUploader:
    def __init__(self, minio_server, access_key, secret_key, bucket_name, folder_name):
        self.minio_client = Minio(
            minio_server,
            access_key=access_key,
            secret_key=secret_key,
        )
        self.bucket_name = bucket_name
        self.folder_name = folder_name
        self.logger = MyLogger()

    def create_bucket(self):
        if not self.minio_client.bucket_exists(self.bucket_name):
            self.minio_client.make_bucket(self.bucket_name)
            self.logger.info("Created bucket %s", self.bucket_name)
        else:
            self.logger.info("Bucket %s already exists", self.bucket_name)

    def object_exists(self, object_name):
        try:
            self.minio_client.stat_object(self.bucket_name, object_name)
            return True
        except S3Error as e:
            if e.code == 'NoSuchKey':
                return False
            else:
                raise

    def upload_image_to_minio(self, source_file, destination_file):
        if not self.object_exists(destination_file):
            with open(source_file, 'rb') as data:
                data_length = os.path.getsize(source_file)
                self.minio_client.put_object(self.bucket_name, destination_file, data, data_length)
                self.logger.info(
                    "%s successfully uploaded as object %s to bucket %s",
                    source_file, destination_file, self.bucket_name
                )
        else:
            self.logger.info("Object %s already exists in bucket %s. Skipping upload.", destination_file,
                             self.bucket_name)

    def upload_folder_to_minio(self, image_folder):
        for root, dirs, files in os.walk(image_folder):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg')):
                    source_file = os.path.join(root, file)
                    relative_folder = os.path.relpath(root, image_folder)
                    destination_folder = os.path.join(self.folder_name, relative_folder)
                    destination_file = os.path.join(destination_folder, file)
                    self.upload_image_to_minio(source_file, destination_file)
