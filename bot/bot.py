# # import logging
# # import os
# # import tempfile

# # logger = logging.getLogger(__name__)

# # from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
# # from telegram.ext import (
# #     Application, CommandHandler, MessageHandler, ConversationHandler,
# #     CallbackQueryHandler, filters, ContextTypes,
# # )
# # from asgiref.sync import sync_to_async

# # # ── Conversation states ────────────────────────────────────────────────────────
# # LANG, PHONE, TEXT, FILE = range(4)

# # # ── Translations ───────────────────────────────────────────────────────────────
# # T = {
# #     'uz': {
# #         'welcome': (
# #             "⚖️ *LegalFlow*ga xush kelibsiz!\n\n"
# #             "Biz sizga professional yuridik yordam ko'rsatamiz.\n"
# #             "Tilni tanlang:"
# #         ),
# #         'lang_set': "Til o'rnatildi: O'zbek\n\nDavom etish uchun telefon raqamingizni ulashing.",
# #         'share_phone': "📱 Telefon raqamini ulashish",
# #         'phone_saved': (
# #             "✅ Telefon raqami saqlandi!\n\n"
# #             "Quyidagi buyruqlardan foydalaning:\n"
# #             "/new — Yangi ariza yuborish\n"
# #             "/status — Ariza holatini tekshirish\n"
# #             "/invoice — To'lov ma'lumotlari\n"
# #             "/help — Yordam"
# #         ),
# #         'need_start': "Iltimos, avval /start buyrug'ini bajaring.",
# #         'describe': "📝 Yuridik muammoingizni batafsil yozing:\n\n_(Masalan: shartnoma, oilaviy nizo, mehnat huquqi va h.k.)_",
# #         'attach_doc': "📎 Hujjat biriktiring (PDF, DOC, JPG) yoki o'tkazib yuboring:",
# #         'skip': "⏭ O'tkazib yuborish",
# #         'submitted': (
# #             "✅ *Arizangiz qabul qilindi!*\n\n"
# #             "🔖 Ariza raqami: *#{}*\n"
# #             "📋 Holat: Ko'rib chiqilmoqda\n\n"
# #             "Administrator tez orada siz bilan bog'lanadi.\n"
# #             "Holat tekshirish: /status"
# #         ),
# #         'no_requests': "Sizda hali ariza yo'q. /new buyrug'i bilan yangi ariza yuboring.",
# #         'your_requests': "📋 *Sizning arizalaringiz:*\n\n",
# #         'status_map': {
# #             'new': '🆕 Yangi',
# #             'reviewing': '🔍 Ko\'rib chiqilmoqda',
# #             'offered': '💼 Taklif yuborildi',
# #             'paid': '✅ To\'langan',
# #             'assigned': '👨‍⚖️ Yurist tayinlandi',
# #             'closed': '🏁 Yopildi',
# #         },
# #         'no_invoice': "Hozircha to'lov topilmadi.",
# #         'invoice_pending': "Hisob-faktura tayyorlanmoqda. Iltimos, kuting.",
# #         'invoice_info': (
# #             "💳 *Hisob-faktura ma'lumotlari*\n\n"
# #             "📄 Raqam: `{number}`\n"
# #             "💰 To'lov miqdori (10%): *{amount} UZS*\n"
# #             "📌 Holat: {status}"
# #         ),
# #         'paid_status': '✅ To\'langan',
# #         'pending_status': '⏳ Kutilmoqda',
# #         'cancelled': "❌ Bekor qilindi.",
# #         'help': (
# #             "⚖️ *LegalFlow — Yuridik Yordam*\n\n"
# #             "*Buyruqlar:*\n"
# #             "/start — Botni ishga tushirish\n"
# #             "/new — Yangi ariza yuborish\n"
# #             "/status — Ariza holatini tekshirish\n"
# #             "/invoice — To'lov ma'lumotlari\n"
# #             "/lang — Tilni o'zgartirish\n"
# #             "/cancel — Bekor qilish\n\n"
# #             "*Ish tartibi:*\n"
# #             "1. Ariza yuboring\n"
# #             "2. Administrator ko'rib chiqadi\n"
# #             "3. Taklif va hisob-faktura yuboriladi\n"
# #             "4. 10% to'lovdan so'ng yurist tayinlanadi\n"
# #             "5. Shaxsiy kabinetda muloqot"
# #         ),
# #     },
# #     'ru': {
# #         'welcome': (
# #             "⚖️ Добро пожаловать в *LegalFlow*!\n\n"
# #             "Мы оказываем профессиональную юридическую помощь.\n"
# #             "Выберите язык:"
# #         ),
# #         'lang_set': "Язык установлен: Русский\n\nПоделитесь номером телефона для продолжения.",
# #         'share_phone': "📱 Поделиться номером телефона",
# #         'phone_saved': (
# #             "✅ Номер телефона сохранён!\n\n"
# #             "Доступные команды:\n"
# #             "/new — Подать новую заявку\n"
# #             "/status — Проверить статус заявки\n"
# #             "/invoice — Информация об оплате\n"
# #             "/help — Помощь"
# #         ),
# #         'need_start': "Пожалуйста, сначала выполните команду /start.",
# #         'describe': "📝 Опишите вашу юридическую проблему подробно:\n\n_(Например: договор, семейный спор, трудовое право и т.д.)_",
# #         'attach_doc': "📎 Прикрепите документ (PDF, DOC, JPG) или пропустите:",
# #         'skip': "⏭ Пропустить",
# #         'submitted': (
# #             "✅ *Ваша заявка принята!*\n\n"
# #             "🔖 Номер заявки: *#{}*\n"
# #             "📋 Статус: На рассмотрении\n\n"
# #             "Администратор свяжется с вами в ближайшее время.\n"
# #             "Проверить статус: /status"
# #         ),
# #         'no_requests': "У вас пока нет заявок. Используйте /new для подачи заявки.",
# #         'your_requests': "📋 *Ваши заявки:*\n\n",
# #         'status_map': {
# #             'new': '🆕 Новая',
# #             'reviewing': '🔍 На рассмотрении',
# #             'offered': '💼 Предложение отправлено',
# #             'paid': '✅ Оплачено',
# #             'assigned': '👨‍⚖️ Юрист назначен',
# #             'closed': '🏁 Закрыта',
# #         },
# #         'no_invoice': "Счёт на оплату не найден.",
# #         'invoice_pending': "Счёт готовится. Пожалуйста, подождите.",
# #         'invoice_info': (
# #             "💳 *Информация о счёте*\n\n"
# #             "📄 Номер: `{number}`\n"
# #             "💰 Сумма к оплате (10%): *{amount} UZS*\n"
# #             "📌 Статус: {status}"
# #         ),
# #         'paid_status': '✅ Оплачено',
# #         'pending_status': '⏳ Ожидает оплаты',
# #         'cancelled': "❌ Отменено.",
# #         'help': (
# #             "⚖️ *LegalFlow — Юридическая помощь*\n\n"
# #             "*Команды:*\n"
# #             "/start — Запустить бота\n"
# #             "/new — Подать новую заявку\n"
# #             "/status — Проверить статус заявки\n"
# #             "/invoice — Информация об оплате\n"
# #             "/lang — Сменить язык\n"
# #             "/cancel — Отмена\n\n"
# #             "*Как это работает:*\n"
# #             "1. Подайте заявку\n"
# #             "2. Администратор рассмотрит её\n"
# #             "3. Вам отправят предложение и счёт\n"
# #             "4. После оплаты 10% назначается юрист\n"
# #             "5. Общение в личном кабинете"
# #         ),
# #     },
# #     'en': {
# #         'welcome': (
# #             "⚖️ Welcome to *LegalFlow*!\n\n"
# #             "We provide professional legal assistance.\n"
# #             "Please select your language:"
# #         ),
# #         'lang_set': "Language set: English\n\nPlease share your phone number to continue.",
# #         'share_phone': "📱 Share phone number",
# #         'phone_saved': (
# #             "✅ Phone number saved!\n\n"
# #             "Available commands:\n"
# #             "/new — Submit a new request\n"
# #             "/status — Check request status\n"
# #             "/invoice — Payment information\n"
# #             "/help — Help"
# #         ),
# #         'need_start': "Please run /start first.",
# #         'describe': "📝 Describe your legal issue in detail:\n\n_(e.g. contract dispute, family law, employment issue, etc.)_",
# #         'attach_doc': "📎 Attach a document (PDF, DOC, JPG) or skip:",
# #         'skip': "⏭ Skip",
# #         'submitted': (
# #             "✅ *Request submitted successfully!*\n\n"
# #             "🔖 Request ID: *#{}*\n"
# #             "📋 Status: Under review\n\n"
# #             "An administrator will contact you shortly.\n"
# #             "Check status: /status"
# #         ),
# #         'no_requests': "No requests found. Use /new to submit one.",
# #         'your_requests': "📋 *Your requests:*\n\n",
# #         'status_map': {
# #             'new': '🆕 New',
# #             'reviewing': '🔍 Under Review',
# #             'offered': '💼 Offer Sent',
# #             'paid': '✅ Paid',
# #             'assigned': '👨‍⚖️ Lawyer Assigned',
# #             'closed': '🏁 Closed',
# #         },
# #         'no_invoice': "No invoice found.",
# #         'invoice_pending': "Invoice is being prepared. Please wait.",
# #         'invoice_info': (
# #             "💳 *Invoice Details*\n\n"
# #             "📄 Number: `{number}`\n"
# #             "💰 Amount due (10%): *{amount} UZS*\n"
# #             "📌 Status: {status}"
# #         ),
# #         'paid_status': '✅ Paid',
# #         'pending_status': '⏳ Pending payment',
# #         'cancelled': "❌ Cancelled.",
# #         'help': (
# #             "⚖️ *LegalFlow — Legal Assistance*\n\n"
# #             "*Commands:*\n"
# #             "/start — Start the bot\n"
# #             "/new — Submit a new request\n"
# #             "/status — Check request status\n"
# #             "/invoice — Payment information\n"
# #             "/lang — Change language\n"
# #             "/cancel — Cancel\n\n"
# #             "*How it works:*\n"
# #             "1. Submit your request\n"
# #             "2. Admin reviews it\n"
# #             "3. You receive an offer and invoice\n"
# #             "4. After 10% payment, a lawyer is assigned\n"
# #             "5. Communicate via your personal cabinet"
# #         ),
# #     },
# # }


