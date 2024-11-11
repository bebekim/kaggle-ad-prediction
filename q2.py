import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import numpy as np

# Create figure with multiple plots
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

# 1. Histogram with KDE
sns.histplot(data=df, x='age', kde=True, ax=ax1)
ax1.set_title('Age Distribution with KDE')

# 2. Q-Q plot
stats.probplot(df['age'].dropna(), dist="norm", plot=ax2)
ax2.set_title('Q-Q Plot')

# 3. Box plot
sns.boxplot(y=df['age'], ax=ax3)
ax3.set_title('Box Plot of Age')

# 4. Density plot
sns.kdeplot(data=df, x='age', ax=ax4)
ax4.set_title('Density Plot of Age')

plt.tight_layout()
plt.show()

# Calculate skewness and kurtosis
print("\nSkewness:", stats.skew(df['age'].dropna()))
print("Kurtosis:", stats.kurtosis(df['age'].dropna()))

# Basic statistics
print("\nDescriptive Statistics for Age:")
print(df['age'].describe())

# Normality test (Shapiro-Wilk)
stat, p_value = stats.shapiro(df['age'].dropna())
print("\nShapiro-Wilk test:")
print(f"Statistic: {stat:.4f}")
print(f"P-value: {p_value:.4e}")


# Drop rows where age or time_of_day is missing
df_clean = df.dropna(subset=['age', 'time_of_day'])

# Create figure and axis
plt.figure(figsize=(12, 7))

# Create boxplot
bp = sns.boxplot(x='time_of_day', y='age', data=df_clean)

# Calculate and annotate statistics for each time period
for i, time in enumerate(df_clean['time_of_day'].unique()):
    subset = df_clean[df_clean['time_of_day'] == time]['age']
    
    # Calculate statistics
    median = subset.median()
    q1 = subset.quantile(0.25)
    q3 = subset.quantile(0.75)
    iqr = q3 - q1
    
    # Annotate median
    plt.text(i, median + 1, f'Median: {median:.1f}', 
             horizontalalignment='center', color='darkred')
    
    # Annotate IQR
    plt.text(i, q3 + 2, f'IQR: {iqr:.1f}', 
             horizontalalignment='center', color='darkblue')

plt.title('Age Distribution by Time of Day')
plt.xlabel('Time of Day')
plt.ylabel('Age')

# Add some padding to y-axis to fit annotations
plt.ylim(15, 70)

plt.tight_layout()
plt.show()


from scipy.stats import kruskal

# Group the age data by time_of_day
grouped_data = [group['age'].values for name, group in df_clean.groupby('time_of_day')]

# Perform the Kruskal-Wallis test
stat, p_value = kruskal(*grouped_data)

# Print the result
print(f"Kruskal-Wallis Test Statistic: {stat}, p-value: {p_value}")

# Check if the result is significant
if p_value < 0.05:
    print("There is a significant difference in age distribution across time_of_day categories.")
else:
    print("No significant difference in age distribution across time_of_day categories.")


# Perform Kruskal-Wallis test
from scipy import stats

# 1. Prepare data - group ages by time of day
afternoon_ages = ad_prediction[ad_prediction['time_of_day'] == 'Afternoon']['age'].dropna()
evening_ages = ad_prediction[ad_prediction['time_of_day'] == 'Evening']['age'].dropna()
morning_ages = ad_prediction[ad_prediction['time_of_day'] == 'Morning']['age'].dropna()
night_ages = ad_prediction[ad_prediction['time_of_day'] == 'Night']['age'].dropna()

# 2. Perform Kruskal-Wallis H-test
h_stat, p_value = stats.kruskal(afternoon_ages, evening_ages, morning_ages, night_ages)

# 3. Print results
print("Kruskal-Wallis test results:")
print(f"H-statistic: {h_stat:.4f}")
print(f"p-value: {p_value:.4f}")

# 4. Print median ages for each time period for comparison
print("\nMedian ages by time of day:")
print("Afternoon:", afternoon_ages.median())
print("Evening:", evening_ages.median())
print("Morning:", morning_ages.median())
print("Night:", night_ages.median())

# 5. Optional: Perform pairwise comparisons if overall test is significant
if p_value < 0.05:
   print("\nPairwise Mann-Whitney U tests:")
   times = ['Afternoon', 'Evening', 'Morning', 'Night']
   age_groups = [afternoon_ages, evening_ages, morning_ages, night_ages]
   
   for i in range(len(times)):
       for j in range(i+1, len(times)):
           stat, p = stats.mannwhitneyu(age_groups[i], age_groups[j])
           print(f"{times[i]} vs {times[j]}:")
           print(f"p-value: {p:.4f}")

# 6. Visualize
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(12, 6))
sns.boxplot(data=ad_prediction, x='time_of_day', y='age')
plt.title('Age Distribution by Time of Day')
plt.xlabel('Time of Day')
plt.ylabel('Age')

# Add median age annotations
for i, time in enumerate(['Afternoon', 'Evening', 'Morning', 'Night']):
   median_age = ad_prediction[ad_prediction['time_of_day'] == time]['age'].median()
   plt.text(i, median_age, f'Median: {median_age:.1f}', 
            horizontalalignment='center', verticalalignment='bottom')

plt.show()