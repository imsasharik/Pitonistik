import logging
from io import BytesIO
from pathlib import Path
from typing import List, Dict

import pandas as pd
import telebot
from telebot.types import Message
from windrose import WindroseAxes
import matplotlib.pyplot as plt

BOT_TOKEN = '8135578984:AAGelc2RM-Nf8TYknJX_6ah_3c87amG5q7c'
bot = telebot.TeleBot(BOT_TOKEN)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def convert_rumb_to_degrees(rumb: str) -> float:
    """ Конвертирует название румба в градусы """
    directions = {'С': 0, 'ССВ': 22.5, 'СВ': 45, 'ВСВ': 67.5, 'В': 90, 'ВЮВ': 112.5, 'ЮВ': 135, 'ЮЮВ': 157.5,
                  'Ю': 180, 'ЮЮЗ': 202.5, 'ЮЗ': 225, 'ЗЮЗ': 247.5, 'З': 270, 'ЗСЗ': 292.5, 'СЗ': 315, 'ССЗ': 337.5}
    return directions[rumb.strip()]


@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    logger.info(f"User {message.chat.id} started the bot")
    bot.send_message(message.chat.id, "Привет! Отправь мне CSV-файл с данными о ветре.")


@bot.message_handler(content_types=["document"])
def handle_csv_file(message: Message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        df = pd.read_csv(BytesIO(downloaded_file), encoding='utf-8', sep=';', decimal=',',
                         parse_dates={'datetime': ['YY', 'MM', 'DD', 'hh']}, index_col='datetime')

        df['DD'] = df['DD'].apply(convert_rumb_to_degrees)

        wind_speed = df['Ff']
        wind_direction = df['DD']

        ax = WindroseAxes.from_ax()
        ax.bar(wind_direction, wind_speed, normed=True, opening=0.8, edgecolor='white')
        plt.title('Роза ветров')
        img_buf = BytesIO()
        plt.savefig(img_buf, format='png')
        img_buf.seek(0)

        bot.send_photo(message.chat.id, photo=img_buf)
        logger.info(f"Rose plot sent to user {message.chat.id}.")
    except Exception as ex:
        logger.error(f"Error processing file from user {message.chat.id}: {ex}")
        bot.send_message(message.chat.id, "Ошибка обработки файла. Попробуйте отправить другой файл.")


if __name__ == "__main__":
    bot.polling()