# # def t(context, key):
# #     lang = context.user_data.get('lang', 'ru')
# #     return T.get(lang, T['ru']).get(key, T['en'].get(key, key))


# # def lang_keyboard():
# #     return InlineKeyboardMarkup([
# #         [
# #             InlineKeyboardButton("🇺🇿 O'zbek", callback_data='lang_uz'),
# #             InlineKeyboardButton("🇷🇺 Русский", callback_data='lang_ru'),
# #             InlineKeyboardButton("🇬🇧 English", callback_data='lang_en'),
# #         ]
# #     ])


# # # ── /start ─────────────────────────────────────────────────────────────────────
# # async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     await update.message.reply_text(
# #         T['ru']['welcome'],
# #         reply_markup=lang_keyboard(),
# #         parse_mode='Markdown',
# #     )
# #     return LANG


# # async def select_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     query = update.callback_query
# #     await query.answer()
# #     lang = query.data.replace('lang_', '')
# #     context.user_data['lang'] = lang

# #     kb = [[KeyboardButton(T[lang]['share_phone'], request_contact=True)]]
# #     await query.edit_message_text(T[lang]['lang_set'], parse_mode='Markdown')
# #     await query.message.reply_text(
# #         T[lang]['lang_set'],
# #         reply_markup=ReplyKeyboardMarkup(kb, one_time_keyboard=True, resize_keyboard=True),
# #     )
# #     return PHONE


# # # ── /lang ──────────────────────────────────────────────────────────────────────
# # async def change_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     await update.message.reply_text(
# #         T['ru']['welcome'],
# #         reply_markup=lang_keyboard(),
# #         parse_mode='Markdown',
# #     )
# #     return LANG


# # # ── Phone ──────────────────────────────────────────────────────────────────────
# # async def receive_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     if update.message.contact:
# #         context.user_data['phone'] = update.message.contact.phone_number
# #     else:
# #         context.user_data['phone'] = update.message.text
# #     await update.message.reply_text(
# #         t(context, 'phone_saved'),
# #         reply_markup=ReplyKeyboardRemove(),
# #         parse_mode='Markdown',
# #     )
# #     return ConversationHandler.END


# # # ── /new ───────────────────────────────────────────────────────────────────────
# # async def new_request_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     if 'phone' not in context.user_data:
# #         await update.message.reply_text(t(context, 'need_start'))
# #         return ConversationHandler.END
# #     await update.message.reply_text(t(context, 'describe'), parse_mode='Markdown')
# #     return TEXT


# # async def receive_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     context.user_data['request_text'] = update.message.text
# #     kb = [[KeyboardButton(t(context, 'skip'))]]
# #     await update.message.reply_text(
# #         t(context, 'attach_doc'),
# #         reply_markup=ReplyKeyboardMarkup(kb, one_time_keyboard=True, resize_keyboard=True),
# #     )
# #     return FILE


# # async def receive_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     from django.core.files import File
# #     from contact.models import Request

# #     file_path = None
# #     if update.message.document or update.message.photo:
# #         tg_file = await (update.message.document or update.message.photo[-1]).get_file()
# #         ext = (
# #             'jpg' if update.message.photo
# #             else (update.message.document.file_name or 'file').rsplit('.', 1)[-1]
# #         )
# #         tmp = tempfile.NamedTemporaryFile(delete=False, suffix=f'.{ext}')
# #         tmp.close()
# #         await tg_file.download_to_drive(tmp.name)
# #         file_path = tmp.name

# #     chat_id = str(update.effective_chat.id)
# #     name = update.effective_user.full_name or 'Telegram User'
# #     phone = context.user_data.get('phone', '')
# #     text = context.user_data.get('request_text', '')

# #     @sync_to_async
# #     def save_request():
# #         req = Request(
# #             customer_name=name,
# #             phone=phone,
# #             text=text,
# #             source=Request.SOURCE_BOT,
# #             telegram_chat_id=chat_id,
# #         )
# #         if file_path:
# #             with open(file_path, 'rb') as f:
# #                 req.file.save(os.path.basename(file_path), File(f), save=False)
# #         req.save()
# #         return req.pk

# #     req_pk = await save_request()

# #     await update.message.reply_text(
# #         t(context, 'submitted').format(req_pk),
# #         reply_markup=ReplyKeyboardRemove(),
# #         parse_mode='Markdown',
# #     )
# #     context.user_data.pop('request_text', None)
# #     return ConversationHandler.END


# # async def skip_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     return await receive_file(update, context)


# # # ── /status ────────────────────────────────────────────────────────────────────
# # async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     from contact.models import Request
# #     chat_id = str(update.effective_chat.id)
# #     status_map = t(context, 'status_map')

# #     @sync_to_async
# #     def get_requests():
# #         return list(Request.objects.filter(telegram_chat_id=chat_id).order_by('-date')[:5])

# #     reqs = await get_requests()
# #     if not reqs:
# #         await update.message.reply_text(t(context, 'no_requests'))
# #         return

# #     lines = []
# #     for r in reqs:
# #         status_label = status_map.get(r.status, r.status)
# #         lines.append(f"*#{r.pk}* — {status_label}\n📅 {r.date.strftime('%d.%m.%Y %H:%M')}")

# #     await update.message.reply_text(
# #         t(context, 'your_requests') + "\n\n".join(lines),
# #         parse_mode='Markdown',
# #     )


