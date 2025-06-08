import os
import sys
import time
import threading
import json
import subprocess
import winsound
import tkinter as tk
from tkinter import messagebox, scrolledtext
import customtkinter as ctk
from PIL import Image, ImageTk  # Pillowライブラリを使う
import webbrowser
#======--=================
 #利用規約GUIウインドウ

def install_process():
    print("インストール処理を開始します...")
    print("インストールが完了しました。")


class TermsWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("利用規約 / Terms of Service")
        self.geometry("720x700")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_decline)

        # ブランドロゴ表示（あれば）
        try:
            pil_img = Image.open("U-16python.png")
            pil_img = pil_img.resize((300, 100), Image.ANTIALIAS)
            self.logo_img = ImageTk.PhotoImage(pil_img)
            logo_label = ctk.CTkLabel(self, image=self.logo_img)
            logo_label.pack(pady=(10,5))
        except Exception:
            pass

        title_label = ctk.CTkLabel(self, text="ご利用規約 / Terms of Service", font=("Helvetica", 24, "bold"))
        title_label.pack(pady=(0,15))
        # 利用規約（日本語・法律風） 
        terms_jp = (
            "第1条（適用）\n"
            "本利用規約（以下、「本規約」といいます。）は、ユーザーが本アプリケーションを利用する際の一切の行為に適用されるものとします。\n\n"
            "第2条（免責事項）\n"
            "当方は、本アプリケーションの利用に起因して生じる一切の損害について、故意または重大な過失がある場合を除き、一切責任を負わないものとします。\n\n"
            "第3条（データ管理）\n"
            "ユーザーは、自己の責任においてデータを管理し、重要な情報のバックアップを行うものとします。\n\n"
            "第4条（準拠法および管轄）\n"
            "本規約の解釈および適用については日本法を準拠法とし、本アプリケーションに関して生じる紛争については東京地方裁判所を専属的合意管轄裁判所とします。\n\n"
            "以上の内容に同意の上、下記「同意する」ボタンを押してください。"
            )

        # 英語版利用規約（日本語の下に表示）
        terms_en = (
            "Article 1 (Application)\n"
            "These Terms of Service (hereinafter referred to as \"Terms\") apply to all actions when the user uses this application.\n\n"
            "Article 2 (Disclaimer)\n"
            "The provider shall not be liable for any damages arising from the use of this application except in cases of willful misconduct or gross negligence.\n\n"
            "Article 3 (Data Management)\n"
            "Users are responsible for managing their own data and are advised to back up important information.\n\n"
            "Article 4 (Governing Law and Jurisdiction)\n"
            "These Terms shall be governed by the laws of Japan, and the Tokyo District Court shall have exclusive jurisdiction over any disputes related to this application.\n\n"
            "Please press the \"Agree\" button below if you agree to the above terms."
        )

        combined_terms = f"【日本語】\n\n{terms_jp}\n\n{'-'*60}\n\n【English】\n\n{terms_en}"

        textbox = ctk.CTkTextbox(self, width=680, height=440, corner_radius=10)
        textbox.pack(padx=15, pady=10)
        textbox.insert("0.0", combined_terms)
        textbox.configure(state="disabled", font=("Meiryo UI", 14))
        # スクロールバーを追加
        scrollbar = ctk.CTkScrollbar(self, command=textbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 利用規約全文リンク
        def open_terms_link(event=None):
            url = "https://github.com/byakuya-121/byakuya-121.git"
            webbrowser.open(url)

        link_label = ctk.CTkLabel(self, text="利用規約全文はこちら", text_color="blue", cursor="hand2", font=("Helvetica", 14, "underline"))
        link_label.pack(pady=(0,10))
        link_label.bind("<Button-1>", open_terms_link)

        # ボタンフレーム
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=10)

        agree_btn = ctk.CTkButton(btn_frame, text="同意する / Agree", width=150, fg_color="#0078D7",
                                  hover_color="#005A9E", font=("Helvetica", 16, "bold"),
                                  command=self.on_agree)
        agree_btn.grid(row=0, column=0, padx=20)

        decline_btn = ctk.CTkButton(btn_frame, text="同意しない / Decline", width=150, fg_color="#D9534F",
                                    hover_color="#A94442", font=("Helvetica", 16, "bold"),
                                    command=self.on_decline)
        decline_btn.grid(row=0, column=1, padx=20)

        self.parent = parent
        self.user_agreed = False

    def on_agree(self):
        self.user_agreed = True
        self.destroy()

    def on_decline(self):
        self.user_agreed = False
        self.destroy()
        if self.parent:
            self.parent.destroy()

