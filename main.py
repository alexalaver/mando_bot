from aiogram import Bot, Dispatcher, executor, types
from database import Data
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import config as cfg
import logging

logging.basicConfig(level=logging.INFO)

bot = Bot(cfg.token)
dp = Dispatcher(bot, storage=MemoryStorage())
db = Data('127.0.0.1', '5432', 'mando_base', 'mando_admin', 'mando443322')

class register_column(StatesGroup):
    text = State()

class del_column(StatesGroup):
    del_text = State()


class register_column_text(StatesGroup):
    column_name = State()
    column_text = State()
    column_lang = State()

class settings_user(StatesGroup):
    settings_us = State()
    settings_lang = State()


@dp.message_handler(commands='start')
async def start(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        user_id = message.from_user.id
        user_first_name = message.from_user.first_name
        user_username = message.from_user.username
        if(not db.get_user(user_id)):
            db.add_user(user_id, user_first_name, user_username)
        if db.get_lang(user_id) == 0:
            await message.delete()
            markup = types.InlineKeyboardMarkup(row_width=2)
            button1 = types.InlineKeyboardButton(cfg.but_arm, callback_data='armenian')
            button2 = types.InlineKeyboardButton(cfg.but_ru, callback_data='russian')
            button3 = types.InlineKeyboardButton(cfg.but_en, callback_data='english')
            markup.add(button1, button2, button3)
            await message.answer(cfg.begin_language_arm + "\n\n" + cfg.begin_language_ru + "\n\n" + cfg.begin_language_en, reply_markup=markup)
        else:
            await message.delete()
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            button1 = types.KeyboardButton(db.get_texts(user_id, 'settings'))
            button2 = types.KeyboardButton(db.get_texts(user_id, 'begin'))
            button3 = types.KeyboardButton(db.get_texts(user_id, 'registration'))
            button4 = types.KeyboardButton(db.get_texts(user_id, 'example'))
            button5 = types.KeyboardButton(db.get_texts(user_id, 'about_us'))
            button6 = types.KeyboardButton(db.get_texts(user_id, 'rules'))
            markup.add(button2, button3, button4, button5, button6, button1)
            text = db.get_texts(user_id, 'greetings')
            await message.answer(text.replace("\\n", "\n"), reply_markup=markup)

@dp.message_handler(commands='settings')
async def settings_command(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        user_id = message.from_user.id
        if db.get_lang(user_id) > 0:
            change_lang = db.get_texts(user_id, 'change_language')
            back = db.get_texts(user_id, 'back')
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            button1 = types.KeyboardButton(change_lang)
            button2 = types.KeyboardButton(back)
            markup.add(button1, button2)
            await message.answer(db.get_texts(user_id, 'setting_text'), reply_markup=markup)
        else:
            await message.delete()
            markup = types.InlineKeyboardMarkup(row_width=2)
            button1 = types.InlineKeyboardButton(cfg.but_arm, callback_data='armenian')
            button2 = types.InlineKeyboardButton(cfg.but_ru, callback_data='russian')
            button3 = types.InlineKeyboardButton(cfg.but_en, callback_data='english')
            markup.add(button1, button2, button3)
            await message.answer(cfg.begin_language_arm + "\n\n" + cfg.begin_language_ru + "\n\n" + cfg.begin_language_en, reply_markup=markup)



@dp.message_handler(state=register_column.text)
async def reg_column(message: types.Message, state: FSMContext):
    if message.chat.type == types.ChatType.PRIVATE:
        user_id = message.from_user.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        button1 = types.KeyboardButton(db.get_texts(user_id, 'settings'))
        button2 = types.KeyboardButton(db.get_texts(user_id, 'begin'))
        button3 = types.KeyboardButton(db.get_texts(user_id, 'registration'))
        button4 = types.KeyboardButton(db.get_texts(user_id, 'example'))
        button5 = types.KeyboardButton(db.get_texts(user_id, 'about_us'))
        button6 = types.KeyboardButton(db.get_texts(user_id, 'rules'))
        markup.add(button2, button3, button4, button5, button6, button1)
        if message.text == db.get_texts(user_id, 'cancel_operations'):
            await state.reset_state()
            await message.answer(db.get_texts(user_id, 'cancel_operation_text'), reply_markup=markup)
        else:
            if(not db.get_column(message.text)):
                db.add_column(message.text)
                await state.finish()
                await message.answer(db.get_texts(user_id, "deal"), reply_markup=markup)
            else:
                await message.answer(db.get_texts(user_id, "error_column"))
                await register_column.text.set()

@dp.message_handler(state=register_column_text.column_name)
async def reg_column_name(message: types.Message, state: FSMContext):
    if message.chat.type == types.ChatType.PRIVATE:
        user_id = message.from_user.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        button1 = types.KeyboardButton(db.get_texts(user_id, 'settings'))
        button2 = types.KeyboardButton(db.get_texts(user_id, 'begin'))
        button3 = types.KeyboardButton(db.get_texts(user_id, 'registration'))
        button4 = types.KeyboardButton(db.get_texts(user_id, 'example'))
        button5 = types.KeyboardButton(db.get_texts(user_id, 'about_us'))
        button6 = types.KeyboardButton(db.get_texts(user_id, 'rules'))
        markup.add(button2, button3, button4, button5, button6, button1)
        if message.text == db.get_texts(user_id, 'cancel_operations'):
            await state.reset_state()
            await message.answer(db.get_texts(user_id, 'cancel_operation_text'), reply_markup=markup)
            db.delete_cashe(user_id)
        else:
            if(not db.get_column(message.text)):
                await message.answer(db.get_texts(user_id, "error_name_column"))
                await register_column_text.column_name.set()
            else:
                db.update_cashe_column(user_id, message.text)
                await message.answer(db.get_texts(user_id, "reg_column_opis"))
                await register_column_text.column_text.set()

# @dp.message_handler(state=register_column.column_name)
# async def reg_column_name(message: types.Message, state: FSMContext):
#     if message.chat.type == types.ChatType.PRIVATE:
#         user_id = message.from_user.id
#         user_text = message.text
#         if message.text == db.get_texts(user_id, 'cancel_operations'):
#             await state.reset_state()
#             markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
#             button1 = types.KeyboardButton(db.get_texts(user_id, 'settings'))
#             markup.add(button1)
#             await message.answer(db.get_texts(user_id, 'cancel_operation_text'), reply_markup=markup)
#             db.delete_cashe(user_id)
#         else:
#             db.update_cashe_column(user_id, user_text)
#             await message.answer(db.get_texts(user_id, "reg_column_opis"))
#             await register_column.column_text.set()

@dp.message_handler(state=register_column_text.column_text)
async def reg_column_col_text(message: types.Message, state: FSMContext):
    if message.chat.type == types.ChatType.PRIVATE:
        user_id = message.from_user.id
        user_text = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        button1 = types.KeyboardButton(db.get_texts(user_id, 'settings'))
        button2 = types.KeyboardButton(db.get_texts(user_id, 'begin'))
        button3 = types.KeyboardButton(db.get_texts(user_id, 'registration'))
        button4 = types.KeyboardButton(db.get_texts(user_id, 'example'))
        button5 = types.KeyboardButton(db.get_texts(user_id, 'about_us'))
        button6 = types.KeyboardButton(db.get_texts(user_id, 'rules'))
        markup.add(button2, button3, button4, button5, button6, button1)
        if message.text == db.get_texts(user_id, 'cancel_operations'):
            await state.reset_state()
            await message.answer(db.get_texts(user_id, 'cancel_operation_text'), reply_markup=markup)
            db.delete_cashe(user_id)
        else:
            text = db.get_texts(user_id, "reg_column_lang")
            db.update_cashe_text(user_id, user_text)
            await message.answer(text.replace("\\n", "\n"))
            await register_column_text.column_lang.set()

@dp.message_handler(state=register_column_text.column_lang)
async def reg_column_col_lang(message: types.Message, state: FSMContext):
    if message.chat.type == types.ChatType.PRIVATE:
        user_id = message.from_user.id
        user_text = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        button1 = types.KeyboardButton(db.get_texts(user_id, 'settings'))
        button2 = types.KeyboardButton(db.get_texts(user_id, 'begin'))
        button3 = types.KeyboardButton(db.get_texts(user_id, 'registration'))
        button4 = types.KeyboardButton(db.get_texts(user_id, 'example'))
        button5 = types.KeyboardButton(db.get_texts(user_id, 'about_us'))
        button6 = types.KeyboardButton(db.get_texts(user_id, 'rules'))
        markup.add(button2, button3, button4, button5, button6, button1)
        if message.text == db.get_texts(user_id, 'cancel_operations'):
            await state.reset_state()
            await message.answer(db.get_texts(user_id, 'cancel_operation_text'), reply_markup=markup)
            db.delete_cashe(user_id)
        else:
            try:
                if 1 <= int(user_text) <= 3:
                    await state.finish()
                    text = db.get_texts(user_id, "deal")
                    get_cashe_1 = db.get_cashe(user_id)[0]
                    get_cashe_2 = db.get_cashe(user_id)[1]
                    db.add_column_option(get_cashe_1, get_cashe_2, int(user_text))
                    await message.answer(text.replace("\\n", "\n"), reply_markup=markup)
                    db.delete_cashe(user_id)
                else:
                    await message.answer(db.get_texts(user_id, "error_lang_column"))
                    await register_column_text.column_lang.set()
            except Exception as _ex:
                print("[ERROR]", _ex)
                await message.answer(db.get_texts(user_id, "error_lang_column"))
                await register_column_text.column_lang.set()

@dp.message_handler(state=del_column.del_text)
async def del_column_text(message: types.Message, state: FSMContext):
    if message.chat.type == types.ChatType.PRIVATE:
        user_id = message.from_user.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        button1 = types.KeyboardButton(db.get_texts(user_id, 'settings'))
        button2 = types.KeyboardButton(db.get_texts(user_id, 'begin'))
        button3 = types.KeyboardButton(db.get_texts(user_id, 'registration'))
        button4 = types.KeyboardButton(db.get_texts(user_id, 'example'))
        button5 = types.KeyboardButton(db.get_texts(user_id, 'about_us'))
        button6 = types.KeyboardButton(db.get_texts(user_id, 'rules'))
        markup.add(button2, button3, button4, button5, button6, button1)
        if message.text == db.get_texts(user_id, 'cancel_operations'):
            await state.reset_state()
            await message.answer(db.get_texts(user_id, 'cancel_operation_text'), reply_markup=markup)
        else:
            db.del_column(message.text)
            await state.finish()
            await message.answer(db.get_texts(user_id, "deal"), reply_markup=markup)

@dp.message_handler(commands=['add_column'])
async def add_column(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        user_id = message.from_user.id
        if db.get_lvl(user_id) > 0:
            if db.get_lang(user_id) > 0:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                button1 = types.KeyboardButton(db.get_texts(user_id, 'cancel_operations'))
                markup.add(button1)
                await message.answer(db.get_texts(user_id, 'name_column'), reply_markup=markup)
                await register_column.text.set()
            else:
                await message.delete()
                markup = types.InlineKeyboardMarkup(row_width=2)
                button1 = types.InlineKeyboardButton(cfg.but_arm, callback_data='armenian')
                button2 = types.InlineKeyboardButton(cfg.but_ru, callback_data='russian')
                button3 = types.InlineKeyboardButton(cfg.but_en, callback_data='english')
                markup.add(button1, button2, button3)
                await message.answer(cfg.begin_language_arm + "\n\n" + cfg.begin_language_ru + "\n\n" + cfg.begin_language_en, reply_markup=markup)

@dp.message_handler(commands=['del_column'])
async def del_column(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        user_id = message.from_user.id
        if db.get_lvl(user_id) > 0:
            if db.get_lang(user_id) > 0:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                button1 = types.KeyboardButton(db.get_texts(user_id, 'cancel_operations'))
                markup.add(button1)
                await del_column.del_text.set()
                await message.answer(db.get_texts(user_id, 'reg_column'), reply_markup=markup)
            else:
                await message.delete()
                markup = types.InlineKeyboardMarkup(row_width=2)
                button1 = types.InlineKeyboardButton(cfg.but_arm, callback_data='armenian')
                button2 = types.InlineKeyboardButton(cfg.but_ru, callback_data='russian')
                button3 = types.InlineKeyboardButton(cfg.but_en, callback_data='english')
                markup.add(button1, button2, button3)
                await message.answer(cfg.begin_language_arm + "\n\n" + cfg.begin_language_ru + "\n\n" + cfg.begin_language_en, reply_markup=markup)

@dp.message_handler(commands=['add_column_options'])
async def add_column_options(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        user_id = message.from_user.id
        if db.get_lvl(user_id) > 0:
            if db.get_lang(user_id) > 0:
                db.delete_cashe(user_id)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                button1 = types.KeyboardButton(db.get_texts(user_id, 'cancel_operations'))
                markup.add(button1)
                db.add_cashe(user_id)
                await message.answer(db.get_texts(user_id, 'name_column'), reply_markup=markup)
                await register_column_text.column_name.set()
            else:
                await message.delete()
                markup = types.InlineKeyboardMarkup(row_width=2)
                button1 = types.InlineKeyboardButton(cfg.but_arm, callback_data='armenian')
                button2 = types.InlineKeyboardButton(cfg.but_ru, callback_data='russian')
                button3 = types.InlineKeyboardButton(cfg.but_en, callback_data='english')
                markup.add(button1, button2, button3)
                await message.answer(cfg.begin_language_arm + "\n\n" + cfg.begin_language_ru + "\n\n" + cfg.begin_language_en, reply_markup=markup)



@dp.callback_query_handler()
async def language(callback_query: types.CallbackQuery):
    if callback_query.message.chat.type == types.ChatType.PRIVATE:
        user_id = callback_query.from_user.id
        if callback_query.data == 'armenian':
            db.set_lang(user_id, 1)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            button1 = types.KeyboardButton(db.get_texts(user_id, 'settings'))
            button2 = types.KeyboardButton(db.get_texts(user_id, 'begin'))
            button3 = types.KeyboardButton(db.get_texts(user_id, 'registration'))
            button4 = types.KeyboardButton(db.get_texts(user_id, 'example'))
            button5 = types.KeyboardButton(db.get_texts(user_id, 'about_us'))
            button6 = types.KeyboardButton(db.get_texts(user_id, 'rules'))
            markup.add(button2, button3, button4, button5, button6, button1)
            await callback_query.message.delete()
            await callback_query.message.answer(db.get_texts(user_id, 'lang_right'), reply_markup=markup)
        elif callback_query.data == 'russian':
            db.set_lang(user_id, 2)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            button1 = types.KeyboardButton(db.get_texts(user_id, 'settings'))
            button2 = types.KeyboardButton(db.get_texts(user_id, 'begin'))
            button3 = types.KeyboardButton(db.get_texts(user_id, 'registration'))
            button4 = types.KeyboardButton(db.get_texts(user_id, 'example'))
            button5 = types.KeyboardButton(db.get_texts(user_id, 'about_us'))
            button6 = types.KeyboardButton(db.get_texts(user_id, 'rules'))
            markup.add(button2, button3, button4, button5, button6, button1)
            await callback_query.message.delete()
            await callback_query.message.answer(db.get_texts(user_id, 'lang_right'), reply_markup=markup)
        elif callback_query.data == 'english':
            db.set_lang(user_id, 3)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            button1 = types.KeyboardButton(db.get_texts(user_id, 'settings'))
            button2 = types.KeyboardButton(db.get_texts(user_id, 'begin'))
            button3 = types.KeyboardButton(db.get_texts(user_id, 'registration'))
            button4 = types.KeyboardButton(db.get_texts(user_id, 'example'))
            button5 = types.KeyboardButton(db.get_texts(user_id, 'about_us'))
            button6 = types.KeyboardButton(db.get_texts(user_id, 'rules'))
            markup.add(button2, button3, button4, button5, button6, button1)
            await callback_query.message.delete()
            await callback_query.message.answer(db.get_texts(user_id, 'lang_right'), reply_markup=markup)

@dp.callback_query_handler(state=settings_user.settings_lang)
async def settings_lang(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.message.chat.type == types.ChatType.PRIVATE:
        user_id = callback_query.from_user.id
        if callback_query.data == 'armenians':
            db.set_lang(user_id, 1)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            button1 = types.KeyboardButton(db.get_texts(user_id, 'settings'))
            button2 = types.KeyboardButton(db.get_texts(user_id, 'begin'))
            button3 = types.KeyboardButton(db.get_texts(user_id, 'registration'))
            button4 = types.KeyboardButton(db.get_texts(user_id, 'example'))
            button5 = types.KeyboardButton(db.get_texts(user_id, 'about_us'))
            button6 = types.KeyboardButton(db.get_texts(user_id, 'rules'))
            markup.add(button2, button3, button4, button5, button6, button1)
            await callback_query.message.delete()
            await callback_query.message.answer(db.get_texts(user_id, 'change_lang_begin'), reply_markup=markup)
            await state.finish()
        elif callback_query.data == 'russians':
            db.set_lang(user_id, 2)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            button1 = types.KeyboardButton(db.get_texts(user_id, 'settings'))
            button2 = types.KeyboardButton(db.get_texts(user_id, 'begin'))
            button3 = types.KeyboardButton(db.get_texts(user_id, 'registration'))
            button4 = types.KeyboardButton(db.get_texts(user_id, 'example'))
            button5 = types.KeyboardButton(db.get_texts(user_id, 'about_us'))
            button6 = types.KeyboardButton(db.get_texts(user_id, 'rules'))
            markup.add(button2, button3, button4, button5, button6, button1)
            await callback_query.message.delete()
            await callback_query.message.answer(db.get_texts(user_id, 'change_lang_begin'), reply_markup=markup)
            await state.finish()
        elif callback_query.data == 'englishs':
            db.set_lang(user_id, 3)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            button1 = types.KeyboardButton(db.get_texts(user_id, 'settings'))
            button2 = types.KeyboardButton(db.get_texts(user_id, 'begin'))
            button3 = types.KeyboardButton(db.get_texts(user_id, 'registration'))
            button4 = types.KeyboardButton(db.get_texts(user_id, 'example'))
            button5 = types.KeyboardButton(db.get_texts(user_id, 'about_us'))
            button6 = types.KeyboardButton(db.get_texts(user_id, 'rules'))
            markup.add(button2, button3, button4, button5, button6, button1)
            await callback_query.message.delete()
            await callback_query.message.answer(db.get_texts(user_id, 'change_lang_begin'), reply_markup=markup)
            await state.finish()

@dp.message_handler(state=settings_user.settings_lang)
async def settings_lang_text(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        user_id = message.from_user.id
        back = db.get_texts(user_id, 'back')
        change_lang = db.get_texts(user_id, 'change_language')
        if message.text == back:
            markup_settings = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            button1 = types.KeyboardButton(change_lang)
            button2 = types.KeyboardButton(back)
            markup_settings.add(button1, button2)
            await message.answer(db.get_texts(user_id, 'back_text'), reply_markup=markup_settings)
            await settings_user.settings_us.set()

@dp.message_handler(state=settings_user.settings_us)
async def settings(message: types.Message, state: FSMContext):
    if message.chat.type == types.ChatType.PRIVATE:
        user_id = message.from_user.id
        change_lang = db.get_texts(user_id, 'change_language')
        back = db.get_texts(user_id, 'back')
        markups = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        buttons1 = types.KeyboardButton(back)
        markups.add(buttons1)
        if message.text == change_lang:
            markup_inline = types.InlineKeyboardMarkup(row_width=2)
            button1 = types.InlineKeyboardButton(cfg.but_arm, callback_data='armenians')
            button2 = types.InlineKeyboardButton(cfg.but_ru, callback_data='russians')
            button3 = types.InlineKeyboardButton(cfg.but_en, callback_data='englishs')
            markup_inline.add(button1, button2, button3)
            await message.answer(db.get_texts(user_id, 'correct_button'), reply_markup=markups)
            await message.answer(db.get_texts(user_id, 'change_language_text'), reply_markup=markup_inline)
            await settings_user.settings_lang.set()
        elif message.text == back:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            button1 = types.KeyboardButton(db.get_texts(user_id, 'settings'))
            button2 = types.KeyboardButton(db.get_texts(user_id, 'begin'))
            button3 = types.KeyboardButton(db.get_texts(user_id, 'registration'))
            button4 = types.KeyboardButton(db.get_texts(user_id, 'example'))
            button5 = types.KeyboardButton(db.get_texts(user_id, 'about_us'))
            button6 = types.KeyboardButton(db.get_texts(user_id, 'rules'))
            markup.add(button2, button3, button4, button5, button6, button1)
            await message.answer(db.get_texts(user_id, 'back_text'), reply_markup=markup)
            await state.reset_state()


@dp.message_handler()
async def other(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        user_id = message.from_user.id
        if db.get_lang(user_id) > 0:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            button1 = types.KeyboardButton(db.get_texts(user_id, 'settings'))
            button2 = types.KeyboardButton(db.get_texts(user_id, 'begin'))
            button3 = types.KeyboardButton(db.get_texts(user_id, 'registration'))
            button4 = types.KeyboardButton(db.get_texts(user_id, 'example'))
            button5 = types.KeyboardButton(db.get_texts(user_id, 'about_us'))
            markup.add(button2, button3, button4, button5, button1)
            settings = db.get_texts(user_id, 'settings')
            change_lang = db.get_texts(user_id, 'change_language')
            back = db.get_texts(user_id, 'back')
            if message.text == settings:
                markup_settings = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                button1 = types.KeyboardButton(change_lang)
                button2 = types.KeyboardButton(back)
                markup_settings.add(button1, button2)
                await message.answer(db.get_texts(user_id, 'setting_text'), reply_markup=markup_settings)
                await settings_user.settings_us.set()
            elif message.text == db.get_texts(user_id, 'begin'):
                text = db.get_texts(user_id, 'greetings')
                await message.answer(text.replace("\\n", "\n"))
            elif message.text == db.get_texts(user_id, 'rules'):
                text = db.get_texts(user_id, 'rules_text')
                await message.answer(text.replace("\\n", "\n"))
        else:
            await message.delete()
            markup_error_lang = types.InlineKeyboardMarkup(row_width=2)
            button1 = types.InlineKeyboardButton(cfg.but_arm, callback_data='armenian')
            button2 = types.InlineKeyboardButton(cfg.but_ru, callback_data='russian')
            button3 = types.InlineKeyboardButton(cfg.but_en, callback_data='english')
            markup_error_lang.add(button1, button2, button3)
            await message.answer(cfg.begin_language_arm + "\n\n" + cfg.begin_language_ru + "\n\n" + cfg.begin_language_en, reply_markup=markup_error_lang)

if __name__ == "__main__":
    executor.start_polling(dp)