# # # ── /invoice ───────────────────────────────────────────────────────────────────
# # async def invoice_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     from contact.models import Request
# #     chat_id = str(update.effective_chat.id)

# #     @sync_to_async
# #     def get_invoice_info():
# #         req = Request.objects.filter(
# #             telegram_chat_id=chat_id, status__in=['offered', 'paid']
# #         ).last()
# #         if not req:
# #             return None
# #         inv = getattr(req, 'invoice', None)
# #         if not inv:
# #             return 'no_invoice'
# #         return {'number': inv.invoice_number, 'amount': str(inv.ten_percent_amount), 'paid': inv.paid}

# #     info = await get_invoice_info()
# #     if info is None:
# #         await update.message.reply_text(t(context, 'no_invoice'))
# #     elif info == 'no_invoice':
# #         await update.message.reply_text(t(context, 'invoice_pending'))
# #     else:
# #         status = t(context, 'paid_status') if info['paid'] else t(context, 'pending_status')
# #         await update.message.reply_text(
# #             t(context, 'invoice_info').format(**info, status=status),
# #             parse_mode='Markdown',
# #         )


# # # ── /help ──────────────────────────────────────────────────────────────────────
# # async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     await update.message.reply_text(t(context, 'help'), parse_mode='Markdown')


# # # ── /cancel ────────────────────────────────────────────────────────────────────
# # async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     context.user_data.pop('request_text', None)
# #     await update.message.reply_text(t(context, 'cancelled'), reply_markup=ReplyKeyboardRemove())
# #     return ConversationHandler.END


# # # ── Build app ──────────────────────────────────────────────────────────────────
# # def build_application(token: str) -> Application:
# #     app = Application.builder().token(token).build()

# #     # /start + language selection
# #     start_conv = ConversationHandler(
# #         entry_points=[CommandHandler('start', start), CommandHandler('lang', change_language)],
# #         states={
# #             LANG: [CallbackQueryHandler(select_language, pattern='^lang_')],
# #             PHONE: [
# #                 MessageHandler(filters.CONTACT, receive_phone),
# #                 MessageHandler(filters.TEXT & ~filters.COMMAND, receive_phone),
# #             ],
# #         },
# #         fallbacks=[CommandHandler('cancel', cancel)],
# #     )

# #     # /new request flow
# #     new_conv = ConversationHandler(
# #         entry_points=[CommandHandler('new', new_request_start)],
# #         states={
# #             TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_text)],
# #             FILE: [
# #                 MessageHandler(filters.Document.ALL | filters.PHOTO, receive_file),
# #                 MessageHandler(filters.TEXT & ~filters.COMMAND, skip_file),
# #             ],
# #         },
# #         fallbacks=[CommandHandler('cancel', cancel)],
# #     )

# #     app.add_handler(start_conv)
# #     app.add_handler(new_conv)
# #     app.add_handler(CommandHandler('status', status_command))
# #     app.add_handler(CommandHandler('invoice', invoice_command))
# #     app.add_handler(CommandHandler('help', help_command))
# #     return app


# # if __name__ == '__main__':
# #     import sys
# #     import django
# #     sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# #     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'law_crm.settings')
# #     django.setup()
# #     from django.conf import settings as django_settings

# #     token = django_settings.TELEGRAM_BOT_TOKEN
# #     if not token or token == 'DEMO_NO_TOKEN':
# #         print("ERROR: Set TELEGRAM_BOT_TOKEN in your .env file first.")
# #     else:
# #         print("Starting LegalFlow bot...")
# #         build_application(token).run_polling()


# import logging
# import os
# import tempfile

# logger = logging.getLogger(__name__)

# from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
# from telegram.ext import (
#     Application, CommandHandler, MessageHandler, ConversationHandler,
#     CallbackQueryHandler, filters, ContextTypes,
# )
# from asgiref.sync import sync_to_async

# # ── Conversation states ────────────────────────────────────────────────────────
# LANG, PHONE, TEXT, FILE = range(4)

