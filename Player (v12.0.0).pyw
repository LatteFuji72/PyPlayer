
# -*- coding: utf-8 -*-

import vlc
import glob
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import colorchooser
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import pathlib
import traceback
from itertools import chain
import pickle
import sys
from datetime import datetime, timedelta
import time

def OpenError(MainFile):
    messagebox.showwarning("警告", "プレイリストを認識できませんでした")
    global List1, List2, List3, List4, List5, ext_list, play_index, play_position
    List1 = sorted(list(chain.from_iterable([glob.glob(MainFile+"/**/*."+ext, recursive=True) for ext in ext_list])))
    #print(List1)
    List2 = []
    for l in List1:
        file = pathlib.Path(l).stem
        List2.append(file)
    List3 = []
    List4 = []
    List5 = []
    play_index = 0
    play_position = 0

def OpenFile():
    global MainFile, THIS_DIR_NAME, List1, List2, List3, List4, List5, img_file, ext_list, play_index, play_position, OE, img_color
    MainFile = filedialog.askdirectory(initialdir = THIS_DIR_NAME)
    if MainFile == "":
        messagebox.showerror('エラー', 'フォルダが選択されていません')
        root.destroy()
        root.mainloop()
        sys.exit()
    try:
        List1 = sorted(list(chain.from_iterable([glob.glob(MainFile+"/Music/**/*."+ext, recursive=True) for ext in ext_list])))
        List3 = sorted(list(glob.glob(MainFile+"/Lyrics/**/*.txt", recursive=True)))
        img_file = str(MainFile + "/PlayerImage.jpg")
        List2 = []
        for l in List1:
            file = pathlib.Path(l).stem
            List2.append(file)
        List4 = []
        List5 = []
        for l in List3:
            with open(l,"r", encoding="UTF-8") as f:
                d = f.read()
                List4.append(d)
        for l in List3:
            file = pathlib.Path(l).stem
            List5.append(file)
        if len(List1)==0:
            OpenError(MainFile)
            OE = True
        else:
            try:
                with open(MainFile+"/data.pickle", "rb") as file:
                    data = pickle.load(file)
                try:
                    img_color = data["color"]
                except:
                    pass
                name = data["name"]
                play_index = List2.index(name)
                play_position = data["position"]
                ret = messagebox.askyesno("確認", "前回の場所から再生しますか？")
                if ret != True:
                    play_index = 0
                    play_position = 0
            except:
                #print(traceback.format_exc())
                play_index = 0
                play_position = 0
            OE = False
    except:
        OpenError(MainFile)
        OE = True
        play_index = 0
        play_position = 0

def loop():
    global loop_bool, loop_num
    if loop_bool:
        loop_bool = False
        loop_num = None
    else:
        loop_bool = True
        p = player.get_media_player()
        loop_num = mediaList.index_of_item(p.get_media())

def listbox_selected1(event):
    for i in lsb1.curselection():
        file = lsb1.get(i)
        list_index = List2.index(file)
        p = player.get_media_player()
        while True:
            player.next()
            media_index = mediaList.index_of_item(p.get_media())
            if list_index == media_index:
                break

def listbox_selected2(event):
    for i in lsb2.curselection():
        file = lsb2.get(i)
        num = List5.index(file)
        txt1.configure(state=tk.NORMAL)
        txt1.delete("1.0", tk.END)
        txt1.insert("1.0", List4[num])
        txt1.configure(state=tk.DISABLED)

def play():
    global player, play_index, play_position
    p = player.get_media_player()
    while True:
        media_index = mediaList.index_of_item(p.get_media())
        if play_index == media_index:
            break
        player.next()
    p.set_position(play_position)

def color_conv(color):
    global MainFile, var5, PASSWORD
    if color != None:
        word = simpledialog.askstring("Password", "パスワードを入力してください", show='*')
        if word == PASSWORD:
            try:
                with open(MainFile+"/data.pickle", "rb") as file:
                    data = pickle.load(file)
            except:
                data = {}
            data["color"] = color
            with open(MainFile+"/data.pickle", "wb") as file:
                pickle.dump(data, file)
            var5.set("現在の色："+str(color))

def timer_conv(time):
    global timer, var6
    if not time:
        timer = False
        var6.set("設定されていません")
    else:
        now = datetime.now().replace(microsecond=0)
        time = timedelta(minutes = float(time))
        timer = now + time
        hour = timer.hour
        minu = timer.minute
        var6.set("現在の設定：{0} 時 {1} 分".format(hour, minu))

THIS_DIR_NAME = os.path.dirname(os.path.abspath(__file__))
PASSWORD = "Latte72"

root = tk.Tk()
root.title("Player")
root.geometry("860x430")
root.iconbitmap(THIS_DIR_NAME+"/Player.ico") 

note = ttk.Notebook(root)
note.pack()
music = ttk.Frame(note,width=860,height=410)
note.add(music,text="音楽")
lyric = ttk.Frame(note,width=860,height=410)
note.add(lyric,text="歌詞")
config = ttk.Frame(note,width=860,height=410)
note.add(config,text="設定")

