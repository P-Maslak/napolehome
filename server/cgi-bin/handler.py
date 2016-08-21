# -*- coding: utf-8 -*- ?
import sqlite3
import cgi

# подключаемся к БД
con = sqlite3.connect("news.db")
with con:
        cursor = con.cursor()
        # создаем таблицу если она не создана
        cursor.execute("CREATE TABLE IF NOT EXISTS devices(id INT, temperature INT, door INT);")

        # получаем все данные из запроса
        form = cgi.FieldStorage()
        device_id = int(form.getfirst("id", "0"))
        temperature = int(form.getfirst("temperature", "0"))
        door = int(form.getfirst("door", "0"))

        # ищем устройство в БД
        cursor.execute("SELECT * FROM devices WHERE id = %s" % device_id)
        divice = cursor.fetchall()

        # проверяем сущестувет ли устройство
        if not user:
            # заносим устройство в БД (т.к. Оно впервые подключилось к сети)
            cursor.execute("INSERT INTO devices VALUES(?,?,?)",(device_id,temperature,door))
        else:
            # изменяем данные на новые
            cursor.execute("UPDATE users SET temperature = ? AND door = ? WHERE id = ?",(temperature, door, device_id))
