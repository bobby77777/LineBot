import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def get_halfyear(country):
    url = 'https://rate.bot.com.tw/xrt/quote/l6m/'+ country
    headers={
    'accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': '_tb_token_=berT80V49uJ9PFEJKGPI; cna=IhV+FpiDqRsCAXE54OSIgfFP; v=0; t=bb1c685b877ff64669f99c9dade7042c; cookie2=1e5103120f9886062722c86a5fad8c64; uc1=cookie14=UoTbm8P7LhIRQg%3D%3D; isg=BJWVw-e2ZCOuRUDfqsuI4YF0pJFFPHuu_ffxbBc6UYxbbrVg3-JZdKMoODL97mFc; l=dBMDiW9Rqv8wgDSFBOCiVZ9JHt_OSIRAguWfypeMi_5Zl681GgQOkUvZ8FJ6VjWftBTB4tm2-g29-etki6jgwbd6TCNQOxDc.',
    'referer': 'https://item-paimai.taobao.com/pmp_item/609160317276.htm?s=pmp_detail&spm=a213x.7340941.2001.61.1aec2cb6RKlKoy',
    'sec-fetch-mode': 'cors',
    "sec-fetch-site": 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
    }
    read = requests.get(url,headers=headers).text
    soup = BeautifulSoup(read, 'html.parser')
    i = 0
    date = []
    money = []
    [date.append(t.getText()) for t in soup.find_all('td', class_="text-center") if t.getText().find(country)==-1]
    for t in soup.find_all('td', class_="rate-content-sight"):
        if i % 2:
            money.append(float(t.getText()))
        i+=1

    # plot graph
    plt.figure(figsize=(40,20))
    plt.grid(axis='y',linestyle='-.', color='gray')
    plt.plot(date[::-1], money[::-1],c = "m",alpha=0.6)
    # 設定圖例，參數為標籤、位置
    # plt.xlabel("Date", fontsize = 12, fontweight = "bold")
    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(12))
    plt.xticks(rotation=15,fontsize=20)
    
    # plt.gca().yaxis.set_major_locator(ticker.MultipleLocator((max(money)-min(money))/8))
    # plt.ylabel(country,labelpad=50, fontsize = 15, fontweight = "bold")
    plt.yticks(fontsize=20)
    
    plt.title("Taiwan Bank Exchange Rate - "+country, fontsize = 25, fontweight = "bold", pad=30)
    
    plt.savefig("currency.png")

    
    return [date[0],money[0]]
    
if __name__ == '__main__':
    country = 'JPY'
    # country = 'USD'
    get_halfyear(country)