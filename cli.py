from projectDeepCopy import copy_source_to_bucket
from firebaseInit import Firebase
from projectConfig import ProjectConfig
from projectFilepaths import build_and_upload_directory_tree
from projectData import upload_project_information
import logging
import argparse
import os


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    def main():
        parser = argparse.ArgumentParser(description="Arguemnts for either rebuilding your porjects Directory-Tree json file, Uploading your source code to Firestore, or both.")
        parser.add_argument('--build-tree', '-bt', action="store_true", help="Rebuilds your projects Directory Tree, and uploads the \"directories.json\" to Firebase Cloud")
        parser.add_argument('--deep-copy', '-dc', action="store_true", help="Walks your source Directory, and deep copies the same exact directory structure along with files with the correct extension to Firebase Cloud. Ignoring any Specified Files.")
        parser.add_argument('--send-data', '-sd', action="store_true", help="Takes Section \"ProjectInformation\" in projectSettings.yaml and converts the Key|Value pairs into a Firebase Document under your specified Collection Name")
        parser.add_argument('--all', '-a', action="store_true", help="Will run both \"--build_tree\" functions.")
        parser.add_argument("--test", "-t", action="store_true", help="Run Given actions in test mode. Will print all compiled data, without actually uploading anything.")
        args = parser.parse_args()

        BUILDTREE = args.build_tree
        DEEPCOPY = args.deep_copy
        SENDDATA = args.send_data
        ALL = args.all
        TESTING = args.test

        print(f"BUILDTREE = {BUILDTREE}")
        print(f"DEEPCOPY  = {DEEPCOPY}")
        print(f"SENDDATA  = {SENDDATA}")
        print(f"RUNALL    = {ALL}")
        print(f"TESTING   = {TESTING}")

        filePath  = os.path.dirname(os.path.abspath(__file__))
        yamlFile ="/projectSettings.yaml"
        settingsYamlFile = filePath + yamlFile
        config = ProjectConfig(settingsYamlFile, TESTING=TESTING)

        credPath = filePath + config.CredentialsPath + config.FirebaseCred
        firebase = Firebase(credPath, config.BucketPath)

        def build_tree():
            logging.info(f' --> Building a new Directory tree and Uploading it to your Firebase Bucket path @ \"{config.BucketPath}\"')
            build_and_upload_directory_tree(config, firebase)
        def deep_copy():
            logging.info(f" --> Walking your Source Directory, and copying it's exact structure to your Firebase Bucket path @ \"{config.BucketPath}\"")
            copy_source_to_bucket(config, firebase)
        def send_project_data():
            logging.info(f" --> Taking your Project data from {yamlFile} and pushing it to your Firestore Colleciton")
            upload_project_information(config, firebase, settingsYamlFile)

        if ALL:
            build_tree()
            deep_copy()
            send_project_data()
            return
        if BUILDTREE:
            build_tree()
        if DEEPCOPY:
            deep_copy()
        if SENDDATA:
            send_project_data()
#---------------
    main()

