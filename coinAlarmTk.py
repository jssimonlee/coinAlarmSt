import tkinter.ttk as ttk
from tkinter import * 
import time
import threading
import json
from websocket import WebSocketApp
import asyncio
import telegram

root = Tk()
root.title("Coin Alarm")

curVal = 0  # 현재가 저장
killws = False  # socket 스트리밍을 먼저 죽이지 않으면 다음 실행시 두개가 실행되고, 종료도 안된다.
# thread를 이용하지 않으면 선행 스크립트가 무한 루프라서 돌아오지 않음
def runCoinData():
    txtTicker = txt_ticker.get()
    if len(txtTicker) == 0:
        ticker = 'btcusdt@kline_1m'
    else:
        ticker = txtTicker.lower().replace("usdt","") + "usdt@kline_1m"
    # monitor_print(f"{ticker.replace('@kline_1m','')} 현재가")
    
    def on_message(ws,message):
        message = json.loads(message)
        manipulation(message,ws)

    # socket = "wss://stream.binance.com:9443/stream?streams="+assets
    socket = "wss://fstream.binance.com/stream?streams="+ticker

    def manipulation(source,ws):
        global killws
        global curVal
        if killws:
            ws.close()
        now = time
        rel_data = source["data"]['k']['c']
        curTime = f"{format(now.localtime().tm_hour,'02')}:{format(now.localtime().tm_min,'02')}:{format(now.localtime().tm_sec,'02')}"
        monitor_print(f"[{curTime}] : {rel_data}")
        curVal = rel_data

    ws = WebSocketApp(socket, on_message=on_message)
    ws.run_forever()

def sendToTelegram():
    prevData = 0
    uboveValue = txt_high.get().split(',')
    belowValue = txt_low.get().split(',')

    # def readData(): # 데이터가 있는 파일 읽어오기
    #     with open("btc.txt", "r") as f:
    #         return f.read()

    def is_any_greater(a, lst): # 고점 값보다 큰지 비교해서 return
        for value in lst:
            if float(a) >= float(value):
                lst.remove(value)
                return float(value)
        return False

    def is_any_lower(a, lst):   # 저점 값보다 작은지 비교해서 return
        for value in lst:
            if float(a) <= float(value):
                lst.remove(value)
                return float(value)
        return False

    async def send_daily_message(): # main routine
        global prevData
        global curVal
        rel_data = curVal
        token = "6649818604:AAFDSXZgaCpEosbuKyIiZk6inAI_PsdyNXg" 
        chat_id = "-4130705553"
        bot = telegram.Bot(token = token)

        message = str(rel_data)
        # print(message)
        # diff = float(rel_data) - float(prevData)
        # print(diff)
        # if diff > 100 and float(prevData) > 0:
        #     print("100불이상 급등")
        #     await bot.send_message(chat_id,message + "(" + str(prevData) + "): $100 Up")
        # elif diff < -100:
        #     print("100불이상 급낙")
        #     await bot.send_message(chat_id,message + "(" + str(prevData) + "): $100 Down")
        upSignal = is_any_greater(rel_data,txt_high.get().split(','))
        lowSignal = is_any_lower(rel_data,txt_low.get().split(','))
        if upSignal > 0:
            print("고점 도달 : " + str(upSignal))
            await bot.send_message(chat_id,message + " 고점 도달 : " + str(upSignal))
        if lowSignal > 0:
            print("저점 도달 : " + str(lowSignal))
            await bot.send_message(chat_id,message + " 저점 도달 : " + str(lowSignal))
        prevData = rel_data

    async def main():
        while True:
            await send_daily_message()
            await asyncio.sleep(1) # 24시간 대기
    asyncio.run(main())

def start():
    global killws
    if len(txt_ticker.get()) == 0:
        monitor_print("BTCUSDT 현재가")
    else:
        monitor_print(f"{txt_ticker.get().upper()} 현재가")
    # patch coin Price from runCoinData.py
    # 이전 실행중인 소켓이 있을 경우를 대비하여 먼저 소켓을 죽이고 다시 시작
    killws = True
    time.sleep(2)
    killws = False

    thread_1 = threading.Thread(target = runCoinData)
    thread_1.start()

    thread_2 = threading.Thread(target = sendToTelegram)
    thread_2.start()


def monitor_print(ins_String,fgcolor="Yellow"):
    list_monitor.insert(END,ins_String)
    list_monitor.see("end")
    list_monitor.itemconfig(END, foreground=fgcolor)

def signal_print(ins_String,fgcolor="Yellow"):
    tele_monitor.insert(END,ins_String)
    tele_monitor.see("end")
    tele_monitor.itemconfig(END, foreground=fgcolor)

def highSignal():
    signal_print("High CK: " + str(highVar.get()))

def lowSignal():
    signal_print("Low CK: " + str(lowVar.get()))

def fiveLongSignal():
    signal_print("FiveLong CK: " + str(fiveLongVar.get()))

def fiveShortSignal():
    signal_print("FiveShort CK: " + str(fiveShortVar.get()))

def shootSignal():
    signal_print("급등 CK: " + str(shootVar.get()))

def dropSignal():
    signal_print("급낙 CK: " + str(dropVar.get()))

def stopProgram():
    global killws
    global root
    killws = True
    root.quit()

# 저장 경로 프레임
setUp = LabelFrame(root, text="설정")
setUp.pack(side="left",fill="x", padx=5, pady=5, ipady=5)

# Ticker 설정
ticker_frame = LabelFrame(setUp, text="Ticker")
ticker_frame.pack(side = "top", fill="x", padx=5, pady=5, ipady=5)

