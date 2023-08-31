import os

def CopySourceToBucket(config, bucket):
    print("  --> Starting Source Directory Deep Copy.")
    storage_path = f"portfolio/{config.Name.lower()}/{config.SourceDir}"

    settingsPath  = os.path.dirname(os.path.abspath(__file__))

    for root, _, files in os.walk(settingsPath + "/../" + config.SourceDir):

        for file in files:
            _, ext = os.path.splitext(file)

            # Ignore all Ignored Extensions
            if ext not in config.Extensions:
                continue;

            local_file_path = os.path.join(root, file)
            childPath = local_file_path.split(config.SourceDir)[1]
            blob_path = storage_path + childPath

            blob = bucket.blob(blob_path)
            blob.upload_from_filename(local_file_path)
            print(f" --> {blob_path} has been uploaded to Firebase Storage")
