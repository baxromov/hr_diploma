import datetime
from tempfile import NamedTemporaryFile

from django.core.files import File
from rest_framework.response import Response
from rest_framework.views import APIView
from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, Update, ReplyKeyboardRemove
import time
from app import models

API_TOKEN = '1791631754:AAEDzJQKcjBX9Nx47kkYIurZqhM8whS6haM'

bot = TeleBot(API_TOKEN)


class UpdateBot(APIView):
    def post(self, request):
        json_string = request.body.decode('UTF-8')
        update = Update.de_json(json_string)
        bot.process_new_updates([update])
        return Response({'code': 200})


@bot.message_handler(commands=['start'])
def start(message):
    user, created = models.NewStaff.objects.get_or_create(tg_user_id=message.from_user.id)
    if not created:
        user.delete()
    rkm = ReplyKeyboardMarkup(True, row_width=2)
    rkm.row(
        KeyboardButton("Ro'yxatdan o'tish"),
        KeyboardButton("Kompaniya haqida to'liq ma'lumot")
    )
    bot.send_message(message.from_user.id, "Algorithm Gateway - ishga topshirish botiga hush kelibsiz",
                     reply_markup=rkm)
    bot.register_next_step_handler(message, answer_questions)


def auth_bot_or_info(message):
    if message.text == "Ro'yxatdan o'tish":
        user = models.NewStaff.objects.get(tg_user_id=message.from_user.id)
        rkm = ReplyKeyboardMarkup(True)
        rkm.add("🔙 Orqaga")
        # if created:
        user.tg_username = message.from_user.username
        user.save()
        bot.send_message(message.from_user.id, "Ismingizni kiriting\nmasalan: Ahrorov  Jasur...", reply_markup=rkm)
        bot.register_next_step_handler(message, get_name)
    elif message.text == "Kompaniya haqida to'liq ma'lumot":
        info_company = models.Company.objects.order_by('-id')
        if info_company.exists():
            info_company = info_company.first()
        images = info_company.get_images

        bot.send_message(
            message.from_user.id, f"""
{info_company.text}

{info_company.url}
""")
        time.sleep(1)
        bot.send_media_group(message.from_user.id, images)

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
            user = models.NewStaff.objects.get(tg_user_id=message.from_user.id)
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
            user = models.NewStaff.objects.get(tg_user_id=message.from_user.id)
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
                    user = models.NewStaff.objects.get(tg_user_id=message.from_user.id)
                    user.birth_date = a
                    user.save()
                    bot.send_message(message.from_user.id, "Rasmingizni yuboring", reply_markup=rkm)
                    bot.register_next_step_handler(message, get_image)
            except:
                bot.send_message(message.from_user.id, "Tu'gilgan sanangizni anniq kiriting", reply_markup=rkm)
                bot.register_next_step_handler(message, get_age)


@bot.message_handler(content_types=['photo'])
def get_image(message):
    if message.text == "🔙 Orqaga":
        message.text = None
        get_address(message)
    else:
        if message.photo:
            user = models.NewStaff.objects.get(tg_user_id=message.from_user.id)
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
            user = models.NewStaff.objects.get(tg_user_id=message.from_user.id)
            user.phone_number = message.contact.phone_number
            user.save()
            rkm = ReplyKeyboardRemove()
            bot.send_message(message.from_user.id,
                             "Ma'lumotlaringiz qabul qilindi.\n\nBotdan foydalanishingiz mumkin", reply_markup=rkm)
            bot.register_next_step_handler(message, get_departments)
        else:
            bot.send_message(message.from_user.id, "Telefon raqam aniqlanmadi.\nPastdagi tugmani bosish yetarli.")
            bot.register_next_step_handler(message, get_phone)


def get_departments(message):
    departments = models.Department.objects.all()
    rkm = ReplyKeyboardMarkup(True, row_width=3)
    department_menu = []
    for department in departments:
        department_menu.append(department.name)
    rkm.add(*department_menu)
    bot.send_message(message.from_user.id, 'Bolimni tanlang', reply_markup=rkm)
    bot.register_next_step_handler(message, answer_questions)


def answer_questions(message):
    user = models.NewStaff.objects.get(tg_user_id=message.from_user.id)
    department = models.Department.objects.filter(name__exact=message.text).first()
    user.department = department
    qs = models.Question.objects.filter(department=user.department)
    if qs.exists():
        questions = qs.order_by('id')
        user.question_step = 1
        user.department = department
        answer = models.Answer.objects.create(
            candidate=user,
            question=questions[user.question_step - 1],
        )
        user.tg_answer_id = answer.id
        user.save()
        bot.send_message(message.from_user.id, questions[0].question)
        bot.register_next_step_handler(message, answer_question_1)

        # questions_all = []
        # for item in questions:
        #     questions_all.append(item.question)

    else:
        departments = models.Department.objects.all()
        rkm = ReplyKeyboardMarkup(True, row_width=3)
        department_menu = []
        for department in departments:
            department_menu.append(department.name)
        rkm.add(*department_menu)
        bot.send_message(message.from_user.id, 'Bolimni tanlang', reply_markup=rkm)
        bot.register_next_step_handler(message, answer_questions)


def answer_question_1(message):
    user = models.NewStaff.objects.get(tg_user_id=message.from_user.id)
    qs = models.Question.objects.filter(department=user.department)
    if qs.exists():
        questions = qs.order_by('id')
        bot.send_message(message.from_user.id, questions[user.question_step])
        answer = models.Answer.objects.get(pk=user.tg_answer_id)
        answer.answer = message.text
        answer.save()
        user.question_step += 1
        answer = models.Answer.objects.create(
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
    user = models.NewStaff.objects.get(tg_user_id=message.from_user.id)
    questions = models.Question.objects.filter(department=user.department).order_by('id')
    bot.send_message(message.from_user.id, questions[user.question_step])
    answer = models.Answer.objects.get(pk=user.tg_answer_id)
    answer.answer = message.text
    answer.save()
    user.question_step += 1
    answer = models.Answer.objects.create(
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
    user = models.NewStaff.objects.get(tg_user_id=message.from_user.id)
    answer = models.Answer.objects.get(pk=user.tg_answer_id)
    answer.answer = message.text
    answer.save()
    user.tg_answer_id = None
    user.save()
    bot.send_message(message.from_user.id, "Finish bo'ldi")
