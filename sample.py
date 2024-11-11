import pandas as pd
import numpy as np

def sample_csv(input_file, output_file, sample_fraction=0.5, random_state=42):
    """
    Sample a CSV file and save the results to a new file.
    
    Parameters:
    -----------
    input_file : str
        Path to the input CSV file
    output_file : str
        Path where the sampled CSV will be saved
    sample_fraction : float, default 0.5
        Fraction of rows to sample (between 0 and 1)
    random_state : int, default 42
        Random seed for reproducibility
    """
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    # Get the number of rows to sample
    n_samples = int(len(df) * sample_fraction)
    
    # Sample the dataframe
    sampled_df = df.sample(n=n_samples, random_state=random_state)
    
    # Sort by index to maintain some order (optional)
    sampled_df = sampled_df.sort_index()
    
    # Save to new CSV file
    sampled_df.to_csv(output_file, index=False)
    
    print(f"Original file size: {len(df)} rows")
    print(f"Sampled file size: {len(sampled_df)} rows")
    print(f"Sampled data saved to: {output_file}")

# Example usage
if __name__ == "__main__":
    input_file = "ad_click_dataset.csv"  # Replace with your input file path
    output_file = "ad_click_dataset_sample.csv"  # Replace with desired output path
    
    sample_csv(input_file, output_file)