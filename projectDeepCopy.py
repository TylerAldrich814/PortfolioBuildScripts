import logging
import os

def copy_source_to_bucket(config, firebase):
    logging.info("  --> Starting Source Directory Deep Copy.")
    storage_path = f"{config.Bucket}/{config.Name.lower()}/{config.SourceDir}"

    settingsPath  = os.path.dirname(os.path.abspath(__file__))

    for root, _, files in os.walk(settingsPath + "/../" + config.SourceDir):
        currentDir = os.path.basename(root)
        if currentDir in config.IgnoreDirs:
            continue

        for file in files:
            if not config.filter_file(file):
                continue
            _, ext = os.path.splitext(file)

            # Ignore all Ignored Extensions
            if ext not in config.Extensions:
                continue;

            local_file_path = os.path.join(root, file)
            childPath = local_file_path.split(config.SourceDir)[1]
            bucket_path = storage_path + childPath

            logging.info(" --> BEFORE upload_file_to_bucket")
            firebase.upload_file_to_bucket(
                bucket_path=bucket_path,
                file_path=local_file_path,
            )
            logging.info(f" --> {bucket_path} has been uploaded to Firebase Storage")
