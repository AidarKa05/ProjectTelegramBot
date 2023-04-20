import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup as BS
import config
from parsing import get_info
from db import db_add_user


bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('static/welcome.tgs', 'rb')
    bot.send_sticker(message.chat.id, sti)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Новости")
    item2 = types.KeyboardButton("Игры")
    item3 = types.KeyboardButton("Киберспорт")
    item4 = types.KeyboardButton("Кино")
    item5 = types.KeyboardButton("Технологии")
    item6 = types.KeyboardButton("Скидки")

    markup.add(item1, item2, item3, item4, item5, item6)

    bot.send_message(message.chat.id,
                     f"Добро пожаловать, {message.from_user.first_name}!\n"
                     f"Здесь собраны актуальные новости об играх, фильмах и сериалах, современных технологиях и киберспорте.",
                     parse_mode='html', reply_markup=markup)

    us_id = message.from_user.id
    user_name = message.from_user.username

    db_add_user(user_id=us_id, user_name=user_name)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Игровые новости - последние новости об играх на ПК, PS4, Xbox X, Android, iOS.\n'
                                      '------------------------------------------------------------------------\n'
                                      'Киберспорт - новости, киберспортивные турниры по CS:GO, Dota 2, LoL, PUBG и другим играм.\n'
                                      '------------------------------------------------------------------------\n'
                                      'Новости кино - фильмы и сериалы, даты выхода, анонсы, трейлеры, сборы.\n'
                                      '------------------------------------------------------------------------\n'
                                      'Новости высоких технологий - анонсы и обзоры смартфонов, консолей, компьютерных комплектующих.\n'
                                      '------------------------------------------------------------------------\n'
                                      'Скидки на игры для ПК, PS4, Xbox One - игровые распродажи в Steam, PS Store, Epic Games Store.\n'
                                      '------------------------------------------------------------------------\n'
                                      '/updatenews - команда для обновления новостей.')


news = get_info('https://www.igromania.ru/news/')
f_news = True
c_news = 0

games = get_info('https://www.igromania.ru/news/game/')
f_games = True
c_games = 0

cyber = get_info('https://www.igromania.ru/news/cybersport/')
f_cyber = True
c_cyber = 0

movie = get_info('https://www.igromania.ru/news/kino/')
f_movie = True
c_movie = 0

electr = get_info('https://www.igromania.ru/news/hard/')
f_electr = True
c_electr = 0

discount = get_info('https://www.igromania.ru/news/sale/')
f_discount = True
c_discount = 0

sp = []
active = ''


@bot.message_handler(commands=['updatenews'])
def updatenews(message):
    global news, f_news, c_news, games, f_games, c_games, cyber, f_cyber, c_cyber, movie, f_movie, c_movie, electr, f_electr, c_electr, discount, f_discount, c_discount
    s = []
    update = False
    if news != get_info('https://www.igromania.ru/news/'):
        news = get_info('https://www.igromania.ru/news/')
        f_news = True
        c_news = 0
        s.append('новости')
        update = True
    if games != get_info('https://www.igromania.ru/news/game/'):
        games = get_info('https://www.igromania.ru/news/game/')
        f_games = True
        c_games = 0
        s.append('игры')
        update = True
    if cyber != get_info('https://www.igromania.ru/news/cybersport/'):
        cyber = get_info('https://www.igromania.ru/news/cybersport/')
        f_cyber = True
        c_cyber = 0
        s.append('киберспорт')
        update = True
    if movie != get_info('https://www.igromania.ru/news/kino/'):
        movie = get_info('https://www.igromania.ru/news/kino/')
        f_movie = True
        c_movie = 0
        s.append('кино')
        update = True
    if electr != get_info('https://www.igromania.ru/news/hard/'):
        electr = get_info('https://www.igromania.ru/news/hard/')
        f_electr = True
        c_electr = 0
        s.append('технологии')
        update = True
    if discount != get_info('https://www.igromania.ru/news/sale/'):
        discount = get_info('https://www.igromania.ru/news/sale/')
        f_discount = True
        c_discount = 0
        s.append('скидки')
        update = True
    if update:
        ln = ', '.join(s)
        bot.send_message(message.chat.id, f'Найдены новые новости в разделе: {ln}.')
    if not update:
        bot.send_message(message.chat.id, f'Новые новости не найдены.')


