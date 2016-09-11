import yaml
import json

def load_yaml(filepath):
    f = open(filepath)
    document = yaml.load(f)
    f.close();
    return document;

def load_json(filepath):
    f = open(filepath)
    document = json.load(f)
    f.close();
    return document;

def load(filepaths):
    definitions = []
    for filepath in filepaths:
        if filepath.endswith('.yaml'):
            definition = load_yaml(filepath)
        elif filepath.endswith('.json'):
            definition = load_json(filepath)
        else:
            continue
        definitions.append(definition)
    return definitions

