from yamlLoader import get_yaml_section

def upload_project_information(firebase, yamlSection, yamlFile):
    raw = get_yaml_section(yamlFile, yamlSection)
    col_doc = raw.get("Meta", {})
    info = raw.get("BuildDetails", {})

    firebase.add_to_collection(
        col_doc["Collection"],
        col_doc["Document"],
        {info["projectName"].lower() : info}
    )

