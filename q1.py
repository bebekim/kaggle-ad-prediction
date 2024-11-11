import pandas as pd

file_path = './ad_click_dataset_sample.csv'
df = pd.read_csv(file_path)

# Distribution Analysis
# First let's see the total distribution including NaN
print("Distribution of ad positions including NaN:")
position_counts = (df['ad_position']
                  .value_counts(dropna=False)
                  .to_frame('Count')
                  .assign(Percentage = lambda x: round(x['Count'] / len(df) * 100, 2))
                 )
# Format percentage for display
position_counts['Percentage'] = position_counts['Percentage'].astype(str) + '%'
position_counts

# CTR Analysis without duplicate columns
ctr_by_position = (df
    .groupby('ad_position', dropna=False)
    .agg({
        'click': ['count', 'sum', 'mean']
    })
    .pipe(lambda x: x.set_axis(['Impressions', 'Clicks', 'CTR'], axis=1))
    .assign(
        CTR_pct=lambda x: (x['CTR'] * 100).round(2)  # Numeric column for plotting
    )
    .assign(
        CTR=lambda x: x['CTR_pct'].astype(str) + '%'  # Format CTR as percentage
    )
    .drop('CTR_pct', axis=1)  # Remove the temporary numeric column after plotting
)

print("\nCTR Analysis by Position (including NaN):")
ctr_by_position

import seaborn as sns
import matplotlib.pyplot as plt

# For plotting, we'll need the CTR values as numbers, so let's create a temporary column just for plotting
plot_data = ctr_by_position.assign(
    CTR_pct=lambda x: x['CTR'].str.rstrip('%').astype(float)
    )

# Create visualization
plt.figure(figsize=(10, 6))
ax = sns.barplot(
    x=plot_data.index, 
    y='CTR_pct', 
    data=plot_data, 
    palette='viridis'
)

# Add value labels on top of bars
for i, v in enumerate(plot_data['CTR_pct']):
    ax.text(i, v + 1, f'{v:.1f}%', ha='center')

# Customize the plot
plt.title('Click-Through Rate by Ad Position', pad=20)
plt.xlabel('Ad Position')
plt.ylabel('Click-Through Rate (%)')

# Add grid for better readability
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()

# 1. First, let's check if missing ad positions are related to other variables
# Create a binary column for missing ad_position
df['is_missing_position'] = df['ad_position'].isna()

# Check relationship with other variables
print("Pattern Analysis of Missing Values:")
print("\n1. Relationship with device_type:")
print(pd.crosstab(df['is_missing_position'], df['device_type'], normalize='index'))

print("\n2. Relationship with time_of_day:")
print(pd.crosstab(df['is_missing_position'], df['time_of_day'], normalize='index'))

print("\n3. Relationship with gender:")
print(pd.crosstab(df['is_missing_position'], df['gender'], normalize='index'))

print("\n4. Click rates comparison:")
print("CTR for records with missing position:", 
      df[df['is_missing_position']]['click'].mean())
print("CTR for records with known position:",
      df[~df['is_missing_position']]['click'].mean())
