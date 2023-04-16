import telebot
import config
from get_info import news, games, cybersport, movie, electronics, discount
from sqlighter import SQLighter
from telebot import types

bot = telebot.TeleBot(config.TOKEN)
db = SQLighter('db.db')


@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('static/welcome.tgs', 'rb')
    bot.send_sticker(message.chat.id, sti)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Новости")
    item2 = types.KeyboardButton("Игры")
    item3 = types.KeyboardButton("Киберспорт")
    item4 = types.KeyboardButton("Кино")
    item5 = types.KeyboardButton("Электроника")
    item6 = types.KeyboardButton("Скидки")

    markup.add(item1, item2, item3, item4, item5, item6)

    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!\n<b>{1.first_name}</b> - здесь Вы найдете последние новости из мира игр, а также новости из киноиндустрии, электроники и скидки.".format(message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


'''@bot.message_handler(commands=['subscribe'])
def subscribe(message):
    if not db.subscriber_exists(message.from_user.id):
        db.add_subscriber(message.from_user.id)
    else:
        db.update_subscription(message.from_user.id, True)
        bot.send_message(message.chat.id,
        "Вы успешно подписались на рассылку!\nЖдите, скоро выйдут новые обзоры и вы узнаете о них первыми =)")


@bot.message_handler(commands=['unsubscribe'])
def unsubscribe(message):
    if not db.subscriber_exists(message.from_user.id):
        db.add_subscriber(message.from_user.id, False)
        bot.send_message(message.chat.id, "Вы итак не подписаны.")
    else:
        db.update_subscription(message.from_user.id, False)
        bot.send_message(message.chat.id, "Вы успешно отписаны от рассылки.")'''


news = news()
f_news = True
c_news = 0

games = games()
f_games = True
c_games = 0

cyber = cybersport()
f_cyber = True
c_cyber = 0

movie = movie()
f_movie = True
c_movie = 0

electr = electronics()
f_electr = True
c_electr = 0

discount = discount()
f_discount = True
c_discount = 0

sp = []
active = ''


@bot.message_handler(content_types=['text'])
def text(message):
    global sp, news, f_news, c_news, games, f_games, c_games, cyber, f_cyber, c_cyber, movie, f_movie, c_movie, electr, f_electr, c_electr, discount, f_discount, c_discount, active
    if message.chat.type == 'private':
        if message.text == 'Новости' and f_news:
            sp = news
            active = 'Новости'
            tit, img, dop, ss = [el for el in sp[c_news]]
            bot.send_message(message.chat.id, tit)
            markup = types.InlineKeyboardMarkup(row_width=3)
            item1 = types.InlineKeyboardButton("Подробнее", callback_data='more')
            markup.add(item1)
            c_news += 1
            bot.send_photo(message.chat.id, img, caption=dop, reply_markup=markup)
            if c_news == len(sp):
                bot.send_message(message.chat.id, 'Это все новости на сегодня')
                c_news = 0
                f_news = False
        if message.text == 'Игры' and f_games:
            sp = games
            active = 'Игры'
            tit, img, dop, ss = [el for el in sp[c_games]]
            bot.send_message(message.chat.id, tit)
            markup = types.InlineKeyboardMarkup(row_width=3)
            item1 = types.InlineKeyboardButton("Подробнее", callback_data='more')
            markup.add(item1)
            c_games += 1
            bot.send_photo(message.chat.id, img, caption=dop, reply_markup=markup)
            if c_games == len(sp):
                bot.send_message(message.chat.id, 'Это все игровые новости на сегодня')
                c_games = 0
                f_games = False
        if message.text == 'Киберспорт' and f_cyber:
            sp = cyber
            active = 'Кибер'
            tit, img, dop, ss = [el for el in sp[c_cyber]]
            bot.send_message(message.chat.id, tit)
            markup = types.InlineKeyboardMarkup(row_width=3)
            item1 = types.InlineKeyboardButton("Подробнее", callback_data='more')
            markup.add(item1)
            c_cyber += 1
            bot.send_photo(message.chat.id, img, caption=dop, reply_markup=markup)
            if c_cyber == len(sp):
                bot.send_message(message.chat.id, 'Это все новости по киберспорту на сегодня')
                c_cyber = 0
                f_cyber = False
        if message.text == 'Кино' and f_movie:
            sp = movie
            active = 'Кино'
            tit, img, dop, ss = [el for el in sp[c_movie]]
            bot.send_message(message.chat.id, tit)
            markup = types.InlineKeyboardMarkup(row_width=3)
            item1 = types.InlineKeyboardButton("Подробнее", callback_data='more')
            markup.add(item1)
            c_movie += 1
            bot.send_photo(message.chat.id, img, caption=dop, reply_markup=markup)
            if c_movie == len(sp):
                bot.send_message(message.chat.id, 'Это все новости в киноиндустрии на сегодня')
                c_movie = 0
                f_movie = False
        if message.text == 'Электроника' and f_electr:
            sp = electr
            active = 'Электр'
            tit, img, dop, ss = [el for el in sp[c_electr]]
            bot.send_message(message.chat.id, tit)
            markup = types.InlineKeyboardMarkup(row_width=3)
            item1 = types.InlineKeyboardButton("Подробнее", callback_data='more')
            markup.add(item1)
            c_electr += 1
            bot.send_photo(message.chat.id, img, caption=dop, reply_markup=markup)
            if c_electr == len(sp):
                bot.send_message(message.chat.id, 'Это все новости электроники на сегодня')
                c_electr = 0
                f_electr = False
        if message.text == 'Скидки' and f_discount:
            sp = discount
            active = 'Скидки'
            tit, img, dop, ss = [el for el in sp[c_discount]]
            bot.send_message(message.chat.id, tit)
            markup = types.InlineKeyboardMarkup(row_width=3)
            item1 = types.InlineKeyboardButton("Подробнее", callback_data='more')
            markup.add(item1)
            c_discount += 1
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
                bot.send_message(call.message.chat.id, sp[c_news - 1][3])
            if active == 'Игры':
                bot.send_message(call.message.chat.id, sp[c_games - 1][3])
            if active == 'Кибер':
                bot.send_message(call.message.chat.id, sp[c_cyber - 1][3])
            if active == 'Кино':
                bot.send_message(call.message.chat.id, sp[c_movie - 1][3])
            if active == 'Электр':
                bot.send_message(call.message.chat.id, sp[c_electr - 1][3])
            if active == 'Скидки':
                bot.send_message(call.message.chat.id, sp[c_discount - 1][3])


bot.polling(none_stop=True)
