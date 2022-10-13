import asyncio
import random
import aiogram
from aiogram import executor, Bot, Dispatcher, types
import logging
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
loop =asyncio.get_event_loop()
import time
import datetime
import pickle

storage = MemoryStorage()
with open('TOKEN.txt') as f:
    TOKEN = f.read()
bot = Bot(TOKEN)
logging.basicConfig(level = logging.INFO)
dp = Dispatcher(bot, storage=storage)


channel_Error = []
only_error = []
delete_id = []

keyboard = types.InlineKeyboardMarkup()
mes = types.InlineKeyboardButton(text='text', callback_data='id')
dict_message = {}

dict_mes_id = {}

start_keyboard_1 = types.KeyboardButton('Главное меню', callback_data='start_menu')
start_key = types.ReplyKeyboardMarkup(resize_keyboard=True).add(start_keyboard_1)


#загружаем данные
async def update_dict(dict_mes_id):
    text = await readline_dict()
    text.update(dict_mes_id)
    with open('data.pkl', 'wb') as f:
        pickle.dump(text, f)
#Выгружаем данные
async def readline_dict():
    with open('data.pkl', 'rb') as f:
        text = pickle.load(f)
        return text


@dp.message_handler(commands='lll')
async def ffff(message: types.message):
    x = await readline_dict()
    z = await text_r()
    print(z)
    print('---------------------------------------------------------')
    print(x)
    await bot.delete_message(-1001471502515, 36)

#Изменение данных уменьшение кол-ва словарей
async def edit_dict():
    text = await readline_dict()
    if len(text) >= 10:
        num = 0
        iter = text.copy()
        for i in iter.keys():
            num += 1
            del text[i]
            if num == 7:
                with open('data.pkl', 'wb') as f:#загружаем оставшиеся данные
                    pickle.dump(text, f)
                break

#Добавление нового id канала в файл
async def text_append(spis):
    data = await text_r()
    data.append(spis)
    with open('data_id_message.pkl', 'wb') as f:
        pickle.dump(data, f)

#Обновление списка каналов после удаления
async def update_text(spis):
    with open('data_id_message.pkl', 'wb') as f:
        pickle.dump(spis, f)
        print("Update")

#Чтение файла с id channel
async def text_r():
    with open('data_id_message.pkl', 'rb') as f:
        spis = pickle.load(f)
        return spis
#Поиск и проверка id channel  в файле
async def check_text(mes_id):
    data = await text_r()
    if data.count(mes_id) == 0:
        await text_append(mes_id)

#Чтение файла с удаленными каналами
async def delete_id_channel():
    with open('delete.pkl', 'rb') as f:
        text = pickle.load(f)
        return text
#Пополнение списка удаленных каналов
async def append_delete_id_channel(id):
    spis = await delete_id_channel()
    new_spis = spis + id
    with open('delete.pkl', 'wb') as f:
        pickle.dump(new_spis, f)


#Перехватывает уведомление о том что бот был добавлен в канал адменистратором
@dp.my_chat_member_handler()
async def some_handler(my_chat_member: types.ChatMemberUpdated):
    chat_id = my_chat_member["chat"]
    id = chat_id["id"]
    await bot.send_message(915510200, f'{id}')
    await check_text(id)
    zxc = await text_r()


@dp.message_handler(commands='start')
async def start(message: types.message):
    await message.answer('''
1) /text_photo (отправляет текст и фото)
2) /text_video (отравляет текст и видео) 
3) /only_text (отправляет просто текст, без возможности изменения)
3) /check_time (показывает время когда было отправлено сообщение (в виде списка)) 
4) /edit_text_message (для изменения текста конкретного сообщение(его дата)(Для остановки процесса отправь: stop))
5) /check_id_channel (Список каналов)
6) /list_delete (Просмотр удаленных каналов)
7) /delete_message (Удалить сообщения из каналов)
    ''', reply_markup=start_key)

