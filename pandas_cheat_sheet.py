import pandas as pd
import numpy as np

# 1. Creating DataFrames and Series
# From a dictionary
data = {'col1': [1, 2, 3], 'col2': ['A', 'B', 'C']}
df = pd.DataFrame(data)

# From a list of lists
df_list = pd.DataFrame([[1, 'A'], [2, 'B']], columns=['col1', 'col2'])

# Creating a Series
s = pd.Series([10, 20, 30], name='my_series')

# 2. Reading and Writing Data
# Read from CSV
df_csv = pd.read_csv('file.csv')

# Write to CSV
df.to_csv('output.csv', index=False) # index=False prevents writing the DataFrame index

# Read from Excel
df_excel = pd.read_excel('file.xlsx', sheet_name='Sheet1')

# 3. Basic DataFrame Operations
# Display first/last n rows
df.head(5)
df.tail(3)

# Get info about the DataFrame (data types, non-null counts)
df.info()

# Get descriptive statistics
df.describe()

# Get shape (rows, columns)
df.shape

# Get column names
df.columns

# 4. Selecting Data
# Select a single column
df['col1']
df.col1 # Alternative for single column selection

# Select multiple columns
df[['col1', 'col2']]

# Select rows by index
df.iloc[0] # First row
df.iloc[0:2] # First two rows

# Select rows and columns by label
df.loc[0, 'col1'] # Value at row 0, column 'col1'
df.loc[0:1, ['col1', 'col2']] # Rows 0-1, columns 'col1' and 'col2'

# 5. Filtering Data
# Filter rows based on a condition
df[df['col1'] > 1]

# Filter with multiple conditions
df[(df['col1'] > 1) & (df['col2'] == 'C')]

# Filter using isin()
df[df['col1'].isin([1, 3])]

# Filter using string methods (for Series of strings)
df[df['col2'].str.contains('A')]

# 6. Handling Missing Data
# Check for missing values
df.isna()
df.isnull().sum() # Count missing values per column

# Fill missing values
df.fillna(0) # Fill with a specific value
df.fillna(method='ffill') # Forward fill
df.fillna(method='bfill') # Backward fill

# Drop rows/columns with missing values
df.dropna() # Drop rows with any NaN
df.dropna(axis=1) # Drop columns with any NaN

# 7. Grouping and Aggregation
# Group by a column and calculate mean
df.groupby('col2')['col1'].mean()

# Group by multiple columns and aggregate with multiple functions
df.groupby(['col1', 'col2']).agg({'col1': 'sum', 'col2': 'count'})

# 8. Adding and Modifying Columns
# Add a new column
df['new_col'] = df['col1'] * 2

# Apply a function to a column
df['col1_squared'] = df['col1'].apply(lambda x: x**2)

# 9. Sorting Data
df.sort_values(by='col1', ascending=False)

# 10. Merging and Joining
df1 = pd.DataFrame({'key': ['A', 'B'], 'value1': [1, 2]})
df2 = pd.DataFrame({'key': ['A', 'C'], 'value2': [3, 4]})

# Inner merge
pd.merge(df1, df2, on='key', how='inner')

# Left join
pd.merge(df1, df2, on='key', how='left')