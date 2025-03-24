import logging
import requests

class ReplicationManager:
    def __init__(self, nodes):
        self.nodes = nodes

    def replicate_file(self, filename, content):
        for node in self.nodes.values():
            success = self._send_to_node(node, filename, content)
            if not success:
                logging.warning(f"Failed to replicate {filename} to {node}")

    def _send_to_node(self, node, filename, content):
        try:
            response = requests.post(
                f"http://{node}/replicate",
                json={"filename": filename, "content": content},
                timeout=3
            )
            if response.status_code == 200:
                logging.info(f"Successfully replicated {filename} to {node}")
                return True
            else:
                logging.error(f"Failed to replicate {filename} to {node}. Response: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            logging.error(f"Replication error for {node}: {e}")
            return False
