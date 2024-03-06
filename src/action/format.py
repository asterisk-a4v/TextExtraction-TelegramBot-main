def format_input(trade):
    return f"""

Symbol: {trade["SYMBOL"]}
Action: {trade["ACTION"]}
Stop Loss: {trade["S/L"]}
Take Profit: {trade["T/P"]}
_______________________
Entry Price: {trade["ENTRY PRICE"]}
Current Price: {trade["CURRENT PRICE"]}
"""