# # ── Translations (3 til: O'zbek, Rus, Ingliz) ─────────────────────────────────
# T = {
#     'uz': {
#         'welcome': (
#             "⚖️ *LegalFlow*ga xush kelibsiz!\n\n"
#             "Biz sizga professional yuridik yordam ko'rsatamiz.\n"
#             "Tilni tanlang:"
#         ),
#         'lang_set': "✅ Til o'rnatildi: O'zbek tili\n\n",
#         'ask_phone': "📱 Davom etish uchun telefon raqamingizni ulashing yoki yozing:",
#         'share_phone': "📱 Telefon raqamini ulashish",
#         'phone_saved': (
#             "✅ Telefon raqami saqlandi!\n\n"
#             "Quyidagi buyruqlardan foydalaning:\n"
#             "/new — Yangi ariza yuborish\n"
#             "/status — Ariza holatini tekshirish\n"
#             "/invoice — To'lov ma'lumotlari\n"
#             "/lang — Tilni o'zgartirish\n"
#             "/help — Yordam"
#         ),
#         'need_start': "❌ Iltimos, avval /start buyrug'ini bajaring.",
#         'describe': "📝 Yuridik muammoingizni batafsil yozing:\n\n_(Masalan: shartnoma, oilaviy nizo, mehnat huquqi va h.k.)_",
#         'attach_doc': "📎 Hujjat biriktiring (PDF, DOC, JPG) yoki quyidagi tugmani bosing:",
#         'skip': "⏭ O'tkazib yuborish",
#         'submitted': (
#             "✅ *Arizangiz qabul qilindi!*\n\n"
#             "🔖 Ariza raqami: *#{}*\n"
#             "📋 Holat: Ko'rib chiqilmoqda\n\n"
#             "Administrator tez orada siz bilan bog'lanadi.\n"
#             "Holat tekshirish: /status"
#         ),
#         'no_requests': "📭 Sizda hali ariza yo'q. /new buyrug'i bilan yangi ariza yuboring.",
#         'your_requests': "📋 *Sizning arizalaringiz:*\n\n",
#         'status_map': {
#             'new': '🆕 Yangi',
#             'reviewing': '🔍 Ko\'rib chiqilmoqda',
#             'offered': '💼 Taklif yuborildi',
#             'paid': '✅ To\'langan',
#             'assigned': '👨‍⚖️ Yurist tayinlandi',
#             'closed': '🏁 Yopildi',
#         },
#         'no_invoice': "📭 Hozircha to'lov topilmadi.",
#         'invoice_pending': "⏳ Hisob-faktura tayyorlanmoqda. Iltimos, kuting.",
#         'invoice_info': (
#             "💳 *Hisob-faktura ma'lumotlari*\n\n"
#             "📄 Raqam: `{}`\n"
#             "💰 To'lov miqdori (10%): *{} UZS*\n"
#             "📌 Holat: {}"
#         ),
#         'paid_status': '✅ To\'langan',
#         'pending_status': '⏳ Kutilmoqda',
#         'cancelled': "❌ Bekor qilindi.",
#         'help': (
#             "⚖️ *LegalFlow — Yuridik Yordam*\n\n"
#             "*Buyruqlar:*\n"
#             "/start — Botni ishga tushirish\n"
#             "/new — Yangi ariza yuborish\n"
#             "/status — Ariza holatini tekshirish\n"
#             "/invoice — To'lov ma'lumotlari\n"
#             "/lang — Tilni o'zgartirish\n"
#             "/cancel — Bekor qilish\n\n"
#             "*Ish tartibi:*\n"
#             "1️⃣ Ariza yuboring\n"
#             "2️⃣ Administrator ko'rib chiqadi\n"
#             "3️⃣ Taklif va hisob-faktura yuboriladi\n"
#             "4️⃣ 10% to'lovdan so'ng yurist tayinlanadi\n"
#             "5️⃣ Shaxsiy kabinetda muloqot"
#         ),
#         'error': "❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.",
#     },
#     'ru': {
#         'welcome': (
#             "⚖️ Добро пожаловать в *LegalFlow*!\n\n"
#             "Мы оказываем профессиональную юридическую помощь.\n"
#             "Выберите язык:"
#         ),
#         'lang_set': "✅ Язык установлен: Русский\n\n",
#         'ask_phone': "📱 Поделитесь номером телефона или введите его вручную:",
#         'share_phone': "📱 Поделиться номером телефона",
#         'phone_saved': (
#             "✅ Номер телефона сохранён!\n\n"
#             "Доступные команды:\n"
#             "/new — Подать новую заявку\n"
#             "/status — Проверить статус заявки\n"
#             "/invoice — Информация об оплате\n"
#             "/lang — Сменить язык\n"
#             "/help — Помощь"
#         ),
#         'need_start': "❌ Пожалуйста, сначала выполните команду /start.",
#         'describe': "📝 Опишите вашу юридическую проблему подробно:\n\n_(Например: договор, семейный спор, трудовое право и т.д.)_",
#         'attach_doc': "📎 Прикрепите документ (PDF, DOC, JPG) или нажмите кнопку ниже:",
#         'skip': "⏭ Пропустить",
#         'submitted': (
#             "✅ *Ваша заявка принята!*\n\n"
#             "🔖 Номер заявки: *#{}*\n"
#             "📋 Статус: На рассмотрении\n\n"
#             "Администратор свяжется с вами в ближайшее время.\n"
#             "Проверить статус: /status"
#         ),
#         'no_requests': "📭 У вас пока нет заявок. Используйте /new для подачи заявки.",
#         'your_requests': "📋 *Ваши заявки:*\n\n",
#         'status_map': {
#             'new': '🆕 Новая',
#             'reviewing': '🔍 На рассмотрении',
#             'offered': '💼 Предложение отправлено',
#             'paid': '✅ Оплачено',
#             'assigned': '👨‍⚖️ Юрист назначен',
#             'closed': '🏁 Закрыта',
#         },
#         'no_invoice': "📭 Счёт на оплату не найден.",
#         'invoice_pending': "⏳ Счёт готовится. Пожалуйста, подождите.",
#         'invoice_info': (
#             "💳 *Информация о счёте*\n\n"
#             "📄 Номер: `{}`\n"
#             "💰 Сумма к оплате (10%): *{} UZS*\n"
#             "📌 Статус: {}"
#         ),
#         'paid_status': '✅ Оплачено',
#         'pending_status': '⏳ Ожидает оплаты',
#         'cancelled': "❌ Отменено.",
#         'help': (
#             "⚖️ *LegalFlow — Юридическая помощь*\n\n"
#             "*Команды:*\n"
#             "/start — Запустить бота\n"
#             "/new — Подать новую заявку\n"
#             "/status — Проверить статус заявки\n"
#             "/invoice — Информация об оплате\n"
#             "/lang — Сменить язык\n"
#             "/cancel — Отмена\n\n"
#             "*Как это работает:*\n"
#             "1️⃣ Подайте заявку\n"
#             "2️⃣ Администратор рассмотрит её\n"
#             "3️⃣ Вам отправят предложение и счёт\n"
#             "4️⃣ После оплаты 10% назначается юрист\n"
#             "5️⃣ Общение в личном кабинете"
#         ),
#         'error': "❌ Произошла ошибка. Пожалуйста, попробуйте снова.",
#     },
#     'en': {
#         'welcome': (
#             "⚖️ Welcome to *LegalFlow*!\n\n"
#             "We provide professional legal assistance.\n"
#             "Please select your language:"
#         ),
#         'lang_set': "✅ Language set: English\n\n",
#         'ask_phone': "📱 Please share your phone number or enter it manually:",
#         'share_phone': "📱 Share phone number",
#         'phone_saved': (
#             "✅ Phone number saved!\n\n"
#             "Available commands:\n"
#             "/new — Submit a new request\n"
#             "/status — Check request status\n"
#             "/invoice — Payment information\n"
#             "/lang — Change language\n"
#             "/help — Help"
#         ),
#         'need_start': "❌ Please run /start first.",
#         'describe': "📝 Describe your legal issue in detail:\n\n_(e.g. contract dispute, family law, employment issue, etc.)_",
#         'attach_doc': "📎 Attach a document (PDF, DOC, JPG) or press the button below:",
#         'skip': "⏭ Skip",
#         'submitted': (
#             "✅ *Request submitted successfully!*\n\n"
#             "🔖 Request ID: *#{}*\n"
#             "📋 Status: Under review\n\n"
#             "An administrator will contact you shortly.\n"
#             "Check status: /status"
#         ),
#         'no_requests': "📭 No requests found. Use /new to submit one.",
#         'your_requests': "📋 *Your requests:*\n\n",
#         'status_map': {
#             'new': '🆕 New',
#             'reviewing': '🔍 Under Review',
#             'offered': '💼 Offer Sent',
#             'paid': '✅ Paid',
#             'assigned': '👨‍⚖️ Lawyer Assigned',
#             'closed': '🏁 Closed',
#         },
#         'no_invoice': "📭 No invoice found.",
#         'invoice_pending': "⏳ Invoice is being prepared. Please wait.",
#         'invoice_info': (
#             "💳 *Invoice Details*\n\n"
#             "📄 Number: `{}`\n"
#             "💰 Amount due (10%): *{} UZS*\n"
#             "📌 Status: {}"
#         ),
#         'paid_status': '✅ Paid',
#         'pending_status': '⏳ Pending',
#         'cancelled': "❌ Cancelled.",
#         'help': (
#             "⚖️ *LegalFlow — Legal Assistance*\n\n"
#             "*Commands:*\n"
#             "/start — Start the bot\n"
#             "/new — Submit a new request\n"
#             "/status — Check request status\n"
#             "/invoice — Payment information\n"
#             "/lang — Change language\n"
#             "/cancel — Cancel\n\n"
#             "*How it works:*\n"
#             "1️⃣ Submit your request\n"
#             "2️⃣ Admin reviews it\n"
#             "3️⃣ You receive an offer and invoice\n"
#             "4️⃣ After 10% payment, a lawyer is assigned\n"
#             "5️⃣ Communicate via your personal cabinet"
#         ),
#         'error': "❌ An error occurred. Please try again.",
#     },
# }


# def get_text(context: ContextTypes.DEFAULT_TYPE, key: str, *args) -> str:
#     """Tilga qarab matn qaytarish"""
#     lang = context.user_data.get('lang', 'ru')
#     text = T.get(lang, T['ru']).get(key, T['en'].get(key, key))
#     if args:
#         return text.format(*args)
#     return text


# def get_lang_keyboard():
#     """3 tilda til tanlash tugmalari"""
#     return InlineKeyboardMarkup([
#         [
#             InlineKeyboardButton("🇺🇿 O'zbek", callback_data='lang_uz'),
#             InlineKeyboardButton("🇷🇺 Русский", callback_data='lang_ru'),
#             InlineKeyboardButton("🇬🇧 English", callback_data='lang_en'),
#         ]
#     ])


# def get_phone_keyboard(context: ContextTypes.DEFAULT_TYPE):
#     """Telefon raqam ulashish tugmasi (tanlangan tilda)"""
#     lang = context.user_data.get('lang', 'ru')
#     button_text = T[lang]['share_phone']
#     return ReplyKeyboardMarkup(
#         [[KeyboardButton(button_text, request_contact=True)]],
#         one_time_keyboard=True,
#         resize_keyboard=True
#     )


# def get_skip_keyboard(context: ContextTypes.DEFAULT_TYPE):
#     """O'tkazib yuborish tugmasi (tanlangan tilda)"""
#     lang = context.user_data.get('lang', 'ru')
#     button_text = T[lang]['skip']
#     return ReplyKeyboardMarkup(
#         [[KeyboardButton(button_text)]],
#         one_time_keyboard=True,
#         resize_keyboard=True
#     )


