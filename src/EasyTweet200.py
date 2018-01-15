# -*- coding: utf-8 -*-
# EasyTweet GUI Version
# by I_am_4a

# 1.下準備
# 各種モジュールの読み込み
"""
wxPython
os
time
datetime
unicodedata
sys
webbrowser
tkinter
"""

import wx, os, time, datetime, unicodedata, sys, webbrowser
import tweepy as tp
import tkinter as tk
import tkinter.messagebox as tkmsg
import tkinter.filedialog as tkfd

# ファイル選択画面のデフォルトディレクトリをこのファイルのディレクトリに指定
iDir = os.path.abspath(os.path.dirname(sys.argv[0]))
# ファイルのタイプを指定
fType = [('キーファイル','*.key')]

# tkinterのGUIを表示させないコード
root = tk.Tk()
root.withdraw()

consumer_key = "Mc0Kez2hOc0rpDKCm3VvPUxe5"
consumer_secret = "WuFVHJtfhnLnjbTe8fzH4MtgRLos87STIPNttpSygUwqkuNLYc"

# ---------------------------------------

# 2.各種関数作成

def event_auth(event):
	"""
	void event_auth(event)

	wxPythonのイベント用関数。
	認証イベントが発生した際に実行。
	認証画面表示やキーをセーブできたりするようにする。
	"""

	auth = tp.OAuthHandler(consumer_key, consumer_secret)
	webbrowser.open(auth.get_authorization_url())
	dlg = wx.TextEntryDialog(None, '表示されたPINコードを入力してください', 'EasyTweet Authorization')
	dlg.ShowModal()
	dlg.Destroy()

	pin = dlg.GetValue()
	auth.get_access_token(pin)

	fn = tkfd.asksaveasfilename(filetypes=fType,initialdir=iDir)
	if fn.find(".key") == -1:
		fn = fn + ".key"
	try:
		f = open(fn, "w")
		f.write(auth.access_token+","+auth.access_token_secret)
		f.close()
		tkmsg.showinfo('EasyTweet Authorization', 'セーブ完了('+fn+')')
	except UnboundLocalError:
		tkmsg.showerror('EasyTweet Authorization', 'セーブに失敗しました。。。')
		pass

def version():
	"""
	String version(void)

	現在のEasyTweetのバージョンを返します。

	例)

	print(version())
	# 2.0.0
	"""
	return "2.0.0"

def search(event):
	"""
	void search(event)

	wxPythonのイベント用関数。
	サーチ用イベントが発生した際に実行。
	名前検索を行い、その結果をフォームにセット。
	"""

	# まずはすべての値をクリア
	input_search_user_location.Clear()
	input_search_user_name.Clear()
	input_search_user_description.Clear()
	input_search_user_url.Clear()
	input_search_user_friends.Clear()
	input_search_user_tweet.Clear()

	# Twitterへと接続
	try:
		frame.SetStatusText('接続中…')
		auth = tp.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(input_at.GetValue(), input_as.GetValue())
		api = tp.API(auth)
		api.user_timeline()
		frame.SetStatusText('接続成功！')
	except tp.error.TweepError: # キーが不正な場合
		frame.SetStatusText('接続失敗…キーを確認してください')
	time.sleep(0.5) # いったん落ち着くため
	frame.SetStatusText('データ取得中…')
	# ユーザーデータを取得
	try:
		user = api.get_user(screen_name=input_search_screen_name.GetValue())
	except tp.error.TweepError:
		frame.SetStatusText('データ取得失敗…')
		pass

	# 値のセット
	try:
		input_search_user_location.SetValue(user.location)
	except KeyError:
		pass
	try:
		input_search_user_name.SetValue(user.name)
	except:
		pass
	try:
		input_search_user_description.SetValue(user.description)
	except KeyError:
		pass
	try:
		input_search_user_url.SetValue(user.entities['url']['urls'][0]['expanded_url'])
	except:
		pass
	input_search_user_friends.SetValue(str(user.friends_count)+' / '+str(user.followers_count))
	input_search_user_tweet.SetValue(str(user.statuses_count))
	frame.SetStatusText('データ取得完了！')

def sl_r_change(event):
	"""
	void sl_r_change(event)

	wxPythonのイベント用関数。
	RGBバーのRのチェンジイベントが発生した際に実行。
	16進数変換を行い、その結果をフォームにセット。
	"""

	# 16進数変換
	colR = hex(input_profile_col_R.GetValue()).replace("0x", "")
	if len(colR) == 1: # 一桁だったら
		colR = "0"+colR
	elif len(colR) == 0: # 何もなかったら
		colB = "00"
	colG = hex(input_profile_col_G.GetValue()).replace("0x", "")
	if len(colG) == 1:
		colG = "0"+colG
	elif len(colG) == 0:
		colG = "00"
	colB = hex(input_profile_col_B.GetValue()).replace("0x", "")
	if len(colB) == 1:
		colB = "0"+colB
	elif len(colB) == 0:
		colB = "00"
	col = colR+colG+colB
	input_profile_col_text.Hide()
	input_profile_col_text.SetLabel("#"+col)
	input_profile_col_text.SetBackgroundColour("#"+col)
	input_profile_col_text.Show()