# ── 初期設定 ──
ctk.set_default_color_theme("blue")
ctk.set_appearance_mode("dark")

BATCH_FILE     = "install_pyGUI.bat"
BACKUP_FILE    = "ranking_backup.json"
ADMIN_PASSWORD = "itosyun1201"

ranking_data = []
admin_mode    = False
app           = None
anser         = None # インストール後の再起動確認用
#─────────────────────────────────────
# インストール確認＋バッチ実行
def prompt_and_install():
    root = tk.Tk(); root.withdraw()
    if messagebox.askyesno("⚠Caution", "🔧 必要な依存モジュールをインストールしますか？"):
        win = InstallerWindow(root)
        win.grab_set()
        win.mainloop()
    root.destroy()
    TermsWindow(ctk.CTk())  # 利用規約ウィンドウを表示
    
class InstallerWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("インストール中...")
        self.geometry("600x400")
        self.textbox = scrolledtext.ScrolledText(self, wrap=tk.WORD)
        self.textbox.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        self.protocol("WM_DELETE_WINDOW", lambda: None)
        self.after(100, self.run_batch)

    def run_batch(self):
        threading.Thread(target=self._exec, daemon=True).start()

    def _exec(self):
        if not os.path.exists(BATCH_FILE):
            self._append(f"{BATCH_FILE} が見つかりません。\n"); return
        proc = subprocess.Popen([BATCH_FILE], shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                text=True, bufsize=1)
        for line in proc.stdout:
            self._append(line)
        proc.wait()
        self._append("\n✅ 完了\n" if proc.returncode==0 else "\n❌ 失敗\n")
        if proc.returncode != 1:
            messagebox.showerror("エラー", "インストールに失敗しました。\n詳細はログを確認してください。")
        else:
            self._append("必要なパッケージがインストールされました。\n")
            self._append("アプリケーションを再起動します。\n")
            self.after(1000, self.ask_restart)

    def ask_restart(self):
        """インストール完了後の再起動問い合わせ"""
        if messagebox.askyesno("再起動", "インストールが完了しました。\nアプリケーションを再起動しますか？"):
            # Python プロセス自身を再起動
            os.execv(sys.executable, [sys.executable] + sys.argv)
            TermsWindow(ctk.CTk())  # 利用規約ウィンドウを表示
    def _append(self, text):
        self.textbox.insert(tk.END, text)
        self.textbox.see(tk.END)  # スクロールを最新行に合わせる
        if anser == 1:
            self.ask_restart()
