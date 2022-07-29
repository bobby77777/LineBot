import os
import json
import requests
from linebot import LineBotApi, WebhookHandler

Authorization_token = "Bearer"+ os.environ["channel_access_token"]
headers = {"Authorization":Authorization_token, "Content-Type":"application/json"}

body = json.load(open('../json/rich_menu_body.json'))

req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu',
                       headers=headers,data=json.dumps(body).encode('utf-8'))


line_bot_api = LineBotApi(os.environ["channel_access_token"])
rich_menu_id = json.loads(req.text)["richMenuId"]

path = "./photos/richmenu.png" # 主選單的照片路徑

with open(path, 'rb') as f:
    line_bot_api.set_rich_menu_image(rich_menu_id, "image/png", f)
req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/'+rich_menu_id,
                       headers=headers)


# Delete rich menu
# for item in rich_menu_list:
#     req = requests.request('DELETE', 'https://api.line.me/v2/bot/richmenu/'+item.rich_menu_id,
#                        headers=headers)
    # line_bot_api.delete_rich_menu(item.rich_menu_id)  # with api
rich_menu_list = line_bot_api.get_rich_menu_list()
print(rich_menu_list)