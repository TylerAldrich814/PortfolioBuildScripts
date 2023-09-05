import datetime
import firebase_admin
import logging
from firebase_admin import credentials, storage, firestore
from google.cloud.exceptions import Forbidden, GoogleCloudError, NotFound

class Firebase():
    def __init__(self, cred, bucket_path):
        cred = credentials.Certificate(cred)
        firebase_admin.initialize_app(cred, {
            'storageBucket' : f"{bucket_path}"
        })

        self.bucket = storage.bucket()
        self.db = firestore.client()

        logging.info(" --> SUCCESSFULLY INITIALIZED FIREBASE APP.")

    def generate_signed_url(self, bucket_path):
        url = self.__wrapped_firebase_error_handler__(
            lambda blob: blob.\
                generate_signed_url(
                    expiration=datetime.timedelta(seconds=300)
                ),
            bucket_path
        )
        logging.info(f" --> File has been created @ \"{url}\"")

    def upload_file_to_bucket(self, bucket_path, file_path):
        self.__wrapped_firebase_error_handler__(
            func=lambda blob: blob.upload_from_filename(file_path),
            bucket_path=bucket_path
        )
        logging.info(f" --> Uploaded: \"{file_path}\" ->> {bucket_path}")

    def upload_string_to_bucket(self, bucket_path, string):
        self.__wrapped_firebase_error_handler__(
            func=lambda blob: blob.upload_from_string(string),
            bucket_path=bucket_path
        )
        logging.info(f" --> Uploaded: Project Structure to {bucket_path}")

    def add_to_collection(self, collection, document, info):
        self.__wrapped_firebase_error_handler__(
            func=lambda: self.db.\
                collection(collection)\
                .document(document)\
                .set(info, merge=True),
        )
        project = list(info.keys())[0]
        logging.info(f" --> Successfully uploaded your project information to Firestore @ \"{collection}/{document}/{project}\"")

    def __wrapped_firebase_error_handler__(self,func,bucket_path=None):
        try:
            # -> Uploading to Firebase Storage
            if bucket_path is not None:
                blob = self.bucket.blob(bucket_path)
                return func(blob)
            # -> Uploading to Firebase Firestore
            else:
                func()
        except NotFound as e:
            logging.error(f" --> !Bucket path({bucket_path}) or blob not found: {e}")
        except Forbidden as e:
            logging.error(f" --> !Insufficient permissions to upload to bucket: {e}")
        except GoogleCloudError as e:
            logging.error(f" --> !An error occurred with Google Cloud Storage: {e}")
        except Exception as e:
            logging.error(f" --> !An unexpected error occurred: {e}")

