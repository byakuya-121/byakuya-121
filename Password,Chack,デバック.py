""""|プログラムコードの内容と趣旨｜(Contents and purpose of the program code)
-----------------------------------------------------------------------------------------------------------------
・アルゴリズムの内容
 #このPython言語のソースコードは、特定のパスワードをGUIのテキストボックスに入れ" 確認"のボタンを押すことで指定した
 time.sleep(2)のカッコ内の数値に合わせて処理をする様に模擬をした後にパスワードの関数処理を行う。
 エントリーボックスの中は[*]で文字を隠します。

#(*注意事項)：プログラムコードを変える際には”必ず”保存してから内容を変える様にお願いします。
 実行する前に,コマンドプロンプトでしなければならないリストを書きました。以下を参照してください。
=================================================================================
pip install tkinter
pip install PhotoImage
pip install PIL
pip install tqdm #入れなくてもいい                                             
# 実行する前に,以下のコマンドをターミナルで実行してください。     
=============================================================================
ソースコードの内容を変えて実行する場合、必ず前に実行したウインドは閉じてください。閉じ無くて実行しても変わりません。
-----------------------------------------------------------------------------------------------------------------
・使用方法について
 # あらかじめ設定したパスワードをテキストボックスに記入し合っていたら[解除成功しました!!]と表示しパスワードが間違いがある
 場合には、[パスワードが違います.もう一度入れてください。]と表示されます。
以上です。
"""
#///////////////////////////////////////////////////////////////////////////////
# **********//Definitions//******************
import os  #絶対パス定義 OS
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from threading import Thread
import time
from tkinter import ttk  # 進行状況バー用
# ******//Number of Value Substitution Definitions//****************
Button_WIDTH = 5   # width of the button 
Button_HEIGHT= 2  # height of the button
TEXT_WIDTH = 40 # width of the text box
#STOP_GUI = 5.0 # Mock stop time(in seconds)
WIDTH_GUI = 50  #Processing GUI width
LOADING_GUI = 5000 # 1000 = 1 second
# **特定のパスワード**
SET_PASSWORDS = 'ito' #Insert the password of the password number
print ('===========Configured password======================')
print("Your settings password is :" + SET_PASSWORDS )
print ('====================================================')
# ******************************************************************
# |Display the code processing taskbar|
# // GUI setup code // 
root = tk.Tk()
 #//root = tkinter.Tk()
root.title("SPYハッカーWind")
root.configure(bg='#333333')
# GUI setup icon
root.iconbitmap(os.path.abspath('images/OIP.ico'))
# Image setup
img = ImageTk.PhotoImage(Image.open(os.path.abspath('E:/VSCコード保存ファイル/文化祭準備プログラムコード/images/Shun.png')))

# Canvas setup
c = tk.Canvas(root, width=400, height=250)
c_img = c.create_image(200, 125, image=img)  # 画像の配置
c.pack()

# ===============|絶対パス(画像挿入)|============================== 
"""
# 画像の読み込み
# グローバル変数として保持
img = None
# 画像の読み込み
try:
    img_path = os.path.abspath('images/Shutt.png')  # 画像のパスを指定
    img = Image.open(img_path)
    photo = ImageTk.PhotoImage(img)
    # Canvasを作成
    c = tk.Canvas(root, width=600, height=300)
    c.pack()
    # 画像をCanvasに挿入
    c.create_image(300, 150, image=photo)  # 中央に配置

except Exception as e:
    print("エラーが発生しました:", e)
print("画像のパス:", img_path)
"""
#****************//Chack the code Run //**********************
# 画像の絶対パスを取得
img_path = os.path.abspath('images/shutt.png')
print("画像の絶対パス:", img_path)
# 画像ファイルが存在するか確認
if os.path.exists(img_path):
    print("画像ファイルは存在します。")
else:
    print("画像ファイルは存在しません。")
#**********************************************************
#---//GUI size seting code//--
root.geometry("400x250")
correct_password = SET_PASSWORDS # set the correct password
#  //GUi Labeling code //
label = tk.Label(root, text="パスワードを入力してください",fg="#85D5BF",bg="#000000",font=("Adobe Thai",17),relief="sunken",bd=10)
label.pack(pady=10)

# ロード画面を作成する関数
def show_loading():
    loading_window = tk.Toplevel(root)
    loading_window.title("ロード中")
    loading_window.geometry("200x100")
    loading_window.configure(bg='#333333')
    # 「処理中...」ラベルの設定
    loading_label = tk.Label(loading_window, text="処理中...", fg="#85D5BF", bg="#333333", font=("Adobe Thai", 14))
    loading_label.pack(pady=10)
    # 進行状況バーの設定
    progress = ttk.Progressbar(loading_window, orient=tk.HORIZONTAL, length=200, mode='determinate')
    progress.pack(pady=20)
    
    return loading_window,progress

def show_success():
    success_window = tk.Toplevel(root)
    success_window.title("成功")
    success_window.geometry("475x356")
    success_window.configure(bg='#333333')
    # 画像の設定
    img_success = ImageTk.PhotoImage(Image.open(os.path.abspath('images/hatukaa.png')))
    img_label = tk.Label(success_window, image=img_success)
    img_label.image = img_success  # 参照を保持するために必要
    success_label = tk.Label(success_window,text="ロック解除されました!", fg="#2F4F4F", bg="#00FF00", font=("Verdana 12", 20))
    img_label.pack(pady=10)
    success_label.pack(pady=50)
    success_window.after(LOADING_GUI, success_window.destroy) #<---LOADING_GUI秒後にウィンドウを閉じる


# //パスワードを確認する関数//
def check_password():
    loading_window,progress = show_loading()
    
    # スレッドで時間のかかる処理を行う
    def run_check():
        for i in range(100):
           time.sleep(2)  # ここで処理を模擬し待つ（2秒待つ）
           progress['value'] += 1
           loading_window.update_idletasks()
    input_password = entry.get()
    loading_window.destroy()  # ロード画面を閉じる

    if input_password == correct_password:
            messagebox.showinfo("結果", "Success (アクセスに成功しました...)")
            show_success()
    else:
        messagebox.showerror("結果", "Failure(パスワードが間違っています...アクセス拒否)")
        entry.delete(0, tk.END)  # 入力ボックスをクリア

    # 新しいスレッドでパスワード確認を実行
    Thread(target=run_check).start()

# エントリーボックス 
entry = tk.Entry(root, show="*",width=TEXT_WIDTH)
entry.pack(pady=5)

# ボタン
button = tk.Button(root, text="確認", command=check_password ,bg="#696969",width= Button_WIDTH,height=Button_HEIGHT)
button.pack(pady=20)

# メインループの開始
root.mainloop()
print("//All green// set up GUI !!")
print()
# //////////////////////////////////////////////////////////////////////////////
#------------------------------------------------------------------------
 # **Memo in https site**
""" 
/GUI setting clor References https://itsakura.com/html-color-codes
・My Gif hub https://github.com/byakuya-121/byakuya-121.git
"""
#------------------------------------------------------------------------
