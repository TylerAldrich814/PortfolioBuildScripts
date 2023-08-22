import firebase_admin
from firebase_admin import credentials, datetime, storage

class FirebaseBucket():
    def __init__(self, cred, bucketPath):
        cred = credentials.Certificate(cred)
        firebase_admin.initialize_app(cred, {
            'storageBucket' : f"{bucketPath}"
        })
        self.bucket = storage.bucket()
        print(" -> SUCCESSFULLY INITIALIZED FIREBASE APP.")

    def generate_signed_url(self, blob):
        url = blob.generate_signed_url(expiration=datetime.timedelta(seconds=300))
        print(f"File has been created @ \"{url}\"")

    def blob(self, path):
        return self.bucket.blob(path)
