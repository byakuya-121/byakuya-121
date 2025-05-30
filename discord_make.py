#importモジュールを使用する。
# discord.py を discord からインポートする。
#pip install discord.py とvscodeのターミナルで実行する。
import discord
from discord.ext import commands
import datetime # import datetimeで日時を取得するモジュール。
import time # import time で待機時間を追加する  import　モジュール。
import logging #import logging でDiscord botのログイン記録をしてくれる。
 #コマンドの内容によってはimport モジュールを追加する。

"""以下はimportのモジュールの追加方法です。""" 
#コメント欄:
#Discord bot 制作の参照動画&記事： URLのリンクを開きたい場合は ctrl + 参照URLをクリック してください。
# ・https://qiita.com/1ntegrale9/items/9d570ef8175cf178468f　(Pythonで実用Discord Bot(discordpy解説))
# ・https://www.youtube.com/@dainy_san　(Python　Discord bot の作り方解説動画のチャンネル)
   #https://github.com/dainy117/botcode/tree/main (動画参照元のGit hub)
"""
・pip install discord.py
・pip install discord
・pip install logging
・pip install time 
"""
#正直言ってimport Time は無くても別に問題はないが、もし要らない場合はソースコード内にある time.sleep() を消して実行して下さい。
#======================================================================
 #変数 code*
TOKEN = 'YOUR_BOT_TOKEN'    #TOKEN という変数に代入する。
 # ここのYOUR_BOT_TOKENを消してtokenをセットアップする。
BOT_VERSION = float(1.37)
#======================================================================
# botの起動とサーバーへの接続
 #このソースコードは実行した時に接続エラーにならないようにしています。
print("="*30)
print('--Sever connection Run code**--')
time.sleep(4)
bot.remove_command('ping') # ping command is not needed in this bot
bot.remove_command('invite') # invite command is not needed in this bot
bot.remove_command('server') # server command is not needed in this bot
bot.remove_command('ban') # ban command is not needed in this bot
bot.remove_command('load') # load command is not needed in this bot
bot.remove_command('unload') # unload command is not needed in this bot
bot.remove_command('reload') # reload command is not needed in this bot
bot.remove_command('eval') # eval command is not needed in this bot
bot.remove_command('shutdown') # shutdown command is not needed in this bot
bot.remove_command('help') # help command is not needed in this bot
bot.load_extension('cogs.admin')
bot.load_extension('cogs.moderation')
bot.load_extension('cogs.fun')
bot.load_extension('cogs.utility')
bot.load_extension('cogs.users')   
print("="*30)
time.sleep(2.1)
print("<Sever connection Run END!...>")
#================================================================

# Botのインスタンスを生成する。
    # tokenにはDiscord Developer Portalで取得したBOTのトークンを設定する。
bot = commands.Bot(command_prefix='!')
 #botという変数にコマンドの命令形をここで完成させる。ommand_prefix='!'の!マークを元に動かす。
 # 以下のbot.eventで、Botが起動したときやメッセージが送られたときに発火するイベントを定義する。

@bot.event  #@bot.eventではbotが動いている時に発動するcodes*
async def on_ready():
    print('Botが起動しました')
    print(f'ログイン中: {bot.user.name}')
    print(f'ユーザーID: {bot.user.id}')
    #コード内が実行されたらターミナルにBotが起動したとだす。 
#async def <コマンド名>():
    # <コマンドの処理を記述する>
    # await bot.say('<メッセージを送信するテキスト>')
    # コマンドを実行したらメッセージを送信する。
    # 例えば、!pingと入力するとpongとメッセージが送信される。
     #なお、pingはbotとサーバー接続の通信速度を計測する。
    #以下はそのコマンドです。
