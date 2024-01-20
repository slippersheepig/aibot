from langchain import HuggingFaceHub, LLMChain
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from typing import Final
from telegram import Update, ChatAction
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os

# Load environment variables from .env file
load_dotenv()

TOKEN: Final = os.getenv("TOKEN")
BOT_USERNAME: Final = os.getenv("BOT_USERNAME")
MODEL_REPO_ID: Final = os.getenv("MODEL_REPO_ID")

# Ensure that TOKEN, BOT_USERNAME, and MODEL_REPO_ID are defined in the .env file
if TOKEN is None or BOT_USERNAME is None or MODEL_REPO_ID is None:
    raise ValueError("TOKEN, BOT_USERNAME, and MODEL_REPO_ID must be defined in the .env file.")

# Initialize HuggingFaceHub outside the handle_responses function
hub_llm = HuggingFaceHub(
    repo_id=MODEL_REPO_ID,
    model_kwargs={"temperature": 0.7, "max_length": 8000},
)

prompt = PromptTemplate(
    input_variables=["question"],
    template="You are a helpful assistant. {question}?"
)

hub_chain = LLMChain(prompt=prompt, llm=hub_llm)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello, at the moment I can only answer questions. What is your question?')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    if message_type == 'group' and BOT_USERNAME in text:
        new_text: str = text.replace(BOT_USERNAME, '').strip()
    else:
        new_text = text

    # Send "typing" action
    await context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)

    response: str = hub_chain.run(new_text)

    print(f'User({update.message.chat.id}) in {message_type}: "{text}"')
    print('bot:', response)

    # Remove "typing" action and send the response
    await context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update{update} caused error {context.error}')

if __name__ == '__main__':
    print('Starting Bot...')
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_error_handler(error)

    print('Polling...')
    app.run_polling(poll_interval=3)