def sl_g_change(event):
	"""
	void sl_g_change(event)

	wxPythonのイベント用関数。
	RGBバーのGのチェンジイベントが発生した際に実行。
	16進数変換を行い、その結果をフォームにセット。
	"""

	colR = hex(input_profile_col_R.GetValue()).replace("0x", "")
	if len(colR) == 1:
		colR = "0"+colR
	elif len(colR) == 0:
		colB = "00"
	colG = hex(input_profile_col_G.GetValue()).replace("0x", "")
	if len(colG) == 1:
		colG = "0"+colG
	elif len(colG) == 0:
		colG = "00"
	colB = hex(input_profile_col_B.GetValue()).replace("0x", "")
	if len(colB) == 1:
		colB = "0"+colB
	elif len(colB) == 0:
		colB = "00"
	col = colR+colG+colB
	col = colR+colG+colB
	input_profile_col_text.Hide()
	input_profile_col_text.SetLabel("#"+col)
	input_profile_col_text.SetBackgroundColour("#"+col)
	input_profile_col_text.Show()

def sl_b_change(event):
	"""
	void sl_b_change(event)

	wxPythonのイベント用関数。
	RGBバーのBのチェンジイベントが発生した際に実行。
	16進数変換を行い、その結果をフォームにセット。
	"""

	colR = hex(input_profile_col_R.GetValue()).replace("0x", "")
	if len(colR) == 1:
		colR = "0"+colR
	elif len(colR) == 0:
		colB = "00"
	colG = hex(input_profile_col_G.GetValue()).replace("0x", "")
	if len(colG) == 1:
		colG = "0"+colG
	elif len(colG) == 0:
		colG = "00"
	colB = hex(input_profile_col_B.GetValue()).replace("0x", "")
	if len(colB) == 1:
		colB = "0"+colB
	elif len(colB) == 0:
		colB = "00"
	col = colR+colG+colB
	col = colR+colG+colB
	input_profile_col_text.Hide()
	input_profile_col_text.SetLabel("#"+col)
	input_profile_col_text.SetBackgroundColour("#"+col)
	input_profile_col_text.Show()

def update_name(event):
	"""
	void update_name(event)

	wxPythonのイベント用関数。
	更新ボタンが押された時の処理。
	Twitter APIのupdate_profileを利用し名前を変更。
	"""

	try: # 接続してみる
		frame.SetStatusText('接続中…')
		auth = tp.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(input_at.GetValue(), input_as.GetValue())
		api = tp.API(auth)
		d = api.get_settings()
		screen_name = d["screen_name"]
		user = api.get_user(screen_name)
		frame.SetStatusText('接続成功！')
	except tp.error.TweepError:
		frame.SetStatusText('接続失敗…キーを確認してください')
	time.sleep(0.5)
	frame.SetStatusText('更新中…')
	try: # 更新してみる
		api.update_profile(name=input_profile_name.GetValue())
		frame.SetStatusText('更新完了！')
	except tp.error.TweepError:
		frame.SetStatusText('更新失敗。。。')

def update_url(event):
	"""
	void update_url(event)

	wxPythonのイベント用関数。
	更新ボタンが押された時の処理。
	Twitter APIのupdate_profileを利用しURLを変更。
	"""

	try:
		frame.SetStatusText('接続中…')
		auth = tp.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(input_at.GetValue(), input_as.GetValue())
		api = tp.API(auth)
		d = api.get_settings()
		screen_name = d["screen_name"]
		user = api.get_user(screen_name)
		frame.SetStatusText('接続成功！')
	except tp.error.TweepError:
		frame.SetStatusText('接続失敗…キーを確認してください')
	time.sleep(0.5)
	frame.SetStatusText('更新中…')
	try:
		api.update_profile(url=input_profile_url.GetValue())
		frame.SetStatusText('更新完了！')
	except tp.error.TweepError:
		frame.SetStatusText('更新失敗。。。')

def update_description(event):
	"""
	void update_description(event)

	wxPythonのイベント用関数。
	更新ボタンが押された時の処理。
	Twitter APIのupdate_profileを利用し説明文を変更。
	"""

	try:
		frame.SetStatusText('接続中…')
		auth = tp.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(input_at.GetValue(), input_as.GetValue())
		api = tp.API(auth)
		d = api.get_settings()
		screen_name = d["screen_name"]
		user = api.get_user(screen_name)
		frame.SetStatusText('接続成功！')
	except tp.error.TweepError:
		frame.SetStatusText('接続失敗…キーを確認してください')
	time.sleep(0.5)
	frame.SetStatusText('更新中…')
	try:
		api.update_profile(description=input_profile_description.GetValue().replace("\n", " "))
		frame.SetStatusText('更新完了！')
	except tp.error.TweepError:
		frame.SetStatusText('更新失敗。。。')

def update_location(event):
	"""
	void update_location(event)

	wxPythonのイベント用関数。
	更新ボタンが押された時の処理。
	Twitter APIのupdate_profileを利用し位置情報を変更。
	"""

	try:
		frame.SetStatusText('接続中…')
		auth = tp.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(input_at.GetValue(), input_as.GetValue())
		api = tp.API(auth)
		d = api.get_settings()
		screen_name = d["screen_name"]
		user = api.get_user(screen_name)
		frame.SetStatusText('接続成功！')
	except tp.error.TweepError:
		frame.SetStatusText('接続失敗…キーを確認してください')
	time.sleep(0.5)
	frame.SetStatusText('更新中…')
	try:
		api.update_profile(location=input_profile_location.GetValue())
		frame.SetStatusText('更新完了！')
	except tp.error.TweepError:
		frame.SetStatusText('更新失敗。。。')

def update_color(event):
	"""
	void update_color(event)

	wxPythonのイベント用関数。
	更新ボタンが押された時の処理。
	Twitter APIのupdate_profileを利用しテーマカラーを変更。
	"""

	try:
		frame.SetStatusText('接続中…')
		auth = tp.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(input_at.GetValue(), input_as.GetValue())
		api = tp.API(auth)
		d = api.get_settings()
		screen_name = d["screen_name"]
		user = api.get_user(screen_name)
		frame.SetStatusText('接続成功！')
	except tp.error.TweepError:
		frame.SetStatusText('接続失敗…キーを確認してください')
	time.sleep(0.5)
	frame.SetStatusText('更新中…')
	try:
		api.update_profile(profile_link_color=input_profile_col_text.GetLabel())
		frame.SetStatusText('更新完了！')
	except tp.error.TweepError:
		frame.SetStatusText('更新失敗。。。')

