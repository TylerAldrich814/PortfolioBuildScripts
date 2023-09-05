import yaml

def get_yaml_section(file_path, section):
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"The file '{file_path}' doesn't exist.")
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error while Parsing YAML File: {e}")

    try:
        return data[section]
    except KeyError:
        raise KeyError(f"'{section}' doesn't exist within '{file_path}'")

