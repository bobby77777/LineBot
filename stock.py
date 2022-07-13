import pandas as pd
import numpy as np
import json
import requests
from datetime import date, timedelta

def Get_StockPrice(Symbol, previousDay=1):
    Date = str(date.today()).replace('-','')
    url = f'https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date={Date}&stockNo={Symbol}'

    data = requests.get(url).text
    json_data = json.loads(data)
    stock_name = [item for item in json_data["title"].split(' ') if item != ''][-2]
    try:
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
        
        # StockPrice = StockPrice.set_index('Date', drop = True)
        StockPrice = StockPrice[['Date', 'Close','Open','High','Low','Volume']]
        # print(StockPrice[-previousDay: :])
        # if len(Date) < 8:
        # print(StockPrice.loc[Date[:4]+'-'+Date[4:6]+'-'+Date[-2:]:])
        return [stock_name, StockPrice[-int(previousDay): :]]
    except:
        return 'incorrect'

if __name__ == '__main__':
    userSend = ['2330', '5']
    data = Get_StockPrice('2330', '5')
    print(data[0])
    for d in data[1].values:
        print('\n{}\n收盤:{}\n開盤:{}\n最高價:{}\n最低價:{}\n交易量(張):{}'.format(\
                d[0].date(), d[1], d[2], d[3], d[4], d[5]))