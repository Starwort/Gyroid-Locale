import os, yaml, json

for file_name in os.listdir():
    if not file_name.endswith(".yml"):
        continue
    print(file_name)
    with open(file_name.replace(".yml", ".json"), "w") as out_file:
        with open(file_name, errors="replace") as in_file:
            json.dump(yaml.load(in_file), out_file, indent=4)
