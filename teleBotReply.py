import os
from telegram import ForceReply, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import threading

# thread를 이용하지 않으면 선행 스크립트가 무한 루프라서 돌아오지 않음
def runCoinData():
    os.system("readCoinData.py")

thread_1 = threading.Thread(target = runCoinData)
thread_1.start()

def runCoinAlarm():
    os.system("teleBotTime.py")

thread_2 = threading.Thread(target = runCoinAlarm)
thread_2.start()


def readData():
    with open("btc.txt", "r") as f:
        return f.read()

token = "6649818604:AAFDSXZgaCpEosbuKyIiZk6inAI_PsdyNXg" 
chat_id = "-4130705553"

helpList = """
/c : 코인선물 현재가
"""


# 몇 가지 명령 핸들러를 정의합니다. 일반적으로 업데이트와 컨텍스트의 두 인수를 받습니다.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/start 명령이 실행되면 메시지를 보냅니다."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )
 
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """도움말 명령이 실행되면 메시지를 보냅니다."""
    await update.message.reply_text(helpList)

async def coinPrice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(str(readData()))
 
##async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
##    """사용자 메시지를 에코합니다."""
##    await update.message.reply_text(update.message.text)
 
# 애플리케이션을 생성하고 봇의 토큰을 전달합니다.
app = ApplicationBuilder().token(token).build()
 
# 다른 명령에 대해 - 텔레그램으로 답변하기
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("c", coinPrice))
 
# 텔레그램에서 메시지를 에코합니다.
##app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
 
# 사용자가 Ctrl-C를 누를 때까지 봇을 실행합니다.
app.run_polling()
