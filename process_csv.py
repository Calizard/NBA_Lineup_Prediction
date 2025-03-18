import os
import pandas as pd
import logging

# Setup logging to output to a file
logging.basicConfig(filename='csv_process.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Relative path to the NBA-CSV folder
base_dir = 'NBA-CSV'

# Output file path
output_file_path = os.path.join(base_dir, 'matchups_combined_cleaned.csv')

# List of columns to drop (excluding 'outcome')
columns_to_drop = [ 'end_min',
                    'fga_home', 'fta_home', 'fgm_home', 'fga_2_home', 'fgm_2_home', 'fga_3_home', 'fgm_3_home',
                    'ast_home', 'blk_home', 'pf_home', 'reb_home', 'dreb_home', 'oreb_home', 'to_home', 'pts_home', 'pct_home', 'pct_2_home', 'pct_3_home', 
                    'fga_visitor', 'fta_visitor', 'fgm_visitor', 'fga_2_visitor', 'fgm_2_visitor', 'fga_3_visitor', 'fgm_3_visitor',
                    'ast_visitor', 'blk_visitor', 'pf_visitor', 'reb_visitor', 'dreb_visitor', 'oreb_visitor', 'to_visitor', 'pts_visitor', 'pct_visitor', 'pct_2_visitor', 'pct_3_visitor']

def process_csv_file(csv_file_path):
    try:
        logging.debug(f"Processing file: {csv_file_path}")
        print(f"Processing file: {csv_file_path}")

        # Load the CSV file into a pandas DataFrame
        df = pd.read_csv(csv_file_path)

        # Drop specified columns if they exist in the DataFrame
        df_cleaned = df.drop(columns=[col for col in columns_to_drop if col in df.columns], errors='ignore')

        # Remove rows where 'outcome' is -1
        if 'outcome' in df_cleaned.columns:
            df_cleaned = df_cleaned[df_cleaned['outcome'] != -1]

        # Return the cleaned DataFrame
        return df_cleaned

    except Exception as e:
        logging.error(f"Error processing {csv_file_path}: {e}")
        print(f"Error processing {csv_file_path}: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error

def traverse_and_process(base_dir, output_file_path):
    # Check if the output file already exists
    if os.path.exists(output_file_path):
        logging.warning(f"Output file {output_file_path} already exists. Skipping processing.")
        print(f"Output file {output_file_path} already exists. Skipping processing.")
        return  # Exit the function early
    
    # List to collect all cleaned DataFrames
    cleaned_dfs = []
    
    # Find all .csv files
    files = [file for file in os.listdir(base_dir) if file.endswith(".csv")]

    # Process each file in the base directory
    for file in files:
        csv_file_path = os.path.join(base_dir, file)
        cleaned_df = process_csv_file(csv_file_path)
        
        # Check if cleaned_df is not empty
        if not cleaned_df.empty:
            cleaned_dfs.append(cleaned_df)
        else:
            logging.warning(f"Skipping empty or invalid DataFrame for {csv_file_path}")
            print(f"Skipping empty or invalid DataFrame for {csv_file_path}")

    # Combine all cleaned DataFrames into one
    if cleaned_dfs:
        combined_df = pd.concat(cleaned_dfs, ignore_index=True)
        
        # Save the combined DataFrame to a new CSV file
        output_file_path = os.path.join(base_dir, 'matchups_combined_cleaned.csv')
        combined_df.to_csv(output_file_path, index=False)

        logging.info(f"Successfully combined all cleaned files into {output_file_path}")
        print(f"Successfully combined all cleaned files into {output_file_path}")
    else:
        logging.warning("No data to combine.")
        print("No data to combine.")

# Start logging
logging.info("CSV processing script started.")
print("CSV processing script started.")

# Start processing
traverse_and_process(base_dir, output_file_path)

logging.info("CSV processing script finished.")
print("CSV processing script finished.")
