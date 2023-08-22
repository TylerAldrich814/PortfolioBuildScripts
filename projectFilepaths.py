import os
import json

def BuildAndUploadDirectoryTree(config, bucket):
    def extractProjectStructure(startpath):
        structure = {}

        for root, _, files in os.walk(startpath):
            current = structure
            root_parts = root.replace(startpath, '').split(os.sep)[1:]
            parent = structure

            for part in root_parts[:-1]:
                parent = parent.setdefault(part, {})

            last_part = root_parts[-1] if root_parts else None

            for part in root_parts:
                current = current.setdefault(part, {})

            current["files"] = [file for file in files if any(file.endswith(ext) for ext in config.Extensions)]

            if not current["files"]:
                if last_part:
                    parent.pop(last_part, None)
                else:
                    structure.clear()

        extraction =  {config.RootDir[2:]: structure}
        return json.dumps(extraction, indent=2)

    sourDir = config.RootDir + config.SourceDir
    print(sourDir)
    fileStructure = extractProjectStructure(config.CompleteSrcDir)

    storage_path = f"portfolio/{config.Name.lower()}/structure/directories.json"

    blob = bucket.blob(storage_path)
    blob.upload_from_string(fileStructure)
    bucket.generate_signed_url(blob)


