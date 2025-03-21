import os
import logging
import hashlib

class FileStorageManager:
    def __init__(self, storage_dir="storage"):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)
        logging.info(f"Storage directory set to: {self.storage_dir}")

    def hash_content(self, content):
        return hashlib.sha256(content.encode()).hexdigest()

    def store_file(self, filename, content):
        file_path = os.path.join(self.storage_dir, filename)
        try:
            with open(file_path, "w") as f:
                f.write(content)
            logging.info(f"File '{filename}' stored successfully.")
            return self.hash_content(content)
        except Exception as e:
            logging.error(f"Failed to store file '{filename}': {e}")
            return None

    def retrieve_file(self, filename):
        file_path = os.path.join(self.storage_dir, filename)
        try:
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    return f.read()
            logging.warning(f"File '{filename}' not found.")
            return None
        except Exception as e:
            logging.error(f"Error retrieving file '{filename}': {e}")
            return None
