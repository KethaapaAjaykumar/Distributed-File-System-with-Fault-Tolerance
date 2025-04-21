import threading
import logging
from node_manager import NodeManager
from file_storage_manager import FileStorageManager
from replication_manager import ReplicationManager
from metadata_manager import MetadataManager
from fault_tolerance_manager import FaultToleranceManager
from security_manager import SecurityManager
from client_api import ClientAPI
from web_server import run_server

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    node_manager = NodeManager()
    file_manager = FileStorageManager()
    replication_manager = ReplicationManager(node_manager.get_active_nodes())
    metadata_manager = MetadataManager()
    fault_tolerance_manager = FaultToleranceManager(node_manager.get_active_nodes())
    security_manager = SecurityManager()
    client_api = ClientAPI(file_manager, replication_manager, metadata_manager, security_manager)

    # Get input from the user
    file_name = input("Enter the file name to upload (e.g., 'file.txt'): ")
    file_content = input("Enter the file content: ")

    # Upload and download the file
    file_hash = client_api.upload_file(file_name, file_content)
    downloaded_content = client_api.download_file(file_name, file_hash)

    print("\nFile created successfully")
    # print(downloaded_content) eneble this if you want to view content wtitten in that file 
    # Fault detection and recovery
    failed_nodes = fault_tolerance_manager.detect_failures()
    fault_tolerance_manager.auto_recover(failed_nodes)
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
