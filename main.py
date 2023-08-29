import moviepy.editor
from config import tg_bot_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


bot: Bot = Bot(token=tg_bot_token)
dp: Dispatcher = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer('Привет! Пришли мне видеофайл в ".mp4", я пришлю тебе ответ в виде ".mp3"!')


@dp.message_handler(content_types='video')
async def get_audio(message: types.Message, file_name="video.mp4"):
    print('Complete one!')
    try:
        chat_id = message.chat.id
        file_id = message.video.file_id  # Get file id
        file = await bot.get_file(file_id)  # Get file path
        await bot.download_file(file.file_path, file_name)  # Download video and save output in file "video.mp4"

        video = moviepy.editor.VideoFileClip(file_name)
        audio = video.audio
        str_file_name = str(file_name)[:-4]
        audio.write_audiofile(f'{str_file_name}.mp3')

        audio = open(f'{str_file_name}.mp3', 'rb')
        await bot.send_audio(chat_id, audio)
        print('Complete!')
    except Exception as ex:
        print(ex)
        await message.answer("Вы отправили не видео!")


if __name__ == "__main__":
    executor.start_polling(dp)
