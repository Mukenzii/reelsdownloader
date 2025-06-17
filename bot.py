import glob
import os
import uuid
import shutil
from dotenv import load_dotenv
from telebot import TeleBot
from telebot.types import Message
import instaloader

load_dotenv()

TOKEN = os.getenv('TOKEN')
ADMIN = os.getenv("ADMIN")


bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def reaction_start(message: Message):
    chat_id = message.chat.id
    first_name = message.from_user.full_name
    username = message.from_user.username
    bot.send_message(chat_id, "Yo guy! Salom. Instadan reels download qib beraman. Linkni tashang!")

    bot.send_message(ADMIN, f'New user in da house {chat_id},\nName: {first_name},\nUsername: {username}')


@bot.message_handler(func=lambda message: 'instagram.com/reel/' in message.text)
def download_reel(message: Message):
    chat_id = message.chat.id
    shortcode = message.text.split("/reel/")[1].split("/")[0]
    bot.send_message(chat_id, 'Video yuklanmoqda...')
    try:
        folder = f'reels_{uuid.uuid4().hex}'
        os.makedirs(folder)

        loader = instaloader.Instaloader(dirname_pattern=folder)
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        loader.download_post(post, target='reels')

        video_files = glob.glob(f"{folder}/*.mp4")
        with open(video_files[0], 'rb') as video:
            file_size = os.path.getsize(video_files[0])
            if file_size > 49 * 1024 * 1024:
                bot.send_document(chat_id, video)
            else:
                bot.send_video(chat_id, video)

        shutil.rmtree(folder, ignore_errors=True)

    except:
        bot.send_message(chat_id, "Xatolik berdi, videoni yuklab bo'lmadi! Urlni tekshiring")


if __name__ == '__main__':
    bot.infinity_polling()
