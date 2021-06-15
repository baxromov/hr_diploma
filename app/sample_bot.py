import datetime
import time
from tempfile import NamedTemporaryFile

from django.core.files import File
from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


TOKEN = None
bot = TeleBot(TOKEN)

import os
import sys
import django
from django.apps import apps

BASE_DIR = os.getcwd()
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

Bot = apps.get_model(app_label='app', model_name='Bot')
Staff = apps.get_model(app_label='app', model_name='Staff')
NewStaff = apps.get_model(app_label='app', model_name='NewStaff')
Department = apps.get_model(app_label='app', model_name='Department')
Company = apps.get_model(app_label='app', model_name='Company')
Answer = apps.get_model(app_label='app', model_name='Answer')
Question = apps.get_model(app_label='app', model_name='Question')
EntryText = apps.get_model(app_label='app', model_name='EntryText')
FinishText = apps.get_model(app_label='app', model_name='FinishText')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, 'hello')

    NewStaff.objects.filter(tg_user_id=message.from_user.id).delete()
    NewStaff.objects.create(tg_user_id=message.from_user.id)
    entry_text = EntryText.objects.last()

    rkm = ReplyKeyboardMarkup(True, row_width=2)
    rkm.row(
        KeyboardButton("Ro'yxatdan o'tish"),
        KeyboardButton("Kompaniya haqida to'liq ma'lumot")
    )
    bot.send_message(message.from_user.id, entry_text, reply_markup=rkm)
    bot.register_next_step_handler(message, auth_bot_or_info)


def auth_bot_or_info(message):
    if message.text == "Ro'yxatdan o'tish":
        user = NewStaff.objects.get(tg_user_id=message.from_user.id)
        rkm = ReplyKeyboardMarkup(True)
        rkm.add("🔙 Orqaga")
        user.tg_username = message.from_user.username
        user.save()
        bot.send_message(message.from_user.id, "Ismingizni kiriting\nmasalan: Ahrorov  Jasur...", reply_markup=rkm)
        bot.register_next_step_handler(message, get_name)
    elif message.text == "Kompaniya haqida to'liq ma'lumot":
        info_company = Company.objects.last()

        bot.send_photo(message.chat.id, info_company.image, info_company.text)
        time.sleep(1)
        # bot.send_media_group(message.from_user.id, images)

        bot.register_next_step_handler(message, auth_bot_or_info)
    else:
        rkm = ReplyKeyboardMarkup(True)
        rkm.add("🔙 Orqaga")
        bot.send_message(message.from_user.id, "Ismingizni kiriting\nmasalan: Ahrorov  Jasur...", reply_markup=rkm)
        bot.register_next_step_handler(message, get_name)


def get_name(message):
    if message.text == "🔙 Orqaga":
        start(message)
    else:
        rkm = ReplyKeyboardMarkup(True)
        rkm.add("🔙 Orqaga")
        if message.text is not None:
            user = NewStaff.objects.get(tg_user_id=message.from_user.id)
            user.full_name = message.text
            user.save()
        bot.send_message(message.from_user.id, "Manzilingizni kiriting:\nmasalan: Andijon,Bobur shox 2, ... ",
                         reply_markup=rkm)
        bot.register_next_step_handler(message, get_address)


def get_address(message):
    if message.text == "🔙 Orqaga":
        auth_bot_or_info(message)
    else:
        rkm = ReplyKeyboardMarkup(True)
        rkm.add("🔙 Orqaga")
        if message.text is not None:
            user = NewStaff.objects.get(tg_user_id=message.from_user.id)
            user.address = message.text
            user.save()
        bot.send_message(message.from_user.id, "Tug;ilgan sanangizni kiriting\nmasalan: 24.05.1999", reply_markup=rkm)
        bot.register_next_step_handler(message, get_age)


def get_age(message):
    if message.text == "🔙 Orqaga":
        message.text = None
        get_name(message)
    else:
        rkm = ReplyKeyboardMarkup(True)
        rkm.add("🔙 Orqaga")
        if message.text is not None:
            try:
                sana = message.text
                a = datetime.datetime.strptime(sana, "%d.%m.%Y").date()
                a.strftime('%Y-%m-%d')
                print(a)
                if a:
                    user = NewStaff.objects.get(tg_user_id=message.from_user.id)
                    user.birth_date = a
                    user.save()
                    bot.send_message(message.from_user.id, "Rasmingizni yuboring", reply_markup=rkm)
                    bot.register_next_step_handler(message, get_image)
            except:
                bot.send_message(message.from_user.id, "Tug'ilgan sanangizni aniq kiriting", reply_markup=rkm)
                bot.register_next_step_handler(message, get_age)