ext_list = ["mp3", "wav", "aac", "wma", "m4a"]
img_color = "#F7D358"
OpenFile()

player = vlc.MediaListPlayer()
mediaList = vlc.MediaList(List1)
player.set_media_list(mediaList)
player.set_playback_mode(vlc.PlaybackMode.loop)
player.play()

timer = False

cv1 = tk.Canvas(music, width = 600, height = 400, bg = "white")
cv1.pack(side = "left")

cvframe = tk.Frame(music)
cvframe.pack(side = "right")

cv5 = tk.Canvas(cvframe, width = 250, height = 290)
cv5.pack(side = "top")

cv2 = tk.Canvas(cvframe, width = 250, height = 100, bg = "#FFCAA2")
cv2.pack(side = "bottom")

cv3 = tk.Canvas(lyric, width = 600, height = 400)
cv3.pack(side = "left")

cv4 = tk.Canvas(lyric, width = 250, height = 400)
cv4.pack(side = "right")

cv6 = tk.Canvas(config, width = 850, height = 400, bg = "white")
cv6.pack(side = "left")

#########

try:
    img = Image.open(img_file)
except:
    img = Image.open(THIS_DIR_NAME+"/PlayerImage.jpg")
img = ImageTk.PhotoImage(img)
cv1.create_image(0, 0, image=img, anchor=tk.NW)

var1 = tk.StringVar()
var1.set(" ")
lab1 = tk.Label(
    cv1,
    textvariable=var1,
    font = ('HGS明朝E', 14),
    bg = img_color)
lab1.place(x=15,y=30)

#'Frank Ruhl Hofshi', 'HGS明朝E'

var2 = tk.StringVar()
var2.set(" ")
lab2 = tk.Label(
    cv1,
    textvariable=var2,
    font = ('', 20),
    bg = img_color)
lab2.place(x=15,y=70)

var3 = tk.StringVar()
var3.set(" ")
lab3 = tk.Label(
    cv2,
    textvariable=var3,
    font = ('', 17),
    bg = "#FFCAA2")
lab3.place(x=20,y=10)

var4 = tk.StringVar()
var4.set(" ")
lab4 = tk.Label(
    cv2,
    textvariable=var4,
    font = ('', 17),
    bg = "#FFCAA2")
lab4.place(x=20,y=40)

but1 = tk.Button(
    cv1,
    text = "◀",
    width = 3,
    height = 1,
    font = ("", 25),
    bg = "yellow",
    command = lambda:player.previous())
but1.place(x=40,y=320)

but2 = tk.Button(
    cv1,
    text = "||",
    width = 3,
    height = 1,
    font = ("", 25),
    bg = "yellow",
    command = lambda:player.pause())
but2.place(x=220,y=320)

but3 = tk.Button(
    cv1,
    text = "▶",
    width = 3,
    height = 1,
    font = ("", 25),
    bg = "yellow",
    command = lambda:player.next())
but3.place(x=400,y=320)

loop_bool = False
loop_num = None

but4 = tk.Button(
    cv1,
    text = "↻",
    width = 3,
    height = 1,
    font = ("", 25),
    bg = "yellow",
    command = loop)
but4.place(x=490,y=320)

p = player.get_media_player()

but5 = tk.Button(
    cv1,
    text = "◁",
    width = 3,
    height = 1,
    font = ("", 25),
    bg = "yellow",
    command = lambda:p.set_position(p.get_position()-0.05))
but5.place(x=130,y=320)

but6 = tk.Button(
    cv1,
    text = "▷",
    width = 3,
    height = 1,
    font = ("", 25),
    bg = "yellow",
    command = lambda:p.set_position(p.get_position()+0.05))
but6.place(x=310,y=320)

var5 = tk.StringVar(value=tuple(List2))
lsb1 = tk.Listbox(
    cv5,
    listvariable=var5,
    height=14,
    width = 29,
    selectmode = 'browse',
    bg = "#FBEAD6",
    font = ("メイリオ", 10))
lsb1.bind('<<ListboxSelect>>', listbox_selected1)
lsb1.pack(fill='y', side = "left")

scr1 = ttk.Scrollbar(
    cv5,
    orient=tk.VERTICAL, 
    command=lsb1.yview)
lsb1['yscrollcommand']=scr1.set
scr1.pack(fill='y', side = "right")

cop1=tk.Label(
    cv2,
    bg = "#FFCAA2",
    text='©2019 RyoFujinami.',
    font=("Gabriola", 12))
cop1.place(x=130,y=65)

########

fra1 = tk.Frame(cv4)
fra1.pack(side = "top")

var6 = tk.StringVar(value=tuple(List5))
lsb2 = tk.Listbox(
    fra1,
    listvariable=var6,
    height=16,
    width = 23,
    bg = "#FBEAD6",
    font = ("メイリオ", 12))
