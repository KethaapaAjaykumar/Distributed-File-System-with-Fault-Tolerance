import logging
from file_storage_manager import FileStorageManager
from replication_manager import ReplicationManager
from metadata_manager import MetadataManager 
from security_manager import SecurityManager

class ClientAPI:
    def __init__(self, file_manager, replication_manager, metadata_manager, security_manager):
        self.file_manager = file_manager
        self.replication_manager = replication_manager
        self.metadata_manager = metadata_manager
        self.security_manager = security_manager

    def upload_file(self, filename, content):
        try:
            file_hash = self.file_manager.store_file(filename, content)
            if file_hash:
                self.replication_manager.replicate_file(filename, content)
                self.metadata_manager.update_metadata(filename, "Node_1")
                return file_hash
            return None
        except Exception as e:
            logging.error(f"Error uploading file '{filename}': {e}")
            return None

    def download_file(self, filename, expected_hash):
        try:
            content = self.file_manager.retrieve_file(filename)
            if content and self.security_manager.verify_integrity(content, expected_hash):
                return content
            logging.warning(f"File '{filename}' integrity compromised or not found.")
            return None
        except Exception as e:
            logging.error(f"Error downloading file '{filename}': {e}")
            return None
