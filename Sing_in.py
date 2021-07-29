import telebot
import DB_controller
import configparser
# import GUI


#@TFS_task_bot

config = configparser.ConfigParser()  # создаём объекта парсера
config.read("config.ini")

bot = telebot.TeleBot()
db_object = DB_controller.DB()

name = ''
sname = ''
mail = ''
phone = ''
tech_log = ''
tech_pas = ''
login_tech_flag = 0

keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
button_contacts = telebot.types.KeyboardButton(text="Регистрация", request_contact=True)
send_file = telebot.types.KeyboardButton(text="Кинуть ДЗ-шку", request_contact=False)
response = telebot.types.KeyboardButton(text="Оставить отзыв", request_contact=False)
achievement = telebot.types.KeyboardButton(text="Ачивки", request_contact=False)
help = telebot.types.KeyboardButton(text="Помощь", request_contact=False)

homework = telebot.types.KeyboardButton(text ="Домашка студентов",request_contact=False)
markup = telebot.types.KeyboardButton(text="Оценить дз",request_contact=False)

@bot.message_handler(commands=['start'])
def logging(mes):
    keyboard = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True
    ).add(button_contacts)
    bot.send_message(mes.chat.id, 'Добро пожаловать в 🔥IT-Академию🔥', reply_markup=keyboard)







@bot.message_handler(content_types=['contact'])
def get_data_from_phone(mes):
    bot.send_message(mes.chat.id, 'Ты зерегистрировался на курс по Python. Дороги назад нет...')
    bot.send_message(mes.chat.id, 'Теперь немного информации о тебе')
    bot.send_message(mes.chat.id, 'Как тебя зовут?')
    bot.register_next_step_handler(mes, name)
    global phone
    phone = str(mes.contact.phone_number)






def name(mes):
    bot.send_message(mes.chat.id, 'Напиши свою фамилию')
    global name
    name = str(mes.text)
    bot.register_next_step_handler(mes, sname)

def sname(mes):
    bot.send_message(mes.chat.id, 'И последнее, напиши свою почту')
    global sname
    sname = str(mes.text)

    bot.register_next_step_handler(mes, mail)

def mail(mes):
    keyboard = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True).add(send_file, achievement, response)
    global mail
    mail = str(mes.text)
    db_object.add_to_base(str(mes.from_user.id), name, sname, phone, mail)
    bot.send_message(mes.chat.id, 'Спасибо\nТеперь мы знаем всё про тебя😈\nДо встречи...', reply_markup=to_main())

def tech_login(mes):
    global tech_log
    tech_log = str(mes.text)
    bot.send_message(mes.chat.id, 'Введи свой пароль')
    bot.register_next_step_handler(mes, tech_pass)

def tech_pass(mes):
    global tech_pas
    global tech_log
    tech_pas = str(mes.text)
    if db_object.get_admin_data(tech_log,tech_pas):
        print("def")
        print(mes.chat.id)
        db_object.set_admin(mes.chat.id)
        bot.send_message(mes.chat.id, 'Вход выполнен', reply_markup=to_tech())
        tech_log = 0
        tech_pas = 0
    else:
        bot.send_message(mes.chat.id, 'Вход не выполнен', reply_markup=to_main())




def to_main():
    keyboard = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True).add(send_file, achievement, response,help)
    return keyboard

def to_tech():
    keyboard = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True).add(homework,markup)
    return keyboard

def to_ans():
    keyboard = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton(text='Оповестить о получении', callback_data='add')
    keyboard.add(button)
    return keyboard

def check_is_tech(tel_id):
    return db_object.get_admin(tel_id)

def send_homework_to_tech(file_name, file_id, chat_id):
    teacher_id = db_object.find_teacher_for_work(file_name[0])[0]
    if file_name[0] is not None:
        bot.send_document(teacher_id,file_id)

        send_mas_from_teach(teacher_id[0], file_name[0], chat_id, file_name[2])


def send_mas_from_teach(chat_id, file_name, stud_chat_id, number):
    student_name = db_object.get_student(stud_chat_id)
    bot.send_message(chat_id, "Студент группы " + str(file_name) + " " + student_name + " прислал домашенее задание номер : "+number, reply_markup=to_ans())


    @bot.callback_query_handler(func=lambda call: True)
    def query_handler(call):
        if call.data == 'add':
            bot.answer_callback_query(callback_query_id=call.id, text='Студенту отправлено оповещение')
            bot.send_message(stud_chat_id, text="Домашнее задание получено" )




@bot.message_handler(content_types=['document'])
def save_fl_to_db(mes):
    chat_id = mes.chat.id
    extension = mes.document.file_name[-3:]  # Определения расширения файла
    if extension in 'zip':
        bot.send_message(mes.chat.id, 'Супер, засейвил твоё ДЗ, теперь препод не отвертится😉', reply_markup=to_main())
        db_object.save_file_to_db(mes.document.file_name, mes.document.file_id)
        send_homework_to_tech(mes.document.file_name, mes.document.file_id, chat_id)
    else:
        bot.send_message(mes.chat.id, 'Не, родной, не катит, я сохраняю только .zip 🤷‍♂️', reply_markup=to_main())

@bot.message_handler(content_types=['text'])
def mes_text(mes):
    print(mes.chat.id)

    if str(mes.text) in 'Главное меню':
        bot.send_message(mes.chat.id, 'Возврат в главное меню', reply_markup=to_main())

    if str(mes.text) in 'Помощь':
        bot.send_sticker(mes.chat.id,'CAACAgIAAxkBAAK8O2AMmJ3wfnzEpfZLb0-sLE0VVNR4AAIJAgACmS9LCnrjYeoV8vAfHgQ', reply_markup=to_main())

    if str(mes.text) in 'Ачивки':
        achive_list = db_object.get_all_achivment(mes.chat.id)
        bot.send_message(mes.chat.id, 'Пока что у тебя есть такие стикеры за домашку : ')
        for achive in achive_list :
            bot.send_sticker(mes.chat.id, achive[0])
        bot.send_message(mes.chat.id, 'За какую домашку какой стикер уточняй у препода, такой разработки в тз не было🤷‍♂️',reply_markup=to_main())

    if str(mes.text) in 'Кинуть ДЗ-шку':
        bot.send_message(mes.chat.id, 'Добро, закинь мне архив формата zip. Имя файла - “номер группы-номер урока-номер версии дз. zip” пример “3-2-4. zip” .\nЯ сохраню твою прелесь для препода👌 ')

    if str(mes.text) in 'Я препод':
        if check_is_tech(mes.chat.id):
            bot.send_message(mes.chat.id, 'Вход выполнен', reply_markup=to_tech())
        else:
            bot.send_message(mes.chat.id, 'Введи свой логин')
            bot.register_next_step_handler(mes, tech_login)

    if (str(mes.text) in 'Домашка студентов'):
        if check_is_tech(mes.chat.id):
            bot.send_message(mes.chat.id, 'Держи',reply_markup=to_tech())
        else:
            bot.send_message(mes.chat.id, 'Для доступа к ДЗ нужно залогиниться как преподаватель',reply_markup=to_main())

bot.polling()
