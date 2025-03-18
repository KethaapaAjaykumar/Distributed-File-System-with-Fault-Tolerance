import socket
import time
import logging

class FaultToleranceManager:
    def __init__(self, nodes, max_retries=3):
        self.nodes = nodes
        self.max_retries = max_retries

    def detect_failures(self):
        failed_nodes = []
        for node in self.nodes:
            if not self._ping_node(node):
                failed_nodes.append(node)
                logging.warning(f"Node {node} is down!")
        return failed_nodes

    def _ping_node(self, node):
        try:
            socket.create_connection((node, 80), timeout=2)
            return True
        except Exception:
            return False

    def auto_recover(self, failed_nodes):
        for node in failed_nodes:
            for attempt in range(1, self.max_retries + 1):
                logging.info(f"Attempting to recover node {node}, Attempt {attempt}...")
                time.sleep(2)
                if self._ping_node(node):
                    logging.info(f"Node {node} recovered successfully.")
                    break
                if attempt == self.max_retries:
                    logging.error(f"Failed to recover node {node} after {self.max_retries} attempts.")
