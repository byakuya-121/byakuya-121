from flask import Flask, request, abort 
import requests
import json

app = Flask(__name__)

access_token = '5EUPbzVmE3cFftCNGEBdI2BS0S/itvb5MFUVlgUsct1q7gXg4eqtGF7gv5RbQydRQ0c+vsgS0S5VlxQoSgLcyDCJyvJn8y9sc1MAk5Kzo6ZRM4HUmVc9OUeWNVm/WUPb68gq1ZRmTB5bxiZvDG+0JQdB04t89/1O/w1cDnyilFU='
banned_keywords = ['badword1', 'badword2', 'badword3']
reply_url = 'https://api.line.me/v2/bot/message/reply'
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {access_token}'
}

@app.route('/callback', methods=['POST'])
def callback():
    try:
        body = request.get_json()
        
        if 'events' not in body:
            return 'OK'
        
        for event in body['events']:
            if event['type'] == 'massage' and event['message']['type'] == 'text':
                user_message = event['message']['text']
                reply_token = event['replyToken']
                
                if any(keyword in user_message for keyword in banned_keywords):
                    reply_message = '不適切なメッセージが検出されました。'
                    send_reply(reply_token, reply_message)
        
        return 'OK'
    except Exception as e:
        print(f'Error: {e}')
        abort(500)

def send_reply(reply_token, message):
    data = {
        'replyToken': reply_token,
        'messages': [
            {
                'type': 'text',
                'text': message
            }
        ]
    }
    
    try:
        response = requests.post(reply_url, headers=headers, json=data)
        print(response.status_code)
        print(response.json())
    except Exception as e:
        print(f'Error sending reply: {e}')

if __name__ == "__main__":
    app.run(debug=True)