#─────────────────────────────────────
# メインGUI起動
def launch_gui():
    global app
    app = ctk.CTk()
    app.title("U-16 チェイサー ランキングGUI")
    app.geometry("1000x780")
    app.resizable(True, True)

    # アイコン設定
    try:
        if sys.platform=="win32":
            app.iconbitmap("U-16python.ico")
        else:
            img = Image.open("icon.png")
            ico = ctk.CTkImage(light_image=img,dark_image=img,size=(32,32))
            app.iconphoto(False, ico)
    except:
        pass

    #── レイアウト ──
    main = ctk.CTkFrame(app); main.pack(expand=True,fill="both",padx=10,pady=10)
    main.grid_columnconfigure(0,weight=0); main.grid_columnconfigure(1,weight=1)

    # 左：検索＋入力パネル
    left = ctk.CTkFrame(main, width=350); left.grid(row=0,column=0,sticky="ns",padx=(0,10))
    ctk.CTkLabel(left,text="名前検索",font=("Arial",16,"bold")).pack(pady=(0,5))
    global name_search; name_search = ctk.CTkEntry(left,placeholder_text="選手名を入力…")
    name_search.pack(fill="x",padx=15,pady=(0,15))
    name_search.bind("<Return>",lambda e:update_display())

    ctk.CTkLabel(left,text="新規エントリー作成",font=("Arial",16,"bold")).pack(pady=(0,10))
    global name_entry,score_entry,team_entry,block_option,status_option
    name_entry  = ctk.CTkEntry(left,placeholder_text="選手名")
    score_entry = ctk.CTkEntry(left,placeholder_text="獲得ポイント")
    team_entry  = ctk.CTkEntry(left,placeholder_text="チーム名")
    block_option= ctk.CTkOptionMenu(left,values=[
        "Aブロック","Bブロック","Cブロック","Dブロック",
        "Eブロック","Fブロック","Gブロック","Hブロック",
        "準優勝","3位決定戦","決勝"
    ]); block_option.set("Aブロック")
    status_option= ctk.CTkOptionMenu(left,values=["成功","失格"]); status_option.set("成功")
    for w in (name_entry,score_entry,team_entry,block_option,status_option):
        w.pack(fill="x",padx=15,pady=5)

    ctk.CTkButton(left,text="追加",command=add_entry,font=("Helvetica",18,"bold")).pack(fill="x",padx=15,pady=(15,5))
    ctk.CTkButton(left,text="管理者ログイン",command=login_admin).pack(fill="x",padx=15,pady=5)
    ctk.CTkButton(left, text="テーマ切替💻", font=("Helvetica", 16, "bold"), command=toggle_theme).pack(fill="x", padx=15, pady=5)
    ctk.CTkLabel(left,text="現時刻",font=("Helvetica",19,"bold")).pack(pady=(20,5))
    global timer_label; timer_label=ctk.CTkLabel(left,text="",font=("Impact",24)); timer_label.pack()
    ctk.CTkButton(left,text="全データリセット",fg_color="red",hover_color="#aa0000",command=reset_all_data).pack(fill="x",padx=15,pady=10)
    ctk.CTkButton(left,text="タイマー⏲️",fg_color="#197fc3",hover_color="#5d94c4",command=open_timer_window).pack(fill="x",padx=15,pady=10)
    ctk.CTkButton(left, text="🏅ブロック1位表示", command=open_top1_window, font=("Helvetica", 16)).pack(fill="x", padx=15, pady=(5, 15))


    # 右：結果表示
    right = ctk.CTkFrame(main); right.grid(row=0,column=1,sticky="nsew")
    ctk.CTkLabel(right,text="U-16 チェイサー ランキング",font=("Impact",24)).pack(pady=(0,10))
    global result_frame; result_frame=ctk.CTkScrollableFrame(right,width=620,height=650)
    result_frame.pack(fill="both",expand=True,padx=10,pady=(0,10))

    # ショートカット
    app.bind("<Control-r>",lambda e:os.execv(sys.executable,['python']+sys.argv))
    app.bind("<Control-q>",lambda e:app.quit())
    app.bind("<Control-s>",lambda e:save_data())
    app.bind("<Control-l>",lambda e:login_admin())

    # 初期化
    start_timer(); load_data(); update_display()
    app.mainloop()

#─────────────────────────────────────
# データ保存／読み込み
def save_data():
    try:
        with open(BACKUP_FILE,"w",encoding="utf-8") as f:
            json.dump(ranking_data,f,ensure_ascii=False,indent=2)
    except Exception as e:
        print("保存エラー:",e)

