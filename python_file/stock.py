import os
import json
import requests
import numpy as np
import pandas as pd
import matplotlib
import mplfinance as mpf
import matplotlib.pyplot as plt
from datetime import date

headers={
        'accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
        # 'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-TW,zh;q=0.9',
        'sec-fetch-mode': 'cors',
        "sec-fetch-site": 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
        }

def Get_StockPrice(Symbol, previousDay=1, Date=str(date.today()).replace('-','')):
    global headers
    url = f'https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date={Date}&stockNo={Symbol}'
    data = requests.get(url,headers=headers).text
    json_data = json.loads(data)
    try:
        stock_code = [item for item in json_data["title"].split(' ') if item != ''][-2]
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
        StockPrice = StockPrice[['Date','Open','High','Low', 'Close', 'Volume']]
        # print(StockPrice[-previousDay: :])
        # if len(Date) < 8:
        # print(StockPrice.loc[Date[:4]+'-'+Date[4:6]+'-'+Date[-2:]:])
        return [stock_code, StockPrice[-int(previousDay): :]]
    except:
        return 'incorrect'

def stock_graph(stock_code, data):
    data = data.set_index('Date', drop = True)
    mc = mpf.make_marketcolors(up='r', down='g', inherit=True)
    s = mpf.make_mpf_style(base_mpf_style='yahoo', marketcolors=mc)
    kwargs = dict(type='candle', mav=(5,20), volume=True, panel_ratios=(3,1), figratio=(20,10), figscale=0.75, title='\n\n'+stock_code, style=s)
    mpf.plot(data, **kwargs,savefig='./photos/send.png')

def top5():
    info = '    TOP 5 (股數排行) \n===================\n'
    url = 'https://www.twse.com.tw/exchangeReport/MI_INDEX20?response=csv&date=' + str(date.today()).replace('-','')
    global headers
    
    read = requests.get(url,headers=headers).text
    data = read.replace('=','').replace('\r','').split('\n')[2:7]

    for d in data:
        d = [item for item in d.split('\"') if item != '' and item != ',']
        for i in range(5):
            if i == 4:
                info += '\n'
            elif i == 0:
                info += d[i]+ '. '
            else:
                if d[i].find(',') != -1:
                    info += d[i][:d[i].find(',')+2].replace(',','.') + 'M'
                else:
                    info += d[i] + ' '
    return info[:-1]

if __name__ == '__main__':
    userSend = ['6830', '5']
    Date = '20220701'
    data = Get_StockPrice(userSend[0],  userSend[1], '20220902')
    while len(data[1]) < int(userSend[1]):
        month = str(int(Date[4:6])-1)
        if month == '0':
            Date = str(int(Date[0:4])-1)+'1201'
        else:
            month = '0'+month if len(month) < 2 else month
            Date = Date[0:4]+month+'01'
        if type(Get_StockPrice(userSend[0],  str(int(userSend[1])-len(data[1])), Date)[1]) != type(str()):
            print('------')
            print(type(Get_StockPrice(userSend[0],  str(int(userSend[1])-len(data[1])), Date)[1]))
            print('------')
            data[1] = pd.concat([Get_StockPrice(userSend[0],  str(int(userSend[1])-len(data[1])), Date)[1],data[1]])
        else: break
        # new = pd.concat(,)
    # for d in data[1].values:
    #     print('\n{}\n收盤:{}\n開盤:{}\n最高價:{}\n最低價:{}\n交易量(張):{}'.format(\
    #             d[0].date(), d[1], d[2], d[3], d[4], d[5]))
    # stock_graph('2334',data[1])
    # print(top5())