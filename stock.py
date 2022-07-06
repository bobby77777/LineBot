import pandas as pd
import numpy as np
import json
import requests
from datetime import date

def Get_StockPrice(Symbol, Date=str(date.today()).replace('-','')):

    url = f'https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date={Date}&stockNo={Symbol}'

    data = requests.get(url).text
    json_data = json.loads(data)
    Stock_data = json_data['data']
    StockPrice = pd.DataFrame(Stock_data, columns = ['Date','Volume','Volume_Cash','Open','High','Low','Close','Change','Order'])
    StockPrice['Date'] = StockPrice['Date'].str.replace('/','').astype(int) + 19110000
    StockPrice['Date'] = pd.to_datetime(StockPrice['Date'].astype(str))
    StockPrice['Volume'] = StockPrice['Volume'].str.replace(',','').astype(float)/1000
    StockPrice['Volume_Cash'] = StockPrice['Volume_Cash'].str.replace(',','').astype(float)
    StockPrice['Order'] = StockPrice['Order'].str.replace(',','').astype(float)

    StockPrice['Open'] = StockPrice['Open'].str.replace(',','').astype(float)
    StockPrice['High'] = StockPrice['High'].str.replace(',','').astype(float)
    StockPrice['Low'] = StockPrice['Low'].str.replace(',','').astype(float)
    StockPrice['Close'] = StockPrice['Close'].str.replace(',','').astype(float)

    StockPrice = StockPrice.set_index('Date', drop = True)
    StockPrice = StockPrice[['Open','High','Low','Close','Volume']]
    # if len(Date) < 8:
    print(StockPrice.loc[Date[:4]+'-'+Date[4:6]+'-'+Date[-2:]:])
    return StockPrice.loc[Date[:4]+'-'+Date[4:6]+'-'+Date[-2:]:]

if __name__ == '__main__':

    data = Get_StockPrice('2330','20220531')
    print(data.Open)