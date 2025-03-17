import logging
class NodeManager:
    def __init__(self):
        self.nodes = {}

    def register_node(self, node_id, address):
        if node_id in self.nodes:
            logging.warning(f"Node {node_id} is already registered.")
            return False
        self.nodes[node_id] = address
        logging.info(f"Node {node_id} registered successfully.")
        return True

    def get_active_nodes(self):
        return self.nodes