def load_data():
    global ranking_data
    if os.path.exists(BACKUP_FILE):
        try:
            with open(BACKUP_FILE,"r",encoding="utf-8") as f:
                ranking_data=json.load(f)
        except Exception as e:
            print("読み込みエラー:",e)

#─────────────────────────────────────

# 管理者ログイン
def login_admin():
    def verify():
        nonlocal win
        if pwd.get()==ADMIN_PASSWORD:
            global admin_mode; admin_mode=True
            messagebox.showinfo("成功","管理者モード有効")
            win.destroy(); update_display(); save_data()
        else:
            messagebox.showerror("エラー","パスワードが違います")

    win=ctk.CTkToplevel(app); win.title("管理者ログイン"); win.geometry("300x150")
    ctk.CTkLabel(win,text="PIN:").pack(pady=10)
    pwd=ctk.CTkEntry(win,show="*"); pwd.pack(pady=5)
    ctk.CTkButton(win,text="ログイン",command=verify).pack(pady=10)

#─────────────────────────────────────
# 追加／削除／表示更新
def get_option_values(opt): return list(opt._values)

def update_display():
    keyword=name_search.get().strip()
    for w in result_frame.winfo_children(): w.destroy()
    for blk in get_option_values(block_option):
        entries=[e for e in ranking_data if e["block"]==blk]
        if keyword: entries=[e for e in entries if keyword in e["name"]]
        if not entries: continue
        ctk.CTkLabel(result_frame,text=f"── {blk} ──",font=("Impact",20),text_color="cyan").pack(pady=(10,2),anchor="w")
        for idx,e in enumerate(sorted(entries,key=lambda x:x["score"],reverse=True),1):
            bg="#2b2b2b" if idx%2==0 else "#1e1e1e"
            row=ctk.CTkFrame(result_frame,fg_color=bg); row.pack(fill="x",padx=5,pady=1)
            cols=[f"{idx}位",e["name"],f"{e['score']}点",e["team"],e["status"]]
            wids=[80,200,120,160,120]
            for i,txt in enumerate(cols):
                col="#00ff00" if i==4 and e["status"]=="成功" else "#ff3333" if i==4 and e["status"]=="失格" else "white"
                ctk.CTkLabel(row,text=txt,width=wids[i],font=("Impact",18),text_color=col).grid(row=0,column=i,padx=5)
            if admin_mode:
                ctk.CTkButton(row,text="削除",width=80,command=lambda n=e["name"],b=e["block"]:delete_entry(n,b)).grid(row=0,column=5,padx=10)

def add_entry():
    name=name_entry.get().strip(); team=team_entry.get().strip()
    stat=status_option.get(); blk=block_option.get()
    try: score=int(score_entry.get())
    except: messagebox.showerror("Error","スコアは整数で入力して下さい"); return
    if not name or not team:
        messagebox.showwarning("Error","名前とチームを入力して下さい"); return
    ranking_data.append({"name":name,"score":score,"team":team,"status":stat,"block":blk})
    save_data(); update_display()

def delete_entry(name,block):
    global ranking_data
    ranking_data=[e for e in ranking_data if not(e["name"]==name and e["block"]==block)]
    save_data(); update_display()

def reset_all_data():
    global ranking_data
    confirm = messagebox.askyesno("確認", "全データをリセットしてもよろしいですか？🥺")
    if confirm:
        ranking_data = []       # メモリ上のリストを空にする
        save_data()             # ファイルにも反映（空データで上書き）
        update_display()        # 画面表示をクリア
        messagebox.showinfo("完了", "すべてのデータをリセットしました。👀✨")
        
# ──── リセット処理 ────
def reset_app(event=None):
    """Ctrl + R でアプリケーションをリセットして再起動"""
    os.execv(sys.executable, ['python'] + sys.argv)

#─────────────────────────────────────
def start_timer():
    def run():
        while True:
            timer_label.configure(text=time.strftime("%H:%M:%S"))
            time.sleep(1)
    threading.Thread(target=run,daemon=True).start()
