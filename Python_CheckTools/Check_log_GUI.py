#==========================================
import re
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading
import psutil
import os
import sys
from datetime import datetime
from tkinter import filedialog
from tkinter import scrolledtext
import time
import winsound
#========================================
 #Python GUI 設定
root = tk.Tk()
root.title("Developer Tools")
root.configure(bg='#233B6C')
root.geometry("680x550")
background_color = '#c18af5'
#========================================
# システム通知音を再生
winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)

def update_status():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    cpu_label.config(text=f"・CPU使用率: {cpu_usage}%")
    memory_label.config(text=f"・メモリ使用率: {memory_info.percent}%")
    root.update_idletasks()

    if cpu_usage >= 100:
        add_warning_message()

    if memory_info.percent >= 90:
        add_memory_message()

    root.after(1000, update_status)

def add_warning_message():
    warning_textbox.delete(1.0, tk.END)
    warning_textbox.insert(tk.END, "Warning⚠️:CPUの使用率が100%超えています!*")
    root.after(1000, add_warning_message)


def add_memory_message():
    warning_textbox.delete(1.0, tk.END)
    warning_textbox.insert(tk.END, "Warning⚠️: メモリーの使用率が90%超えています!*")

warning_textbox = tk.Text(root, height=4, width=30) #警告用テキストボックス
warning_textbox.place(x=430, y=40)
warning_textbox.insert(tk.END, "--Text dedicated to the warning message*!📋--")


cpu_label = ttk.Label(root, text="CPU使用率:", background=background_color, width=50)
cpu_label.place(x=20, y=40)

memory_label = ttk.Label(root, text="メモリ使用率:", background=background_color, width=50)
memory_label.place(x=20, y=60)

info_text = tk.Label(root, text="現在の情報:INFO PC", bg='#c18af5', width=50)
info_text.place(x=20, y=5)

time_info = tk.Label(root, text="現在の時間:", background=background_color, width=50)
time_info.place(x=20, y=100)

time_label = tk.Label(root, font=('Helvetica', 14))
time_label.place(x=30, y=130)

Warning_info = tk.Label(root, text="警告メッセージlog", background='#f6f26a', width=20)
Warning_info.place(x=430, y=13)

log_text = tk.Label(root, text="*Logs テキストボックス*", font=('Helvetica',10))
log_text.place(x=15, y=190)

def update_time():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time_label.config(text=current_time)
    root.after(1000, update_time)

update_time()

root.after(1000, update_status)  # ステータス更新のループを開始する

def confirm_exit():
    if messagebox.askyesno("終了確認", "本当に終了しますか？"):
        sys.exit(0)

button = tk.Button(root, text="アプリケーションを終了", command=confirm_exit, width=20, padx=20)
button.place(x=460, y=470)

def reset_key(event):
    python = sys.executable
    messagebox.askyesno('リセットコマンド',"アプリケーションをリセットします...")
    os.execl(python, python, *sys.argv)

root.bind("<r>", reset_key)

text_box = scrolledtext.ScrolledText(root, width=60, height=23, wrap=tk.WORD)
text_box.place(x=15, y=210)



def text_box_in():
    text_box.insert(tk.END, "="*30  + "\n")
    text_box.insert(tk.END, "・On_redy Python set up Log text box~$\n")
    text_box.insert(tk.END, "--Select and open the file in Open File.--\n")
    text_box.insert(tk.END, "・In this log.py GUI, I get an error message if you put in anything other than a .txt file.\n")
    text_box.insert(tk.END, "="*30)
def text_LODE():
    text_box.insert(tk.END, "Inserting into text box...\n")
    

def reset():
    python = sys.executable
    messagebox.askyesno('リセットコマンド',"テキストボックスをクリアにしました。")
    text_box.delete('1.0', tk.END)
    text_box_in()

