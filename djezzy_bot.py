#!/usr/bin/env python3
"""
Djezzy Telegram Bot
بوت تيليغرام لأداة جيزي
"""

import logging
import os
import sys
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, ContextTypes, filters, CallbackQueryHandler
from datetime import datetime
import djezzy_utils

# Configure logging
import threading
from concurrent.futures import ThreadPoolExecutor

# executor used for offloading long-running registration tasks
_BG_EXECUTOR = ThreadPoolExecutor(max_workers=50)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('djezzy_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Conversation states
PHONE_NUMBER, OTP_CODE, ADMIN_MENU, ADMIN_BROADCAST, ADMIN_BAN, ADMIN_UNBAN = range(6)

# Store user data temporarily
user_sessions = {}

# --- admin configuration -------------------------------------------------
# The bot can be restricted so that only one or more specific telegram user
# IDs can view statistics / info.  Normal users will only have the "register"
# button available.  IDs may be provided via the ADMIN_ID(S) environment
# variable (comma-separated) or, for backward compatibility with earlier
# example deployments, via CHAT_ID.

ADMIN_IDS = set()
env_admins = os.getenv("ADMIN_IDS") or os.getenv("ADMIN_ID") or os.getenv("CHAT_ID")
if env_admins:
    for part in env_admins.split(","):
        part = part.strip()
        if not part:
            continue
        try:
            ADMIN_IDS.add(int(part))
        except ValueError:
            logger.warning(f"Skipped non-numeric admin id: {part}")

    if not ADMIN_IDS and env_admins:
        logger.warning("Provided ADMIN_ID/CHAT_ID values could not be parsed as integers.")


def is_admin(user_id: int) -> bool:
    """Return True when the given user id is configured as an administrator."""
    return user_id in ADMIN_IDS


def is_banned(user_id: int) -> bool:
    """Check if a user is banned from using the bot."""
    try:
        banned = djezzy_utils.load_banned_users()
    except Exception:
        banned = []
    return user_id in banned

# -------------------------------------------------------------------------


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start command - show main menu"""
    user_id = update.effective_user.id
    # record this user as having started (for broadcast purposes)
    try:
        djezzy_utils.save_seen_user(user_id, update.effective_user.username or "")
    except Exception:
        pass

    if is_banned(user_id) and not is_admin(user_id):
        await update.message.reply_text("❌ تم حظرك من استخدام هذا البوت.")
        return
    # always show same base buttons for everyone; admins get extra management option
    keyboard = [
        [InlineKeyboardButton("📱 تسجيل رقم جديد", callback_data='register')],
        [InlineKeyboardButton("📊 إحصائيات", callback_data='stats')],
        [InlineKeyboardButton("📋 آخر التسجيلات", callback_data='recent')],
        [InlineKeyboardButton("ℹ️ معلومات", callback_data='info')],
    ]
    if is_admin(user_id):
        keyboard.append([InlineKeyboardButton("⚙️ إدارة", callback_data='admin')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "👋 مرحباً بك في بوت جيزي\n\n"
        "اختر العملية المطلوبة:",
        reply_markup=reply_markup
    )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int | None:
    """Handle button presses"""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id if query.from_user else None
    # block banned users immediately
    if user_id and is_banned(user_id) and not is_admin(user_id):
        await query.edit_message_text("❌ لقد تم حظرك من الاستمرار.")
        return ConversationHandler.END

    if query.data == 'register':
        await query.edit_message_text(
            "📱 أدخل رقم جيزي الخاص بك\n"
            "مثال: 0770123456 أو 213770123456"
        )
        return PHONE_NUMBER
    
    if query.data == 'menu':
        # user asked to go back to main menu
        await show_main_menu(update, context)
        return ConversationHandler.END

    # only admin may access the following commands
    
    if query.data == 'admin' and is_admin(user_id):
        # show administration submenu
        keyboard = [
            [InlineKeyboardButton("📣 بث رسالة", callback_data='broadcast')],
            [InlineKeyboardButton("⛔ حظر مستخدم", callback_data='ban')],
            [InlineKeyboardButton("✅ رفع الحظر", callback_data='unban')],
            [InlineKeyboardButton("📋 عرض المستخدمين", callback_data='list_users')],
            [InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data='menu')],
        ]
        await query.edit_message_text("🔧 لوحة إدارة المشرف:", reply_markup=InlineKeyboardMarkup(keyboard))
        return ADMIN_MENU

    if query.data == 'stats':
        # admin sees global count, others see their own
        if is_admin(user_id):
            count = djezzy_utils.get_registered_count()
            text = f"📊 إحصائيات عامة:\n\n✅ عدد الأرقام المسجلة: {count}\n"
        else:
            count = djezzy_utils.get_registered_count(user_id=user_id)
            text = f"📊 إحصائياتك:\n\n✅ عدد التسجيلات الخاصة بك: {count}\n"
            # show last registration if any
            recent = djezzy_utils.get_recent_registrations(limit=1, user_id=user_id)
            if recent:
                r = recent[-1]
                text += f"\nآخر تسجيل:\n{r['sender']} ➜ {r['target']} ({r['timestamp']})\n"
        text += f"\nالتاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        keyboard = [[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data='menu')]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        return ConversationHandler.END
    
    elif query.data == 'recent':
        if is_admin(user_id):
            recent = djezzy_utils.get_recent_registrations(limit=10)
            title = "📋 آخر التسجيلات العامة:"
        else:
            recent = djezzy_utils.get_recent_registrations(limit=10, user_id=user_id)
            title = "📋 تسجيلاتك الأخيرة:"
        if not recent:
            text = "📋 لا توجد تسجيلات حتى الآن"
        else:
            text = title + "\n\n"
            for i, reg in enumerate(recent, 1):
                text += f"{i}. {reg['sender']} ➜ {reg['target']}\n   {reg['timestamp']}\n\n"
        keyboard = [[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data='menu')]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        return ConversationHandler.END
    
    elif query.data == 'info':
        keyboard = [[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data='menu')]]
        await query.edit_message_text(
            "ℹ️ معلومات البوت:\n\n"
            "هذا البوت يساعدك على تسجيل 1 جيغا مجاني من جيزي\n\n"
            "الخطوات:\n"
            "1️⃣ أدخل رقم هاتفك\n"
            "2️⃣ سيتم إرسال كود التحقق\n"
            "3️⃣ أدخل الكود\n"
            "4️⃣ سيتم تسجيل رقمك\n"
            "5️⃣ عند النجاح ستحصل على 1 جيغا\n\n"
            "⚠️ تنويه: قد تستغرق العملية عدة دقائق",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return ConversationHandler.END

    # admin submenu choices
    if query.data == 'broadcast' and is_admin(user_id):
        await query.edit_message_text("📣 أدخل الرسالة التي تريد بثها:")
        return ADMIN_BROADCAST
    if query.data == 'ban' and is_admin(user_id):
        await query.edit_message_text("⛔ أدخل معرف المستخدم الذي تريد حظره:")
        return ADMIN_BAN
    if query.data == 'unban' and is_admin(user_id):
        await query.edit_message_text("✅ أدخل معرف المستخدم الذي تريد رفع الحظر عنه:")
        return ADMIN_UNBAN
    if query.data == 'list_users' and is_admin(user_id):
        users = djezzy_utils.load_seen_users()
        if not users:
            text = "📋 لا يوجد مستخدمون بعد."
        else:
            text = "📋 المستخدمون الذين بدأوا المحادثة:\n\n"
            for u in users:
                text += f"{u['user_id']} ({u.get('user_name','')})\n"
        keyboard = [[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data='menu')]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        return ConversationHandler.END


async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show main menu again"""
    # same base keyboard for everyone; admins get admin button
    keyboard = [
        [InlineKeyboardButton("📱 تسجيل رقم جديد", callback_data='register')],
        [InlineKeyboardButton("📊 إحصائيات", callback_data='stats')],
        [InlineKeyboardButton("📋 آخر التسجيلات", callback_data='recent')],
        [InlineKeyboardButton("ℹ️ معلومات", callback_data='info')],
    ]
    if is_admin(update.effective_user.id if update.effective_user else None):
        keyboard.append([InlineKeyboardButton("⚙️ إدارة", callback_data='admin')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            "اختر العملية المطلوبة:",
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            "اختر العملية المطلوبة:",
            reply_markup=reply_markup
        )


async def receive_phone_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Receive phone number from user"""
    phone = update.message.text.strip()
    
    if not phone or not phone.replace("0", "").replace("213", "").isdigit():
        await update.message.reply_text("❌ رقم غير صحيح. حاول مرة أخرى")
        return PHONE_NUMBER
    
    # Store phone and format it
    formatted_phone = djezzy_utils.format_num(phone)
    user_sessions[update.effective_user.id] = {'phone': formatted_phone, 'original': phone}
    
    # Request OTP
    await update.message.reply_text("🔄 جاري إرسال كود التحقق...")
    
    response = djezzy_utils.request_otp(formatted_phone)
    
    if response and response.status_code in [200, 201]:
        await update.message.reply_text(
            f"✅ تم إرسال كود التحقق إلى الرقم {phone}\n\n"
            "📨 أدخل الكود الذي وصلك:"
        )
        return OTP_CODE
    else:
        await update.message.reply_text(
            "❌ فشل إرسال الكود. تحقق من الرقم وحاول مرة أخرى.\n"
            "/start للعودة للقائمة الرئيسية"
        )
        return ConversationHandler.END


async def receive_otp(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Receive OTP from user"""
    otp = update.message.text.strip()
    user_id = update.effective_user.id
    
    if user_id not in user_sessions:
        await update.message.reply_text("❌ نقص البيانات. حاول من جديد.\n/start")
        return ConversationHandler.END
    
    phone = user_sessions[user_id]['phone']
    original_phone = user_sessions[user_id]['original']
    
    await update.message.reply_text("🔄 جاري معالجة طلبك... قد يستغرق الأمر عدة دقائق")

    # prepare thread-safe progress callback
    loop = asyncio.get_running_loop()
    chat_id = update.effective_chat.id
    bot = context.bot

    def progress_callback(message):
        # schedule send on event loop to avoid thread issues
        loop.call_soon_threadsafe(lambda: bot.send_message(chat_id=chat_id, text=message))

    def worker():
        # this runs in a thread; avoid saving log entries
        success, msg, data = djezzy_utils.register_with_number(
            phone,
            otp,
            max_attempts=50,
            callback=progress_callback,
            user_id=user_id,
            user_name=update.effective_user.username or "",
            record=False,
        )
        # send final result back to user
        if success:
            text = (
                f"✅✅✅ النجاح! ✅✅✅\n\n"
                f"الرقم المرسل: {original_phone}\n"
                f"الرقم المستقبل: {data.get('target','')}\n"
                f"الحالة: {data.get('status','')}\n"
                f"الوقت: {data.get('timestamp','')}\n\n"
                f"🎉 حصلت على 1 جيغا مجاني!"
            )
        else:
            text = (
                f"❌ فشلت العملية\n\n"
                f"السبب: {msg}\n"
                f"حاول مرة أخرى لاحقاً"
            )
        loop.call_soon_threadsafe(lambda: bot.send_message(chat_id=chat_id, text=text))

    # schedule the work in background using shared executor (allows many simultaneous jobs)
    loop.run_in_executor(_BG_EXECUTOR, worker)

    # remove session data now that processing is delegated
    if user_id in user_sessions:
        del user_sessions[user_id]

    # return to menu quickly
    await show_main_menu(update, context)
    return ConversationHandler.END


async def handle_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Receive broadcast text from admin and send to all users"""
    msg = update.message.text.strip()
    users = djezzy_utils.load_seen_users()
    for u in users:
        try:
            await context.bot.send_message(chat_id=u['user_id'], text=msg)
        except Exception:
            pass
    await update.message.reply_text("✅ تم إرسال الرسالة إلى جميع المستخدمين.")
    await show_main_menu(update, context)
    return ConversationHandler.END


async def handle_ban(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()
    try:
        uid = int(text)
    except ValueError:
        await update.message.reply_text("❌ المعرف غير صالح. أدخل رقماً فقط.")
        return ADMIN_BAN
    banned = djezzy_utils.load_banned_users()
    if uid in banned:
        await update.message.reply_text("⚠️ المستخدم محظور بالفعل.")
    else:
        banned.append(uid)
        djezzy_utils.save_banned_users(banned)
        await update.message.reply_text(f"✅ تم حظر المستخدم {uid}.")
    await show_main_menu(update, context)
    return ConversationHandler.END


async def handle_unban(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()
    try:
        uid = int(text)
    except ValueError:
        await update.message.reply_text("❌ المعرف غير صالح. أدخل رقماً فقط.")
        return ADMIN_UNBAN
    banned = djezzy_utils.load_banned_users()
    if uid not in banned:
        await update.message.reply_text("⚠️ هذا المستخدم ليس محظوراً.")
    else:
        banned = [x for x in banned if x != uid]
        djezzy_utils.save_banned_users(banned)
        await update.message.reply_text(f"✅ تم رفع الحظر عن المستخدم {uid}.")
    await show_main_menu(update, context)
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel the operation"""
    user_id = update.effective_user.id
    if user_id in user_sessions:
        del user_sessions[user_id]
    
    await update.message.reply_text(
        "❌ تم الإلغاء\n/start للعودة للقائمة الرئيسية"
    )
    return ConversationHandler.END


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show help message"""
    help_text = (
        "🔍 أوامر البوت:\n\n"
        "/start - عرض القائمة الرئيسية\n"
        "/help - عرض هذه الرسالة\n"
        "/cancel - إلغاء العملية الحالية\n\n"
        "💡 للبدء اضغط على /start\n\n"
        "⚠️ ملاحظة: أوامر الإحصائيات والمعلومات مخصصة للمشرف فقط "
        "(يتم تحديده عبر ADMIN_ID أو CHAT_ID)."
    )
    await update.message.reply_text(help_text)


async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Broadcast text to all users who have started the bot (admin only)"""
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("❌ لست مشرفًا")
        return
    text = " ".join(context.args)
    if not text:
        await update.message.reply_text("📣 الاستخدام: /broadcast رسالة")
        return
    users = djezzy_utils.load_seen_users()
    for u in users:
        try:
            await context.bot.send_message(chat_id=u['user_id'], text=text)
        except Exception:
            pass
    await update.message.reply_text("✅ تم إرسال البث إلى جميع المستخدمين.")

async def ban_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("❌ لست مشرفًا")
        return
    if not context.args:
        await update.message.reply_text("⛔ الاستخدام: /ban <user_id>")
        return
    try:
        uid = int(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ معرف غير صالح")
        return
    banned = djezzy_utils.load_banned_users()
    if uid in banned:
        await update.message.reply_text("⚠️ المستخدم محظور بالفعل.")
    else:
        banned.append(uid)
        djezzy_utils.save_banned_users(banned)
        await update.message.reply_text(f"✅ تم حظر المستخدم {uid}.")

async def unban_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("❌ لست مشرفًا")
        return
    if not context.args:
        await update.message.reply_text("✅ الاستخدام: /unban <user_id>")
        return
    try:
        uid = int(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ معرف غير صالح")
        return
    banned = djezzy_utils.load_banned_users()
    if uid not in banned:
        await update.message.reply_text("⚠️ هذا المستخدم ليس محظورًا.")
    else:
        banned = [x for x in banned if x != uid]
        djezzy_utils.save_banned_users(banned)
        await update.message.reply_text(f"✅ تم رفع الحظر عن المستخدم {uid}.")


def main() -> None:
    """Start the bot"""
    # prefer token from environment variable; keep placeholder as fallback
    DEFAULT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", DEFAULT_TOKEN)

    if TOKEN == DEFAULT_TOKEN or not TOKEN:
        logger.error("Telegram bot token is not set.\n" \
                     "Please set TELEGRAM_BOT_TOKEN environment variable or edit this file.")
        sys.exit(1)

    # validate format
    import re
    if not re.match(r"^[0-9]+:[A-Za-z0-9_-]+$", TOKEN):
        logger.error("Telegram bot token has an invalid format.\n"
                     "It should look like 1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh")
        sys.exit(1)

    # Create the Application
    application = Application.builder().token(TOKEN).build()

    # Add conversation handler
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            # allow all button presses handled by button_callback
            CallbackQueryHandler(button_callback),
        ],
        states={
            PHONE_NUMBER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_phone_number),
                CommandHandler("cancel", cancel),
            ],
            OTP_CODE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_otp),
                CommandHandler("cancel", cancel),
            ],
            ADMIN_MENU: [
                CallbackQueryHandler(button_callback),
                CommandHandler("cancel", cancel),
            ],
            ADMIN_BROADCAST: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_broadcast),
                CommandHandler("cancel", cancel),
            ],
            ADMIN_BAN: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_ban),
                CommandHandler("cancel", cancel),
            ],
            ADMIN_UNBAN: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_unban),
                CommandHandler("cancel", cancel),
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
            CommandHandler("start", start),
        ],
        allow_reentry=True,
    )

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("broadcast", broadcast_command))
    application.add_handler(CommandHandler("ban", ban_command))
    application.add_handler(CommandHandler("unban", unban_command))
    application.add_handler(conv_handler)

    # Start the bot
    logger.info("🤖 تم بدء البوت...")
    application.run_polling()


if __name__ == '__main__':
    main()
