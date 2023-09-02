import os
import json

def BuildAndUploadDirectoryTree(config, bucket):
    def extractProjectStructure(startpath):
        structure = {}

        for root, _, files in os.walk(startpath):
            current = structure
            root_parts = root.replace(startpath, '').strip(os.sep).split(os.sep)
            filtered_files = [file for file in files if any(file.endswith(ext) for ext in config.Extensions)]

            if not filtered_files:
                continue

            # Handles if there's fiels in the root directory.
            if root == startpath:
                current["files"] = filtered_files
                continue

            for part in root_parts:
                current = current.setdefault(part, {})

            current["files"] = filtered_files

        extraction =  {config.SourceDir[:-1]: structure}
        return json.dumps(extraction, indent=2)

    sourceDir = config.RootDir + config.SourceDir
    print(f" -> SourceDirectory => {sourceDir}")
    fileStructure = extractProjectStructure(config.CompleteSrcDir)
    storage_path = f"{config.BucketName}/{config.Name.lower()}/structure/directories.json"

    blob = bucket.blob(storage_path)
    blob.upload_from_string(fileStructure)
    bucket.generate_signed_url(blob)