@dp.message_handler(lambda message: message.text == 'Главное меню')
async def qqqqqqqq(message: types.Message):
    await message.answer('''
1) /text_photo (отправляет текст и фото)
2) /text_video (отравляет текст и видео) 
3) /only_text (отправляет просто текст, без возможности изменения)
3) /check_time (показывает время когда было отправлено сообщение (в виде списка)) 
4) /edit_text_message (для изменения текста конкретного сообщение(его дата)(Для остановки процесса отправь: stop))
5) /check_id_channel (Список каналов)
6) /list_delete (Просмотр удаленных каналов)
7) /delete_message (Удалить сообщения из каналов)
    ''')


class UserState(StatesGroup):
    text = State()
    only_text = State()
    text_photo = State()
    edit_text_photo = State()
    time_data = State()
    delete_mes = State()
#Отправка сообщения с видео
@dp.message_handler(commands='text_video')
async def text(message: types.message):
    await message.answer('Напиши текст который отправить на канал')
    await UserState.text.set()

@dp.message_handler(state=UserState.text)
async def send(message: types.message, state: FSMContext):
    await message.answer('Пришли видео')
    await state.update_data(text=message.text)
    data = await state.get_data()
    await message.answer(text=f"text: {data['text']}")
    await state.reset_state(with_data=False)

@dp.message_handler(content_types=['video'])
async def video_state(message: types.message, state: FSMContext):
    await message.answer(text='file send')
    video_id = message.video.file_id
    data = await state.get_data()
    t = datetime.datetime.now()
    t = t.strftime("Date: %d/%m/%Y  time: %H:%M:%S")
    only_error = []
    async def start1(data, video_id):
        channel_id = await text_r()
        for id in channel_id:
            try:
               x = await bot.send_video(id, video_id, caption = data['text'])
               message_id = x.message_id
               dict_mes_id[f'{id}'] = message_id
            except:
                try:
                    delete_id.append(id)
                    x = await bot.get_chat(id)
                    zxc = f'Chat_name: {x["title"]} || https://t.me/{x["username"]}'
                    channel_Error.append(zxc)
                except:
                    only_error.append(id)
    async def main(data, video_id):
        await start1(data, video_id)

    await main(data, video_id)
    await message.answer(f'{channel_Error}\n Не удалось отправить в эти каналы')
    await message.answer(f'{only_error}\n id каналов в которые вообще не был добавлен бот')
    dict_message[t] = dict_mes_id.copy()
    await update_dict(dict_message)

    if len(delete_id) != 0:
        class DeleteState(UserState):
            text_y_n = State()
        await message.answer('Удалить каналы в которые не удалось отправить?')
        await DeleteState.text_y_n.set()
        @dp.message_handler(state=DeleteState.text_y_n)
        async def delete_y_n(message: types.message, state: FSMContext):
            await state.update_data(text=message.text)
            text_delete = await state.get_data()
            channel_error_delete_now = []
            if text_delete['text'].lower() == 'да':
                for i in delete_id:
                    try:
                        x = await bot.get_chat(i)
                        zxc = f'Chat_name: {x["title"]} || https://t.me/{x["username"]}'
                        channel_error_delete_now.append(zxc)
                    except Exception as f:
                        print(f)
                await while_delete(delete_id, only_error) #Удаление id каналов
                await state.reset_state(with_data=False)
                await message.answer(f'----Список удаленных каналов----\n{channel_error_delete_now}')

                time.sleep(0.2)
                delete_id.clear()
                only_error.clear()
                channel_error_delete_now.clear()
            else:
                only_error.clear()
                delete_id.clear()
                await message.answer("Каналы не удалены")
                await state.reset_state(with_data=False)

    time.sleep(1)
    dict_mes_id.clear()
    channel_Error.clear()
    await edit_dict()

#Отправляет просто текст
@dp.message_handler(commands='only_text')
async def text(message: types.message):
    await message.answer('Напиши текст который отправить на канал')
    await UserState.only_text.set()

