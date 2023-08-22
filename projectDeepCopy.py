import os

def CopySourceToBucket(config, bucket):
    print("  --> Starting Source Directory Deep Copy.")
    storage_path = f"portfolio/{config.Name.lower()}/{config.SourceDir}"

    settingsPath  = os.path.dirname(os.path.abspath(__file__))

    print(" ----> " + settingsPath + "/../" + config.SourceDir)

    for root, _, files in os.walk(settingsPath + "/../" + config.SourceDir):
        print(f"  --> root: {root} files: {files}")
        for file in files:
            _, ext = os.path.splitext(file)
            if ext not in config.Extensions:
                # print(f" -> File '${file}' Ignrored.")
                continue;

            local_file_path = os.path.join(root, file)
            blob_path = os.path.join(
                storage_path,
                os.path.relpath(
                    local_file_path,
                    config.SourceDir
                )
            )

            blob = bucket.blob(blob_path)
            blob.upload_from_filename(local_file_path)
            print(f'{local_file_path} uplodated to {blob_path}')