# # ── /start ─────────────────────────────────────────────────────────────────────
# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Botni ishga tushirish va til tanlash"""
#     await update.message.reply_text(
#         T['ru']['welcome'],  # Default til - rus
#         reply_markup=get_lang_keyboard(),
#         parse_mode='Markdown',
#     )
#     return LANG


# async def select_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Til tanlangandan keyin telefon raqam so'rash"""
#     query = update.callback_query
#     await query.answer()
    
#     lang = query.data.replace('lang_', '')
#     context.user_data['lang'] = lang
    
#     # Til tanlanganligi haqida xabar
#     await query.edit_message_text(
#         get_text(context, 'lang_set'),
#         parse_mode='Markdown',
#     )
    
#     # Telefon raqam so'rash
#     await query.message.reply_text(
#         get_text(context, 'ask_phone'),
#         reply_markup=get_phone_keyboard(context),
#     )
#     return PHONE


# # ── /lang (tilni o'zgartirish) ─────────────────────────────────────────────────
# async def change_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Tilni o'zgartirish buyrug'i"""
#     await update.message.reply_text(
#         T['ru']['welcome'],
#         reply_markup=get_lang_keyboard(),
#         parse_mode='Markdown',
#     )
#     return LANG


# # ── Phone (telefon raqam) ─────────────────────────────────────────────────────
# async def receive_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Telefon raqamni qabul qilish"""
#     if update.message.contact:
#         context.user_data['phone'] = update.message.contact.phone_number
#     else:
#         context.user_data['phone'] = update.message.text.strip()
    
#     await update.message.reply_text(
#         get_text(context, 'phone_saved'),
#         reply_markup=ReplyKeyboardRemove(),
#         parse_mode='Markdown',
#     )
#     return ConversationHandler.END


# # ── /new (yangi ariza) ────────────────────────────────────────────────────────
# async def new_request_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Yangi ariza yuborish - matn so'rash"""
#     if 'phone' not in context.user_data:
#         await update.message.reply_text(get_text(context, 'need_start'))
#         return ConversationHandler.END
    
#     await update.message.reply_text(
#         get_text(context, 'describe'),
#         parse_mode='Markdown',
#     )
#     return TEXT


# async def receive_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Ariza matnini qabul qilish"""
#     context.user_data['request_text'] = update.message.text
    
#     await update.message.reply_text(
#         get_text(context, 'attach_doc'),
#         reply_markup=get_skip_keyboard(context),
#     )
#     return FILE


# async def receive_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Faylni qabul qilish va arizani saqlash"""
#     from django.core.files import File
#     from contact.models import Request
    
#     file_path = None
    
#     # Faylni yuklab olish
#     if update.message.document:
#         tg_file = await update.message.document.get_file()
#         file_name = update.message.document.file_name or 'document'
#         ext = file_name.rsplit('.', 1)[-1] if '.' in file_name else 'bin'
#         tmp = tempfile.NamedTemporaryFile(delete=False, suffix=f'.{ext}')
#         tmp.close()
#         await tg_file.download_to_drive(tmp.name)
#         file_path = tmp.name
        
#     elif update.message.photo:
#         tg_file = await update.message.photo[-1].get_file()
#         tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
#         tmp.close()
#         await tg_file.download_to_drive(tmp.name)
#         file_path = tmp.name
    
#     chat_id = str(update.effective_chat.id)
#     name = update.effective_user.full_name or 'Telegram User'
#     phone = context.user_data.get('phone', '')
#     text = context.user_data.get('request_text', '')
    
#     @sync_to_async
#     def save_request():
#         req = Request(
#             customer_name=name,
#             phone=phone,
#             text=text,
#             source=Request.SOURCE_BOT,
#             telegram_chat_id=chat_id,
#         )
#         if file_path:
#             with open(file_path, 'rb') as f:
#                 req.file.save(os.path.basename(file_path), File(f), save=False)
#         req.save()
#         return req.pk
    
#     try:
#         req_pk = await save_request()
        
#         # Vaqtinchalik faylni o'chirish
#         if file_path and os.path.exists(file_path):
#             os.unlink(file_path)
        
#         await update.message.reply_text(
#             get_text(context, 'submitted', req_pk),
#             reply_markup=ReplyKeyboardRemove(),
#             parse_mode='Markdown',
#         )
#     except Exception as e:
#         logger.error(f"Error saving request: {e}")
#         await update.message.reply_text(get_text(context, 'error'))
    
#     context.user_data.pop('request_text', None)
#     return ConversationHandler.END


# async def skip_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Faylni o'tkazib yuborish"""
#     return await receive_file(update, context)


# # ── /status ────────────────────────────────────────────────────────────────────
# async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Ariza holatini tekshirish"""
#     from contact.models import Request
    
#     chat_id = str(update.effective_chat.id)
#     status_map = T.get(context.user_data.get('lang', 'ru'), {}).get('status_map', {})
    
#     @sync_to_async
#     def get_requests():
#         return list(Request.objects.filter(
#             telegram_chat_id=chat_id
#         ).order_by('-date')[:10])
    
#     try:
#         reqs = await get_requests()
#         if not reqs:
#             await update.message.reply_text(get_text(context, 'no_requests'))
#             return
        
#         lines = [get_text(context, 'your_requests')]
#         for r in reqs:
#             status_label = status_map.get(r.status, r.status)
#             lines.append(f"*#{r.pk}* — {status_label}\n📅 {r.date.strftime('%d.%m.%Y %H:%M')}")
        
#         await update.message.reply_text(
#             "\n\n".join(lines),
#             parse_mode='Markdown',
#         )
#     except Exception as e:
#         logger.error(f"Error getting status: {e}")
#         await update.message.reply_text(get_text(context, 'error'))


# # ── /invoice ───────────────────────────────────────────────────────────────────
# async def invoice_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """To'lov ma'lumotlarini ko'rish"""
#     from contact.models import Request
    
#     chat_id = str(update.effective_chat.id)
    
#     @sync_to_async
#     def get_invoice_info():
#         req = Request.objects.filter(
#             telegram_chat_id=chat_id, status__in=['offered', 'paid']
#         ).last()
#         if not req:
#             return None
#         inv = getattr(req, 'invoice', None)
#         if not inv:
#             return 'no_invoice'
#         return {
#             'number': inv.invoice_number,
#             'amount': str(inv.ten_percent_amount),
#             'paid': inv.paid
#         }
    
#     try:
#         info = await get_invoice_info()
        
#         if info is None:
#             await update.message.reply_text(get_text(context, 'no_invoice'))
#         elif info == 'no_invoice':
#             await update.message.reply_text(get_text(context, 'invoice_pending'))
#         else:
#             status = get_text(context, 'paid_status') if info['paid'] else get_text(context, 'pending_status')
#             await update.message.reply_text(
#                 get_text(context, 'invoice_info', info['number'], info['amount'], status),
#                 parse_mode='Markdown',
#             )
#     except Exception as e:
#         logger.error(f"Error getting invoice: {e}")
#         await update.message.reply_text(get_text(context, 'error'))


# # ── /help ──────────────────────────────────────────────────────────────────────
# async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Yordam buyrug'i"""
#     await update.message.reply_text(
#         get_text(context, 'help'),
#         parse_mode='Markdown',
#     )


# # ── /cancel ────────────────────────────────────────────────────────────────────
# async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Bekor qilish"""
#     context.user_data.pop('request_text', None)
#     await update.message.reply_text(
#         get_text(context, 'cancelled'),
#         reply_markup=ReplyKeyboardRemove(),
#     )
#     return ConversationHandler.END


# # ── Build application ──────────────────────────────────────────────────────────
# def build_application(token: str) -> Application:
#     """Bot aplikatsiyasini yaratish"""
#     app = Application.builder().token(token).build()
    
