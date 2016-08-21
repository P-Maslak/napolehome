# -*- coding: utf-8 -*- ?
import config
import telebot
import sqlite3

bot	= telebot.TeleBot(config.token)

# Метод для регестрации пользователя
@bot.message_handler(commands = ["reg"])
def	reg(message):
    # разбиваем сообщение от пользователя на массив слов
    cmd = message.text.split()

    # проверям что была введелена не только команада но и ID устройства (второе слово)
    if len(cmd) < 2:
        bot.send_message(message.chat.id, "ID устройства не указан.")
    else:
        # подключаемся к базе данных и начинаем работу с ней
        con = sqlite3.connect("news.db")
        with con:
            cursor = con.cursor()

            # создаем таблицу пользователей если она отстутствует
            cursor.execute("CREATE TABLE IF NOT EXISTS users(user_id INT, device_id INT);")
            cursor.execute("CREATE TABLE IF NOT EXISTS devices(id INT, temperature INT, door INT);")

            # ищем пользователя в БД
            cursor.execute("SELECT * FROM users WHERE user_id = %s" % message.chat.id)
            user = cursor.fetchall()

            # проверяем сущестувет ли пользователь
            if not user:
                # заносим пользователя в БД (т.к. Он впервые подключился)
                cursor.execute("INSERT INTO users VALUES(?,?)",(message.chat.id,cmd[1]))
                bot.send_message(message.chat.id, "Вы успешно зарегестрированны!")
            else:
                # изменяем устройство на указаный id
                cursor.execute("UPDATE users SET device_id = ? WHERE user_id = ?",(cmd[1],message.chat.id))
                bot.send_message(message.chat.id, "ID устройства успешно изменен!")

# Метод для проверки закрытия двери
@bot.message_handler(commands = ["door"])
def	door(message):
    # подключаемся к базе и начинаем работу с ней
    con = sqlite3.connect("news.db")
    with con:
        cursor = con.cursor()

        # создаем таблицу пользователей если она отстутствует
        cursor.execute("CREATE TABLE IF NOT EXISTS users(user_id INT, device_id INT);")
        cursor.execute("CREATE TABLE IF NOT EXISTS devices(id INT, temperature INT, door INT);")

        # ищем в таблице пользователей человека отправившего сообщение
        cursor.execute("SELECT * FROM users WHERE user_id = %s" % message.chat.id)
        users_row = cursor.fetchall()

        # проверяем что строка существует
        if users_row:
            # получаем id устройства к которому привязан пользователь
            device_id = users_row[0][1]


            # по полученому id получаем все данные устройства
            cursor.execute("SELECT * FROM devices WHERE id = %s" % device_id)
            devices_row = cursor.fetchall()

            # проверяем на существование строки
            if devices_row:
                if devices_row[0][2]: bot.send_message(message.chat.id, "Дверь открыта!")
                else: bot.send_message(message.chat.id, "Дверь закрыта!")
            else:
                bot.send_message(message.chat.id, "Информация отсутствует")
        else:
            bot.send_message(message.chat.id, "Вы не зарегестрированнны! Используйте комманду /reg")

if	__name__ == '__main__':
    bot.polling(none_stop=True)