def tweet_templete(event):
	"""
	void tweet_templete(event)

	wxPythonのイベント用関数。
	ツイートボタンが押された時の処理。
	テンプレートを用意しツイートすることができる。
	"""

	"""
	%follow%: フォロー数に置換
	%follower%: フォロワー数に置換
	%id%: Twitter IDに置換
	%name%: ユーザーネームに置換
	%description%: 説明文に置換
	%url%: URLに置換
	%location%: 位置情報に置換
	%tweet_count%: ツイート数に置換
	"""

	try:
		frame.SetStatusText('接続中…')
		auth = tp.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(input_at.GetValue(), input_as.GetValue())
		api = tp.API(auth)
		d = api.get_settings()
		screen_name = d["screen_name"]
		user = api.get_user(screen_name)
		frame.SetStatusText('接続成功！')
	except tp.error.TweepError:
		frame.SetStatusText('接続失敗…キーを確認してください')
	time.sleep(0.5)
	text = input_template_tweet.GetValue()

	# 置換作業
	text = text.replace("%follow%", str(user.friends_count))
	text = text.replace("%follower%", str(user.followers_count))
	text = text.replace("%id%", screen_name)
	text = text.replace("%name%", user.name)
	text = text.replace("%description%", user.description)
	try:
		text = text.replace("%url%", user.entities['url']['urls'][0]['expanded_url'])
	except KeyError:
		pass
	text = text.replace("%location%", user.location)
	text = text.replace("%tweet_count%", str(user.statuses_count))
	frame.SetStatusText('ツイート送信中…')
	try: # ツイート
		api.update_status(status=text)
		frame.SetStatusText('ツイート送信完了！')
	except tp.error.TweepError:
		frame.SetStatusText('ツイート送信に失敗。。。')
def hl1_event(e):
	"""
	void hl1_event(event)

	wxPythonのイベント用関数。
	URLの処理。
	指定されたURlをブラウザで開く。
	"""

	if e.LeftUp():
		webbrowser.open("https://twitter.com/I_am_4a")
	e.Skip()
def hl2_event(e):
	"""
	void hl2_event(event)

	wxPythonのイベント用関数。
	URLの処理。
	指定されたURlをブラウザで開く。
	"""
	if e.LeftUp():
		webbrowser.open("mailto:ts3@f5.si?subject=Contact%20to%20I_am_4a")
	e.Skip()

def profile_refresh_default():
	"""
	void profile_refresh_default(void)

	初期化用関数。
	すべてのフォームを準備するための関数。
	"""

	try:
		frame.SetStatusText('接続中…')
		auth = tp.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(input_at.GetValue(), input_as.GetValue())
		api = tp.API(auth)
		api.user_timeline()
		frame.SetStatusText('接続成功！')
	except tp.error.TweepError:
		frame.SetStatusText('接続失敗…キーを確認してください')
	time.sleep(0.5)
	frame.SetStatusText('データ取得中…')
	d = api.get_settings()
	screen_name = d["screen_name"]
	user = api.get_user(screen_name)
	"""
	text_user_screen_name = wx.StaticText(panel3, -1, 'Twitter ID:')
	text_user_name = wx.StaticText(panel3, -1, 'ユーザーネーム:')
	text_user_description = wx.StaticText(panel3, -1, '説明文:')
	text_user_url = wx.StaticText(panel3, -1, 'URL:')
	text_user_geo = wx.StaticText(panel3, -1, '位置情報:')
	text_user_friends_count = wx.StaticText(panel3, -1, 'フォロー/フォロワー数:')
	text_user_tweet_count = wx.StaticText(panel3, -1, 'ツイート数: ')
	"""

	text_user_screen_name.SetLabel('Twitter ID:')
	text_user_name.SetLabel('ユーザーネーム:')
	text_user_description.SetLabel('説明文:')
	text_user_url.SetLabel('URL:')
	text_user_geo.SetLabel('位置情報:')
	text_user_friends_count.SetLabel('フォロー/フォロワー数:')
	text_user_tweet_count.SetLabel('ツイート数:')

	text_user_screen_name.SetLabel('Twitter ID: @'+screen_name)
	try:
		text_user_geo.SetLabel('位置情報: '+user.location)
		input_profile_location.SetValue(user.location)
	except KeyError:
		pass
	try:
		text_user_name.SetLabel('ユーザーネーム: '+user.name)
		input_profile_name.SetValue(user.name)
	except:
		pass
	try:
		text_user_description.SetLabel('説明文: '+user.description)
		input_profile_description.SetValue(user.description)
	except KeyError:
		pass
	try:
		text_user_url.SetLabel('URL: '+user.entities['url']['urls'][0]['expanded_url'])
		input_profile_url.SetValue(user.entities['url']['urls'][0]['expanded_url'])
	except KeyError:
		pass
	input_profile_col_text.SetLabel("#"+user.profile_link_color)
	input_profile_col_R.SetValue(int(user.profile_link_color[0:2], 16))
	input_profile_col_G.SetValue(int(user.profile_link_color[2:4], 16))
	input_profile_col_B.SetValue(int(user.profile_link_color[4:6], 16))
	
	text_user_friends_count.SetLabel('フォロー/フォロワー数: '+str(user.friends_count)+' / '+str(user.followers_count))
	text_user_tweet_count.SetLabel('ツイート数: '+str(user.statuses_count))

	frame.SetStatusText('更新成功！')

