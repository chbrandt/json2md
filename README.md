# json2md
JSON to Markdown Translation Task

### Installation
Clone the repository
```shell
git clone https://github.com/mejdanid/json2md.git
```

Authenticate with the personal github account and change directory
```shell
cd json2md
```

Run the script to convert json format metadata to markdown format. Path of json file is passed as argument
```shell
python convert.py ./data/mar-c-arsinoes.json
```

### Information
 - config.json contains the mapping rules between the json and markdown metadata
 - convert.py validates the json metadata file and creates a new file README.md with the corresponding metadata in the 
 same directory as the json file. Validation schema is inside convert.py.