#     # /start + language selection conversation (persistent=True qo'shildi)
#     start_conv = ConversationHandler(
#         entry_points=[CommandHandler('start', start), CommandHandler('lang', change_language)],
#         states={
#             LANG: [CallbackQueryHandler(select_language, pattern='^lang_')],
#             PHONE: [
#                 MessageHandler(filters.CONTACT, receive_phone),
#                 MessageHandler(filters.TEXT & ~filters.COMMAND, receive_phone),
#             ],
#         },
#         fallbacks=[CommandHandler('cancel', cancel)],
#         name="start_conversation",
#         persistent=True,
#     )
    
#     # /new request conversation
#     new_conv = ConversationHandler(
#         entry_points=[CommandHandler('new', new_request_start)],
#         states={
#             TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_text)],
#             FILE: [
#                 MessageHandler(filters.Document.ALL | filters.PHOTO, receive_file),
#                 MessageHandler(filters.TEXT & ~filters.COMMAND, skip_file),
#             ],
#         },
#         fallbacks=[CommandHandler('cancel', cancel)],
#         name="new_request_conversation",
#         persistent=True,
#     )
    
#     # Handlerlarni qo'shish
#     app.add_handler(start_conv)
#     app.add_handler(new_conv)
#     app.add_handler(CommandHandler('status', status_command))
#     app.add_handler(CommandHandler('invoice', invoice_command))
#     app.add_handler(CommandHandler('help', help_command))
#     app.add_handler(CommandHandler('lang', change_language))
    
#     return app


# # ── Main ───────────────────────────────────────────────────────────────────────
# if __name__ == '__main__':
#     import sys
#     import django
    
#     # Django sozlamalarini yuklash
#     sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'law_crm.settings')
#     django.setup()
    
#     from django.conf import settings as django_settings
    
#     token = getattr(django_settings, 'TELEGRAM_BOT_TOKEN', None)
    
#     if not token or token == 'DEMO_NO_TOKEN':
#         print("❌ ERROR: Set TELEGRAM_BOT_TOKEN in your .env file first.")
#         print("   Example: TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz")
#     else:
#         print("🤖 Starting LegalFlow bot...")
#         print(f"✅ Bot token loaded: {token[:15]}...")
#         print("🌍 Supported languages: O'zbek, Русский, English")
#         print("📱 Bot is running. Press Ctrl+C to stop.")
        
#         # Botni ishga tushirish
#         application = build_application(token)
#         application.run_polling(allowed_updates=Update.ALL_TYPES)
import logging
import os
import tempfile

logger = logging.getLogger(__name__)

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application, CommandHandler, MessageHandler, ConversationHandler,
    CallbackQueryHandler, filters, ContextTypes, PicklePersistence  # PicklePersistence qo'shildi
)
from asgiref.sync import sync_to_async

# ── Conversation states ────────────────────────────────────────────────────────
LANG, PHONE, TEXT, FILE = range(4)

# ── Translations (3 til: O'zbek, Rus, Ingliz) ─────────────────────────────────
T = {
    'uz': {
        'welcome': (
            "⚖️ *LegalFlow*ga xush kelibsiz!\n\n"
            "Biz sizga professional yuridik yordam ko'rsatamiz.\n"
            "Tilni tanlang:"
        ),
        'lang_set': "✅ Til o'rnatildi: O'zbek tili\n\n",
        'ask_phone': "📱 Davom etish uchun telefon raqamingizni ulashing yoki yozing:",
        'share_phone': "📱 Telefon raqamini ulashish",
        'phone_saved': (
            "✅ Telefon raqami saqlandi!\n\n"
            "Quyidagi buyruqlardan foydalaning:\n"
            "/new — Yangi ariza yuborish\n"
            "/status — Ariza holatini tekshirish\n"
            "/invoice — To'lov ma'lumotlari\n"
            "/lang — Tilni o'zgartirish\n"
            "/help — Yordam"
        ),
        'need_start': "❌ Iltimos, avval /start buyrug'ini bajaring.",
        'describe': "📝 Yuridik muammoingizni batafsil yozing:\n\n_(Masalan: shartnoma, oilaviy nizo, mehnat huquqi va h.k.)_",
        'attach_doc': "📎 Hujjat biriktiring (PDF, DOC, JPG) yoki quyidagi tugmani bosing:",
        'skip': "⏭ O'tkazib yuborish",
        'submitted': (
            "✅ *Arizangiz qabul qilindi!*\n\n"
            "🔖 Ariza raqami: *#{}*\n"
            "📋 Holat: Ko'rib chiqilmoqda\n\n"
            "Administrator tez orada siz bilan bog'lanadi.\n"
            "Holat tekshirish: /status"
        ),
        'no_requests': "📭 Sizda hali ariza yo'q. /new buyrug'i bilan yangi ariza yuboring.",
        'your_requests': "📋 *Sizning arizalaringiz:*\n\n",
        'status_map': {
            'new': '🆕 Yangi',
            'reviewing': '🔍 Ko\'rib chiqilmoqda',
            'offered': '💼 Taklif yuborildi',
            'paid': '✅ To\'langan',
            'assigned': '👨‍⚖️ Yurist tayinlandi',
            'closed': '🏁 Yopildi',
        },
        'no_invoice': "📭 Hozircha to'lov topilmadi.",
        'invoice_pending': "⏳ Hisob-faktura tayyorlanmoqda. Iltimos, kuting.",
        'invoice_info': (
            "💳 *Hisob-faktura ma'lumotlari*\n\n"
            "📄 Raqam: `{}`\n"
            "💰 To'lov miqdori (10%): *{} UZS*\n"
            "📌 Holat: {}"
        ),
        'paid_status': '✅ To\'langan',
        'pending_status': '⏳ Kutilmoqda',
        'cancelled': "❌ Bekor qilindi.",
        'help': (
            "⚖️ *LegalFlow — Yuridik Yordam*\n\n"
            "*Buyruqlar:*\n"
            "/start — Botni ishga tushirish\n"
            "/new — Yangi ariza yuborish\n"
            "/status — Ariza holatini tekshirish\n"
            "/invoice — To'lov ma'lumotlari\n"
            "/lang — Tilni o'zgartirish\n"
            "/cancel — Bekor qilish\n\n"
            "*Ish tartibi:*\n"
            "1️⃣ Ariza yuboring\n"
            "2️⃣ Administrator ko'rib chiqadi\n"
            "3️⃣ Taklif va hisob-faktura yuboriladi\n"
            "4️⃣ 10% to'lovdan so'ng yurist tayinlanadi\n"
            "5️⃣ Shaxsiy kabinetda muloqot"
        ),
        'error': "❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.",
    },
    'ru': {
        'welcome': (
            "⚖️ Добро пожаловать в *LegalFlow*!\n\n"
            "Мы оказываем профессиональную юридическую помощь.\n"
            "Выберите язык:"
        ),
        'lang_set': "✅ Язык установлен: Русский\n\n",
        'ask_phone': "📱 Поделитесь номером телефона или введите его вручную:",
        'share_phone': "📱 Поделиться номером телефона",
        'phone_saved': (
            "✅ Номер телефона сохранён!\n\n"
            "Доступные команды:\n"
            "/new — Подать новую заявку\n"
            "/status — Проверить статус заявки\n"
            "/invoice — Информация об оплате\n"
            "/lang — Сменить язык\n"
            "/help — Помощь"
        ),
        'need_start': "❌ Пожалуйста, сначала выполните команду /start.",
        'describe': "📝 Опишите вашу юридическую проблему подробно:\n\n_(Например: договор, семейный спор, трудовое право и т.д.)_",
        'attach_doc': "📎 Прикрепите документ (PDF, DOC, JPG) или нажмите кнопку ниже:",
        'skip': "⏭ Пропустить",
        'submitted': (
            "✅ *Ваша заявка принята!*\n\n"
            "🔖 Номер заявки: *#{}*\n"
            "📋 Статус: На рассмотрении\n\n"
            "Администратор свяжется с вами в ближайшее время.\n"
            "Проверить статус: /status"
        ),
        'no_requests': "📭 У вас пока нет заявок. Используйте /new для подачи заявки.",
        'your_requests': "📋 *Ваши заявки:*\n\n",
        'status_map': {
            'new': '🆕 Новая',
            'reviewing': '🔍 На рассмотрении',
            'offered': '💼 Предложение отправлено',
            'paid': '✅ Оплачено',
            'assigned': '👨‍⚖️ Юрист назначен',
            'closed': '🏁 Закрыта',
        },
        'no_invoice': "📭 Счёт на оплату не найден.",
        'invoice_pending': "⏳ Счёт готовится. Пожалуйста, подождите.",
        'invoice_info': (
            "💳 *Информация о счёте*\n\n"
            "📄 Номер: `{}`\n"
            "💰 Сумма к оплате (10%): *{} UZS*\n"
            "📌 Статус: {}"
        ),
        'paid_status': '✅ Оплачено',
        'pending_status': '⏳ Ожидает оплаты',
        'cancelled': "❌ Отменено.",
        'help': (
            "⚖️ *LegalFlow — Юридическая помощь*\n\n"
            "*Команды:*\n"
            "/start — Запустить бота\n"
            "/new — Подать новую заявку\n"
            "/status — Проверить статус заявки\n"
            "/invoice — Информация об оплате\n"
            "/lang — Сменить язык\n"
            "/cancel — Отмена\n\n"
            "*Как это работает:*\n"
            "1️⃣ Подайте заявку\n"
            "2️⃣ Администратор рассмотрит её\n"
            "3️⃣ Вам отправят предложение и счёт\n"
            "4️⃣ После оплаты 10% назначается юрист\n"
            "5️⃣ Общение в личном кабинете"
        ),
        'error': "❌ Произошла ошибка. Пожалуйста, попробуйте снова.",
    },
    'en': {
        'welcome': (
            "⚖️ Welcome to *LegalFlow*!\n\n"
            "We provide professional legal assistance.\n"
            "Please select your language:"
        ),
        'lang_set': "✅ Language set: English\n\n",
        'ask_phone': "📱 Please share your phone number or enter it manually:",
        'share_phone': "📱 Share phone number",
        'phone_saved': (
            "✅ Phone number saved!\n\n"
            "Available commands:\n"
            "/new — Submit a new request\n"
            "/status — Check request status\n"
            "/invoice — Payment information\n"
            "/lang — Change language\n"
            "/help — Help"
        ),
        'need_start': "❌ Please run /start first.",
        'describe': "📝 Describe your legal issue in detail:\n\n_(e.g. contract dispute, family law, employment issue, etc.)_",
        'attach_doc': "📎 Attach a document (PDF, DOC, JPG) or press the button below:",
        'skip': "⏭ Skip",
        'submitted': (
            "✅ *Request submitted successfully!*\n\n"
            "🔖 Request ID: *#{}*\n"
            "📋 Status: Under review\n\n"
            "An administrator will contact you shortly.\n"
            "Check status: /status"
        ),
        'no_requests': "📭 No requests found. Use /new to submit one.",
        'your_requests': "📋 *Your requests:*\n\n",
        'status_map': {
            'new': '🆕 New',
            'reviewing': '🔍 Under Review',
            'offered': '💼 Offer Sent',
            'paid': '✅ Paid',
            'assigned': '👨‍⚖️ Lawyer Assigned',
            'closed': '🏁 Closed',
        },
        'no_invoice': "📭 No invoice found.",
        'invoice_pending': "⏳ Invoice is being prepared. Please wait.",
        'invoice_info': (
            "💳 *Invoice Details*\n\n"
            "📄 Number: `{}`\n"
            "💰 Amount due (10%): *{} UZS*\n"
            "📌 Status: {}"
        ),
        'paid_status': '✅ Paid',
        'pending_status': '⏳ Pending',
        'cancelled': "❌ Cancelled.",
        'help': (
            "⚖️ *LegalFlow — Legal Assistance*\n\n"
            "*Commands:*\n"
            "/start — Start the bot\n"
            "/new — Submit a new request\n"
            "/status — Check request status\n"
            "/invoice — Payment information\n"
            "/lang — Change language\n"
            "/cancel — Cancel\n\n"
            "*How it works:*\n"
            "1️⃣ Submit your request\n"
            "2️⃣ Admin reviews it\n"
            "3️⃣ You receive an offer and invoice\n"
            "4️⃣ After 10% payment, a lawyer is assigned\n"
            "5️⃣ Communicate via your personal cabinet"
        ),
        'error': "❌ An error occurred. Please try again.",
    },
}


