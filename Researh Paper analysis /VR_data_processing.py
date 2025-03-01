import pandas as pd
import numpy as np

def process_vr_data_to_vectors(df, sampling_rate=90):
    """
    Process VR tracking data into 90-dimensional vectors for (H+D+N)×(P+E) condition.
    Each second of data will yield one 90-dimensional vector.

    The 90 dimensions come from:
    - 3 devices (Head, Left Hand, Right Hand)
    - 6 features per device (3 position + 3 euler rotation)
    - 5 statistical measures per feature
    3 * 6 * 5 = 90 dimensions

    Parameters:
    df: pandas DataFrame with the VR tracking data
    sampling_rate: frames per second (default 90)

    Returns:
    DataFrame where each row is a 90-dimensional vector for one second of data
    """
    # Mapping of our features
    features_map = {
        'head': {
            'pos': ['head_pos_x', 'head_pos_y', 'head_pos_z'],
            'euler': ['head_rot_x', 'head_rot_y', 'head_rot_z']
        },
        'left_hand': {
            'pos': ['left_hand_pos_x', 'left_hand_pos_y', 'left_hand_pos_z'],
            'euler': ['left_hand_rot_x', 'left_hand_rot_y', 'left_hand_rot_z']
        },
        'right_hand': {
            'pos': ['right_hand_pos_x', 'right_hand_pos_y', 'right_hand_pos_z'],
            'euler': ['right_hand_rot_x', 'right_hand_rot_y', 'right_hand_rot_z']
        }
    }
    
    # Statistical functions to compute
    stats_funcs = ['max', 'min', 'median', 'mean', 'std']
    
    processed_segments = []
    
    # Process data in 1-second segments
    for start_idx in range(0, len(df), sampling_rate):
        end_idx = start_idx + sampling_rate
        segment = df.iloc[start_idx:end_idx]
        
        if len(segment) < sampling_rate:  # Skip incomplete segments
            continue
            
        segment_features = {}
        
        # Calculate statistics for each device and feature
        for device, features in features_map.items():
            for feat_type in ['pos', 'euler']:
                for col in features[feat_type]:
                    # Skip if column doesn't exist
                    if col not in segment.columns:
                        continue
                        
                    # Calculate all statistics for this feature
                    feature_data = segment[col]
                    stats = {
                        'max': feature_data.max(),
                        'min': feature_data.min(),
                        'median': feature_data.median(),
                        'mean': feature_data.mean(),
                        'std': feature_data.std()
                    }
                    
                    # Store each statistic with a descriptive name
                    for stat_name, value in stats.items():
                        feat_name = f"{col}_{stat_name}"
                        segment_features[feat_name] = value
        
        # Add metadata if needed
        segment_features['user'] = segment['user'].iloc[0]
        segment_features['subject'] = segment['subject'].iloc[0]
        segment_features['session'] = segment['session'].iloc[0]
        segment_features['build'] = segment['build'].iloc[0]
        
        processed_segments.append(segment_features)
    
    # Convert to DataFrame
    result_df = pd.DataFrame(processed_segments)
    
    # Verify we have 90 feature dimensions (excluding metadata columns)
    feature_cols = [col for col in result_df.columns 
                   if any(stat in col for stat in stats_funcs)]
    assert len(feature_cols) == 90, f"Expected 90 features, got {len(feature_cols)}"
    
    return result_df


def process_example_data(file_path):
    """
    Reads the VR tracking data from a file, processes it into 90-dimensional vectors,
    and saves the processed data into a CSV file.

    Parameters:
    file_path: Path to the raw VR tracking data file

    Returns:
    processed_df: Processed DataFrame with 90-dimensional vectors
    """
    # Read the data
    df = pd.read_csv(file_path, sep='\t')
    
    # Process into 90-dimensional vectors
    processed_df = process_vr_data_to_vectors(df)
    
    # Show dimensions of resulting features
    feature_cols = [col for col in processed_df.columns 
                   if any(stat in col for stat in ['max', 'min', 'median', 'mean', 'std'])]
    
    print(f"Total feature dimensions: {len(feature_cols)}")
    print("\nFeature breakdown:")
    print(f"Devices: Head, Left Hand, Right Hand")
    print(f"Per device: 3 position + 3 euler = 6 features")
    print(f"Per feature: 5 statistical measures")
    print(f"Total: 3 devices * 6 features * 5 measures = 90 dimensions")
    
    processed_df.to_csv("DataSets/processed_dataset(90-Features).csv", sep="\t", index=False)
    return processed_df