#─────────────────────────────────────
def toggle_theme(): # テーマ切替
    mode = "light" if ctk.get_appearance_mode() == "Dark" else "dark"
    ctk.set_appearance_mode(mode)


def open_timer_window():
    win = ctk.CTkToplevel(app)
    win.title("タイマー")
    win.geometry("350x260")
    win.transient(app)
    win.attributes("-topmost", True)
    win.focus_force()

    # --- 状態変数 ---
    timer_running2 = False
    remaining = 0.0
    end_time = 0.0

    # --- ラベル ---
    timer_label2 = ctk.CTkLabel(win, text="00:00:00", font=("Impact", 32))
    timer_label2.pack(pady=(10, 5))

    # --- 設定フレーム ---
    setting_frame = ctk.CTkFrame(win)
    setting_frame.pack(pady=(5, 5), padx=10, fill="x")
    ctk.CTkLabel(setting_frame, text="HH").grid(row=0, column=0)
    h_entry = ctk.CTkEntry(setting_frame, placeholder_text="0", width=50)
    h_entry.grid(row=1, column=0, padx=5)
    ctk.CTkLabel(setting_frame, text="MM").grid(row=0, column=1)
    m_entry = ctk.CTkEntry(setting_frame, placeholder_text="0", width=50)
    m_entry.grid(row=1, column=1, padx=5)
    ctk.CTkLabel(setting_frame, text="SS").grid(row=0, column=2)
    s_entry = ctk.CTkEntry(setting_frame, placeholder_text="0", width=50)
    s_entry.grid(row=1, column=2, padx=5)
    # 「セット」ボタン
    def set_timer():
        nonlocal remaining, end_time, timer_running2
        # 入力値取得
        try:
            h = int(h_entry.get() or 0)
            m = int(m_entry.get() or 0)
            s = int(s_entry.get() or 0)
        except ValueError:
            messagebox.showerror("入力エラー", "数字のみ入力してください")
            return
        remaining = h*3600 + m*60 + s
        end_time = time.time() + remaining
        timer_running2 = False
        # ラベルに初期値表示
        hrs, rem = divmod(int(remaining), 3600)
        mins, secs = divmod(rem, 60)
        timer_label2.configure(text=f"{hrs:02d}:{mins:02d}:{secs:02d}")

    ctk.CTkButton(setting_frame, text="セット", command=set_timer).grid(row=1, column=3, padx=10)

    # --- カウントダウン更新 ---
    def update2():
        nonlocal remaining, end_time, timer_running2
        if timer_running2:
            remaining = end_time - time.time()
            if remaining <= 0:
                # 終了
                remaining = 0
                timer_running2 = False
                winsound.Beep(1000, 500)  # 終了音
                messagebox.showinfo("終了", "タイマーが終了しました")
            hrs, rem = divmod(int(remaining), 3600)
            mins, secs = divmod(rem, 60)
            timer_label2.configure(text=f"{hrs:02d}:{mins:02d}:{secs:02d}")
        win.after(200, update2)

    # --- 操作ボタン ---
    def start2():
        nonlocal timer_running2, end_time
        if remaining > 0 and not timer_running2:
            end_time = time.time() + remaining
            timer_running2 = True

    def stop2():
        nonlocal timer_running2, remaining, end_time
        if timer_running2:
            # 一時停止
            remaining = end_time - time.time()
            timer_running2 = False

    def reset2():
        nonlocal timer_running2, remaining, end_time
        timer_running2 = False
        remaining = 0
        timer_label2.configure(text="00:00:00")

    btn_frame = ctk.CTkFrame(win)
    btn_frame.pack(pady=(10, 0))
    ctk.CTkButton(btn_frame, text="Start", command=start2,  width=70).grid(row=0, column=0, padx=5)
    ctk.CTkButton(btn_frame, text="Stop",  command=stop2,   width=70).grid(row=0, column=1, padx=5)
    ctk.CTkButton(btn_frame, text="Reset", command=reset2,  width=70).grid(row=0, column=2, padx=5)

    update2()