def profile_refresh(event):
	"""
	void profile_refresh(void)

	wxPythonのイベント用関数。
	更新ボタンが押された際の処理。
	プロフィールの更新をする。
	"""

	try:
		frame.SetStatusText('接続中…')
		auth = tp.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(input_at.GetValue(), input_as.GetValue())
		api = tp.API(auth)
		api.user_timeline()
		frame.SetStatusText('接続成功！')
	except tp.error.TweepError:
		frame.SetStatusText('接続失敗…キーを確認してください')
	time.sleep(0.5)
	frame.SetStatusText('データ取得中…')
	d = api.get_settings()
	screen_name = d["screen_name"]
	user = api.get_user(screen_name)
	"""
	text_user_screen_name = wx.StaticText(panel3, -1, 'Twitter ID:')
	text_user_name = wx.StaticText(panel3, -1, 'ユーザーネーム:')
	text_user_description = wx.StaticText(panel3, -1, '説明文:')
	text_user_url = wx.StaticText(panel3, -1, 'URL:')
	text_user_geo = wx.StaticText(panel3, -1, '位置情報:')
	text_user_friends_count = wx.StaticText(panel3, -1, 'フォロー/フォロワー数:')
	text_user_tweet_count = wx.StaticText(panel3, -1, 'ツイート数: ')
	"""

	text_user_screen_name.SetLabel('Twitter ID:')
	text_user_name.SetLabel('ユーザーネーム:')
	text_user_description.SetLabel('説明文:')
	text_user_url.SetLabel('URL:')
	text_user_geo.SetLabel('位置情報:')
	text_user_friends_count.SetLabel('フォロー/フォロワー数:')
	text_user_tweet_count.SetLabel('ツイート数:')

	text_user_screen_name.SetLabel('Twitter ID: @'+screen_name)
	try:
		text_user_geo.SetLabel('位置情報: '+user.location)
		input_profile_location.SetValue(user.location)
	except KeyError:
		pass
	try:
		text_user_name.SetLabel('ユーザーネーム: '+user.name)
		input_profile_name.SetValue(user.name)
	except:
		pass
	try:
		text_user_description.SetLabel('説明文: '+user.description)
		input_profile_description.SetValue(user.description)
	except KeyError:
		pass
	try:
		text_user_url.SetLabel('URL: '+user.entities['url']['urls'][0]['expanded_url'])
		input_profile_url.SetValue(user.entities['url']['urls'][0]['expanded_url'])
	except KeyError:
		pass
	input_profile_col_text.SetLabel(user.profile_link_color)
	input_profile_col_R.SetValue(int(user.profile_link_color[0:2], 16))
	input_profile_col_G.SetValue(int(user.profile_link_color[2:4], 16))
	input_profile_col_B.SetValue(int(user.profile_link_color[4:6], 16))
	
	text_user_friends_count.SetLabel('フォロー/フォロワー数: '+str(user.friends_count)+' / '+str(user.followers_count))
	text_user_tweet_count.SetLabel('ツイート数: '+str(user.statuses_count))

	frame.SetStatusText('更新成功！')

def tweet(event):
	"""
	void tweet(void)

	wxPythonのイベント用関数。
	ツイートボタンが押された際の処理。
	ツイートをする。
	"""

	try:
		frame.SetStatusText('接続中…')
		auth = tp.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(input_at.GetValue(), input_as.GetValue())
		api = tp.API(auth)
		api.user_timeline()
		frame.SetStatusText('接続成功！')
	except tp.error.TweepError:
		frame.SetStatusText('接続失敗…キーを確認してください')
	time.sleep(0.5)
	frame.SetStatusText('ツイート送信中…')
	try:
		api.update_status(status=input_tweet.GetValue())
		frame.SetStatusText('ツイート送信完了！')
		if cbox_textsave.GetValue() == False: # 「ツイート本文を…」のチェックボックスがONじゃない場合
			input_tweet.Clear() # クリアする
	except tp.error.TweepError:
		frame.SetStatusText('ツイート送信に失敗。。。')

def key_check(event):
	"""
	void key_check(void)

	wxPythonのイベント用関数。
	チェックボタンが押された際の処理。
	アクセスキー等のチェックをする。
	"""

	try:
		frame.SetStatusText('接続中…')
		auth = tp.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(input_at.GetValue(), input_as.GetValue())
		api = tp.API(auth)
		api.user_timeline()
		frame.SetStatusText('接続成功！')
	except tp.error.TweepError:
		frame.SetStatusText('接続失敗…キーを確認してください')

def key_reset(event):
	"""
	void key_reset(void)

	wxPythonのイベント用関数。
	リセットボタンが押された際の処理。
	アクセスキー等のリセットをする。
	"""

	input_at.Clear()
	input_as.Clear()
	frame.SetStatusText('リセット完了！')

def key_save(event):
	"""
	void key_save(void)

	wxPythonのイベント用関数。
	セーブボタンが押された際の処理。
	アクセスキーをセーブする。
	"""

	fn = tkfd.asksaveasfilename(filetypes=fType,initialdir=iDir)
	if fn.find(".key") == -1:
		fn = fn + ".key"
	try:
		f = open(fn, "w")
		f.write(input_at.GetValue()+","+input_as.GetValue())
		f.close()
		f = open("EasyTweet.tmp", "w") # テンポラリファイルへの書き込み
		f.write(input_at.GetValue()+","+input_as.GetValue()+","+input_template_tweet.GetValue().replace(",", "[SEP]").replace("\n", "[BR]"))
		f.close()
		frame.SetStatusText('セーブ完了('+fn+')')
	except UnboundLocalError:
		frame.SetStatusText('セーブに失敗しました。。。')
		pass

