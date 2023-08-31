from projectDeepCopy import CopySourceToBucket
from firebaseInit import FirebaseBucket
from projectConfig import ProjectConfig
from projectFilepaths import BuildAndUploadDirectoryTree
import argparse
import os


if __name__ == "__main__":
    def main():
        parser = argparse.ArgumentParser(description="Arguemnts for either rebuilding your porjects Directory-Tree json file, Uploading your source code to Firestore, or both.")
        parser.add_argument('--build_tree', '-bt', action="store_true", help="Rebuilds your projects Directory Tree, and uploads the \"directories.json\" to Firebase Cloud")
        parser.add_argument('--deep_copy', '-dc', action="store_true", help="Walks your source Directory, and deep copies the same exact directory structure along with files with the correct extension to Firebase Cloud. Ignoring any Specified Files.")
        parser.add_argument('--run_all', '-ra', action="store_true", help="Will run both \"--build_tree\" functions.")

        args = parser.parse_args()

        filePath  = os.path.dirname(os.path.abspath(__file__))

        settingsPath = filePath + "/projectSettings.yaml"
        config = ProjectConfig(settingsPath)

        credPath = filePath + config.CredentialsPath + config.FirebaseCred
        print(config.CredentialsPath)
        print(credPath)
        bucket = FirebaseBucket(credPath, config.BucketPath)

        print(f" settingsPath = {settingsPath}")
        print(f"     CredPath = {credPath}")

        if args.build_tree:
            print(f' --> Building a new Directory tree and Uploading it to your Firebase Bucket path @ \"{config.BucketPath}\"')
            BuildAndUploadDirectoryTree(config, bucket)
            return

        if args.deep_copy:
            print(f" --> Walking your Source Directory, and copying it's exact structure to your Firebase Bucket path @ \"{config.BucketPath}\"")
            CopySourceToBucket(config, bucket)

        if args.run_all:
            print(f"""
    --> First, we're building a new Directory,""")
            print(f"""
    --> next We'll walk your source
        Directory and deep copy the strucutre and selected files to your
        Firebase Storage Bucket @ \"{config.BucketPath}\"""")
            BuildAndUploadDirectoryTree(config, bucket)
            CopySourceToBucket(config, bucket)
            return
#---------------
    main()