def open_top1_window():
    X = app.winfo_x() + 230
    win = ctk.CTkToplevel(app)
    win.title("ブロックごとの1位ランキング")
    win.geometry("400x500")
    win.transient(app)
    win.attributes("-topmost", True)
    win.focus_force()

    auto_update_interval = 200000  # 自動更新間隔（ミリ秒)
    show_final_var = ctk.BooleanVar(value=True)  # ✅ トグルの状態（初期：表示）

    # 🔄 ランキング表示更新
    def refresh_display():
        for widget in inner_frame.winfo_children():
            widget.destroy()

        blocks = get_option_values(block_option)

        for block in blocks:
            # 非表示条件（チェックが外れていて "決勝" または "準優勝" を含む）
            if not show_final_var.get() and ("決勝" in block or "準優勝" in block):
                continue

            ctk.CTkLabel(inner_frame, text=f"🟥 {block}", font=("Helvetica", 22, "bold"), text_color="cyan")\
                .pack(pady=(15, 5), anchor="w", padx=20)

            block_entries = [
                e for e in ranking_data
                if e["block"] == block and e["status"] not in ("通過", "失格")
            ]

            if not block_entries:
                ctk.CTkLabel(inner_frame, text="▶ 該当者なし", font=("Helvetica", 16), text_color="gray")\
                    .pack(pady=(0, 10), anchor="w", padx=30)
                continue

            max_score = max(e["score"] for e in block_entries)
            top_entries = [e for e in block_entries if e["score"] == max_score]

            for entry in top_entries:
                frame = ctk.CTkFrame(inner_frame, fg_color="#222222", corner_radius=10)
                frame.pack(fill="x", padx=30, pady=5)

                info = (
                    f"🏆 1位: {entry['name']}\n"
                    f"🔢 スコア: {entry['score']}点\n"
                    f"🎽 チーム: {entry['team']}\n"
                    f"📋 状態: {entry['status']}"
                )
                ctk.CTkLabel(frame, text=info, font=("Helvetica", 16), text_color="white", justify="left")\
                    .pack(padx=15, pady=10, anchor="w")

    # 🔄 自動更新スケジューラー
    def schedule_auto_update():
        if win.winfo_exists():
            refresh_display()
            win.after(auto_update_interval, schedule_auto_update)

    # 🖼 スクロールエリア
    canvas = ctk.CTkCanvas(win, width=500, height=620, bg="black", highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = ctk.CTkScrollbar(win, orientation="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    inner_frame = ctk.CTkFrame(canvas, fg_color="transparent")
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    inner_frame.bind("<Configure>", on_configure)

    # 🔄 手動更新ボタン
    refresh_btn = ctk.CTkButton(win, text="🔄 更新", font=("Helvetica", 16, "bold"), command=refresh_display)
    refresh_btn.place(x=X, y=10)

    # ✅ 表示トグル（決勝・準優勝） → 更新ボタンの下に表示
    toggle = ctk.CTkCheckBox(
        win,
        text="決勝・準優勝を表示",
        variable=show_final_var,
        onvalue=True,
        offvalue=False,
        command=refresh_display,
        font=("Helvetica", 14)
    )
    toggle.place(x=X, y=60)  # ← 更新ボタンの下に配置（10px下）
    # 🗑️ 閉じるボタン
    close_btn = ctk.CTkButton(win, text="🗑️ 閉じる", font=("Helvetica", 16, "bold"), command=win.destroy)
    close_btn.place(x=X, y=100)  # ← 更新ボタンの下に配置（10px下）
    refresh_display()
    schedule_auto_update()

def show_public_view_slideshow():
    public = ctk.CTkToplevel()
    public.attributes("-fullscreen", True)
    public.configure(fg_color="black")

    title = ctk.CTkLabel(public, text="U-16 チェイサー 結果発表", font=("Arial", 48, "bold"), text_color="white")
    title.pack(pady=40)

    display_frame = ctk.CTkFrame(public, fg_color="black")
    display_frame.pack(pady=40)

    name_label = ctk.CTkLabel(display_frame, text="", font=("Arial", 48, "bold"), text_color="white")
    name_label.pack(pady=20)

    score_label = ctk.CTkLabel(display_frame, text="", font=("Arial", 40), text_color="white")
    score_label.pack(pady=10)

    block_label = ctk.CTkLabel(display_frame, text="", font=("Arial", 36), text_color="white")
    block_label.pack(pady=10)

    close_btn = ctk.CTkButton(public, text="閉じる (Esc)", font=("Arial", 24), command=public.destroy)
    close_btn.pack(pady=30)

    public.bind("<Escape>", lambda e: public.destroy())

    # 表示対象データを取得
    data = load_data()
    display_data = [d for d in data if d["pass"]]
    display_data.sort(key=lambda x: (-x["score"]))  # スコア順

    index = [0]  # リストで保持してクロージャで変更可能に

    def update_display():
        if not display_data:
            name_label.configure(text="表示する合格者がいません")
            score_label.configure(text="")
            block_label.configure(text="")
            return

        person = display_data[index[0]]
        name_label.configure(text=f"{person['name']}")
        score_label.configure(text=f"{person['score']} 点")
        block_label.configure(text=f"[{person['block']}]")

        index[0] = (index[0] + 1) % len(display_data)
        public.after(3000, update_display)  # 3秒ごとに切り替え

    update_display()


#─────────────────────────────────────
if __name__=="__main__":
    prompt_and_install()
    launch_gui()
#----//コマンドprint内容//----
print("\033[1;32mAll Setup Complete!!\033[0m")  # 緑・太字
print("\033[1;36mU-16 チェイサー ランキング GUI を起動しました。\033[0m")  # シアン・太字

print("\033[33mCtrl + R\033[0m でアプリケーションをリセット")
print("\033[33mCtrl + Q\033[0m でアプリケーションを終了")
print("\033[33mCtrl + S\033[0m でデータを保存")
print("\033[33mCtrl + L\033[0m で管理者ログイン")
print("\033[33mCtrl + T\033[0m でテーマ切替")
print("\033[33mCtrl + A\033[0m で全データリセット")
print("\033[33mCtrl + H\033[0m でヘルプ")

print("\033[90m" + "=-="*25 + "\033[0m")  # グレーの区切り線

print(f"\033[36m実行時刻: {time.strftime('%H:%M:%S', time.localtime())}\033[0m")  # シアン
print("\033[35mSet up time!*:\033[0m ", time.strftime("%H:%M:%S", time.localtime()))  # 紫
print(f"\033[36m現在のGUIバージョン: {ctk.__version__}\033[0m")
print("\033[36mPython Version:\033[0m ", sys.version)

print("\033[1;34m制作者；ロボット部長{GitHub:ID @Nekomimi-120}\033[0m")  # 青・太字
print("\033[1;34m提供者；Itosyun\033[0m")  # 青・太字

print("\033[90m" + "=-="*25 + "\033[0m")  # グレーの区切り線
print("\033[1;32mAll green!!✅\033[0m")  # 緑・太字
# WAVファイルを再生（Windows環境）
winsound.PlaySound("startup.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
#//////////////////////////////////////////////////////////////////////////////
#----//コマンドプログラムの実行//----
load_data()
update_display()
start_timer()
app.bind("<Control-r>", reset_app)  # Ctrl + R でアプリケーションをリセット
app.bind("<Control-q>", lambda event: app.quit())  # Ctrl + Q でアプリケーションを終了 
app.bind("<Control-s>", lambda event: save_data())  # Ctrl + S でデータを保存
app.bind("<Control-l>", lambda event: login_admin())  # Ctrl + L で管理者ログイン
app.mainloop()
#//////////////////////////////////////////////////////////////////////////////
