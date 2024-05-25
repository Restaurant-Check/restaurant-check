# load all json files in this directory and combine them to one json file (list)
import json
import os


def combine_json_files():
    json_data = []
    for file in os.listdir("."):
        if file.endswith(".json") and file != "combined.json":
            with open(file, "r") as f:
                print(file)
                data = json.load(f)
                print(data)
                json_data.append(data)
    with open("combined.json", "w") as f:
        json.dump(json_data, f)


combine_json_files()
