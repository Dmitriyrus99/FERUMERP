# ferum_customs/integrations/telegram_bot.py
import frappe
from frappe import _
# import telegram # Если будете использовать библиотеку python-telegram-bot

# TELEGRAM_BOT_TOKEN = None # Будет загружаться из frappe.conf

# def get_telegram_bot_token():
#     global TELEGRAM_BOT_TOKEN
#     if TELEGRAM_BOT_TOKEN is None:
#         creds_config = frappe.conf.get("ferum_customs_credentials", {})
#         TELEGRAM_BOT_TOKEN = creds_config.get("telegram_bot_token")
#         if not TELEGRAM_BOT_TOKEN:
#             frappe.log_error(
#                 title=_("Ошибка конфигурации Telegram"),
#                 message=_("Токен Telegram бота не настроен в site_config.json ('ferum_customs_credentials.telegram_bot_token').")
#             )
#     return TELEGRAM_BOT_TOKEN

# def send_telegram_message(chat_id, message_text):
#     token = get_telegram_bot_token()
#     if not token:
#         return {"status": "error", "message": "Telegram token not configured"}
    
#     try:
#         bot = telegram.Bot(token=token)
#         bot.send_message(chat_id=chat_id, text=message_text, parse_mode=telegram.ParseMode.HTML)
#         frappe.logger().info(f"Сообщение отправлено в Telegram чат {chat_id}")
#         return {"status": "success"}
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "Telegram Send Message Error")
#         return {"status": "error", "message": str(e)}

# @frappe.whitelist()
# def handle_telegram_webhook(data=None):
#     """
#     Обработчик входящих сообщений от Telegram (если используется webhook).
#     """
#     if not data:
#         data = frappe.form_dict
    
#     token = get_telegram_bot_token()
#     if not token:
#         # Не отвечаем ничего, если токен не настроен, чтобы не раскрывать эндпоинт
#         return

    # frappe.logger().info(f"Получены данные от Telegram webhook: {data}")
    # Здесь будет логика обработки команды от пользователя
    # update = telegram.Update.de_json(data, bot) # Пример десериализации, если используется python-telegram-bot
    # chat_id = update.message.chat_id
    # text = update.message.text
    # ...
    # send_telegram_message(chat_id, f"Вы написали: {text}")
    # pass
