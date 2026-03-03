#!/usr/bin/env python3
"""
Djezzy Telegram Bot
بوت تيليغرام لأداة اتصالات الجزائر
"""

import logging
import os
import sys
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, ContextTypes, filters, CallbackQueryHandler
from datetime import datetime
import djezzy_utils

# Configure logging
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
PHONE_NUMBER, OTP_CODE = range(2)

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

# -------------------------------------------------------------------------


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start command - show main menu"""
    user_id = update.effective_user.id
    # build keyboard depending on whether the user is an admin or not
    keyboard = [[InlineKeyboardButton("📱 تسجيل رقم جديد", callback_data='register')]]
    if is_admin(user_id):
        keyboard.append([InlineKeyboardButton("📊 إحصائيات", callback_data='stats')])
        keyboard.append([InlineKeyboardButton("📋 آخر التسجيلات", callback_data='recent')])
        keyboard.append([InlineKeyboardButton("ℹ️ معلومات", callback_data='info')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "👋 مرحباً بك في بوت اتصالات الجزائر\n\n"
        "اختر العملية المطلوبة:",
        reply_markup=reply_markup
    )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int | None:
    """Handle button presses"""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id if query.from_user else None

    if query.data == 'register':
        await query.edit_message_text(
            "📱 أدخل رقم اتصالات الجزائر الخاص بك\n"
            "مثال: 0770123456 أو 213770123456"
        )
        return PHONE_NUMBER
    
    if query.data == 'menu':
        # user asked to go back to main menu
        await show_main_menu(update, context)
        return ConversationHandler.END

    # only admin may access the following commands
    if query.data in ('stats', 'recent', 'info') and not is_admin(user_id):
        await query.edit_message_text("❌ هذه الميزة متاحة للمشرف فقط.")
        # after denying show restricted main menu
        await show_main_menu(update, context)
        return ConversationHandler.END
    
    if query.data == 'stats':
        count = djezzy_utils.get_registered_count()
        keyboard = [[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data='menu')]]
        await query.edit_message_text(
            f"📊 الإحصائيات:\n\n"
            f"✅ عدد الأرقام المسجلة: {count}\n\n"
            f"التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return ConversationHandler.END
    
    elif query.data == 'recent':
        recent = djezzy_utils.get_recent_registrations(limit=10)
        if not recent:
            text = "📋 لا توجد تسجيلات حتى الآن"
        else:
            text = "📋 آخر التسجيلات:\n\n"
            for i, reg in enumerate(recent, 1):
                text += f"{i}. {reg['sender']} ➜ {reg['target']}\n   {reg['timestamp']}\n\n"
        keyboard = [[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data='menu')]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        return ConversationHandler.END
    
    elif query.data == 'info':
        keyboard = [[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data='menu')]]
        await query.edit_message_text(
            "ℹ️ معلومات البوت:\n\n"
            "هذا البوت يساعدك على تسجيل 1 جيغا مجاني من اتصالات الجزائر\n\n"
            "الخطوات:\n"
            "1️⃣ أدخل رقم هاتفك\n"
            "2️⃣ سيتم إرسال كود التحقق\n"
            "3️⃣ أدخل الكود\n"
            "4️⃣ سيتم البحث عن أرقام عشوائية وإرسال دعوات\n"
            "5️⃣ عند النجاح ستحصل على 1 جيغا\n\n"
            "⚠️ تنويه: قد تستغرق العملية عدة دقائق",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return ConversationHandler.END


async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show main menu again"""
    user_id = None
    if update.effective_user:
        user_id = update.effective_user.id
    keyboard = [[InlineKeyboardButton("📱 تسجيل رقم جديد", callback_data='register')]]
    if is_admin(user_id):
        keyboard.append([InlineKeyboardButton("📊 إحصائيات", callback_data='stats')])
        keyboard.append([InlineKeyboardButton("📋 آخر التسجيلات", callback_data='recent')])
        keyboard.append([InlineKeyboardButton("ℹ️ معلومات", callback_data='info')])
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
    
    def progress_callback(message):
        """Callback to send progress messages"""
        try:
            # Send progress message to user
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=message
            )
        except:
            pass
    
    # Execute registration
    success, message, data = djezzy_utils.register_with_number(
        phone, 
        otp, 
        max_attempts=50,
        callback=progress_callback
    )
    
    if success:
        await update.message.reply_text(
            f"✅✅✅ النجاح! ✅✅✅\n\n"
            f"الرقم المرسل: {original_phone}\n"
            f"الرقم المستقبل: {data['target']}\n"
            f"الحالة: {data['status']}\n"
            f"الوقت: {data['timestamp']}\n\n"
            f"🎉 حصلت على 1 جيغا مجاني!"
        )
    else:
        await update.message.reply_text(
            f"❌ فشلت العملية\n\n"
            f"السبب: {message}\n"
            f"حاول مرة أخرى لاحقاً"
        )
    
    # Clean up session
    if user_id in user_sessions:
        del user_sessions[user_id]
    
    # Show menu
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
    application.add_handler(conv_handler)

    # Start the bot
    logger.info("🤖 تم بدء البوت...")
    application.run_polling()


if __name__ == '__main__':
    main()
