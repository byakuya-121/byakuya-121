from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.exceptions import LineBotApiError

# Flaskなどのウェブフレームワークを使ってWebhookを設定
from flask import Flask, request, abort

app = Flask(__name__)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except LineBotApiError as e:
        print(f"Error: {e}")
        abort(400)
    return 'OK'

if __name__ == "__main__":
    app.run(debug=True)

# LINE Botのアクセストークンとチャンネルシークレット
line_bot_api = LineBotApi('5EUPbzVmE3cFftCNGEBdI2BS0S/itvb5MFUVlgUsct1q7gXg4eqtGF7gv5RbQydRQ0c+vsgS0S5VlxQoSgLcyDCJyvJn8y9sc1MAk5Kzo6ZRM4HUmVc9OUeWNVm/WUPb68gq1ZRmTB5bxiZvDG+0JQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('be7f09e7447db25c1d40962628c6dec1')

# ユーザーの警告回数を記録する辞書
user_warnings = {}

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    group_id = event.source.group_id

    # ルール違反のメッセージを検出
    if "ルール違反" in event.message.text:
        if user_id not in user_warnings:
            user_warnings[user_id] = 1
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="警告: ルールを破りました。次回は追放されます。")
            )
        else:
            user_warnings[user_id] += 1
            if user_warnings[user_id] >= 2:
                try:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text="2回目の警告: グループから追放されます。")
                    )
                    line_bot_api.leave_group(group_id)
                except LineBotApiError as e:
                    print(f"Error: {e}")

if __name__ == "__main__":
    app.run(debug=True)