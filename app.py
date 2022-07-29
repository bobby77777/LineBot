import os
import configparser
import pandas as pd
from datetime import date
from flask import Flask, request, abort
import pyimgur
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
from currency import get_halfyear
from stock import *


line_bot_api = LineBotApi(os.environ["channel_access_token"])
handler = WebhookHandler(os.environ['channel_secret'])
imgur_id = os.environ["imgur_id"]
currency_bubble = json.load(open('./bubble.json'))
app = Flask(__name__)
im = pyimgur.Imgur(imgur_id)


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST','GET'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        print(body, signature)
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'
    

# 處理訊息
@handler.add(MessageEvent)
def handle_message(event):
    # event->使用者資料
    # print(event)
    profile = line_bot_api.get_profile(event.sourcet.userId)
    print(profile.display_name)
    print(profile.user_id)
    if event.message.type != 'text':
        message = TextSendMessage(text='你可以傳個股票代碼試試')
    else:
        userSend = event.message.text
        print('======================')
        print(userSend)
        print('======================')
        userSend = [item for item in userSend.split(' ') if item != '']
        Date = str(date.today()).replace('-','')
        if userSend[0].isdigit():
            if len(userSend) > 1:
                # userSend[0], data[0] -> symbol, 中文名
                pre = int(userSend[1])
                data = Get_StockPrice(userSend[0], pre,Date)
            else:
                pre = 20
                data = Get_StockPrice(userSend[0])
            print('======================')
            print(data)
            print(type(data))
            print('======================')
            if type(data) == type('incorrect'):
                message = TextSendMessage(text='請輸入正確的股票代號')
                
            else:
                # data[0] -> symbol
                while len(data[1]) < int(pre):
                    month = str(int(Date[4:6])-1)
                    if month == '0':
                        Date = str(int(Date[0:4])-1)+'1201'
                    else:
                        month = '0'+month if len(month) < 2 else month
                        Date = Date[0:4]+month+'01'
                    data[1] = pd.concat([Get_StockPrice(userSend[0],  str(pre-len(data[1])), Date)[1],data[1]])
                # TEXT message
                info = data[0]+'\n----------------'
                d = data[1].values[-1]
                info += '\n{}\n收盤:{}\n開盤:{}\n最高價:{}\n最低價:{}\n交易量(張):{}\n'\
                    .format(d[0].date(), d[4], d[1], d[2], d[3], d[5])
                info = info[:-1]
                message = TextSendMessage(text=info)
                # Image message
                stock_graph(userSend[0], data[1])
                path = "./photos/send.png"
                uploaded_image = im.upload_image(path, title="Uploaded with PyImgur")
                image_message = ImageSendMessage(original_content_url=uploaded_image.link,\
                                                preview_image_url=uploaded_image.link)
                reply_arr = [message, image_message]
                line_bot_api.reply_message(event.reply_token, reply_arr)
                return 0
        else:
            if userSend[0] == '匯率':
                bubble_image = im.get_image('x35HtQC').link
                currency_bubble["hero"]["url"] = bubble_image
                message = FlexSendMessage(alt_text='請選擇幣別', contents=currency_bubble)
            elif userSend[0] == '創作者':
                # message = FlexSendMessage(alt_text='請選擇幣別', contents=currency_bubble)
                message = TextSendMessage(text='W.Z\nBobby')
            elif userSend[0] == '使用說明':
                description = '請嘗試輸入：台股上市的股票代碼\n進階輸入:台股上市的股票代碼\" \"統計天數'
                message = TextSendMessage(text=description)
            else:
                message = TextSendMessage(text='你可以傳個股票代碼試試')

    line_bot_api.reply_message(event.reply_token, message)
    return 0
@handler.add(PostbackEvent)
def handle_message(event):   
    date,money = get_halfyear(event.postback.data)
    info = event.postback.data+'\n----------------\n'
    info += '\n'.join([date[idx][5:]+': '+ str(money[idx]) for idx in range(len(date))])
    message = TextSendMessage(text=info)
    path = "./photos/currency.png"
    uploaded_image = im.upload_image(path, title="Uploaded with PyImgur")
    image_message = ImageSendMessage(original_content_url=uploaded_image.link,\
                            preview_image_url=uploaded_image.link)
    reply_arr = [message, image_message]
    line_bot_api.reply_message(event.reply_token, reply_arr)

    return 0




if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)