import plotly.express as px
import pandas as pd

def chart_currency_part(transactions_collection, currencies_collection):
    transaction_data = []
    transactions_collection_find  = transactions_collection.find()
    for transaction in transactions_collection_find:
        transaction_amount = transaction["amount"]
        currency_id = transaction["currency"]
        filter_query = {"_id": currency_id}
        currency = currencies_collection.find_one(filter_query)
        currency_value = currency["value"]
        currency_name = currency["name"]
        current_dict = {'currency_name':currency_name, 'transaction_value':(transaction_amount * currency_value)}
        transaction_data.append(current_dict)
    df = pd.DataFrame(transaction_data)
    currency_total = df.groupby('currency_name')['transaction_value'].sum() 
    total_market_value = currency_total.sum()
    currency_percentage = (currency_total / total_market_value) * 100
    data = {
    'Currency Name': currency_percentage.index,
    'Value (USD)': currency_percentage.values
    }
    pie_df = pd.DataFrame(data)
    fig = px.pie(pie_df, values='Value (USD)', names='Currency Name', title='Crypto Market Cap')
    # Show the chart
    fig.show()