@bot.message_handler(content_types=['text'])
def text(message):
    global sp, news, f_news, c_news, games, f_games, c_games, cyber, f_cyber, c_cyber, movie, f_movie, c_movie, electr, f_electr, c_electr, discount, f_discount, c_discount, active
    if message.chat.type == 'private':
        if message.text == 'Новости' and f_news:
            sp = news
            active = 'Новости'
            tit, dop, ss = [el for el in sp[c_news]]
            bot.send_message(message.chat.id, tit)
            markup = types.InlineKeyboardMarkup(row_width=3)
            item1 = types.InlineKeyboardButton("Подробнее", callback_data='more')
            markup.add(item1)
            c_news += 1
            inf_img = requests.get(ss)
            soup = BS(inf_img.content, 'lxml')
            img = soup.find(class_="lcol").find(class_="main_pic_container").find("img").get("src")
            bot.send_photo(message.chat.id, img, caption=dop, reply_markup=markup)
            if c_news == len(sp):
                bot.send_message(message.chat.id, 'Это все новости на сегодня')
                c_news = 0
                f_news = False
        if message.text == 'Игры' and f_games:
            sp = games
            active = 'Игры'
            tit, dop, ss = [el for el in sp[c_games]]
            bot.send_message(message.chat.id, tit)
            markup = types.InlineKeyboardMarkup(row_width=3)
            item1 = types.InlineKeyboardButton("Подробнее", callback_data='more')
            markup.add(item1)
            c_games += 1
            inf_img = requests.get(ss)
            soup = BS(inf_img.content, 'lxml')
            img = soup.find(class_="lcol").find(class_="main_pic_container").find("img").get("src")
            bot.send_photo(message.chat.id, img, caption=dop, reply_markup=markup)
            if c_games == len(sp):
                bot.send_message(message.chat.id, 'Это все игровые новости на сегодня')
                c_games = 0
                f_games = False
        if message.text == 'Киберспорт' and f_cyber:
            sp = cyber
            active = 'Кибер'
            tit, dop, ss = [el for el in sp[c_cyber]]
            bot.send_message(message.chat.id, tit)
            markup = types.InlineKeyboardMarkup(row_width=3)
            item1 = types.InlineKeyboardButton("Подробнее", callback_data='more')
            markup.add(item1)
            c_cyber += 1
            inf_img = requests.get(ss)
            soup = BS(inf_img.content, 'lxml')
            img = soup.find(class_="lcol").find(class_="main_pic_container").find("img").get("src")
            bot.send_photo(message.chat.id, img, caption=dop, reply_markup=markup)
            if c_cyber == len(sp):
                bot.send_message(message.chat.id, 'Это все новости по киберспорту на сегодня')
                c_cyber = 0
                f_cyber = False
        if message.text == 'Кино' and f_movie:
            sp = movie
            active = 'Кино'
            tit, dop, ss = [el for el in sp[c_movie]]
            bot.send_message(message.chat.id, tit)
            markup = types.InlineKeyboardMarkup(row_width=3)
            item1 = types.InlineKeyboardButton("Подробнее", callback_data='more')
            markup.add(item1)
            c_movie += 1
            inf_img = requests.get(ss)
            soup = BS(inf_img.content, 'lxml')
            img = soup.find(class_="lcol").find(class_="main_pic_container").find("img").get("src")
            bot.send_photo(message.chat.id, img, caption=dop, reply_markup=markup)
            if c_movie == len(sp):
                bot.send_message(message.chat.id, 'Это все новости в киноиндустрии на сегодня')
                c_movie = 0
                f_movie = False
        if message.text == 'Технологии' and f_electr:
            sp = electr
            active = 'Электр'
            tit, dop, ss = [el for el in sp[c_electr]]
            bot.send_message(message.chat.id, tit)
            markup = types.InlineKeyboardMarkup(row_width=3)
            item1 = types.InlineKeyboardButton("Подробнее", callback_data='more')
            markup.add(item1)
            c_electr += 1
            inf_img = requests.get(ss)
            soup = BS(inf_img.content, 'lxml')
            img = soup.find(class_="lcol").find(class_="main_pic_container").find("img").get("src")
            bot.send_photo(message.chat.id, img, caption=dop, reply_markup=markup)
            if c_electr == len(sp):
                bot.send_message(message.chat.id, 'Это все новости электроники на сегодня')
                c_electr = 0
                f_electr = False
        if message.text == 'Скидки' and f_discount:
            sp = discount
            active = 'Скидки'
            tit, dop, ss = [el for el in sp[c_discount]]
            bot.send_message(message.chat.id, tit)
            markup = types.InlineKeyboardMarkup(row_width=3)
            item1 = types.InlineKeyboardButton("Подробнее", callback_data='more')
            markup.add(item1)
            c_discount += 1
            inf_img = requests.get(ss)
            soup = BS(inf_img.content, 'lxml')
            img = soup.find(class_="lcol").find(class_="main_pic_container").find("img").get("src")
            bot.send_photo(message.chat.id, img, caption=dop, reply_markup=markup)
            if c_discount == len(sp):
                bot.send_message(message.chat.id, 'Это все скидки на сегодня')
                c_discount = 0
                f_discount = False


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global sp, c_news, c_games, c_cyber, c_movie, c_electr, c_discount, active
    if call.message:
        if call.data == 'more':
            if active == 'Новости':
                bot.send_message(call.message.chat.id, sp[c_news - 1][2])
            if active == 'Игры':
                bot.send_message(call.message.chat.id, sp[c_games - 1][2])
            if active == 'Кибер':
                bot.send_message(call.message.chat.id, sp[c_cyber - 1][2])
            if active == 'Кино':
                bot.send_message(call.message.chat.id, sp[c_movie - 1][2])
            if active == 'Электр':
                bot.send_message(call.message.chat.id, sp[c_electr - 1][2])
            if active == 'Скидки':
                bot.send_message(call.message.chat.id, sp[c_discount - 1][2])


if __name__ == '__main__':
    bot.polling(none_stop=True)