lsb2.bind('<<ListboxSelect>>', listbox_selected2)
lsb2.pack(side="left")

scr2 = ttk.Scrollbar(
    fra1,
    orient=tk.VERTICAL, 
    command=lsb2.yview)
lsb2['yscrollcommand']=scr2.set
scr2.pack(fill='y', side = "right")

txt1 = tk.Text(
    cv3,
    font=('', '16'),
    height=19,
    width = 53)
txt1.pack(side = "left")
txt1.configure(state=tk.DISABLED)

scr3 = ttk.Scrollbar(
    cv3,
    command=txt1.yview)
txt1.configure(yscrollcommand=scr3.set)
scr3.pack(fill='y', side = "right")

########

lab5 = tk.Label(
    cv6,
    text = "イメージカラー",
    font = ('', 20),
    bg = "#FFCAAA",
    width = 20)
lab5.place(x=60,y=40)

ent1 = tk.Entry(
    cv6,
    width = 12,
    bg = "#F4F8AA",
    font = ('', 20))
ent1.place(x=60,y=80)

lab6 = tk.Label(
    cv6,
    text = "⇚入力欄",
    bg = "white",
    font = ('', 12))
lab6.place(x=235,y=85)

but1 = tk.Button(
    cv6,
    text = "入力されたデータに変更する",
    width = 25,
    font = ("", 16),
    bg = "yellow",
    command = lambda: color_conv(ent1.get()))
but1.place(x=60,y=120)

but2 = tk.Button(
    cv6,
    text = "変更する色を選ぶ",
    width = 25,
    font = ("", 16),
    bg = "yellow",
    command = lambda: color_conv(colorchooser.askcolor()[1]))
but2.place(x=60,y=160)

but2 = tk.Button(
    cv6,
    text = "デフォルトに戻す",
    width = 25,
    font = ("", 16),
    bg = "yellow",
    command = lambda: color_conv("#F7D358"))
but2.place(x=60,y=200)

var5 = tk.StringVar()
var5.set("現在の色："+img_color)
lab5 = tk.Label(
    cv6,
    textvariable=var5,
    font = ('', 16),
    bg = "#FFCAAA",)
lab5.place(x=60,y=250)

lab7 = tk.Label(
    cv6,
    text = "タイマー",
    font = ('', 20),
    bg = "#FFCAAA",
    width = 20)
lab7.place(x=400,y=40)

ent2 = tk.Entry(
    cv6,
    width = 3,
    bg = "#F4F8AA",
    font = ('', 20))
ent2.place(x=400,y=80)

lab8 = tk.Label(
    cv6,
    text = "分後",
    font = ('', 18),
    bg = "#F4F8AA")
lab8.place(x=446,y=80)

lab9 = tk.Label(
    cv6,
    text = "⇚入力欄",
    bg = "white",
    font = ('', 12))
lab9.place(x=550,y=85)

but1 = tk.Button(
    cv6,
    text = "入力されたデータに変更する",
    width = 25,
    font = ("", 16),
    bg = "yellow",
    command = lambda: timer_conv(ent2.get()))
but1.place(x=400,y=120)

but2 = tk.Button(
    cv6,
    text = "タイマーを切る",
    width = 25,
    font = ("", 16),
    bg = "yellow",
    command = lambda: timer_conv(False))
but2.place(x=400,y=160)

var6 = tk.StringVar()
var6.set("設定されていません")
lab6 = tk.Label(
    cv6,
    textvariable=var6,
    font = ('', 16),
    bg = "#FFCAAA",)
lab6.place(x=400,y=210)

########

def save():
    if not OE:
        try:
            with open(MainFile+"/data.pickle", "rb") as file:
                data = pickle.load(file)
        except:
            data = {}
        with open(MainFile+"/data.pickle", "wb") as file:
            p = player.get_media_player()
            media_instance = p.get_media()
            index = mediaList.index_of_item(media_instance)
            name = List2[index]
            position = p.get_position()
            data["name"] = name
            data["position"] = position
            pickle.dump(data, file)

def gameloop():
    try:
        if not timer:
            pass
        else:
            now = datetime.now().replace(microsecond=0)
            if timer == now:
                root.destroy()
                root.mainloop()
        p = player.get_media_player()
        media_instance = p.get_media()
        index = mediaList.index_of_item(media_instance)
        file = List2[index]
        percent = int(p.get_position() * 100)
        if loop_bool == True:
            if index != loop_num:
                while True:
                    player.previous()
                    media_index = mediaList.index_of_item(p.get_media())
                    if loop_num == media_index:
                        break
        var1.set(str(file))
        var2.set(str(index+1)+" / "+str(len(List1))+" 曲")
        var3.set("進行度 : "+str(percent)+" %")
        var4.set("ループ : "+str(loop_bool))
        root.after(50, gameloop) 
    except:
        print(traceback.format_exc())
        var1.set("Error")
        var2.set("Error")
        var3.set("Error")

play()
gameloop()
root.mainloop()
save()
player.stop()


