import os
import os.path as path

from shelter_management_scripts.shelterluv import collect_data as collect_shelterluv_data


env_dir = path.join(path.dirname(path.dirname(path.dirname(__file__))), 'app/.env')

env_files_content = {}

def run_data_collection(config_dict):
    match config_dict.get("DATA_SOURCE"):
        case "shelterluv":
            print("Collecting data from Shelterluv...")
            collect_shelterluv_data(config_dict)
        case _:
            print("Unknown data source specified.")
    
def run_all_data_collections():
    for filename in os.listdir(env_dir):
        file_path = os.path.join(env_dir, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                env_files_content[filename] = f.readlines()

    for fname, lines in env_files_content.items():
        print(f"{fname}:")
        config_dict = {}
        for line in lines:
            config_line = line.strip()
            if config_line and not config_line.startswith('#'):
                tokens = config_line.split('=', 1)
                if len(tokens) == 2:
                    key, value = tokens
                    config_dict[key] = value
        config_dict["SHELTER_NAME"] = fname.split('.')[0]  # e.g., friends4life from friends4life.env

        print('-' * 40)
        run_data_collection(config_dict)

if __name__ == "__main__":
    run_all_data_collections()