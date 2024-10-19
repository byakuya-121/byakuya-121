from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from flask import Flask, request, abort
from linebot.exceptions import InvalidSignatureError
app = Flask(__name__)

# LINE Botのアクセストークンとチャンネルシークレット
line_bot_api = LineBotApi(''YOU_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')

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


