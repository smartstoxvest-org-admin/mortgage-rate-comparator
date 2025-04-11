import pandas as pd

def get_realistic_mortgage_rates():
    # Replace YOUR_USERNAME and YOUR_REPO with your actual GitHub repo path
    csv_url = "https://raw.githubusercontent.com/smartstoxvest-org-admin/mortgage-rate-comparator/main/mortgage_rates.csv"
    return pd.read_csv(csv_url)