@bot.message_handler(content_types=['photo'])
def get_image(message):
    if message.text == "🔙 Orqaga":
        message.text = None
        get_address(message)
    else:
        if message.photo:
            user = NewStaff.objects.get(tg_user_id=message.from_user.id)
            file_id = message.photo[-1].file_id
            file_info = bot.get_file(file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            img_temp = NamedTemporaryFile(delete=True)
            image_type = file_info.file_path.split('.')[-1]
            img_temp.write(downloaded_file)
            img_temp.flush()
            user.image.save(f"image-{message.from_user.id}.{image_type}", File(img_temp), save=True)
            user.save()
            rkm = ReplyKeyboardMarkup(True)
            rkm.add(KeyboardButton("Telefon raqamni yuborish", request_contact=True))
            rkm.add("🔙 Orqaga")
            bot.send_message(message.from_user.id, "Telefon raqamingizni yuboring.", reply_markup=rkm)
            bot.register_next_step_handler(message, get_phone)
        else:
            bot.send_message(message.from_user.id, "Rasm aniqlanmadi. Qaytadan rasm jo'nating.")
            bot.register_next_step_handler(message, get_image)


def get_phone(message):
    if message.text == "🔙 Orqaga":
        message.text = None
        get_age(message)
    else:
        if message.contact:
            user = NewStaff.objects.get(tg_user_id=message.from_user.id)
            user.phone_number = message.contact.phone_number
            user.save()
            rkm = ReplyKeyboardRemove()
            bot.send_message(message.from_user.id,
                             "Ma'lumotlaringiz qabul qilindi.\n\nBotdan foydalanishingiz mumkin", reply_markup=rkm)
            get_departments(message)
        else:
            bot.send_message(message.from_user.id, "Telefon raqam aniqlanmadi.\nPastdagi tugmani bosish yetarli.")
            bot.register_next_step_handler(message, get_phone)


def get_departments(message):
    current_bot = Bot.objects.filter(token=bot.token).last()
    if current_bot:
        departments = Department.objects.filter(company=current_bot.company)
        rkm = ReplyKeyboardMarkup(True, row_width=3)
        department_menu = []
        for department in departments:
            # if department.is_hidden == False:
            department_menu.append(department.name)
        rkm.add(*department_menu)
        bot.send_message(message.from_user.id, '✅', reply_markup=rkm)
        bot.register_next_step_handler(message, answer_questions)
    else:
        bot.send_message(message.from_user.id, "Bo'limlar mavjud emas")


def answer_questions(message):
    user = NewStaff.objects.get(tg_user_id=message.from_user.id)
    current_bot = Bot.objects.filter(token=bot.token).last()
    department = Department.objects.filter(company=current_bot.company, name__exact=message.text).first()
    # bot.send_message(message.from_user.id, (department.info if department.info else "Hozircha ma'lumot yo'q"))
    # time.sleep(1)
    user.department = department
    qs = Question.objects.filter(department=user.department)
    if qs.exists():
        questions = qs.order_by('id')
        user.question_step = 1
        user.department = department
        answer = Answer.objects.create(
            candidate=user,
            question=questions[user.question_step - 1],
        )
        user.tg_answer_id = answer.id
        user.save()
        rkm = ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, questions[0].question, reply_markup=rkm)
        bot.register_next_step_handler(message, answer_question_1)

    else:
        current_bot = Bot.objects.filter(token=bot.token).last()
        departments = Department.objects.filter(company=current_bot.company, name__exact=message.text)
        rkm = ReplyKeyboardMarkup(True, row_width=3)
        department_menu = []
        for department in departments:
            department_menu.append(department.name)
        rkm.add(*department_menu)
        bot.send_message(message.from_user.id, "Bo'limni tanlang", reply_markup=rkm)
        bot.register_next_step_handler(message, answer_questions)


def answer_question_1(message):
    user = NewStaff.objects.get(tg_user_id=message.from_user.id)
    qs = Question.objects.filter(department=user.department)
    if qs.exists():
        questions = qs.order_by('id')
        rkm = ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, questions[user.question_step], reply_markup=rkm)
        answer = Answer.objects.get(pk=user.tg_answer_id)
        answer.answer = message.text
        answer.save()
        user.question_step += 1
        answer = Answer.objects.create(
            candidate=user,
            question=questions[user.question_step - 1],
        )
        user.tg_answer_id = answer.id
        user.save()

        if len(questions) == user.question_step:
            bot.register_next_step_handler(message, finish)
        else:
            bot.register_next_step_handler(message, answer_question_2)
    else:
        bot.send_message(message.from_user.id, "Bo'limni to'g'ri tanlang!")


def answer_question_2(message):
    user = NewStaff.objects.get(tg_user_id=message.from_user.id)
    questions = Question.objects.filter(department=user.department).order_by('id')
    bot.send_message(message.from_user.id, questions[user.question_step])
    answer = Answer.objects.get(pk=user.tg_answer_id)
    answer.answer = message.text
    answer.save()
    user.question_step += 1
    answer = Answer.objects.create(
        candidate=user,
        question=questions[user.question_step - 1],
    )
    user.tg_answer_id = answer.id
    user.save()
    if len(questions) == user.question_step:
        bot.register_next_step_handler(message, finish)
    else:
        bot.register_next_step_handler(message, answer_question_1)


def finish(message):
    user = NewStaff.objects.get(tg_user_id=message.from_user.id)
    finish_text = FinishText.objects.last()
    answer = Answer.objects.get(pk=user.tg_answer_id)
    answer.answer = message.text
    answer.save()
    user.tg_answer_id = None
    current_bot = Bot.objects.filter(token=bot.token).last()
    user.company = current_bot.company
    user.save()
    bot.send_message(message.from_user.id, finish_text)


bot.polling(none_stop=True)
