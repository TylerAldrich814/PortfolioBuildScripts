import logging
# from yamlLoader import get_yaml_section
from yamlLoader import get_yaml_section

class ProjectConfig:
    def __init__(self, file_path):
        self.FirebaseStorage = "FirebaseStorage"
        self.FirebaseFirestore = "FirebaseFirestore"

        project = get_yaml_section(file_path, self.FirebaseStorage)
        meta = project.get("Meta", {})
        details = project.get("BuildDetails", {})

        self.Bucket = meta["Bucket"]
        self.StructurePath = meta["StructurePath"]

        self.Name = details['Name']
        self.RootDir = details['RootDirectory']
        self.SourceDir = details['SourceDirectory']
        self.CompleteSrcDir = self.RootDir + self.SourceDir # ??
        self.AcceptedFiles = details['AcceptedFiles']
        self.IgnoredFiles = details['IgnoredFiles']
        self.IgnoreDirs = details['IgnoreDirs']
        self.FirebaseCred = details['FirebaseCredentials']
        self.CredentialsPath = details['CredentialsPath']
        self.BucketPath = details['BucketPath']
        self.Extensions = details['Extensions']
        self.OnlyAcceptedFiles = False

        if len(self.AcceptedFiles) != 0 and self.IgnoredFiles[0] != "*":
            raise ValueError("If you've added files to 'AcceptedFiles', then you must only add '*' to IgnoredFiles.");
        elif len(self.AcceptedFiles) != 0 and self.IgnoredFiles[0] == "*":
            self.OnlyAcceptedFiles = True


    # For filtering both possible states of this script.
    # Scenario A.) User preselects to have ALL files be ignored by passing '*'
    #   into 'IgnoredFiles', and then Selecting files to allow by adding them
    #   into 'AcceptedFiles'.
    # Scenario B.) User Preselects secific Files to be ignores, and leaves
    #   'AcceptedFiles' empty.
    # Both Scenario's rely on 'Extensions'.
    def filter_file(self, file):
        if self.OnlyAcceptedFiles:
            if file in self.AcceptedFiles:
                return file
        elif file not in config.IgnoredFiles:
            return file


    def test(self):
        logging.info(f"-----------BUCKET - {self.Bucket}")
        logging.info(f"----STRUCTUREPATH - {self.StructurePath}")
        logging.info(f"-------------Name - {self.Name}")
        logging.info(f"----------RootDir - {self.RootDir}")
        logging.info(f"--------SourceDir - {self.SourceDir}")
        logging.info(f"---AccecptedFiles - {self.AcceptedFiles}")
        logging.info(f"------IgnoreFiles - {self.IgnoredFiles}")
        logging.info(f"-------IgnoreDirs - {self.IgnoreDirs}")
        logging.info(f"-----FirebaseCred - {self.FirebaseCred}")
        logging.info(f"--CredentialsPath - {self.CredentialsPath}")
        logging.info(f"-------BucketPath - {self.BucketPath}")
        logging.info(f"-------Extensions - {self.Extensions}")


if __name__ == "__main__":
    config = ProjectConfig('./projectSettings.yaml')
    config.test()
