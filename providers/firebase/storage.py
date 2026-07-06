from firebase_admin import storage
from datetime import timedelta
import uuid

class FirebaseStorageProvider:
    def __init__(self):
        self.bucket = storage.bucket()

    def upload_file(self, file_content, destination_path: str, content_type: str):
        blob = self.bucket.blob(destination_path)
        blob.upload_from_string(file_content, content_type=content_type)
        # Make the blob publicly available for a certain time
        return blob.generate_signed_url(expiration=timedelta(hours=24), method='GET')

    def delete_file(self, file_path: str):
        blob = self.bucket.blob(file_path)
        blob.delete()

firebase_storage = FirebaseStorageProvider()
