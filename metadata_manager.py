import logging

class MetadataManager:
    def __init__(self):
        self.metadata = {}

    def update_metadata(self, filename, location):
        """ Updates metadata with the storage location of a file. """
        self.metadata[filename] = location
        logging.info(f"Metadata updated: {filename} -> {location}")

    def get_file_location(self, filename):
        """ Retrieves the storage location of a file. """
        location = self.metadata.get(filename)
        if location:
            logging.info(f"File '{filename}' is located at: {location}")
        else:
            logging.warning(f"File '{filename}' location not found in metadata.")
        return location
