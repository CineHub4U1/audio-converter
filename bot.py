from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from pydub import AudioSegment
import os

# set the default output format, bitrate, and channels
output_format = 'mp3'
bitrate = '128k'
channels = 2

def convert_audio(update, context):
    # get the audio file from the message
    audio_file = context.bot.getFile(update.message.audio.file_id)

    # download the audio file and save it to disk
    audio_path = os.path.join(os.getcwd(), audio_file.file_path)
    audio_file.download(audio_path)

    # load the audio file using pydub
    audio = AudioSegment.from_file(audio_path)

    # construct the output filename
    output_filename = os.path.splitext(audio_file.file_path)[0] + '.' + output_format

    # set the output options
    output_options = {
        'format': output_format,
        'bitrate': bitrate,
        'channels': channels
    }

    # save the audio file in the desired format
    audio.export(output_filename, **output_options)

    # send the converted audio file back to the user
    context.bot.send_audio(chat_id=update.message.chat_id, audio=open(output_filename, 'rb'))

    # delete the downloaded audio file and the converted audio file from disk
    os.remove(audio_path)
    os.remove(output_filename)

def settings(update, context):
    # get the new settings from the message
    settings = update.message.text.split()[1:]

    # update the output format, bitrate, and channels
    global output_format, bitrate, channels
    if settings:
        output_format = settings[0]
        if len(settings) > 1:
            bitrate = settings[1]
        if len(settings) > 2:
            channels = int(settings[2])

    # send a message back to the user confirming the new settings
    message = f"Output format: {output_format}\nBitrate: {bitrate}\nChannels: {channels}"
    context.bot.send_message(chat_id=update.message.chat_id, text=message)

def main():
    # create an Updater object and attach it to the bot's API token
    updater = Updater('5782051762:AAHt6pMRSorbcipQZggT604rI0hGNKJU5Ic')

    # create a MessageHandler that will handle audio messages
    audio_handler = MessageHandler(Filters.audio, convert_audio)

    # register the MessageHandler with the Updater
    updater.dispatcher.add_handler(audio_handler)

    # create a CommandHandler that will handle the /settings command
    settings_handler = CommandHandler('settings', settings)

    # register the CommandHandler with the Updater
    updater.dispatcher.add_handler(settings_handler)

    # start the bot
    updater.start_polling()

    # run the bot until you press Ctrl-C to stop it
    updater.idle()

if __name__ == '__main__':
    main()
