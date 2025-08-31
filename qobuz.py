import os
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from subprocess import run, PIPE

BOT_TOKEN = '8424803386:AAGnit2whwd1HRVZkm7kOWCSAb56sHEUUSo'
DOWNLOAD_FOLDER = os.path.expanduser('~/QobuzDownloads')
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def is_valid_qobuz_url(url):
    pattern = r'https?://(open\.)?qobuz\.com/.+'
    return re.match(pattern, url) is not None

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please provide a Qobuz track or album URL after the command.")
        return

    url = context.args[0]
    if not is_valid_qobuz_url(url):
        await update.message.reply_text("Invalid Qobuz URL format. Please send a correct link.")
        return

    await update.message.reply_text("Starting download...")

    # Remove old FLAC files to avoid confusion
    for old_file in os.listdir(DOWNLOAD_FOLDER):
        if old_file.endswith('.flac'):
            os.remove(os.path.join(DOWNLOAD_FOLDER, old_file))

    # Download song/album in Hi-Res FLAC quality
    cmd = ['qobuz-dl', 'dl', url, '-q', '27', '-d', DOWNLOAD_FOLDER]
    process = run(cmd, stdout=PIPE, stderr=PIPE, text=True)

    if process.returncode == 0:
        # Find newest .flac file in download folder (sent to user)
        files = sorted(
            [f for f in os.listdir(DOWNLOAD_FOLDER) if f.endswith('.flac')],
            key=lambda x: os.path.getmtime(os.path.join(DOWNLOAD_FOLDER, x)),
            reverse=True
        )
        if files:
            file_path = os.path.join(DOWNLOAD_FOLDER, files[0])
            await update.message.reply_text("Download successful! Sending your song file...")

            with open(file_path, 'rb') as music_file:
                await update.message.reply_audio(music_file)
        else:
            await update.message.reply_text("Download successful, but couldn't find the song file to send.")
    else:
        await update.message.reply_text("Download failed!")

def main():
    print("Bot is starting...")  # This prints to the console!
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("download", download))
    application.run_polling()

if __name__ == '__main__':
    main()
__':
    main()
