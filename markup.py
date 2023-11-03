from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
import sqlite3 as sq
from database import Database
from config import admin_username

db = Database('all.db')
base = sq.connect('all.db')


cur = base.cursor()

def button_1():
    rkb = ReplyKeyboardMarkup(resize_keyboard=True)

    kb_1 = KeyboardButton("📱Профиль")
    kb_2 = KeyboardButton("🚀Бесплатный телеграм премиум")
    kb_3 = KeyboardButton("🔰Купить рекламу")

    return rkb.add(kb_1).add(kb_2).add(kb_3)


def button_2():
    ikm = InlineKeyboardMarkup()

    ikb = InlineKeyboardButton(text="✅ Заказать рекламу", url=f"https://t.me/{admin_username}")

    return ikm.add(ikb)


def button_3():
    rkb = ReplyKeyboardMarkup(resize_keyboard=True)

    kb_1 = KeyboardButton("🥇Premium на год")
    kb_2 = KeyboardButton("🥈Premium на 3 месяца")
    kb_3 = KeyboardButton("🥉Premium на 1 месяц")

    return rkb.add(kb_1).add(kb_2).add(kb_3)


def check():
    ikm = InlineKeyboardMarkup(row_width=True)

    for i in cur.execute("SELECT * FROM `group`"):
        ikb = InlineKeyboardButton(text=i[0], url=i[2])

        ikm.insert(ikb)

    ikb_check = InlineKeyboardButton("✅ Проверить", callback_data="check_sub")

    ikm.add(ikb_check)

    return ikm

def button_4():
    rkm = ReplyKeyboardMarkup(resize_keyboard=True)

    kb = KeyboardButton("↪️ В главное меню")

    return rkm.add(kb)

def check_refer():
    ikm = InlineKeyboardMarkup()

    ikb = InlineKeyboardButton("✅ Я выполнил задание", callback_data="check_refer")

    return ikm.add(ikb)


def button_admin():
    rkb = ReplyKeyboardMarkup(resize_keyboard=True)

    kb_1 = KeyboardButton("📱Профиль")
    kb_2 = KeyboardButton("🚀Бесплатный телеграм премиум")
    kb_3 = KeyboardButton("🔰Купить рекламу")
    kb_4 = KeyboardButton("📖 Админ панель")

    return rkb.add(kb_1).add(kb_2).add(kb_3).add(kb_4)

def admin():
    ikm_admin = InlineKeyboardMarkup()
    ikb1_admin = InlineKeyboardButton("Рассылка", callback_data="admin_mail")
    ikb2_admin = InlineKeyboardButton("Статистика", callback_data="stats")
    ikb3_admin = InlineKeyboardButton("Добавить группу", callback_data="new_group")
    ikb4_admin = InlineKeyboardButton("Удалить группу", callback_data="_dell_group")
    return ikm_admin.add(ikb1_admin, ikb2_admin).add(ikb3_admin, ikb4_admin)

def admin_2():
    ikm = InlineKeyboardMarkup()
    ikb_1 = InlineKeyboardButton("Сдампить базу", callback_data="dump")
    ikb_2 = InlineKeyboardButton("Изменить бота", callback_data="update")
    return ikm.add(ikb_1).add(ikb_2)