def get_text(context: ContextTypes.DEFAULT_TYPE, key: str, *args) -> str:
    """Tilga qarab matn qaytarish"""
    lang = context.user_data.get('lang', 'ru')
    text = T.get(lang, T['ru']).get(key, T['en'].get(key, key))
    if args:
        return text.format(*args)
    return text


def get_lang_keyboard():
    """3 tilda til tanlash tugmalari"""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🇺🇿 O'zbek", callback_data='lang_uz'),
            InlineKeyboardButton("🇷🇺 Русский", callback_data='lang_ru'),
            InlineKeyboardButton("🇬🇧 English", callback_data='lang_en'),
        ]
    ])


def get_phone_keyboard(context: ContextTypes.DEFAULT_TYPE):
    """Telefon raqam ulashish tugmasi (tanlangan tilda)"""
    lang = context.user_data.get('lang', 'ru')
    button_text = T[lang]['share_phone']
    return ReplyKeyboardMarkup(
        [[KeyboardButton(button_text, request_contact=True)]],
        one_time_keyboard=True,
        resize_keyboard=True
    )


def get_skip_keyboard(context: ContextTypes.DEFAULT_TYPE):
    """O'tkazib yuborish tugmasi (tanlangan tilda)"""
    lang = context.user_data.get('lang', 'ru')
    button_text = T[lang]['skip']
    return ReplyKeyboardMarkup(
        [[KeyboardButton(button_text)]],
        one_time_keyboard=True,
        resize_keyboard=True
    )


# ── /start ─────────────────────────────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Botni ishga tushirish va til tanlash"""
    await update.message.reply_text(
        T['ru']['welcome'],  # Default til - rus
        reply_markup=get_lang_keyboard(),
        parse_mode='Markdown',
    )
    return LANG


async def select_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Til tanlangandan keyin telefon raqam so'rash"""
    query = update.callback_query
    await query.answer()
    
    lang = query.data.replace('lang_', '')
    context.user_data['lang'] = lang
    
    # Til tanlanganligi haqida xabar
    await query.edit_message_text(
        get_text(context, 'lang_set'),
        parse_mode='Markdown',
    )
    
    # Telefon raqam so'rash
    await query.message.reply_text(
        get_text(context, 'ask_phone'),
        reply_markup=get_phone_keyboard(context),
    )
    return PHONE


# ── /lang (tilni o'zgartirish) ─────────────────────────────────────────────────
async def change_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tilni o'zgartirish buyrug'i"""
    await update.message.reply_text(
        T['ru']['welcome'],
        reply_markup=get_lang_keyboard(),
        parse_mode='Markdown',
    )
    return LANG


# ── Phone (telefon raqam) ─────────────────────────────────────────────────────
async def receive_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Telefon raqamni qabul qilish"""
    if update.message.contact:
        context.user_data['phone'] = update.message.contact.phone_number
    else:
        context.user_data['phone'] = update.message.text.strip()
    
    await update.message.reply_text(
        get_text(context, 'phone_saved'),
        reply_markup=ReplyKeyboardRemove(),
        parse_mode='Markdown',
    )
    return ConversationHandler.END


