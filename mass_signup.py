import pandas as pd

# Read the CSV file
dataframe = pd.read_csv('do-yoga-data.csv')

# Display the first few rows of the dataframe to get a quick look at its content
print(dataframe.head())

# Number of rows and columns
rows, columns = dataframe.shape
print(f"Number of Rows: {rows}")
print(f"Number of Columns: {columns}")

# Column names and data types
print("\nColumn Information:")
print(dataframe.dtypes)

# Basic statistics for each column (only for numeric columns)
print("\nBasic Statistics:")
print(dataframe.describe())

# Check for missing values
missing_values = dataframe.isnull().sum()
print("\nMissing Values by Column:")
print(missing_values[missing_values > 0])

dataframe.drop_duplicates(inplace=True)
dataframe = dataframe[dataframe['Mobile'].str.isnumeric()]
not_12_digits = dataframe[dataframe['Mobile'].str.len() != 12]

# Print the entries which do not have 12 digits
print(not_12_digits)

# Print the count of such entries
print(f"Count of Entries with Non-12 Digits: {len(not_12_digits)}")
