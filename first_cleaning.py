import pandas as pd
import numpy as np

# Load the CSV file
df = pd.read_csv("~/Downloads/Financials.csv")

# Columns to clean
columns_to_clean = ["Units Sold", "Gross Sales", "Discounts", "Sales", "COGS", "Profit"]

# Clean and convert values
for col in columns_to_clean:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace('[\$,]', '', regex=True) # Remove $ and commas
        .str.replace(r'\((.*?)\)', r'-\1', regex=True) # Convert (1234.56) to -1234.56
        .str.strip()
        .replace({'-': np.nan, '': np.nan})
        .astype(float)
    )

# Reformat the Date column to yyyy-mm-01
df["Date"] = pd.to_datetime(
    df["Year"].astype(str) + "-" +
    df["Month Number"].astype(str).str.zfill(2) + "-01"
)

# Drop unnecessary columns
df.drop(columns=["Month Name", "Month Number", "Year", "Discount Band", "Discounts"], inplace=True)

# Sort by Date
df.sort_values(by="Date", inplace=True)

# Save cleaned and sorted data
df.to_csv("~/Downloads/Cleaned_Financials.csv", index=False)

# Display the cleaned DataFrame
print(df.head())