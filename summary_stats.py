import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load the dataset
financial_dataset = pd.read_csv("~/Downloads/Cleaned_Financials_1.csv", parse_dates=["Date"], dayfirst=True)

# 1. Feature Engineering
financial_dataset["Month"] = financial_dataset["Date"].dt.month
financial_dataset["Year"] = financial_dataset["Date"].dt.year
financial_dataset["Profit Margin"] = financial_dataset["Profit (in $)"] / financial_dataset["Sales (in $)"]
financial_dataset["Sales Efficiency"] = financial_dataset["Sales (in $)"] / financial_dataset["Units Sold (in $)"]

# 2. Handle Missing Values
missing = financial_dataset.isnull().sum()
print("Missing values:\n", missing)
financial_dataset_clean = financial_dataset.dropna()

# 3. Outlier Detection (IQR)
def detect_outliers_iqr(data, column):
    lower_quartile = data[column].quantile(0.25)
    upper_quartile = data[column].quantile(0.75)
    IQR = upper_quartile - lower_quartile
    lower = lower_quartile - 1.5 * IQR
    upper = upper_quartile + 1.5 * IQR
    return data[(data[column] < lower) | (data[column] > upper)]

outliers = detect_outliers_iqr(financial_dataset_clean, "Profit (in $)")
print("\nOutliers in Profit:\n", outliers[["Segment", "Country", "Product", "Profit (in $)"]])

# 4. Summary Statistics (excluding specific columns)
excluded_columns = ["Date", "Month", "Year", "Profit Margin", "Sales (in $)", "Sales", "Sales Efficiency", "Effic"]
included_columns = [col for col in financial_dataset_clean.select_dtypes(include='number').columns if col not in excluded_columns]

summary = financial_dataset_clean[included_columns].describe()
print("\nFiltered Summary Statistics:\n", summary)

# 5. Visualisations
sns.set(style="whitegrid")

# Profit Histogram
plt.figure(figsize=(8, 4))
sns.histplot(financial_dataset_clean["Profit (in $)"], bins=50, kde=True)
plt.title("Distribution of Profit")
plt.xlabel("Profit (in $)")
plt.tight_layout()
plt.show()

# Profit by Segment Boxplot
plt.figure(figsize=(10, 5))
sns.boxplot(x="Segment", y="Profit (in $)", data=financial_dataset_clean)
plt.title("Profit by Segment")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Sales vs Profit Scatter Plot
plt.figure(figsize=(8, 5))
sns.scatterplot(x="Sales (in $)", y="Profit (in $)", hue="Segment", data=financial_dataset_clean)
plt.title("Sales vs Profit by Segment")
plt.tight_layout()
plt.show()

# 6. Grouped Insights
segment_performance = financial_dataset_clean.groupby("Segment")[["Profit (in $)", "Sales (in $)"]].sum().sort_values(by="Profit (in $)", ascending=False)
print("\nSegment Performance:\n", segment_performance)

country_performance = financial_dataset_clean.groupby("Country")[["Profit (in $)", "Sales (in $)"]].sum().sort_values(by="Profit (in $)", ascending=False)
print("\nCountries by Profit:\n", country_performance.head(10))

product_performance = financial_dataset_clean.groupby("Product")[["Profit (in $)", "Sales (in $)"]].sum().sort_values(by="Profit (in $)", ascending=False)
print("\nProducts by Profit:\n", product_performance)

# 7. Save the cleaned, enriched dataset and summary statistics
financial_dataset_clean.to_csv("~/Downloads/Cleaned_Financials_Summary.csv", index=False)
summary.to_csv("~/Downloads/Financial_Summary_Statistics.csv")

# 8. Save all insights into one CSV file with labelled sections
insights_path = os.path.expanduser("~/Downloads/Financial_Insights_Summary.csv")
with open(insights_path, "w") as f:
    f.write("Overall Summary Statistics\n")
    summary.to_csv(f)
    f.write("\n\nSegment Performance\n")
    segment_performance.to_csv(f)
    f.write("\n\nCountry Summary\n")
    country_performance.to_csv(f)
    f.write("\n\nProduct Summary\n")
    product_performance.to_csv(f)