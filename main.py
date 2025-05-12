import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

# Load and clean the CSV
df1 = pd.read_csv("Miner_Metrics.csv")
df1.columns = df1.columns.str.strip()  # Remove whitespace from headers

# Select only the relevant columns
value_vars1 = [col for col in df1.columns if '_hashrate' in col or '_power' in col]

# Melt the dataframe
melted1 = pd.melt(df1, id_vars=['Time'], value_vars=value_vars1,
                 var_name='Source', value_name='Value')

# Extract Miner and Metric (like S11 + hashrate/power)
melted1[['Miner', 'Metric']] = melted1['Source'].str.extract(r'(S\d+).*_(hashrate|power)')

# Drop the original Source column
melted1 = melted1.drop(columns=['Source'])

# Pivot to get separate columns for 'hashrate' and 'power'
pivoted1 = melted1.pivot_table(index=['Time', 'Miner'], columns='Metric', values='Value').reset_index()

# Optional: Rename columns for clarity
pivoted1.columns.name = None
pivoted1 = pivoted1.rename(columns={'hashrate': 'Hashrate', 'power': 'Power'})


# ___________________________Second Source Cleaning 



# Load and clean the CSV
df2 = pd.read_csv("Miner_Intake_Fan_Chip.csv")
df2.columns = df2.columns.str.strip()  # Remove whitespace from headers

# Select only the relevant columns
value_vars2 = [col for col in df2.columns if '_chiptemp' in col or '_minerfans' in col or'_intake' in col]

# Melt the dataframe

melted2 = pd.melt(df2, id_vars=['Time'], value_vars=value_vars2, var_name='Source', value_name='Value')


# Extract Miner and Metric (like S11 + hashrate/power)
melted2[['Miner', 'Metric']] = melted2['Source'].str.extract(r'(S\d+).*_(chiptemp|minerfans|intake)')


# Drop the original Source column
melted2 = melted2.drop(columns=['Source'])

# Pivot to get separate columns for 'hashrate' and 'power'
pivoted2 = melted2.pivot_table(index=['Time', 'Miner'], columns='Metric', values='Value').reset_index()

# Optional: Rename columns for clarity
pivoted2.columns.name = None
pivoted2 = pivoted2.rename(columns={'chiptemp': 'Chiptemp', 'minerfans': 'Minerfans','intake':'Intake'})




#_____________________Data are cleaned and ready for merging

merged = pd.merge(pivoted1, pivoted2, on=['Time', 'Miner'], how='outer' )


#_____________________Merge data ready for Analysis

merged['Hashrate_Power'] = np.round(np.divide(merged['Hashrate'], merged['Power']),2)

# Convert time column and extract day


merged['Time'] = pd.to_datetime(merged['Time'], errors='coerce')
merged = merged.dropna(subset=['Time'])

merged['Time'] = pd.to_datetime(merged['Time'])
merged['YearMonthDate'] = merged['Time'].dt.to_period('D')

# Group by day
Feb_avg = merged.groupby('YearMonthDate').agg({
    'Hashrate': 'mean',
    'Power': 'mean',
    'Hashrate_Power': 'mean',
    'Intake': 'mean',
    'Minerfans': 'mean'
}).round(2)

# Convert Period[D] index to datetime
Feb_avg = Feb_avg.copy()
Feb_avg = Feb_avg.reset_index()  # This brings 'DayPeriod' from index to a column
Feb_avg['YearMonthDate'] = Feb_avg['YearMonthDate'].dt.to_timestamp()

# Drop NaNs and clip extreme values
Feb_avg = Feb_avg.dropna(subset=['YearMonthDate', 'Hashrate_Power'])
Feb_avg = Feb_avg[Feb_avg['Hashrate_Power'] < 3000]

#plot 

plt.figure(figsize=(12, 6))
plt.bar(Feb_avg['YearMonthDate'], Feb_avg['Hashrate_Power'])
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()