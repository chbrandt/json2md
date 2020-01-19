from jsonschema import validate
from jsonschema.exceptions import ValidationError
import json
import os
import sys


def validate_json(json_file_path, config):
    fig_json = config['figure_path']['key']['json']
    ref_json = config['wiki-reference']['key']['json']
    tbl_json = config['table']['key']['json']
    tbl_field_json = config['table']['properties']['field']['key']['json']
    tbl_desc_json = config['table']['properties']['description']['key']['json']

    schema = {
        "type": "object",
        "properties": {
            f"{fig_json}": {
                "type": "string",
                "format": "uri-reference"
            },
            f"{ref_json}": {
                "type": "string",
                "format": "uri"
            },
            f"{tbl_json}": {
                "type": "object",
                "properties": {
                    f"{tbl_field_json}": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "uniqueItems": True
                    },
                    f"{tbl_desc_json}": {
                        "type": "array",
                        "items": {
                            "type": ["string", "number"]
                        }
                    }
                },
                "required": [f"{tbl_field_json}", f"{tbl_desc_json}"]
            }
        },
        "required": [f"{fig_json}", f"{ref_json}", f"{tbl_json}"]
    }

    with open(json_file_path) as fp:
        json_metadata = json.load(fp)

    try:
        validate(instance=json_metadata, schema=schema)
    except ValidationError as e:
        print(e)
        sys.exit("### Validation not successful ###")


def convert_to_md(json_file_path, config):
    fig_json = config['figure_path']['key']['json']
    ref_json = config['wiki-reference']['key']['json']
    tbl_json = config['table']['key']['json']
    tbl_field_json = config['table']['properties']['field']['key']['json']
    tbl_desc_json = config['table']['properties']['description']['key']['json']

    ref_md = config['wiki-reference']['key']['md']
    tbl_field_md = config['table']['properties']['field']['key']['md']
    tbl_desc_md = config['table']['properties']['description']['key']['md']

    with open(json_file_path) as fp:
        json_metadata = json.load(fp)

    md_template = f'''![Browse]({json_metadata[fig_json]})

Materials related to [{ref_md}]({json_metadata[ref_json]})

| {tbl_field_md} | {tbl_desc_md} |
| - | - |'''

    for field, desc in zip(json_metadata[tbl_json][tbl_field_json],
                           json_metadata[tbl_json][tbl_desc_json]):
        md_template += f"\n| {field} | {desc} |"
    md_template += "\n"

    md_file_path = os.path.join(os.path.dirname(json_file_path), "README.md")
    with open(md_file_path, 'w') as md_fp:
        md_fp.write(md_template)

    print(f"{md_file_path} file created!")
    print('### Conversion Successful ###')


if __name__ == '__main__':

    if len(sys.argv) < 2:
        raise RuntimeError("Path of JSON metadata missing")

    # config file; json to md mapping
    with open("config.json") as cfg_fp:
        cfg = json.load(cfg_fp)

    # metadata in json format
    json_fp = sys.argv[1]

    validate_json(json_fp, cfg)
    convert_to_md(json_fp, cfg)
