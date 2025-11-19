import pandas as pd

# Load the dataset
df = pd.read_csv("~/Downloads/Cleaned_Financials.csv", parse_dates=["Date"], dayfirst=True)

# Extract month and year
df["Month"] = df["Date"].dt.month
df["Year"] = df["Date"].dt.year

# Sort by Year then Month (chronological order)
df_sorted = df.sort_values(by=["Year", "Month"])

# Format Date as 01/mm/yyyy
df_sorted["Formatted Date"] = "01/" + df_sorted["Month"].astype(str).str.zfill(2) + "/" + df_sorted["Year"].astype(str)

# Display the top rows
print(df_sorted[["Formatted Date", "Segment", "Country", "Product", "Profit (in $)"]].head())

# Save the sorted DataFrame to CSV
df_sorted.to_csv("~/Downloads/Cleaned_Financials_1.csv", index=False)