txt_ticker = Entry(ticker_frame)
txt_ticker.pack(side="top", fill="x", expand=True, padx=5, pady=5, ipady=4) 

# 고점 설정
high_frame = LabelFrame(setUp, text='고점신호(","로 여러개 설정)')
high_frame.pack(side = "top", fill="x", padx=5, pady=5, ipady=5)

highVar=IntVar()
ckHigh=Checkbutton(high_frame,text="",variable=highVar, command=highSignal)
ckHigh.pack(side="left")

txt_high = Entry(high_frame)
txt_high.pack(side="left", fill="x", expand=True, padx=5, pady=5, ipady=4) 

# 저점 설정
low_frame = LabelFrame(setUp, text='저점신호(","로 여러개 설정)')
low_frame.pack(side = "top", fill="x", padx=5, pady=5, ipady=5)

lowVar=IntVar()
ckLow=Checkbutton(low_frame,text="",variable=lowVar, command=lowSignal)
ckLow.pack(side="left")

txt_low = Entry(low_frame)
txt_low.pack(side="left", fill="x", expand=True, padx=5, pady=5, ipady=4) 

# 5분3틱 Long 설정
fiveLong_frame = LabelFrame(setUp, text='5분 3틱 Long 설정')
fiveLong_frame.pack(side = "top", fill="x", padx=5, pady=5, ipady=5)

fiveLongVar=IntVar()
ckfiveLong=Checkbutton(fiveLong_frame,text="",variable=fiveLongVar, command=fiveLongSignal)
ckfiveLong.pack(side="left")

txt_fiveLong = Entry(fiveLong_frame)
txt_fiveLong.pack(side="left", fill="x", expand=True, padx=5, pady=5, ipady=4) 

# 5분3틱 Short 설정
fiveShort_frame = LabelFrame(setUp, text='5분 3틱 Short 설정')
fiveShort_frame.pack(side = "top", fill="x", padx=5, pady=5, ipady=5)

fiveShortVar=IntVar()
ckfiveShort=Checkbutton(fiveShort_frame,text="",variable=fiveShortVar, command=fiveShortSignal)
ckfiveShort.pack(side="left")

txt_fiveLong = Entry(fiveShort_frame)
txt_fiveLong.pack(side="left", fill="x", expand=True, padx=5, pady=5, ipady=4) 

timeOption = [1,3,5,10,20,30,45,60]
# 급등1 설정
shoot_frame = LabelFrame(setUp, text='급등 설정')
shoot_frame.pack(side = "top", fill="x", padx=5, pady=5, ipady=5)

shootVar=IntVar()
ckshoot=Checkbutton(shoot_frame,text="",variable=shootVar, command=shootSignal)
ckshoot.pack(side="left")

shootOpVar = StringVar(root)
shootOpVar.set(timeOption[0])
opt = OptionMenu(shoot_frame, shootOpVar, *timeOption)
opt.config(width=8,font=("Helvetica", 10))
opt.pack(side="left")

txt_shoot = Entry(shoot_frame)
txt_shoot.pack(side="left", fill="x", expand=True, padx=5, pady=5, ipady=4) 

# 급낙 설정
drop_frame = LabelFrame(setUp, text='급낙 설정')
drop_frame.pack(side = "top", fill="x", padx=5, pady=5, ipady=5)

dropVar=IntVar()
ckdrop=Checkbutton(drop_frame,text="",variable=dropVar, command=dropSignal)
ckdrop.pack(side="left")

dropOpVar = StringVar(root)
dropOpVar.set(timeOption[0])
opt = OptionMenu(drop_frame, dropOpVar, *timeOption)
opt.config(width=8,font=("Helvetica", 10))
opt.pack(side="left")

txt_drop = Entry(drop_frame)
txt_drop.pack(side="left", fill="x", expand=True, padx=5, pady=5, ipady=4) 

# monitor Frame
monitor_frame = Frame(root)
monitor_frame.pack(side="right", fill="x", padx=5, pady=5)

# 리스트 프레임
list_frame = LabelFrame(monitor_frame, text="현재가")
list_frame.pack(side="top", fill="x", padx=5, pady=5)

scrollbar = Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")

list_monitor = Listbox(list_frame, selectmode="extended", height=15,  background="Black", fg="Yellow", yscrollcommand=scrollbar.set, font=('Malgun Gothic', 13))
list_monitor.config(width=30,height=11)
list_monitor.pack(side="right", fill="both", expand=True)
scrollbar.config(command=list_monitor.yview)

# telegram 프레임
tele_frame = LabelFrame(monitor_frame, text="Signal 전송")
tele_frame.pack(side="top", fill="x", padx=5, pady=5)

scrollbar = Scrollbar(tele_frame)
scrollbar.pack(side="right", fill="y")

tele_monitor = Listbox(tele_frame, selectmode="extended", height=15,  background="Black", fg="Yellow", yscrollcommand=scrollbar.set, font=('Malgun Gothic', 13))
tele_monitor.config(width=30,height=12)
tele_monitor.pack(side="right", fill="both", expand=True)
scrollbar.config(command=list_monitor.yview)

# 실행 프레임
frame_run = Frame(setUp)
frame_run.pack(side="bottom", fill="x", padx=5, pady=5)

btn_close = Button(frame_run, padx=5, pady=5, text="종료", width=12, command=stopProgram)
btn_close.pack(side="right", padx=5, pady=5)

btn_start = Button(frame_run, padx=5, pady=5, text="시작", width=12, command=start)
btn_start.pack(side="right", padx=5, pady=5)

root.resizable(False, False)

root.mainloop()
