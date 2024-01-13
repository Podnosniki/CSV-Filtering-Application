import pandas as pd
import os

RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
WHITE = '\033[97m'
RESET = '\033[0m'

def filter_csv(file_path, columns_to_remove, search_column, keywords):
    try:
        df = pd.read_csv(file_path, header=0, delimiter='#', on_bad_lines='skip', engine='python')

        print(f"\n\n{YELLOW}Processing file: {file_path}{RESET}")
        print(f"{YELLOW}Initial number of rows: {len(df)}{RESET}")

        if search_column in df.columns:
            partial_keywords = [kw.strip('[]') for kw in keywords if not kw.startswith('[') or not kw.endswith(']')]
            exact_keywords = [kw.strip('[]') for kw in keywords if kw.startswith('[') and kw.endswith(']')]

            df = df[df[search_column].apply(lambda x: 
                any(partial_keyword in str(x) for partial_keyword in partial_keywords) or
                str(x) in exact_keywords
            )]
            print(f"\n{GREEN}Number of rows after keyword filtering: {len(df)}{RESET}")
        else:
            print(f"\n{RED}Column '{search_column}' not found in file: {file_path}{RESET}")

        filtered_df = df.drop(columns=columns_to_remove, errors='ignore')

        return filtered_df
    except Exception as e:
        print(f"\n{RED}Error processing file {file_path}: {e}{RESET}")
        return pd.DataFrame()

def process_folder(folder_path, config_file_path):
    try:
        with open(config_file_path, 'r') as file:
            config_content = file.read()

        config_dict = {}
        for line in config_content.split('\n'):
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip().strip('[]').replace("'", "")
                if key == 'columns_to_remove':
                    config_dict[key] = [col.strip() for col in value.split(',')]
                elif key in ['data_search_column', 'keywords']:
                    config_dict[key] = value.split(', ') if key == 'keywords' else value

        columns_to_remove = config_dict.get('columns_to_remove', [])
        search_column = config_dict.get('data_search_column', '')
        keywords = config_dict.get('keywords', [])

        for file in os.listdir(folder_path):
            if file.endswith('.csv'):
                file_path = os.path.join(folder_path, file)
                filtered_data = filter_csv(file_path, columns_to_remove, search_column, keywords)
                if not filtered_data.empty:
                    new_file_path = os.path.join(folder_path, f"filtered_{file}")
                    filtered_data.to_csv(new_file_path, index=False, sep='#')
                    print(f"{GREEN}Filtered file saved: {new_file_path}{RESET}\n\n")
                else:
                    print(f"{RED}No data to write for file: {file_path}{RESET}\n\n")
    except FileNotFoundError:
        print(f"{RED}The file '{config_file_path}' was not found.{RESET}")
    except Exception as e:
        print(f"{RED}Error processing the folder: {e}{RESET}")

folder_path = 'files'
config_file_path = 'config.txt'
process_folder(folder_path, config_file_path)
