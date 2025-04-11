import pandas as pd

def get_mock_mortgage_rates():
    data = [
        {"bank": "Halifax", "rate_type": "Fixed", "rate": 4.10, "term": "2 Year", "ltv": "75%", "fee": 999},
        {"bank": "Barclays", "rate_type": "Fixed", "rate": 4.35, "term": "5 Year", "ltv": "60%", "fee": 0},
        {"bank": "Nationwide", "rate_type": "Tracker", "rate": 4.55, "term": "2 Year", "ltv": "90%", "fee": 495},
        {"bank": "NatWest", "rate_type": "Variable", "rate": 5.10, "term": "Lifetime", "ltv": "75%", "fee": 0},
        {"bank": "HSBC", "rate_type": "Fixed", "rate": 4.25, "term": "5 Year", "ltv": "90%", "fee": 999},
    ]
    return pd.DataFrame(data)
