from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from flask import Flask, request, abort
from linebot.exceptions import InvalidSignatureError
app = Flask(__name__)

# LINE Botのアクセストークンとチャンネルシークレット
line_bot_api = LineBotApi('5EUPbzVmE3cFftCNGEBdI2BS0S/itvb5MFUVlgUsct1q7gXg4eqtGF7gv5RbQydRQ0c+vsgS0S5VlxQoSgLcyDCJyvJn8y9sc1MAk5Kzo6ZRM4HUmVc9OUeWNVm/WUPb68gq1ZRmTB5bxiZvDG+0JQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('be7f09e7447db25c1d40962628c6dec1')

# 権限を持つユーザーのリスト
authorized_users = ['Ua0adfa16cd8c5778335c034d36ffa292', 'USER_ID_2']
                     #//Administrators一覧//
                      #自分
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    if user_id in authorized_users:
        if event.message.text == "/active":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="コマンドが実行されました。")
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="無効なコマンドです。")
            )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="あなたにはこのコマンドを実行する権限がありません。")
        )

if __name__ == "__main__":
    app.run(debug=True)


