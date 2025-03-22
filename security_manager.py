import hashlib
import logging

class SecurityManager:
    def hash_content(self, content):
        return hashlib.sha256(content.encode()).hexdigest()

    def verify_integrity(self, content, expected_hash):
        calculated_hash = self.hash_content(content)
        is_valid = calculated_hash == expected_hash
        if not is_valid:
            logging.warning("File integrity check failed!")
        return is_valid

