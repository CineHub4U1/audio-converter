import os
import imdb
import requests

from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler

load_dotenv()

TOKEN = os.getenv('TOKEN')

ia = imdb.IMDb()

def imdb_search(update, context):
    query = ' '.join(context.args)
    movies = ia.search_movie(query)
    if not movies:
        context.bot.send_message(chat_id=update.effective_chat.id, text='No movies found :(')
        return
    movie = ia.get_movie(movies[0].getID())

    # Get poster image
    if 'cover url' in movie:
        image_url = movie['cover url']
        response = requests.get(image_url)
        with open('poster.jpg', 'wb') as f:
            f.write(response.content)

    message = f"*Title:* {movie.get('title', 'N/A')}\n"
    message += f"*Year:* {movie.get('year', 'N/A')}\n"
    message += f"*Genres:* {', '.join(movie.get('genres', ['N/A']))}\n"
    message += f"*IMDb URL:* https://www.imdb.com/title/{movie.getID()}\n"
    message += f"*Country:* {', '.join(movie.get('country', ['N/A']))}\n"
    message += f"*Languages:* {', '.join(movie.get('languages', ['N/A']))}\n"
    message += f"*Quality:* \n"
    message += f"*Subtitles:* \n"
    message += f"\n{movie.get('plot outline', 'N/A')}"

    # Send message with poster image
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('poster.jpg', 'rb'))
    context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode='Markdown')

    # Remove poster image
    os.remove('poster.jpg')

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Welcome to IMDb Search Bot!')

if __name__ == '__main__':
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('imdb', imdb_search))
    updater.start_polling()
    print('Bot is running...')
    updater.idle()
