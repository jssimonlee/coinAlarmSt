import asyncio
import telegram
##import socket


prevData = 0

# def readData():
#     fp = open("shared.pkl")
#     shared = pickle.load(fp)
#     return shared["coinPrice"]

uboveValue = [67000]
belowValue = [66380]


def readData(): # 데이터가 있는 파일 읽어오기
    with open("btc.txt", "r") as f:
        return f.read()

##def readData():
##    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
##    s.bind(("localhost", 12345))
##    s.listen(1)
##    conn, addr = s.accept()
##    data = conn.recv(1024)
##    print(data.decode())
##    conn.close()
##    return data.decode()

def is_any_greater(a, lst): # 고점 값보다 큰지 비교해서 return
    for value in lst:
        if float(a) >= value:
            lst.remove(value)
            return value
    return False

def is_any_lower(a, lst):   # 저점 값보다 작은지 비교해서 return
    for value in lst:
        if float(a) <= value:
            lst.remove(value)
            return value
    return False

async def send_daily_message(): # main routine
    global prevData
    rel_data = readData()
    token = "6649818604:AAFDSXZgaCpEosbuKyIiZk6inAI_PsdyNXg" 
    chat_id = "-4130705553"
    bot = telegram.Bot(token = token)

    message = str(rel_data)
    print(message)
    diff = float(rel_data) - float(prevData)
    print(diff)
    if diff > 100 and float(prevData) > 0:
        print("100불이상 급등")
        await bot.send_message(chat_id,message + "(" + str(prevData) + "): $100 Up")
    elif diff < -100:
        print("100불이상 급낙")
        await bot.send_message(chat_id,message + "(" + str(prevData) + "): $100 Down")
    upSignal = is_any_greater(rel_data,uboveValue)
    lowSignal = is_any_lower(rel_data,belowValue)
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

if __name__ == "__main__":
    asyncio.run(main())
