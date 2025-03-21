import os
import json
import logging
from http.server import SimpleHTTPRequestHandler, HTTPServer
from file_storage_manager import FileStorageManager

storage_manager = FileStorageManager()

class FileServer(SimpleHTTPRequestHandler):
    def do_GET(self):
        """Handles GET requests to list available files or serve a specific file."""
        if self.path == '/files':
            # List stored files
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            file_list = os.listdir(storage_manager.storage_dir)
            self.wfile.write(json.dumps(file_list).encode())
        elif self.path.startswith('/download/'):
            # Serve a specific file
            filename = self.path.split('/')[-1]
            file_content = storage_manager.retrieve_file(filename)
            if file_content:
                self.send_response(200)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(file_content.encode())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"File not found")
        else:
            super().do_GET()  # Serve static files normally

    def do_POST(self):
        """Handles file replication via POST requests."""
        if self.path == "/replicate":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode())
                filename = data.get("filename")
                content = data.get("content")

                if filename and content:
                    storage_manager.store_file(filename, content)
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b"File replicated successfully")
                    logging.info(f"Replicated file '{filename}' successfully.")
                else:
                    raise ValueError("Invalid JSON data received")
            except Exception as e:
                logging.error(f"Replication failed: {e}")
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Bad request")
        else:
            self.send_response(404)
            self.end_headers()

def run_server(port=8000):
    """Starts the HTTP server."""
    server_address = ('', port)
    httpd = HTTPServer(server_address, FileServer)
    logging.info(f"File server running on port {port}")
    httpd.serve_forever()
