import uuid
from os import listdir
from os.path import isfile, join
from telebot import TeleBot
from telebot.types import Message
import os

TOKEN = '7155005136:AAHJJL0XXzT0ovudTRFdAg8ucUZxk-5eBws'

bot = TeleBot(TOKEN)


@bot.message_handler(content_types=['photo'])
def photo(message: Message) -> None:
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    path = f'photos/{message.from_user.username}/'
    if not os.path.isdir(path):
        os.mkdir(path)

    file_path = os.path.join(path, f"{str(uuid.uuid4())}.jpg")
    # with open(file_path, 'wb') as file:
    #     file.write(downloaded_file)


    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    print(onlyfiles)
    # s3.upload_file(
    #     Filename=file_info.file_path,
    #     Bucket=bucket_name,
    #     Key=file_info.file_path
    # )
    #
    # photo_file.download(file_path)

    print(len(message.photo))
    print(message.media_group_id)





if __name__ == '__main__':
    bot.polling(none_stop=True)
