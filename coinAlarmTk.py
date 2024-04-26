import tkinter.ttk as ttk
from tkinter import * 
import time
import threading

root = Tk()
root.title("Coin Alarm")

def start():
    # if len(txt_start.get()) == 0:
    #     monitor_print("시작번호를 넣으세요")
    #     return
    tmain = threading.Thread(target=mainFunc)
    tmain.start()

def monitor_print(ins_String,fgcolor="Yellow"):
    list_monitor.insert(END,ins_String)
    list_monitor.see("end")
    list_monitor.itemconfig(END, foreground=fgcolor)

def signal_print(ins_String,fgcolor="Yellow"):
    tele_monitor.insert(END,ins_String)
    tele_monitor.see("end")
    tele_monitor.itemconfig(END, foreground=fgcolor)

def mainFunc():
    while(True):
        now = time
        curTime = f"{format(now.localtime().tm_hour,'02')}:{format(now.localtime().tm_min,'02')}:{format(now.localtime().tm_sec,'02')}"
        data = readData()
        monitor_print(f"[{curTime}] : {data}")
        if float(data) > float(txt_high.get()):
            signal_print(data)
            signal_print(txt_high.get())
            signal_print("급등신호발생")
        time.sleep(2)
    monitor_print("전체작업 완료","Red")

def readData(): # 데이터가 있는 파일 읽어오기
    with open("btc.txt", "r") as f:
        return f.read()

def highSignal():
    monitor_print("High CK: " + str(highVar.get()))

def lowSignal():
    monitor_print("Low CK: " + str(lowVar.get()))

def fiveLongSignal():
    monitor_print("FiveLong CK: " + str(fiveLongVar.get()))

def fiveShortSignal():
    monitor_print("FiveShort CK: " + str(fiveShortVar.get()))

def shoot1Signal():
    monitor_print("급등1 CK: " + str(shoot1Var.get()))

def shoot2Signal():
    monitor_print("급등2 CK: " + str(shoot2Var.get()))
    
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
shoot1_frame = LabelFrame(setUp, text='급등1 설정')
shoot1_frame.pack(side = "top", fill="x", padx=5, pady=5, ipady=5)

shoot1Var=IntVar()
ckshoot1=Checkbutton(shoot1_frame,text="",variable=shoot1Var, command=shoot1Signal)
ckshoot1.pack(side="left")

shoot1OpVar = StringVar(root)
shoot1OpVar.set(timeOption[0])
opt = OptionMenu(shoot1_frame, shoot1OpVar, *timeOption)
opt.config(width=8,font=("Helvetica", 10))
opt.pack(side="left")

txt_shoot1 = Entry(shoot1_frame)
txt_shoot1.pack(side="left", fill="x", expand=True, padx=5, pady=5, ipady=4) 

# 급등2 설정
shoot2_frame = LabelFrame(setUp, text='급등2 설정')
shoot2_frame.pack(side = "top", fill="x", padx=5, pady=5, ipady=5)

shoot2Var=IntVar()
ckshoot2=Checkbutton(shoot2_frame,text="",variable=shoot2Var, command=shoot2Signal)
ckshoot2.pack(side="left")

shoot2OpVar = StringVar(root)
shoot2OpVar.set(timeOption[0])
opt = OptionMenu(shoot2_frame, shoot2OpVar, *timeOption)
opt.config(width=8,font=("Helvetica", 10))
opt.pack(side="left")

txt_shoot1 = Entry(shoot2_frame)
txt_shoot1.pack(side="left", fill="x", expand=True, padx=5, pady=5, ipady=4) 

# monitor Frame
monitor_frame = Frame(root)
monitor_frame.pack(side="right", fill="x", padx=5, pady=5)

# 리스트 프레임
list_frame = LabelFrame(monitor_frame, text="현재가")
list_frame.pack(side="top", fill="x", padx=5, pady=5)

scrollbar = Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")

list_monitor = Listbox(list_frame, selectmode="extended", height=15,  background="Black", fg="Yellow", yscrollcommand=scrollbar.set)
list_monitor.config(width=30,height=17)
list_monitor.pack(side="right", fill="both", expand=True)
scrollbar.config(command=list_monitor.yview)

# telegram 프레임
tele_frame = LabelFrame(monitor_frame, text="Signal 전송")
tele_frame.pack(side="top", fill="x", padx=5, pady=5)

scrollbar = Scrollbar(tele_frame)
scrollbar.pack(side="right", fill="y")

tele_monitor = Listbox(tele_frame, selectmode="extended", height=15,  background="Black", fg="Yellow", yscrollcommand=scrollbar.set)
tele_monitor.config(width=30,height=18)
tele_monitor.pack(side="right", fill="both", expand=True)
scrollbar.config(command=list_monitor.yview)

# 실행 프레임
frame_run = Frame(setUp)
frame_run.pack(side="bottom", fill="x", padx=5, pady=5)

btn_close = Button(frame_run, padx=5, pady=5, text="종료", width=12, command=root.quit)
btn_close.pack(side="right", padx=5, pady=5)

btn_start = Button(frame_run, padx=5, pady=5, text="시작", width=12, command=start)
btn_start.pack(side="right", padx=5, pady=5)

root.resizable(False, False)

monitor_print("대출권수와 수령날자는 자동으로 입력)","White")
root.mainloop()