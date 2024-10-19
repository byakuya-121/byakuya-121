from CHRLINE import *
import re
import time
import random
email = ""
password = ""
cl = CHRLINE(email, password, device="IOSIPAD")#管理者権限のあるアカウント
email = ""
password = ""
cl2 = CHRLINE(email, password, device="IOSIPAD")
email = ""
password = ""
cl3 = CHRLINE(email, password, device="IOSIPAD")
email = ""
password = ""
cl4 = CHRLINE(email, password, device="IOSIPAD")
email = ""
password = ""
cl5 = CHRLINE(email, password, device="IOSIPAD")
No1 = "" 
No2 = ""
No3 = ""
No4 = ""
No5 = ""
n = 1
word = "passkey[100]"
stime = 1
events = cl.fetchMyEvents()
while True:
    events = cl.fetchMyEvents(syncToken=events[3])
    for e in events[2]:
        print("検知")
        messageText = ""

        try:
            messageText = e[4][30][2][1][10]  
        except:
            pass



        if e[3] == 29:
            
            message = e[4][30][2][1]

            _squareChatMid = message[2]

            if True:
                try:
                    messageText = e[10]
                except:
                    pass

                if cl.squareMemberIdIsMe(message[1]):
                    # 自分のメッセージ
                    if message.get(10) is not None:
                        print(messageText)# テキストメッセージ
                        try:
                            messageText = e[10]
                        except:
                            pass
                                            

                        # 管理者しか打てないコマンド
                        if messageText.startswith("!check"):
                            cl.sendSquareMessage(message[2], "正常に稼働中")


                        if messageText.startswith("!実行word:"):   
                            word = messageText[8:]
                            cl.sendSquareMessage(message[2],"設定完了")
                            print(word)
                        if messageText.startswith("全員呼び出し"):
                            cl.sendSuperEzTagAll(message[2],"")
                        if messageText.startswith("!送信間隔:"):
                            stime=messageText[6:]
                            
                            cl.sendSquareMessage(message[2],"設定完了")
                            print(stime)
                        if messageText.startswith("!ユニコ設定:"):
                            input_string = messageText[7:]
                            try:
                                result1, result2= input_string.split('#')
                            except:
                                cl.sendSquareMessage(message[2],"失敗")
                            if result1 == "No1":
                                No1 = result2
                            if result1 == "No2":
                                No2 = result2
                            if result1 == "No3":
                                No3 = result2
                            if result1 == "No4":
                                No4 = result2
                            if result1 == "No5":
                                No5 = result2  
                            cl.sendSquareMessage(message[2],"設定完了")                                                                                              
                        if messageText.startswith("!help"):
                            cl.sendSquareMessage(message[2],"使い方\n[]の中の文字がコマンド\n[!実行word:ここに実行ワード]で開始コマンドを設定できます\n[!送信間隔:ここに秒単位(0.5なども可)]で送信間隔の指定\n[!ユニコ設定:ユニコの識別子(No1のように記述)#ユニコ]これでユニコの設定")
                        if messageText.startswith("!確認"):
                            cl.sendSquareMessage(message[2],f"送信間隔:{stime}\nキーワード:{word}")    
                        if messageText.startswith("!確認(危険)"):
                            cl.sendSquareMessage(message[2],f"No1:{No1}")   
                        if messageText == word:
                            while True:                
                                try:
                                    No1 = No1[10:]
                                    random_hex_string = '{:x}'.format(random.randint(0, 0xFFFFFF))
                                    cl.sendSquareMessage(squareChatMid=message[2],text=No1+"[No1:"+random_hex_string+"]")
                                    time.sleep(int(stime))
                                except:
                                    pass
                                try:
                                    No2 = No2[10:]
                                    random_hex_string = '{:x}'.format(random.randint(0, 0xFFFFFF))
                                    cl2.sendSquareMessage(squareChatMid=message[2],text=No2+"[No2:"+random_hex_string+"]")
                                    time.sleep(int(stime))
                                except:
                                    pass                            
                                try:
                                    No3 = No3[10:]
                                    random_hex_string = '{:x}'.format(random.randint(0, 0xFFFFFF))
                                    cl3.sendSquareMessage(squareChatMid=message[2],text=No3+"[No3:"+random_hex_string+"]")
                                    time.sleep(int(stime))
                                except:
                                    pass                            

                                try:
                                    No4 = No4[10:]
                                    random_hex_string = '{:x}'.format(random.randint(0, 0xFFFFFF))
                                    cl4.sendSquareMessage(squareChatMid=message[2],text=No4+"[No4:"+random_hex_string+"]")
                                    time.sleep(int(stime))
                                except:
                                    pass                            
                                try:
                                    No5 = No5[10:]
                                    random_hex_string = '{:x}'.format(random.randint(0, 0xFFFFFF))
                                    cl5.sendSquareMessage(squareChatMid=message[2],text=No5+"[No5:"+random_hex_string+"]")
                                    time.sleep(int(stime))
                                except:
                                    pass                            