from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from utils.states import RegistrationStates
from keyboards.inline import get_confirm_keyboard, get_menu_keyboard
from db.services.user import UserService
from db.session import SessionLocal


def start(update: Update, context: CallbackContext) -> int:
    with SessionLocal() as session:
        UserRepo = UserService(session)
        existing_user = UserRepo.get_user(update.effective_user.id)

        if existing_user:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Xush kelibsiz, {existing_user.full_name}! Siz allaqachon ro'yxatdan o'tgansiz.",
                reply_markup=get_menu_keyboard(),
            )
            return ConversationHandler.END

    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Assalomu alaykum! Ismingizni kiriting:"
    )

    return RegistrationStates.SET_NAME


def set_name(update: Update, context: CallbackContext) -> int:
    context.user_data["name"] = update.message.text
    update.message.reply_text("Telefon raqamingizni kiriting:")

    return RegistrationStates.SET_PHONE


def set_phone(update: Update, context: CallbackContext) -> int:
    context.user_data["phone"] = update.message.text
    name = context.user_data["name"]
    phone = context.user_data["phone"]
    update.message.reply_text(
        f"Ismingiz: {name}\nTelefon raqamingiz: {phone}\nTasdiqlaysizmi?",
        reply_markup=get_confirm_keyboard(),
    )

    return RegistrationStates.CONFIRM


def register(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    query.edit_message_text("Ro'yxatdan o'tdingiz! Rahmat!")

    user_id = update.effective_user.id
    name = context.user_data["name"]
    phone = context.user_data["phone"]

    with SessionLocal() as session:
        UserRepo = UserService(session)
        UserRepo.register_user(telegram_id=user_id, full_name=name, phone_number=phone)

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Xush kelibsiz, {name}! Siz muvaffaqiyatli ro'yxatdan o'tdingiz.",
        reply_markup=get_menu_keyboard(),
    )

    return ConversationHandler.END
