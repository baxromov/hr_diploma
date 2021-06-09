import datetime
import time
from tempfile import NamedTemporaryFile

from django.core.files import File
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, Update, ReplyKeyboardRemove

from app import models


# company =
token = models.Bot.objects.last()
# # token = None
if token:
    API_TOKEN = token.token
    # URL = "https://api.telegram.org/bot" + token.token + "/setWebhook?url=https://bp.algobot.uz/bot/" + token.token + "/"
    bot = TeleBot(API_TOKEN)
    # bot.set_webhook(URL)
else:
    API_TOKEN = '123'
    bot = TeleBot(API_TOKEN)
# bot = TeleBot('1887331840:AAE7wuoXUJF1rn_gmxOMWANJaVXCJBlJAlg')


class BotAPIView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request, _token):
        # print(_token)
        # global bot
        # current_bot = models.Bot.objects.filter(token=_token).last()
        # bot = TeleBot(API_TOKEN)
        json_string = request.body.decode('UTF-8')
        update = Update.de_json(json_string)
        bot.process_new_updates([update])
        return Response({'code': 200})


@bot.message_handler(commands=['start'])
def start(message):
    models.NewStaff.objects.filter(tg_user_id=message.from_user.id).delete()
    models.NewStaff.objects.create(tg_user_id=message.from_user.id)
    entry_text = models.EntryText.objects.last()

    rkm = ReplyKeyboardMarkup(True, row_width=2)
    rkm.row(
        KeyboardButton("Ro'yxatdan o'tish"),
        KeyboardButton("Kompaniya haqida to'liq ma'lumot")
    )
    bot.send_message(message.from_user.id, entry_text, reply_markup=rkm)
    bot.register_next_step_handler(message, auth_bot_or_info)


def auth_bot_or_info(message):
    if message.text == "Ro'yxatdan o'tish":
        user = models.NewStaff.objects.get(tg_user_id=message.from_user.id)
        rkm = ReplyKeyboardMarkup(True)
        rkm.add("🔙 Orqaga")
        user.tg_username = message.from_user.username
        user.save()
        bot.send_message(message.from_user.id, "Ismingizni kiriting\nmasalan: Ahrorov  Jasur...", reply_markup=rkm)
        bot.register_next_step_handler(message, get_name)
    elif message.text == "Kompaniya haqida to'liq ma'lumot":
        info_company = models.Company.objects.last()

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
                bot.send_message(message.from_user.id, "Tug'ilgan sanangizni aniq kiriting", reply_markup=rkm)
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
            get_departments(message)
        else:
            bot.send_message(message.from_user.id, "Telefon raqam aniqlanmadi.\nPastdagi tugmani bosish yetarli.")
            bot.register_next_step_handler(message, get_phone)


def get_departments(message):
    current_bot = models.Bot.objects.filter(token=bot.token).last()
    if current_bot:
        departments = models.Department.objects.filter(company=current_bot.company)
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
    user = models.NewStaff.objects.get(tg_user_id=message.from_user.id)
    current_bot = models.Bot.objects.filter(token=bot.token).last()
    department = models.Department.objects.filter(company=current_bot.company, name__exact=message.text).first()
    # bot.send_message(message.from_user.id, (department.info if department.info else "Hozircha ma'lumot yo'q"))
    # time.sleep(1)
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
        rkm = ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, questions[0].question, reply_markup=rkm)
        bot.register_next_step_handler(message, answer_question_1)

    else:
        current_bot = models.Bot.objects.filter(token=bot.token).last()
        departments = models.Department.objects.filter(company=current_bot.company, name__exact=message.text)
        rkm = ReplyKeyboardMarkup(True, row_width=3)
        department_menu = []
        for department in departments:
            department_menu.append(department.name)
        rkm.add(*department_menu)
        bot.send_message(message.from_user.id, "Bo'limni tanlang", reply_markup=rkm)
        bot.register_next_step_handler(message, answer_questions)


def answer_question_1(message):
    user = models.NewStaff.objects.get(tg_user_id=message.from_user.id)
    qs = models.Question.objects.filter(department=user.department)
    if qs.exists():
        questions = qs.order_by('id')
        rkm = ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, questions[user.question_step], reply_markup=rkm)
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
    finish_text = models.FinishText.objects.last()
    answer = models.Answer.objects.get(pk=user.tg_answer_id)
    answer.answer = message.text
    answer.save()
    user.tg_answer_id = None
    current_bot = models.Bot.objects.filter(token=bot.token).last()
    user.company = current_bot.company
    user.save()
    bot.send_message(message.from_user.id, finish_text)