@dp.message_handler(state=UserState.only_text)
async def send(message: types.message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    await message.answer(text=data['text'])
    await state.reset_state(with_data=False)
    async def start1(data):
        channel_id = await text_r()
        for id in channel_id:
            try:
                await bot.send_message(text=f'{data["text"]}', chat_id=id)

            except:
                channel_Error.append(id)
    async def main(data):
        await start1(data)

    await main(data)
    await message.answer(f'{channel_Error}\n Не удалось отправить в эти каналы')
    channel_Error.clear()

#Отправляет сообщения с картинкой
@dp.message_handler(commands='text_photo')
async def text(message: types.message):
    await message.answer('Напиши текст который отправить на канал')
    await UserState.text_photo.set()

@dp.message_handler(state=UserState.text_photo)
async def send(message: types.message, state: FSMContext):
    await message.answer('Пришли картинку')
    await state.update_data(text=message.text)
    data = await state.get_data()
    await message.answer(text=f"text: {data['text']}")
    await state.reset_state(with_data=False)


@dp.message_handler(content_types=['photo'])
async def video_state(message: types.message, state: FSMContext):
    await message.answer(text='file send')
    video_id = message.photo[0].file_id
    data = await state.get_data()
    t = datetime.datetime.now()
    t = t.strftime("Date: %d/%m/%Y  time: %H:%M:%S")
    async def start1(data, video_id):
        channel_id = await text_r()
        for id in channel_id:
            try:
                x = await bot.send_photo(id, video_id, caption = data['text'], reply_markup=keyboard)
                message_id = x.message_id
                dict_mes_id[f'{id}']=message_id
            except:
                try:
                    delete_id.append(id)
                    x = await bot.get_chat(id)
                    zxc = f'Chat_name: {x["title"]} || https://t.me/{x["username"]}'
                    channel_Error.append(zxc)
                except:
                    only_error.append(id)

    async def main(data, video_id):
        print('test')
        await start1(data, video_id)
    await main(data, video_id)
    await message.answer(f'{channel_Error}\n Не удалось отправить в эти каналы')
    await message.answer(f'{only_error}\n id каналов в которые вообще не был добавлен бот')
    dict_message[t] = dict_mes_id.copy()
    await update_dict(dict_message)

    if len(delete_id) != 0:
        class DeleteState(UserState):
            text_y_n = State()
        await message.answer('Удалить каналы в которые не удалось отправить?')
        await DeleteState.text_y_n.set()
        @dp.message_handler(state=DeleteState.text_y_n)
        async def delete_y_n(message: types.message, state: FSMContext):
            await state.update_data(text=message.text)
            text_delete = await state.get_data()
            channel_error_delete_now = []
            if text_delete['text'].lower() == 'да':
                for i in delete_id:
                    try:
                        x = await bot.get_chat(i)
                        zxc = f'Chat_name: {x["title"]} || https://t.me/{x["username"]}'
                        channel_error_delete_now.append(zxc)
                    except Exception as f:
                        print(f)
                await while_delete(delete_id, only_error) #Удаление id каналов
                await state.reset_state(with_data=False)
                await message.answer(f'----Список удаленных каналов----\n{channel_error_delete_now}')

                time.sleep(0.2)
                delete_id.clear()
                only_error.clear()
                channel_error_delete_now.clear()
            else:
                delete_id.clear()
                only_error.clear()
                await message.answer("Каналы не удалены")
                await state.reset_state(with_data=False)


    time.sleep(1)
    dict_mes_id.clear()
    channel_Error.clear()
    await edit_dict()

async def while_delete(delete_id, only_error):
    full_id = await text_r()
    for id in delete_id:
        print(id)
        full_id.remove(id)
    if len(only_error) != 0:
        for i in only_error:
            try:
                full_id.remove(i)
            except Exception as f:
                print(f)
    await update_text(full_id)
    await append_delete_id_channel(delete_id)


@dp.message_handler(commands='check_time')
async def check_time(message: types.message):
    x = await readline_dict()
    for key in x.keys():
        await message.answer(f'{key}')
        time.sleep(0.1)

@dp.message_handler(commands='check_id_channel')
async def check_id_channel(message: types.message):
    await message.answer(f'Список id каналов:{await text_r()}')

#Изменение текста в сообщении
@dp.message_handler(commands='edit_text_message')
async def text(message: types.message):
    await message.answer('Напиши измененый текст который отправить на канал')
    await UserState.edit_text_photo.set()

@dp.message_handler(state=UserState.edit_text_photo)
async def send(message: types.message, state: FSMContext):
    await message.answer('Встать дату сообщения которое нужно изменить')
    await state.update_data(text=message.text)
    data = await state.get_data()
    await message.answer(text=f"text: {data['text']}")
    await UserState.time_data.set()

@dp.message_handler(state=UserState.time_data)
async def send(message: types.message, state: FSMContext):
    await state.update_data(t_data=message.text)
    data = await state.get_data()
    if data['t_data'] == 'stop':
        await state.finish()
        await message.answer('''
        Ты отправил команду "stop"
        1) /text_photo (отправляет текст и фото)
        2) /text_video (отравляет текст и видео) 
        3) /only_text (отправляет просто текст, без возможности изменения)
        3) /check_time (показывает время когда было отправлено сообщение (в виде списка)(Для остановки процесса отправь: stop)) 
        4) /edit_text_message (для изменения текста конкретного сообщение(его дата))
        5) /check_id_channel (Список каналов)
            ''')

    await message.answer(text=f"timedate: {data['t_data']}")
    text = data['text']
    t_data = data['t_data']
    only_error = []
    async def start1(text, t_data):
        data = await readline_dict()
        for items in data[f'{t_data}'].items():
            id, mes = items
            try:
                await bot.edit_message_caption(chat_id=id, message_id=mes, caption=text, reply_markup=keyboard)
            except:
                try:
                    x = await bot.get_chat(id)
                    zxc = f'Chat_name: {x["title"]} || https://t.me/{x["username"]}'
                    channel_Error.append(zxc)
                except:
                    only_error.append(id)
    async def main(text, t_data):
        await start1(text, t_data)
    await main(text, t_data)
    await message.answer(f'{channel_Error}\n Не удалось отправить в эти каналы')
    await message.answer(f'{only_error}\n id каналов в которые вообще не был добавлен бот')
    channel_Error.clear()
    only_error.clear()
    await state.finish()


@dp.message_handler(commands='list_delete')
async def list_delete_read(message: types.message):
    list_delete = await delete_id_channel()
    channel_delete_mes = []
    for i in list_delete:
        try:
            ch = await bot.get_chat(i)
            zxc = f' https://t.me/{ch["username"]} || Chat_name: {ch["title"]}'
            channel_delete_mes.append(zxc)
        except Exception as f:
            print(f)
    await message.answer(f'************Список удаленных каналов************ \n {channel_delete_mes}')
    await message.answer(f'Полный список удаленных каналов\n{list_delete}')
    channel_delete_mes.clear()



#Удаление отправленных сообщений
@dp.message_handler(commands='delete_message')
async def delete_message(message: types.message):
    data = await readline_dict()
    for key, value in data.items():
        await message.answer(key)
    await message.answer('''
    ----------------------------------------------------------------------------------------
    Выбери дату сообщения которое нужно удалить
    И отправь в чат.
    *ВНИМАНИЕ*
    Сообщения будут удалены без возможности
           восстановления!''')
    await UserState.delete_mes.set()
@dp.message_handler(state=UserState.delete_mes)
async def delete_now_message(message: types.message, state: FSMContext):
    await state.update_data(date=message.text)
    date = await state.get_data()
    await state.reset_state(with_data=False)
    spis_date_mes = await readline_dict()
    list_delete = []
    if spis_date_mes.get(date['date']) != None:
        for key, value in spis_date_mes[date['date']].items():
            try:
                await bot.delete_message(key, value)
            except Exception as f:
                print(f)
                list_delete.append(key)
        #Удаление сообщений
        spis_date_mes.pop(date['date'])
        with open('data.pkl', 'wb') as f:
            pickle.dump(spis_date_mes, f)


        channel_delete_mes = []
        if len(list_delete) != 0:
            for i in list_delete:
                try:
                    ch = await bot.get_chat(i)
                    zxc = f' https://t.me/{ch["username"]} || Chat_name: {ch["title"]}'
                    channel_delete_mes.append(zxc)
                except Exception as f:
                    print(f)
            await message.answer(f'************Список каналов в которых сообщение не удалено ************ \n {channel_delete_mes}')
            channel_delete_mes.clear()

        await message.answer('Сообщения удалены.')
    else:
        message.answer('Неверная дата и время')
    list_delete.clear()



















if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