# ── /new (yangi ariza) ────────────────────────────────────────────────────────
async def new_request_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Yangi ariza yuborish - matn so'rash"""
    if 'phone' not in context.user_data:
        await update.message.reply_text(get_text(context, 'need_start'))
        return ConversationHandler.END
    
    await update.message.reply_text(
        get_text(context, 'describe'),
        parse_mode='Markdown',
    )
    return TEXT


async def receive_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ariza matnini qabul qilish"""
    context.user_data['request_text'] = update.message.text
    
    await update.message.reply_text(
        get_text(context, 'attach_doc'),
        reply_markup=get_skip_keyboard(context),
    )
    return FILE


async def receive_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Faylni qabul qilish va arizani saqlash"""
    from django.core.files import File
    from contact.models import Request
    
    file_path = None
    
    # Faylni yuklab olish
    if update.message.document:
        tg_file = await update.message.document.get_file()
        file_name = update.message.document.file_name or 'document'
        ext = file_name.rsplit('.', 1)[-1] if '.' in file_name else 'bin'
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=f'.{ext}')
        tmp.close()
        await tg_file.download_to_drive(tmp.name)
        file_path = tmp.name
        
    elif update.message.photo:
        tg_file = await update.message.photo[-1].get_file()
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
        tmp.close()
        await tg_file.download_to_drive(tmp.name)
        file_path = tmp.name
    
    chat_id = str(update.effective_chat.id)
    name = update.effective_user.full_name or 'Telegram User'
    phone = context.user_data.get('phone', '')
    text = context.user_data.get('request_text', '')
    
    @sync_to_async
    def save_request():
        req = Request(
            customer_name=name,
            phone=phone,
            text=text,
            source=Request.SOURCE_BOT,
            telegram_chat_id=chat_id,
        )
        if file_path:
            with open(file_path, 'rb') as f:
                req.file.save(os.path.basename(file_path), File(f), save=False)
        req.save()
        return req.pk
    
    try:
        req_pk = await save_request()
        
        # Vaqtinchalik faylni o'chirish
        if file_path and os.path.exists(file_path):
            os.unlink(file_path)
        
        await update.message.reply_text(
            get_text(context, 'submitted', req_pk),
            reply_markup=ReplyKeyboardRemove(),
            parse_mode='Markdown',
        )
    except Exception as e:
        logger.error(f"Error saving request: {e}")
        await update.message.reply_text(get_text(context, 'error'))
    
    context.user_data.pop('request_text', None)
    return ConversationHandler.END


async def skip_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Faylni o'tkazib yuborish"""
    return await receive_file(update, context)


# ── /status ────────────────────────────────────────────────────────────────────
async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ariza holatini tekshirish"""
    from contact.models import Request
    
    chat_id = str(update.effective_chat.id)
    status_map = T.get(context.user_data.get('lang', 'ru'), {}).get('status_map', {})
    
    @sync_to_async
    def get_requests():
        return list(Request.objects.filter(
            telegram_chat_id=chat_id
        ).order_by('-date')[:10])
    
    try:
        reqs = await get_requests()
        if not reqs:
            await update.message.reply_text(get_text(context, 'no_requests'))
            return
        
        lines = [get_text(context, 'your_requests')]
        for r in reqs:
            status_label = status_map.get(r.status, r.status)
            lines.append(f"*#{r.pk}* — {status_label}\n📅 {r.date.strftime('%d.%m.%Y %H:%M')}")
        
        await update.message.reply_text(
            "\n\n".join(lines),
            parse_mode='Markdown',
        )
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        await update.message.reply_text(get_text(context, 'error'))


# ── /invoice ───────────────────────────────────────────────────────────────────
async def invoice_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """To'lov ma'lumotlarini ko'rish"""
    from contact.models import Request
    
    chat_id = str(update.effective_chat.id)
    
    @sync_to_async
    def get_invoice_info():
        req = Request.objects.filter(
            telegram_chat_id=chat_id, status__in=['offered', 'paid']
        ).last()
        if not req:
            return None
        inv = getattr(req, 'invoice', None)
        if not inv:
            return 'no_invoice'
        return {
            'number': inv.invoice_number,
            'amount': str(inv.ten_percent_amount),
            'paid': inv.paid
        }
    
    try:
        info = await get_invoice_info()
        
        if info is None:
            await update.message.reply_text(get_text(context, 'no_invoice'))
        elif info == 'no_invoice':
            await update.message.reply_text(get_text(context, 'invoice_pending'))
        else:
            status = get_text(context, 'paid_status') if info['paid'] else get_text(context, 'pending_status')
            await update.message.reply_text(
                get_text(context, 'invoice_info', info['number'], info['amount'], status),
                parse_mode='Markdown',
            )
    except Exception as e:
        logger.error(f"Error getting invoice: {e}")
        await update.message.reply_text(get_text(context, 'error'))


# ── /help ──────────────────────────────────────────────────────────────────────
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Yordam buyrug'i"""
    await update.message.reply_text(
        get_text(context, 'help'),
        parse_mode='Markdown',
    )


# ── /cancel ────────────────────────────────────────────────────────────────────
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bekor qilish"""
    context.user_data.pop('request_text', None)
    await update.message.reply_text(
        get_text(context, 'cancelled'),
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


# ── Build application ──────────────────────────────────────────────────────────
def build_application(token: str) -> Application:
    """Bot aplikatsiyasini yaratish"""
    # Persistence sozlamalari - conversation holatlarini saqlash uchun
    # PicklePersistence foydalanamiz, lekin persistent=False qilamiz (xatolikni oldini olish uchun)
    persistence = PicklePersistence(filepath="conversation_data.pickle")
    
    app = Application.builder().token(token).persistence(persistence).build()
    
    # /start + language selection conversation (persistent=False - xatolikni oldini olish uchun)
    start_conv = ConversationHandler(
        entry_points=[CommandHandler('start', start), CommandHandler('lang', change_language)],
        states={
            LANG: [CallbackQueryHandler(select_language, pattern='^lang_')],
            PHONE: [
                MessageHandler(filters.CONTACT, receive_phone),
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_phone),
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        name="start_conversation",
        persistent=False,  # False qilindi, chunki persistence bilan muammo bor
        per_message=False,  # Warningni oldini olish uchun
    )
    
    # /new request conversation
    new_conv = ConversationHandler(
        entry_points=[CommandHandler('new', new_request_start)],
        states={
            TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_text)],
            FILE: [
                MessageHandler(filters.Document.ALL | filters.PHOTO, receive_file),
                MessageHandler(filters.TEXT & ~filters.COMMAND, skip_file),
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        name="new_request_conversation",
        persistent=False,  # False qilindi
        per_message=False,  # Warningni oldini olish uchun
    )
    
    # Handlerlarni qo'shish
    app.add_handler(start_conv)
    app.add_handler(new_conv)
    app.add_handler(CommandHandler('status', status_command))
    app.add_handler(CommandHandler('invoice', invoice_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('lang', change_language))
    
    return app


# ── Main ───────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    import sys
    import django
    
    # Django sozlamalarini yuklash
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'law_crm.settings')
    django.setup()
    
    from django.conf import settings as django_settings
    
    token = getattr(django_settings, 'TELEGRAM_BOT_TOKEN', None)
    
    if not token or token == 'DEMO_NO_TOKEN':
        print("❌ ERROR: Set TELEGRAM_BOT_TOKEN in your .env file first.")
        print("   Example: TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz")
    else:
        print("🤖 Starting LegalFlow bot...")
        print(f"✅ Bot token loaded: {token[:15]}...")
        print("🌍 Supported languages: O'zbek, Русский, English")
        print("📱 Bot is running. Press Ctrl+C to stop.")
        
        # Botni ishga tushirish
        application = build_application(token)
        application.run_polling(allowed_updates=Update.ALL_TYPES)