def key_load(event):
	"""
	void key_load(void)

	wxPythonのイベント用関数。
	ロードボタンが押された際の処理。
	アクセスキーをファイルから読み込む。
	"""

	fn = tkfd.askopenfilename(filetypes=fType,initialdir=iDir)
	try:
		f = open(fn, "r")
		for row in f:
			list = row.split(",")
		f.close()
		input_at.SetValue(list[0])
		input_as.SetValue(list[1])
		f = open("EasyTweet.tmp", "w") # テンポラリファイルへの書き込み
		f.write(input_at.GetValue()+","+input_as.GetValue())
		f.close()
		frame.SetStatusText('ロード完了('+fn+')')
	except UnboundLocalError:
		frame.SetStatusText('ロードに失敗しました。。。')
		pass
	profile_refresh_default() # フォームの準備

def str_count(event):
	"""
	void str_count(void)

	wxPythonのイベント用関数。
	文字が入力された時の処理。
	文字数とバイト数をカウントする。
	"""

	slist = []
	for i in input_tweet.GetValue():
		slist.append(i)
	cnt = 0
	for var in slist:
		if var.find("\n") != -1:
			cnt = cnt + 1
		elif unicodedata.name(var).find('CJK UNIFIED') != -1 or unicodedata.name(var).find('HIRAGANA') != -1 or unicodedata.name(var).find('KATAKANA') != -1:
			cnt = cnt + 2
		else:
			cnt = cnt + 1
	if cnt > 280: # Twitterの規定バイト数
		text_byte_count.SetLabel('バイト数: '+str(cnt)+"/280 Warning: バイト数をオーバーしています")
	else:
		text_byte_count.SetLabel('バイト数: '+str(cnt)+"/280")
	text_str_count.SetLabel('文字数: '+str(len(input_tweet.GetValue())))

# --------------------------------------

