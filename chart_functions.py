import plotly.express as px
import pandas as pd

def chart_currency_part(transaction_list, currency_list):
    transaction_data = []
    for transaction in transaction_list:
        currency_code = transaction.currency
        transaction_amount = transaction.amount
        for currency in currency_list:
            if currency.code == currency_code:
                currency_value = currency.value
                currency_name = currency.name
                break
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
    fig = px.pie(pie_df, values='Value (USD)', names='Currency Name', title='Currencies as part of whole market')
    # Show the chart
    fig.show()

