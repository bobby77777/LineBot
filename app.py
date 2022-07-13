import os
import configparser
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImagemapSendMessage
from stock import *

# # LINE 聊天機器人的基本資料
# config = configparser.ConfigParser()
# config.read('config.ini')
# print(config.get('line-bot', 'channel_access_token'))

line_bot_api = LineBotApi(os.environ["channel_access_token"])
handler = WebhookHandler(os.environ['channel_secret'])

app = Flask(__name__)


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
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # event->使用者資料
    userSend = event.message.text
    if userSend.isdigit() and len(userSend)==4:
        data = Get_StockPrice(userSend,'20220531')
        print('======================')
        print(data)
        print(type(data))
        print('======================')
        if data == 'incorrect':
            info = '請輸入正確的股票代號'
        else:
            data = data.values[0]
            info = '收盤:{}\n開盤:{}\n最高價:{}\n最低價:{}\n交易量(張):{}'.format(\
                data[0], data[1], data[2], data[3], data[4])
        
            
        message = TextSendMessage(text=info)

    else:
        message = TextSendMessage(text='你可以傳個股票代碼試試')
    
    line_bot_api.reply_message(event.reply_token, message)





if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)