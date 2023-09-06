from pprint import pprint
from yamlLoader import get_yaml_section

def upload_project_information(config, firebase, yamlFile):
    raw = get_yaml_section(yamlFile, config.FirebaseFirestore)
    col_doc = raw.get("Meta", {})
    info = raw.get("BuildDetails", {})

    if config.TESTING:
        print(f" -->    Collection: {col_doc['Collection']}")
        print(f" -->      Document: {col_doc['Document']}")
        print(f" -->   ProjectName: {info['projectName'].lower()}")
    else:
        firebase.add_to_collection(
            col_doc["Collection"],
            col_doc["Document"],
            {info["projectName"].lower() : info}
        )

