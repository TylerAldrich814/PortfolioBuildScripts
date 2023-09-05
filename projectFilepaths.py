import os
import json
import logging

def build_and_upload_directory_tree(config, bucket):
    def test_extracted_files(extracted):
        def count_files(m):
            total_files = 0
            for key, value in m.items():
                if key == "files":
                    total_files += len(value)
                elif isinstance(value, dict):
                    total_files += count_files(value)
            return total_files

        detected = count_files(extracted)
        should_be = len(config.AcceptedFiles)

        if detected != should_be:
            raise ValueError(f"""
                You've opted to only copy over Accepted Files. Yet,
                we detected {detected} files extracted where there
                should be {should_be} files. Please check your
                "AcceptedFiles" array in 'projectSettings.yaml' for
                any grammatical errors.
            """);

    def extract_project_structure(startpath):
        structure = {}
        for root, _, files in os.walk(startpath):

            current = structure
            root_parts = root.replace(startpath, '').strip(os.sep).split(os.sep)

            filtered_files = [
                acceptedFile
                for file in files
                for ext in config.Extensions
                if file.endswith(ext) and (acceptedFile := config.filter_file(file)) if not None
            ]

            if not filtered_files:
                continue

            # Handles if there's files in the root directory.
            if root == startpath:
                current["files"] = filtered_files
                continue

            for part in root_parts:
                current = current.setdefault(part, {})

            current["files"] = filtered_files

        if config.OnlyAcceptedFiles:
            test_extracted_files(structure)

        extraction =  {config.SourceDir[:-1]: structure}
        return json.dumps(extraction, indent=2)


    sourceDir = config.RootDir + config.SourceDir
    logging.info(f" --> SourceDirectory => {sourceDir}")
    fileStructure = extract_project_structure(config.CompleteSrcDir)

    storage_path = f"{config.Bucket}/{config.Name.lower()}/{config.StructurePath}"
    bucket.upload_string_to_bucket(storage_path, fileStructure)
    bucket.generate_signed_url(storage_path)