@bot.command()
async def ping(ctx):
    await ctx.send('pong!') #await ctx.send('コマンドが打たれたチャンネルにbotが返信する内容')
    #!pingと入力するとpongとメッセージが送信される。
    raw_ping = bot.latency
    ping = round(raw_ping * 1000)
    await ctx.reply(f"Pingの検証結果!\nBotのPing値は{ping}msです。") # **result is response
    #ctx.reply()でメッセージを送信する。
    #!pingと入力するとpingの結果がメッセージに表示される。
    #raw_pingはbotとサーバー間のレイテンシーを取得するためのもの。
    #pingはraw_pingの結果を1000で割ってmsに変換したもの。
    #ctx.reply()でメッセージを送信する。
    
@bot.event 
async def on_member_join(member): # 新規メンバーが参加したときの挨拶メッセージ 
    channel = member.guild.system_channel # サーバーのシステムチャンネルを取得 
    if channel is not None: embed = discord.Embed(title="新しいメンバーが参加しました！", description=f"ようこそ! {member.mention} さん!!", color=BOT_COLOR) 
    embed.add_field(name="名前", value=member.name, inline=True) 
    embed.add_field(name="ディスクリミネータ", value=f"#{member.discriminator}", inline=True) 
    embed.add_field(name="ユーザーID", value=member.id, inline=True) 
    embed.add_field(name="アカウント作成日", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
    await channel.send(embed=embed)
@bot.event
async def on_member_remove(member): # メンバーが退出したときのメッセージ
     channel = member.guild.system_channel # サーバーのシステムチャンネルを取得
     if channel is not None: embed = discord.Embed(title="メンバーが退出しました！", description=f"{member.mention}さん、このサーバーからご����いただきありがとうご��いました。", color=BOT_COLOR)
     embed.add_field(name="名前", value=member.name, inline=True)
     embed.add_field(name="ディスクリミネータ", value=f"#{member.discriminator}", inline=True)
     embed.add_field(name="ユーザーID", value=member.id, inline=True)
     embed.add_field(name="退出日時", value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), inline=True)
     await channel.send(embed=embed)
     # bot.eventで、Botが動いている時に起動するcodes*
     #このコードでは新規メンバーが参加したときの挨拶メッセージを出してくれるソースコードとなっています。
     # このコードではメンバーが退出したときのメッセージを出してくれるソースコードとなっています。
     # channel.send()でメッセージを送信する。
     # member.guild.system_channelでサーバーのシステムチャンネルを取得する。
     # embed()でメッセージの中身を作る。
     # add_field()で埋め込み型のメッセージの中身にフィールドを追加する。
     # 最後にembed()で作ったembedをchannel.send()に��してメッセージを送信する。

#================================================================
#   ////Discord bot settings code log///
time.sleep(5.2)
print("**************************************************")
print ("<<<on_ready>>>")#IRC　
print("!*set token Code**"+ TOKEN ) # *!set token chack*
print('Ver' + str(BOT_VERSION)) # !*set bot version**
print ("///Botが起動しました...!! ///")
print("**************************************************")
# Discord bot settings code log*
 #なおこのsettings code log*はBotの実行時間やIDを.txt形式で保存されるソースコードのため、使用しない場合はコメントアウト#でしてください。
Log_bot = logging.INFO
logging.basicConfig(filename='discordbot.txt', level=Log_bot, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s ')
# ディレクトリの内容を表示
directory_path = r'E:< Botのログを保存するファイル名>'
log_file_path = os.path.join(directory_path, 'discordbot.log')
print(log_file_path)
print("--Set all check system startup ⚙️--\n")
#/*logging.info('//This is an info log message.')
#/*logging.error('//This is an error log message.')
# Discord bot settings
#//// Discord bot settings code log///
#**load the bot token from a file!**
#seting the Discord bot Token!**         
bot.run(TOKEN) # TOD
# Botの起動
    # bot.run()を実行するとBotが動き始める。
    # Discord Developer Portalで取得したBOTのトークンをbot.run()に��す。
 # //// END codeing of bot Run ///// 
#   *Check source code running count*
 #/////////////////////////////////////
 # ただし、BOTのトークンはGitHubなどに公開しないようにすることに推奨される。
 
