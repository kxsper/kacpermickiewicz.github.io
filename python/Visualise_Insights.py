# 0. IMPORTS

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import warnings

warnings.filterwarnings("ignore")

# AUTO PATH DETECTION

try:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    SCRIPT_DIR = os.getcwd()
    print("Note: Running in interactive mode (__file__ not defined). "
          f"Searching from current working directory:\n  {SCRIPT_DIR}")

os.chdir(SCRIPT_DIR)


# Helper: Automatically find the cleaned CSV file

def find_cleaned_csv():
    # Search recursively for the exact file name
    pattern = "**/*Cleaned_Gallery_Sales_Data.csv"
    matches = glob.glob(pattern, root_dir=SCRIPT_DIR, recursive=True)

    if not matches:
        # Fallback: check directly in root (common case)
        direct_path = os.path.join(SCRIPT_DIR, "Cleaned_Gallery_Sales_Data.csv")
        if os.path.exists(direct_path):
            matches = [direct_path]
        else:
            print("\n" + "=" * 60)
            print("ERROR: 'Cleaned_Gallery_Sales_Data.csv' NOT FOUND")
            print("=" * 60)
            print(f"Searched in and below: {SCRIPT_DIR}")
            print("\nSuggestions:")
            print("  • Make sure the file is in the project folder (or subfolder like 'data/')")
            print("  • File name must match exactly (case-sensitive on Linux/macOS)")
            print("  • Run from project root:")
            print("      cd /path/to/Gallery-Sales-Project")
            print("      python python/analyze_cleaned_data.py")
            print("  • Or move CSV next to this script")
            sys.exit(1)

    if len(matches) > 1:
        print("Warning: Multiple matching files found. Using the first one:")
        for m in matches:
            print(f"  - {os.path.join(SCRIPT_DIR, m)}")

    full_path = os.path.join(SCRIPT_DIR, matches[0])
    print(f"Found cleaned data file: {full_path}")
    return full_path



# MAIN EXECUTION

try:
    csv_path = find_cleaned_csv()

    # Step 1: Load the data
    df = pd.read_csv(csv_path)

    # Ensure correct data types
    df['SaleDate'] = pd.to_datetime(df['SaleDate'], errors='coerce')
    df['Total_GBP'] = pd.to_numeric(df['Total_GBP'], errors='coerce')
    df = df.dropna(subset=['Total_GBP'])  # Drop any invalid revenue rows

    print("\n" + "=" * 60)
    print("GALLERY SALES ANALYSIS - KEY INSIGHTS")
    print("=" * 60)
    print(f"Loaded {df.shape[0]} transactions")

    # Step 2: Compute key insights
    total_revenue = df['Total_GBP'].sum()
    num_transactions = len(df)
    aov = total_revenue / num_transactions if num_transactions > 0 else 0
    repeat_rate = (df['BuyerType'].value_counts(normalize=True).get('Repeat', 0) * 100)
    return_rate = (df[df['Quantity'] < 0].shape[0] / num_transactions) * 100 if num_transactions > 0 else 0

    top_artists = df.groupby('Artist')['Total_GBP'].sum().sort_values(ascending=False).head(5)
    revenue_by_age = df.groupby('AgeGroup')['Total_GBP'].sum().sort_values(ascending=False)
    revenue_by_buyer = df.groupby('BuyerType')['Total_GBP'].sum()
    revenue_by_artwork = df.groupby('ArtworkType')['Total_GBP'].sum().sort_values(ascending=False)
    payment_dist = df['PaymentMethod'].value_counts(normalize=True) * 100

    # Print results
    print(f"\nTotal Revenue:          £{total_revenue:,.2f}")
    print(f"Number of Transactions: {num_transactions}")
    print(f"Average Order Value:    £{aov:,.2f}")
    print(f"Repeat Purchase Rate:   {repeat_rate:.1f}%")
    print(f"Return Rate:            {return_rate:.1f}%")

    print("\nTop 5 Artists by Revenue:")
    for i, (artist, rev) in enumerate(top_artists.items(), 1):
        print(f"  {i}. {artist:<18} £{rev:,.2f}")

    print("\nRevenue by Age Group:")
    print(revenue_by_age.round(2))

    print("\nRevenue by Buyer Type:")
    print(revenue_by_buyer.round(2))

    print("\nRevenue by Artwork Type:")
    print(revenue_by_artwork.round(2))

    print("\nPayment Method Distribution (%):")
    print(payment_dist.round(1))

    # Step 3: Visualizations
    sns.set(style="whitegrid")

    # PLOT 1: Top 5 Artists by Revenue
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_artists.values, y=top_artists.index, palette="Blues_d")
    plt.title('Top 5 Artists by Revenue')
    plt.xlabel('Revenue (£)')
    plt.ylabel('Artist')
    plt.xlim(0, top_artists.max() * 1.1)
    for i, v in enumerate(top_artists.values):
        plt.text(v + top_artists.max() * 0.02, i, f'£{v:,.0f}', va='center')
    plt.tight_layout()
    plt.savefig('top_artists_revenue.png', dpi=150)
    plt.close()

    # PLOT 2: Revenue by Buyer Type (pie)
    plt.figure(figsize=(8, 8))
    plt.pie(revenue_by_buyer, labels=revenue_by_buyer.index, autopct='%1.1f%%',
            colors=sns.color_palette("pastel"), startangle=90)
    plt.title('Revenue Share by Buyer Type')
    plt.savefig('revenue_by_buyer_type.png', dpi=150)
    plt.close()

    # PLOT 3: Revenue by Age Group
    plt.figure(figsize=(10, 6))
    sns.barplot(x=revenue_by_age.values, y=revenue_by_age.index, palette="Greens_d")
    plt.title('Revenue by Age Group')
    plt.xlabel('Revenue (£)')
    plt.ylabel('Age Group')
    plt.xlim(0, revenue_by_age.max() * 1.1)
    for i, v in enumerate(revenue_by_age.values):
        plt.text(v + revenue_by_age.max() * 0.02, i, f'£{v:,.0f}', va='center')
    plt.tight_layout()
    plt.savefig('revenue_by_age_group.png', dpi=150)
    plt.close()

    # PLOT 4: Monthly Revenue Trend
    monthly_revenue = df.resample('ME', on='SaleDate')['Total_GBP'].sum()
    plt.figure(figsize=(12, 6))
    monthly_revenue.plot(kind='line', marker='o', color='teal')
    plt.title('Monthly Revenue Trend')
    plt.ylabel('Revenue (£)')
    plt.xlabel('Month')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('monthly_revenue_trend.png', dpi=150)
    plt.close()

    print("\n" + "=" * 60)
    print("VISUALIZATIONS SAVED:")
    print("  • top_artists_revenue.png")
    print("  • revenue_by_buyer_type.png")
    print("  • revenue_by_age_group.png")
    print("  • monthly_revenue_trend.png")
    print("=" * 60)
    print(f"All files saved to: {os.getcwd()}")
    print("Analysis complete.")

except FileNotFoundError as e:
    print(e)
    sys.exit(1)
except Exception as e:
    print(f"Error during execution: {e}")
    sys.exit(1)