button_reset = tk.Button(root,text = "Reset_Clean🧹", command=reset, width=20, padx=20)
button_reset.place(x=460, y=410)

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            time.sleep(2.1)
            content = file.read()
            text_box.delete('1.0', tk.END)
            text_box.insert(tk.END, content)
        if file_path is not False:
            text_box.insert(tk.END, "\n<<END log text>>")
            text_box.insert(tk.END, f"\n・File path: {file_path}")
            text_box.insert(tk.END, f"\n・File name: {os.path.basename(file_path)}")
            text_box.insert(tk.END, f"\n・File size: {os.path.getsize(file_path) // 1024} KB")
            text_box.insert(tk.END, f"\n・File date: {datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')}")
            text_box.insert(tk.END, f"\n・File type: {os.path.splitext(file_path)[1][1:]}")
            #開いたファイルの文字数を表示
            text_box.insert(tk.END, f"\n・Text length: {len(content)} characters")
            text_box.insert(tk.END, f"\n・File read completed.\n")
            # 読み込みが完了したらメッセージを表示する
            messagebox.showinfo("読み込み完了", "テキストファイルを読み込みました。")
        

open_button = tk.Button(root, text=".Txtファイルを開く", command=open_file, width=20, padx=20)
open_button.place(x=460, y=440)

#検索/置換のソースコード



def find_text():
    target = find_entry.get()
    content = text_box.get(1.0, tk.END)
    occurrences = content.lower().count(target.lower())
    
    
    if occurrences == 0:
        messagebox.showinfo("検索結果；", "検索対象が存在しません。")
    else:
        messagebox.showinfo("検索結果", f"Log テキストに含まれる文字数は '{occurrences}'です。")

def highlight_text(target):
    content = text_box.get(1.0, tk.END)
    start_pos = "1.0"
    while True:
        start_pos = text_box.search(target, start_pos, tk.END)
        if not start_pos:
            break
        end_pos = f"{start_pos}+{len(target)}c"
        text_box.tag_add("highlight", start_pos, end_pos)
        start_pos = end_pos

    text_box.tag_config("highlight", background="yellow", foreground="black")

def find_and_highlight_text():
    target = find_entry.get()
    text_box.tag_remove("highlight", "1.0", tk.END)  # 既存のハイライトを削除
    highlight_text(target)
    occurrences = text_box.get(1.0, tk.END).lower().count(target.lower())
    
    if occurrences == 0:
        messagebox.showinfo("検索結果", "検索対象が存在しません。 Not found*!")
    else:
        pass

def replace_text():
    target = find_entry.get()
    replacement = replace_entry.get()
    content = text_box.get(1.0, tk.END)
    new_content = content.replace(target, replacement)
    text_box.delete(1.0, tk.END)
    text_box.insert(tk.END, new_content)
    
    if target == '':
        messagebox.showinfo("置換確認", "置換対象が存在しません。")
    else:
        messagebox.showinfo("置換結果", f"'{target}' を '{replacement}' に置換しました。")

find_label = tk.Label(root, text="検索:")
find_label.place(x=410, y=110)
find_entry = tk.Entry(root, width=20)
find_entry.place(x=450, y=110)

replace_label = tk.Label(root, text="置換:")
replace_label.place(x=410, y=140)
replace_entry = tk.Entry(root, width=20)
replace_entry.place(x=450, y=140)

find_button = tk.Button(root, text="検索", command=find_text, width=10)
find_button.config(command=find_and_highlight_text)
find_button.place(x=590, y=105)



replace_button = tk.Button(root, text="置換", command=replace_text, width=10)
replace_button.place(x=590, y=140)


