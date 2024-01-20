from langchain_community.llms import HuggingFaceHub
from langchain.chains import LLMChain
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from typing import Final
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os

# 从.env文件加载环境变量
load_dotenv()

TOKEN: Final = os.getenv("TOKEN")
BOT_USERNAME: Final = os.getenv("BOT_USERNAME")
MODEL_REPO_ID: Final = os.getenv("MODEL_REPO_ID")
TEMPERATURE: Final = float(os.getenv("TEMPERATURE", 0.7))
MAX_LENGTH: Final = int(os.getenv("MAX_LENGTH", 500))

# 确保TOKEN、BOT_USERNAME和MODEL_REPO_ID在.env文件中被定义
if TOKEN is None or BOT_USERNAME is None or MODEL_REPO_ID is None:
    raise ValueError("TOKEN、BOT_USERNAME和MODEL_REPO_ID必须在.env文件中定义.")

# 在handle_responses函数之外初始化HuggingFaceHub
hub_llm = HuggingFaceHub(
    repo_id=MODEL_REPO_ID,
    model_kwargs={"temperature": TEMPERATURE, "max_length": MAX_LENGTH},
)

prompt = PromptTemplate(
    input_variables=["question"],
    template="{question}?"
)

hub_chain = LLMChain(prompt=prompt, llm=hub_llm)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('你好，目前我只能回答问题。你有什么问题吗？')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    if message_type == 'group' and BOT_USERNAME in text:
        new_text: str = text.replace(BOT_USERNAME, '').strip()
    else:
        new_text = text

    # 发送“正在输入”动作
    await context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)

    response: str = hub_chain.invoke(new_text)

    print(f'用户({update.message.chat.id})在{message_type}中: "{text}"')
    print('机器人:', response)

    # 移除“正在输入”动作并发送响应
    await context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'更新{update}引发了错误{context.error}')

if __name__ == '__main__':
    print('启动机器人...')
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_error_handler(error)

    print('轮询中...')
    app.run_polling(poll_interval=3)
