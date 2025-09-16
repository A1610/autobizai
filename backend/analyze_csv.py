import pandas as pd
import os

def analyze_csv(file_path):
    # Convert relative path to absolute path
    abs_path = os.path.abspath(file_path)

    # Read the CSV file using pandas
    df = pd.read_csv(abs_path)

    # Calculate total sales
    total_sales = df['Sales'].sum()

    # Find the top performing product
    top_product = df.groupby('Product')['Sales'].sum().idxmax()

    # Calculate monthly sales summary
    monthly_summary = df.groupby('Month')['Sales'].sum().to_dict()

    # Build insights list
    insights = [
        f"✅ Total sales: ₹{total_sales}",
        f"🏆 Top performing product: {top_product}"
    ]

    for month, sales in monthly_summary.items():
        insights.append(f"📆 {month}: ₹{sales}")

    return insights