def open_help_window():
    help_window = tk.Toplevel(root)
    help_window.title("Help Window?") 
    help_window.geometry("300x200")
    help_window.configure(bg='#c18af5')
    help_label = tk.Label(help_window, text="?How to use Python GUI check text file development applications", bg='#c18af5', font=('Helvetica', 10))
    help_text = tk.Label(help_window, text="//GUIアプリケーションにおけるショートカットキー//", bg='#c18af5', font=('Helvetica', 13))
    help_text1 = tk.Label(help_window, text="rキー  : リセット",bg='#c18af5', font=('Helvetica', 10))
    help_text4 = tk.Label(help_window, text="Ctrl + qキー : アプリケーションを終了", bg='#c18af5', font=('Helvetica', 10))
    bottan_text = tk.Label(help_window, text="//Developer tool でのボタン操作一覧//", bg='#c18af5', font=('Helvetica', 13))
    bottan_text1 = tk.Label(help_window, text=" ファイルを開く : フォルダーに保存されている .Txt形式のファイルを選択しGui のテキストボックスに貼るボタン", bg='#c18af5', font=('Helvetica', 10))
    bottan_text2 = tk.Label(help_window, text="Reset_Clean🧹 : 現在のテキストボックスをクリアし, 初期状態にリセットする", bg='#c18af5', font=('Helvetica', 10))
    bottan_text3 = tk.Label(help_window, text="終了 : アプリケーションを終了する", bg='#c18af5', font=('Helvetica', 10))
    bottan_text4 = tk.Label(help_window, text=" .Txt別名保存: テキストボックスにあるlogを別名に保存するボタン", bg='#c18af5', font=('Helvetica', 10))
    bottan_text5 = tk.Label(help_window, text="Process_Checklist👀✨: PCのCPUやメモリーをlog形式に見ることができます。", bg='#c18af5', font=('Helvetica', 10))
    
    def close_window():
        help_window.destroy()
    
    close_help_window = tk.Button(help_window, text="閉じる",command=close_window, font=('Helvetica', 10))
    close_help_window.place(x=800, y=500)

    help_text.place(x=10, y=100)
    help_label.pack(pady=20)
    help_text1.place(x=10, y=150)
    help_text4.place(x=10, y=170)
    bottan_text.place(x=30, y=280)
    bottan_text1.place(x=30, y=310)
    bottan_text2.place(x=30, y=340)
    bottan_text3.place(x=30, y=360)
    bottan_text4.place(x=30, y=380)
    bottan_text5.place(x=30, y=400)
    

help_button = tk.Button(root, text="Help", command=open_help_window, width=20, padx=20)
help_button.place(x=460, y=380)


def update_disk_status():
    disk_usage = psutil.disk_usage('/')
    disk_label.config(text=f"・ディスク使用率: {disk_usage.percent}%")
    root.update_idletasks()
    root.after(1000, update_disk_status)

disk_label = ttk.Label(root, text="ディスク使用率:", background=background_color, width=50)
disk_label.place(x=20, y=80)  # 位置を微調整

root.after(1000, update_disk_status)  # ディスク状態更新のループを開始する



def list_processes():
    processes = [p.info for p in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent', 'memory_percent'])]
    process_window = tk.Toplevel(root)
    process_window.title("Process_Checklist")
    process_window.geometry("500x400")
    process_window.configure(bg='#c18af5')

    text = scrolledtext.ScrolledText(process_window, width=60, height=20, wrap=tk.WORD)
    for process in processes:
        text.insert(tk.END, f"・PID: {process['pid']} 名前: {process['name']} CPU: {process['cpu_percent']}% メモリ: {process['memory_percent']}%\n")
    text.pack(pady=20)

process_button = tk.Button(root, text="Process_Checklist👀✨", command=list_processes, width=20, padx=20)
process_button.place(x=460, y=350)


# ファイルを保存する関数
def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'w', encoding='utf-8') as file:
            content = text_box.get('1.0', tk.END)
            file.write(content)
    if not file_path:
        return
    print(f"・File saved: {file_path}")

def in_textbox():
    text_box.insert(tk.END,"Inserting into text box\n")
    
    text_box.insert(tk.END, text_box.get('1.0', tk.END))

# ファイル保存ボタンの追加
save_button = tk.Button(root, text=".txt別名保存", command=save_file, width=5, padx=20)
save_button.place(x=370,y=183)
#get_host_lbel = tk.Label(root, text=f"Connect to host ; {get_connected_hosts()} ")
#get_host_lbel.pack(pady=100)


print("="*40)
print("Developer Tools Python GUI *が起動しました。")
print("Python Tools GUI Ver.3.26")
print("Developer Tools GUI use memorey/: 12.8KB  ")
print("<on_redy>\n")
print('使用する際はPython ターミナルを閉じないでください。\n',
      "使用方法は以下の通りです。\n",
      "公式 Pyhon : https://www.python.org/downloads/ にてダウンロードしてPythonの専用ターミナルで以下のファイルをダウンロードしてください。\n"
      'pip install python\n',
      "pip install tkinter\n",
      "pip install psutil\n",
      'pip install os\n',
      'pip install time\n',
      'pip install datetime\n',
      'pip install sys\n',
      'pip install filedialog\n',
      "Danger!:*Do not close the Python terminal when using it.")
print("制作： BYAKUREN")
print("="*40)

# 初期状態にリセット
text_box_in()
root.mainloop()
