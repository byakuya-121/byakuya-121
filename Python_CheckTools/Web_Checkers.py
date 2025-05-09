import ssl
import socket
import time
import requests
from urllib.parse import urlparse
from ping3 import ping
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import re
import json
import os
import threading
import ctypes, winsound
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import subprocess
import sys
import winsound
import re
import requests
from bs4 import BeautifulSoup


SETTINGS_FILE = "settings.json"
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")
print("--All setup*!--")

class WebMonitorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Web-Checkers監視ツール🧰")
        self.geometry("1200x620")
        self.resizable(False, False)
        # システム通知音を再生
        self.settings = self.load_settings()
        self.monitoring = False
        self.monitor_data = []  # ★ 追加：モニター記録用リスト
        winsound.PlaySound("example.wav", winsound.SND_FILENAME)

        self.apply_settings()
        self.show_disclaimer()  # 注意事項表示
        self.create_widgets()
        self.result_box.insert("end", "────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────\n")
        self.result_box.insert("end", "Hello User*!👀✨\n")
        self.result_box.insert("end", "Thank you for using the Web-Checkers monitoring tool!\n")
        self.result_box.insert("end", "$To monitor the URL of the website you want to analyze, insert the URL into the input field for the target URL and press the button to obtain server information.\n The server will respond. By pressing the start monitoring button, it will record at intervals of time. Additionally, the log can be saved in .txt format with a different name.📋\n")
        self.result_box.insert("end", "────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────\n")
    
        self.bind("<Control-r>", lambda event: self.restart_app())
        self.bind("<Control-Shift-R>", lambda event: self.reset_app())

    def show_disclaimer(self):
        """注意事項を表示するメソッド"""
        disclaimer_text = (
            "プライバシーポリシーWeb-Checkers監視ツール（以下「本ツール」といいます）は、ユーザーのプライバシーを非常に重要視しています。本ポリシーは、本ツールの利用中に収集される個人情報の取り扱いについて説明します。本ツールを使用することにより、ユーザーは本ポリシーに同意したものとみなされます。\n"

         """1. 【情報の使用目的】
              収集した情報は以下の目的で使用します：
            ・ユーザーが入力したURLの監視およびパフォーマンスデータの取得
            ・ツールの機能向上とバグ修正のためのデータ分析
            ・ユーザーの設定（テーマ、フォントサイズなど）の保存と適用\n"""

            """アプリケーションの改善およびアップデート

            2. 【情報の共有】
            本ツールでは、収集した個人情報を第三者と共有することはありません。ただし、以下の場合に限り、情報を共有することがあります\n：

            ユーザーの同意がある場合

            法的義務に基づき、適切な機関に情報を提供する必要がある場合（例えば、法的手続きに基づく場合）
            セキュリティ上の問題が発生した場合に、適切な対策を講じるために情報を使用する場合\n
            3. 【クッキーと追跡技術】\n
            本ツールは、ウェブベースの機能を利用する場合、ユーザーのブラウザにクッキーを保存することがあります。これにより、ユーザーの設定を記憶したり、ツールのパフォーマンスを向上させたりすることができます。ユーザーはブラウザの設定でクッキーを無効にすることができますが、その場合、本ツールの一部機能が正常に動作しない可能性があります。
            4. 【データの保存】
            収集したデータは、ユーザーがツールを利用している間に保存され、監視結果や設定情報はユーザーが明示的に削除するまで保持されます。また、保存されるデータは、ツール内で生成される一時的なファイルや設定ファイル（例：settings.json）として保存されます。
            5. 【データの保護】\n
            本ツールは、ユーザーの個人情報を不正アクセスや改ざんから保護するために、適切な技術的および組織的な措置を講じています。しかし、インターネットを通じたデータ送信には完全なセキュリティを保証することはできません。\nそのため、ユーザーは自己の責任で情報の取り扱いにご注意いただき、必要に応じてバックアップや保護を行うことをお勧めします。\n
            """
         """6. 【問い合わせに関して】
            本ポリシーに関する質問や、個人情報の取り扱いについて不明点がある場合は、以下の連絡先にてお問い合わせください：
            連絡先：・Discord  ID; amau_33567            
                   ・公式LINE URL;  http://lin.ee/U8LZFZv"""
        )

        result = messagebox.askokcancel("ご利用にあたっての注意事項", disclaimer_text)
        if not result:
            self.quit()

    def create_widgets(self):
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(pady=10, padx=10)

        self.url_entry = ctk.CTkEntry(top_frame, placeholder_text="🔍監視する対象のURLを入力 例)https://", width=400)
        self.url_entry.grid(row=0, column=0, padx=5)

        self.start_button = ctk.CTkButton(top_frame, text="監視開始", command=self.start_monitoring)
        self.start_button.grid(row=0, column=1, padx=5)

        self.stop_button = ctk.CTkButton(top_frame, text="監視停止", command=self.stop_monitoring)
        self.stop_button.grid(row=0, column=2, padx=5)

        self.fetch_button = ctk.CTkButton(top_frame, text="サーバー情報取得", command=self.get_server_info)
        self.fetch_button.grid(row=1, column=0, padx=5, pady=5)

        self.setting_button = ctk.CTkButton(top_frame, text="⚙設定", command=self.open_settings)
        self.setting_button.grid(row=1, column=1, padx=5, pady=5)

        self.save_button = ctk.CTkButton(top_frame, text="結果保存", command=self.save_results)
        self.save_button.grid(row=1, column=2, padx=5, pady=5)

        self.graph_button = ctk.CTkButton(top_frame, text="📈 グラフ表示", command=self.show_graph)  # ★ グラフボタン
        self.graph_button.grid(row=1, column=3, padx=0, pady=5)

        self.loading_label = ctk.CTkLabel(top_frame, text="")
        self.loading_label.grid(row=0, column=3, rowspan=2, padx=10)

        self.result_frame = ctk.CTkScrollableFrame(self, width=800, height=450)
        self.result_frame.pack(pady=10)
        
        self.result_box = ctk.CTkTextbox(self.result_frame, width=780, height=430, font=("Arial", self.settings.get("font_size", 14)), wrap="none")
        self.result_box.pack()

        bottom_frame = ctk.CTkFrame(self)
        bottom_frame.pack(pady=5, padx=10, fill="x")

        self.status_label = ctk.CTkLabel(bottom_frame, text="ステータス: 待機中")
        self.status_label.pack(side="left")

        self.theme_option = ctk.CTkOptionMenu(
            bottom_frame,
            values=["System", "Light", "Dark"],
            command=self.change_theme
        )
        self.theme_option.pack(side="right", padx=10)
        self.theme_option.set(self.settings.get("theme", "System"))
        self.bind("<Control-q>", lambda event: self.force_quit())

    def force_quit(self):
        self.destroy()

    def set_buttons_state(self, state="normal"):
        self.start_button.configure(state=state)
        self.stop_button.configure(state=state)
        self.fetch_button.configure(state=state)
        self.setting_button.configure(state=state)
        self.save_button.configure(state=state)

    def restart_app(self):
        confirm = messagebox.askyesno("警告！⚠️", "GUI Web-Checkerを再起動しますか？")
        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS) #Windows
        if confirm:
            self.destroy()
            python = sys.executable
            subprocess.Popen([python, os.path.realpath(__file__)])

    def reset_app(self):
        self.monitoring = False
        self.url_entry.delete(0, "end")
        self.result_box.delete("1.0", "end")
        self.monitor_data.clear()
        self.status_label.configure(text="ステータス: 待機中")
        self.show_notification("🔄 リセット完了", "blue")

    def start_monitoring(self):
        if self.monitoring:
            return
        self.monitoring = True
        self.status_label.configure(text="ステータス: 監視中")
        threading.Thread(target=self.monitor, daemon=True).start()

    def stop_monitoring(self):
        self.monitoring = False
        self.status_label.configure(text="ステータス: 停止中")

    def monitor(self):
        while self.monitoring:
            self.loading_label.configure(text="🔄 監視中...")
            self.set_buttons_state("disabled")
            self.get_server_info()
            self.loading_label.configure(text="")
            self.set_buttons_state("normal")
            time.sleep(10)

    def get_server_info(self):
        url = self.url_entry.get()
        if not url:
            self.show_notification("⚠️ Error ; Not found search URL:( ", "red")
            return

        try:
            start_time = time.time()
            r = requests.get(url, timeout=5)
            response_time = round(time.time() - start_time, 4)

            parsed_url = urlparse(url)
            host = parsed_url.hostname
            ip_address = socket.gethostbyname(host)

            ping_result = ping(host, timeout=2)
            ping_ms = round(ping_result * 1000, 2) if ping_result else None

            headers = r.headers
            status_code = r.status_code
            ssl_info = None
            if url.startswith("https://"):
                ssl_info = self.get_ssl_info(url)

            server = headers.get('Server', 'None')
            content_type = headers.get('Content-Type', 'No data')
            charset_match = re.search(r'charset=([\w-]+)', content_type)
            charset = charset_match.group(1) if charset_match else '不明'

            self.result_box.insert("end", "──────────────────────────────────────────\n")
            self.result_box.insert("end", f"監視中のURL👀[{url}]\n")
            self.result_box.insert("end", f"ステータスコード: {status_code}\n")
            self.result_box.insert("end", f"🦈レスポンスタイム: {response_time}s\n")
            self.result_box.insert("end", f"📡IPアドレス: {ip_address}\n")
            self.result_box.insert("end", f"⏱️Ping: {ping_ms} ms\n")
            if ssl_info:
                self.result_box.insert("end", f"SSL情報: {ssl_info}\n")
            self.result_box.insert("end", f"コンテンツタイプ: {content_type}\n")
            self.result_box.insert("end", f"📋使用文字コード: {charset}\n")
            self.result_box.insert("end", f"👤技術スタック(Server): {server}\n")
            self.result_box.insert("end", "──────────────────────────────────────────\n")
            self.result_box.see("end")
            self.result_box.configure(state="disabled")

            if status_code >= 400:
                self.play_alert_sound()
                self.show_notification(f"❌ エラーコード {status_code}", "red")
            else:
                self.show_notification(f"✅ サーバーレスポンスOK {status_code}", "green")

            # ★ データ記録
            self.monitor_data.append({
                "time": time.strftime("%H:%M:%S"),
                "response_time": response_time,
                "ping": ping_ms
            })

        except Exception as e:
            self.show_notification(f"⚠️ 通信エラー: {str(e)}", "orange")
            self.result_box.insert("end", f"[エラー] {str(e)}\n")
            self.result_box.see("end")

    def get_ssl_info(self, url):
        try:
            hostname = urlparse(url).hostname
            context = ssl.create_default_context()
            with context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=hostname) as conn:
                conn.settimeout(3)
                conn.connect((hostname, 443))
                cert = conn.getpeercert()
                issuer = cert.get('issuer', '不明')
                expire = cert.get('notAfter', '不明')
                return f"発行者: {issuer}, 有効期限: {expire}"
        except Exception as e:
            return f"SSL取得失敗: {str(e)}"

    def play_alert_sound(self):
        winsound.Beep(1200, 300)

    def save_results(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.result_box.get("1.0", "end"))
            self.show_notification("✅ 保存完了！", "blue")

    def open_settings(self):
        settings_window = ctk.CTkToplevel(self)
        settings_window.title("設定")
        settings_window.geometry("300x200")

        font_label = ctk.CTkLabel(settings_window, text="フォントサイズ選択")
        font_label.pack(pady=10)

        font_option = ctk.CTkOptionMenu(
            settings_window,
            values=["小", "中", "大"],
            command=self.change_font_size
        )
        font_option.pack(pady=5)

    def change_font_size(self, size):
        font_size = {"小": 12, "中": 14, "大": 18}.get(size, 14)
        self.result_box.configure(font=("Arial", font_size))
        self.settings["font_size"] = font_size
        self.save_settings()

    def change_theme(self, theme):
        ctk.set_appearance_mode(theme.lower())
        self.settings["theme"] = theme
        self.save_settings()

    def show_notification(self, text, color):
        notif = ctk.CTkLabel(self, text=text, bg_color=color, text_color="white", corner_radius=8, font=("Arial", 16))
        notif.place(relx=0.5, rely=0.1, anchor="center")
        self.after(2000, notif.destroy)

    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save_settings(self):
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.settings, f, indent=4, ensure_ascii=False)

    def apply_settings(self):
        theme = self.settings.get("theme", "System")
        ctk.set_appearance_mode(theme.lower())

    def show_graph(self):
        if not self.monitor_data:
            self.show_notification("⚠️ データがありません Not data :( !", "orange")
            return

        times = [d["time"] for d in self.monitor_data]
        response_times = [d["response_time"] for d in self.monitor_data]
        pings = [d["ping"] for d in self.monitor_data]

        fig, ax1 = plt.subplots(figsize=(8, 4))
        ax1.set_xlabel("時間")
        ax1.set_ylabel("レスポンスタイム (秒)", color="tab:blue")
        ax1.plot(times, response_times, label="レスポンスタイム", color="tab:blue", marker="o")
        ax1.tick_params(axis="y", labelcolor="tab:blue")

        if any(pings):
            ax2 = ax1.twinx()
            ax2.set_ylabel("Ping (ms)", color="tab:red")
            ax2.plot(times, pings, label="Ping", color="tab:red", marker="x")
            ax2.tick_params(axis="y", labelcolor="tab:red")

        fig.tight_layout()
        graph_window = ctk.CTkToplevel(self)
        graph_window.title("グラフ表示")
        graph_window.geometry("900x500")

        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

if __name__ == "__main__":
    try:
        app = WebMonitorApp()
        app.mainloop()
    except Exception as e:
        import traceback
        traceback.print_exc()
        messagebox.showerror("エラー", f"アプリの起動に失敗しました:\n{e}")
