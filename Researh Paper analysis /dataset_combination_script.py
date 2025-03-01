import os
import pandas as pd

# Define the root directory
root_dir = "moore_cross_domain23"

# List to store dataframes
df_list = []


# Traverse the directory structure
for sub in os.listdir(root_dir):
    sub_path = os.path.join(root_dir, sub)
    if os.path.isdir(sub_path):  # Ensure it's a directory
        for ses in ["ses-A", "ses-B"]:  # Iterate over session folders
            ses_path = os.path.join(sub_path, ses, "motion")
            if os.path.exists(ses_path):  # Check if motion folder exists
                for file in os.listdir(ses_path):
                    if file.endswith("_motion.tsv"):  # Only pick motion files
                        file_path = os.path.join(ses_path, file)
                        
                        try:
                            df = pd.read_csv(file_path, sep="\t")  # Read TSV
                            
                            # Add metadata columns
                            df["subject"] = sub  # Subject ID
                            df["session"] = ses  # Session (A/B)
                            df["source_file"] = file  # Original file name
                            
                            # Convert timestamp column to datetime if it exists
                            if "timestamp" in df.columns:
                                df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')
                            
                            df_list.append(df)

                        except Exception as e:
                            print(f"Error reading {file_path}: {e}")

# Combine all dataframes if any were found
if df_list:
    combined_df = pd.concat(df_list, ignore_index=True)
    combined_df.to_csv("DataSets/combined_motion_data.tsv", sep="\t", index=False)
    print("✅ All motion TSV files merged successfully into 'combined_motion_data.tsv'")
else:
    print("⚠️ No motion TSV files found.")