# 本処理
if __name__ == '__main__':

	# アプリ作成
	app = wx.App()

	# フレーム(GUIの基)を生成する
	frame = wx.Frame(None, -1, 'EasyTweet Version '+version(), size=(600, 600), pos=(0,0))

	# 上のタブ用
	notebook = wx.Notebook(frame, -1)

	# レイアウトを張り付けるパネル(キー設定用)
	panel = wx.Panel(notebook, -1)

	# パネルに合わせるように並べるボックス(たて)
	vbox = wx.BoxSizer(wx.VERTICAL)

	# パネルに合わせるように並べるボックス(よこ)
	hbox3 = wx.BoxSizer(wx.HORIZONTAL)

	# 各種部品作成・設置
	text_at = wx.StaticText(panel, -1, 'Access Token')
	hbox3.Add(text_at, 0, wx.RIGHT, 8)
	input_at = wx.TextCtrl(panel, -1)
	hbox3.Add(input_at, 1)
	vbox.Add(hbox3, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)

	hbox4 = wx.BoxSizer(wx.HORIZONTAL)
	text_as = wx.StaticText(panel, -1, 'Access Token Secret')
	hbox4.Add(text_as, 0, wx.RIGHT, 8)
	input_as = wx.TextCtrl(panel, -1)
	hbox4.Add(input_as, 1)
	vbox.Add(hbox4, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)

	hbox5 = wx.BoxSizer(wx.HORIZONTAL)
	btn_check = wx.Button(panel, -1, 'キーをチェックする', size=(100, 30))
	btn_check.Bind(wx.EVT_BUTTON, key_check)
	hbox5.Add(btn_check, 0)
	btn_reset = wx.Button(panel, -1, 'キーをリセットする', size=(100, 30))
	btn_reset.Bind(wx.EVT_BUTTON, key_reset)
	hbox5.Add(btn_reset, 0, wx.LEFT | wx.BOTTOM, 5)
	vbox.Add(hbox5, 0, wx.ALIGN_RIGHT | wx.RIGHT, 10)

	hbox6 = wx.BoxSizer(wx.HORIZONTAL)
	btn_save = wx.Button(panel, -1, 'キーをセーブする', size=(100, 20))
	btn_save.Bind(wx.EVT_BUTTON, key_save)
	hbox6.Add(btn_save, 0)
	btn_load = wx.Button(panel, -1, 'キーをロードする', size=(100, 20))
	btn_load.Bind(wx.EVT_BUTTON, key_load)
	hbox6.Add(btn_load, 0)
	vbox.Add(hbox6, 0, wx.ALIGN_RIGHT | wx.RIGHT, 10)

	# パネルにボックスをセット
	panel.SetSizer(vbox)

	# ------------------------------------------------

	# レイアウトを張り付けるパネル(ツイート用)
	panel2 = wx.Panel(notebook, -1)

	vbox1 = wx.BoxSizer(wx.VERTICAL)
	text_tweet = wx.StaticText(panel2, -1, 'ツイート')
	vbox1.Add(text_tweet, 0, wx.LEFT | wx.TOP, 10)
	input_tweet = wx.TextCtrl(panel2, -1, style=wx.TE_MULTILINE, size=(500, 200), pos=(0,0))
	input_tweet.Bind(wx.EVT_TEXT, str_count)
	vbox1.Add(input_tweet, flag=wx.GROW)
	text_byte_count = wx.StaticText(panel2, -1, 'バイト数: 0/280')
	text_str_count = wx.StaticText(panel2, -1, '文字数: 0')
	vbox1.Add(text_byte_count)
	vbox1.Add(text_str_count)
	cbox_textsave = wx.CheckBox(panel2, -1, 'ツイート本文をクリアしない')
	vbox1.Add(cbox_textsave)
	btn_tweet = wx.Button(panel2, -1, 'ツイートする', size=(100, 20))
	btn_tweet.Bind(wx.EVT_BUTTON, tweet)
	vbox1.Add(btn_tweet, flag=wx.ALIGN_RIGHT)

	panel2.SetSizer(vbox1)

	# -----------------------------------------------

	# レイアウトを張り付けるパネル(プロフィール表示用)
	panel3 = wx.Panel(notebook, -1)

	vbox2 = wx.BoxSizer(wx.VERTICAL)
	text_user_screen_name = wx.StaticText(panel3, -1, 'Twitter ID:')
	text_user_name = wx.StaticText(panel3, -1, 'ユーザーネーム:')
	text_user_description = wx.StaticText(panel3, -1, '説明文:')
	text_user_url = wx.StaticText(panel3, -1, 'URL:')
	text_user_geo = wx.StaticText(panel3, -1, '位置情報:')
	text_user_friends_count = wx.StaticText(panel3, -1, 'フォロー/フォロワー数:')
	text_user_tweet_count = wx.StaticText(panel3, -1, 'ツイート数: ')
	vbox2.Add(text_user_screen_name)
	vbox2.Add(text_user_name)
	vbox2.Add(text_user_description)
	vbox2.Add((0, 50))
	vbox2.Add(text_user_url)
	vbox2.Add(text_user_geo)
	vbox2.Add(text_user_friends_count)
	vbox2.Add(text_user_tweet_count)
	btn_refresh = wx.Button(panel3, -1, "更新する", size=(100,20))
	btn_refresh.Bind(wx.EVT_BUTTON, profile_refresh)
	vbox2.Add(btn_refresh, flag=wx.ALIGN_RIGHT)

	panel3.SetSizer(vbox2)

	# --------------------------------------------------

	# レイアウトを張り付けるパネル(About表示用)
	panel4 = wx.Panel(notebook, -1)
	bmp = wx.Bitmap("logo.png")
	control = wx.StaticBitmap(panel4, -1, bmp)
	control.SetPosition((200, 30))

	vbox6 = wx.BoxSizer(wx.VERTICAL)
	vbox6.Add((0, 30))
	vbox6.Add(control, flag=wx.CENTER)
	vbox6.Add((0, 15))
	text_app_title1 = wx.StaticText(panel4, -1, "EasyTweet Version "+version())
	text_app_title2 = wx.StaticText(panel4, -1, "by I_am_4a")
	text_app_description1 = wx.StaticText(panel4, -1, "Copyright (C) "+str(datetime.datetime.today().year)+" I_am_4a All Rights Reserved.")
	text_app_description2 = wx.StaticText(panel4, -1, "Twitter: ")
	text_app_description2_url = wx.StaticText(panel4, -1, "@I_am_4a")
	text_app_description2_url.Bind(wx.EVT_MOUSE_EVENTS, hl1_event)
	text_app_description2_url.Bind(wx.EVT_MOTION, hl1_event)
	font_hl1_2 = wx.Font(8, wx.FONTFAMILY_SWISS, wx.ITALIC, wx.FONTWEIGHT_LIGHT, True)
	text_app_description2_url.SetFont(font_hl1_2)
	text_app_description2_url.SetForegroundColour('#0000ff')
	hl1 = wx.BoxSizer(wx.HORIZONTAL)
	hl1.Add(text_app_description2)
	hl1.Add(text_app_description2_url)
	text_app_description3 = wx.StaticText(panel4, -1, "Mail: ")
	text_app_description3_url = wx.StaticText(panel4, -1, "ts3@f5.si")
	text_app_description3_url.Bind(wx.EVT_MOUSE_EVENTS, hl2_event)
	text_app_description3_url.Bind(wx.EVT_MOTION, hl2_event)
	text_app_description3_url.SetFont(font_hl1_2)
	text_app_description3_url.SetForegroundColour('#0000ff')
	hl2 = wx.BoxSizer(wx.HORIZONTAL)
	hl2.Add(text_app_description3)
	hl2.Add(text_app_description3_url)
	font1 = wx.Font(18, wx.FONTFAMILY_SWISS, wx.ITALIC, wx.FONTWEIGHT_LIGHT)
	font2 = wx.Font(11, wx.FONTFAMILY_SWISS, wx.ITALIC, wx.FONTWEIGHT_LIGHT)
	font3 = wx.Font(8, wx.FONTFAMILY_SWISS, wx.ITALIC, wx.FONTWEIGHT_LIGHT)
	text_app_title1.SetFont(font1)
	text_app_title2.SetFont(font2)
	text_app_description1.SetFont(font3)
	text_app_description2.SetFont(font3)
	text_app_description3.SetFont(font3)
	vbox6.Add(text_app_title1, flag=wx.CENTER)
	vbox6.Add(text_app_title2, flag=wx.CENTER)
	vbox6.Add((0, 15))
	vbox6.Add(text_app_description1, flag=wx.CENTER)
	vbox6.Add(hl1, flag=wx.CENTER)
	vbox6.Add(hl2, flag=wx.CENTER)

	panel4.SetSizer(vbox6)
	
	# ------------------------------------------------
	
	# レイアウトを張り付けるパネル(テンプレートツイート用)
	panel5 = wx.Panel(notebook, -1)

	vbox7 = wx.BoxSizer(wx.VERTICAL)
	text_template_tweet = wx.StaticText(panel5, -1, 'テンプレートツイート')
	vbox7.Add(text_template_tweet, 0, wx.LEFT | wx.TOP, 10)
	input_template_tweet = wx.TextCtrl(panel5, -1, style=wx.TE_MULTILINE, size=(500, 200), pos=(0,0))
	vbox7.Add(input_template_tweet, flag=wx.GROW)
	btn_template_tweet = wx.Button(panel5, -1, 'ツイートする', size=(100, 20))
	btn_template_tweet.Bind(wx.EVT_BUTTON, tweet_templete)
	vbox7.Add(btn_template_tweet, flag=wx.ALIGN_RIGHT)

	panel5.SetSizer(vbox7)

	# ----------------------------------------------

	# レイアウトを張り付けるパネル(プロフィール更新用)
	panel6 = wx.Panel(notebook, -1)

	vbox8 = wx.BoxSizer(wx.VERTICAL)
	hbox7 = wx.BoxSizer(wx.HORIZONTAL)
	text_update_profile_name = wx.StaticText(panel6, -1, "ユーザーネーム:")
	input_profile_name = wx.TextCtrl(panel6, -1)
	hbox7.Add(text_update_profile_name, 0, wx.RIGHT, 8)
	hbox7.Add(input_profile_name, 1)
	vbox8.Add(hbox7, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)
	btn_profile_update_name = wx.Button(panel6, -1, '更新する', size=(100, 30))
	btn_profile_update_name.Bind(wx.EVT_BUTTON, update_name)
	vbox8.Add(btn_profile_update_name, 0, wx.ALIGN_RIGHT | wx.RIGHT, 10)
	hbox8 = wx.BoxSizer(wx.HORIZONTAL)
	text_update_profile_description = wx.StaticText(panel6, -1, "説明:")
	input_profile_description = wx.TextCtrl(panel6, -1, style=wx.TE_MULTILINE)
	hbox8.Add(text_update_profile_description, 0, wx.RIGHT, 8)
	hbox8.Add(input_profile_description, 1)
	vbox8.Add(hbox8, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)
	btn_profile_update_description = wx.Button(panel6, -1, '更新する', size=(100, 30))
	btn_profile_update_description.Bind(wx.EVT_BUTTON, update_description)
	vbox8.Add(btn_profile_update_description, 0, wx.ALIGN_RIGHT | wx.RIGHT, 10)
	hbox8 = wx.BoxSizer(wx.HORIZONTAL)
	text_update_profile_location = wx.StaticText(panel6, -1, "位置情報:")
	input_profile_location = wx.TextCtrl(panel6, -1)
	hbox8.Add(text_update_profile_location, 0, wx.RIGHT, 8)
	hbox8.Add(input_profile_location, 1)
	vbox8.Add(hbox8, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)
	btn_profile_update_location = wx.Button(panel6, -1, '更新する', size=(100, 30))
	btn_profile_update_location.Bind(wx.EVT_BUTTON, update_location)
	vbox8.Add(btn_profile_update_location, 0, wx.ALIGN_RIGHT | wx.RIGHT, 10)
	hbox9 = wx.BoxSizer(wx.HORIZONTAL)
	text_update_profile_url = wx.StaticText(panel6, -1, "URL:")
	input_profile_url = wx.TextCtrl(panel6, -1)
	hbox9.Add(text_update_profile_url, 0, wx.RIGHT, 8)
	hbox9.Add(input_profile_url, 1)
	vbox8.Add(hbox9, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)
	btn_profile_update_url = wx.Button(panel6, -1, '更新する', size=(100, 30))
	btn_profile_update_url.Bind(wx.EVT_BUTTON, update_url)
	vbox8.Add(btn_profile_update_url, 0, wx.ALIGN_RIGHT | wx.RIGHT, 10)

	text_update_profile_col = wx.StaticText(panel6, -1, "テーマカラー:")
	text_update_profile_col_R = wx.StaticText(panel6, -1, "Red")
	text_update_profile_col_G = wx.StaticText(panel6, -1, "Green")
	text_update_profile_col_B = wx.StaticText(panel6, -1, "Blue")
	input_profile_col_text = wx.Button(panel6, -1, "")
	input_profile_col_text.Disable()
	input_profile_col_text.SetForegroundColour("#ffffff")
	input_profile_col_R = wx.Slider(panel6, style=wx.SL_LABELS)
	input_profile_col_R.SetTickFreq(10)
	input_profile_col_R.SetMin(0)
	input_profile_col_R.SetMax(255)
	input_profile_col_R.Bind(wx.EVT_SLIDER, sl_r_change)
	input_profile_col_G = wx.Slider(panel6, style=wx.SL_LABELS)
	input_profile_col_G.SetTickFreq(10)
	input_profile_col_G.SetMin(0)
	input_profile_col_G.SetMax(255)
	input_profile_col_G.Bind(wx.EVT_SLIDER, sl_g_change)
	input_profile_col_B = wx.Slider(panel6, style=wx.SL_LABELS)
	input_profile_col_B.SetTickFreq(10)
	input_profile_col_B.SetMin(0)
	input_profile_col_B.SetMax(255)
	input_profile_col_B.Bind(wx.EVT_SLIDER, sl_b_change)
	vbox8.Add(text_update_profile_col)
	vbox8.Add(text_update_profile_col_R)
	vbox8.Add(input_profile_col_R, flag=wx.GROW)
	vbox8.Add(text_update_profile_col_G)
	vbox8.Add(input_profile_col_G, flag=wx.GROW)
	vbox8.Add(text_update_profile_col_B)
	vbox8.Add(input_profile_col_B, flag=wx.GROW)
	vbox8.Add(input_profile_col_text)
	btn_profile_update_col = wx.Button(panel6, -1, '更新する', size=(100, 30))
	btn_profile_update_col.Bind(wx.EVT_BUTTON, update_color)
	vbox8.Add(btn_profile_update_col, 0, wx.ALIGN_RIGHT | wx.RIGHT, 10)

	panel6.SetSizer(vbox8)

	# -----------------------------------------------------

	# レイアウトを張り付けるパネル(プロフィール検索用)
	panel7 = wx.Panel(notebook, -1)

	vbox9 = wx.BoxSizer(wx.VERTICAL)
	hbox10 = wx.BoxSizer(wx.HORIZONTAL)
	hbox11 = wx.BoxSizer(wx.HORIZONTAL)
	hbox12 = wx.BoxSizer(wx.HORIZONTAL)
	hbox13 = wx.BoxSizer(wx.HORIZONTAL)
	hbox14 = wx.BoxSizer(wx.HORIZONTAL)
	hbox15 = wx.BoxSizer(wx.HORIZONTAL)
	hbox16 = wx.BoxSizer(wx.HORIZONTAL)

	text_search_screen_name = wx.StaticText(panel7, -1, "Twitter ID")
	text_search_user_name = wx.StaticText(panel7, -1, "ユーザー名")
	text_search_user_description = wx.StaticText(panel7, -1, "説明文")
	text_search_user_url = wx.StaticText(panel7, -1, "URL")
	text_search_user_location = wx.StaticText(panel7, -1, "位置情報")
	text_search_user_friends = wx.StaticText(panel7, -1, "フォロー/フォロワー数")
	text_search_user_tweet = wx.StaticText(panel7, -1, "ツイート数")

	input_search_screen_name = wx.TextCtrl(panel7, -1)
	input_search_user_name = wx.TextCtrl(panel7, -1)
	input_search_user_description = wx.TextCtrl(panel7, -1, style=wx.TE_MULTILINE)
	input_search_user_url = wx.TextCtrl(panel7, -1)
	input_search_user_location = wx.TextCtrl(panel7, -1)
	input_search_user_friends = wx.TextCtrl(panel7, -1)
	input_search_user_tweet = wx.TextCtrl(panel7, -1)
	input_search_user_name.Disable()
	input_search_user_description.Disable()
	input_search_user_url.Disable()
	input_search_user_friends.Disable()
	input_search_user_tweet.Disable()
	input_search_user_location.Disable()
	hbox10.Add(text_search_screen_name, 0, wx.RIGHT, 8)
	hbox10.Add(input_search_screen_name, 1)
	vbox9.Add(hbox10, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)
	btn_search = wx.Button(panel7, -1, '検索する', size=(100, 30))
	btn_search.Bind(wx.EVT_BUTTON, search)
	vbox9.Add(btn_search, 0, wx.ALIGN_RIGHT | wx.RIGHT, 10)
	hbox11.Add(text_search_user_name, 0, wx.RIGHT, 8)
	hbox11.Add(input_search_user_name, 1)
	vbox9.Add(hbox11, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)
	hbox12.Add(text_search_user_description, 0, wx.RIGHT, 8)
	hbox12.Add(input_search_user_description, 1)
	vbox9.Add(hbox12, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)
	hbox13.Add(text_search_user_url, 0, wx.RIGHT, 8)
	hbox13.Add(input_search_user_url, 1)
	vbox9.Add(hbox13, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)
	hbox16.Add(text_search_user_location, 0, wx.RIGHT, 8)
	hbox16.Add(input_search_user_location, 1)
	vbox9.Add(hbox16, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)
	hbox14.Add(text_search_user_friends, 0, wx.RIGHT, 8)
	hbox14.Add(input_search_user_friends, 1)
	vbox9.Add(hbox14, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)
	hbox15.Add(text_search_user_tweet, 0, wx.RIGHT, 8)
	hbox15.Add(input_search_user_tweet, 1)
	vbox9.Add(hbox15, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)

	panel7.SetSizer(vbox9)

	# ------------------------------

	# 認証用
	panel8 = wx.Panel(notebook, -1)

	btn_auth = wx.Button(panel8, -1, '認証する')
	btn_auth.Bind(wx.EVT_BUTTON, event_auth)

	vbox10 = wx.BoxSizer(wx.VERTICAL)
	vbox10.Add(btn_auth, flag=wx.ALIGN_CENTER)

	panel8.SetSizer(vbox10)


	# ノートブック(タブ)にパネルを追加
	notebook.InsertPage(0, panel, 'キー設定')
	notebook.InsertPage(1, panel2, 'ツイート')
	notebook.InsertPage(2, panel3, 'プロフィール')
	notebook.InsertPage(3, panel5, 'テンプレートツイート')
	notebook.InsertPage(4, panel6, 'プロフィール変更')
	notebook.InsertPage(5, panel7, 'プロフィール検索')
	notebook.InsertPage(6, panel4, 'About')
	notebook.InsertPage(7, panel8, 'アプリ連携')

	# ステータスバーの設置
	frame.CreateStatusBar()

	# 起動時にテンポラリファイルがあれば読み込み
	if os.path.isfile(".\EasyTweet.tmp"):
		try:
			f = open(".\EasyTweet.tmp", "r")
			for row in f:
				list = row.split(",")
			f.close()
			input_at.SetValue(list[0])
			input_as.SetValue(list[1])
			input_template_tweet.SetValue(list[2].replace("[SEP]", ",").replace("[BR]", "\n"))
			profile_refresh_default()
		except:
			frame.SetStatusText('テンポラリファイルのロードに失敗しました。。。')
			time.sleep(3)
			pass
	frame.SetStatusText("EasyTweet by I_am_4a")

	# センター配置
	frame.Centre()

	# 表示
	frame.Show()

	# 処理開始
	app.MainLoop()