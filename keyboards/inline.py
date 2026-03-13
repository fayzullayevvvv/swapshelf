from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from db.repositories import GenreRepository
from db.session import SessionLocal


def get_confirm_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("Ha", callback_data="ha"),
            InlineKeyboardButton("Yo'q", callback_data="yo'q"),
        ],
        [InlineKeyboardButton("⬅️ Orqaga", callback_data="back")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("📚 Mening Javonim", callback_data="my_books")],
        [InlineKeyboardButton("➕ Kitob Qo'shish", callback_data="add_book")],
        [InlineKeyboardButton("🔍 Kitob Qidirish", callback_data="browse_books")],
        [InlineKeyboardButton("📬 Mening So'rovlaram", callback_data="my_requests")],
        [InlineKeyboardButton("🔄 Mening Almashtirishlarim", callback_data="my_swaps")],
        [InlineKeyboardButton("⭐ Mening Sahifam", callback_data="my_profile")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_genre_keyboard():
    with SessionLocal() as session:
        GenreRepo = GenreRepository(session)
        genres = GenreRepo.get_all_genres()

        keyboard = [
            [
                InlineKeyboardButton(
                    genre.name, callback_data=f"add_book:genre:{genre.id}"
                )
            ]
            for genre in genres
        ]

        keyboard.append([InlineKeyboardButton("⬅️ Orqaga", callback_data="back")])

    return InlineKeyboardMarkup(keyboard)


def get_status_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(
                "🆕 Yangi, ishlatilmagan", callback_data="add_book:status:New"
            )
        ],
        [
            InlineKeyboardButton(
                "👍 Yaxshi holatda", callback_data="add_book:status:Good"
            )
        ],
        [
            InlineKeyboardButton(
                "👌 O'rtacha holatda", callback_data="add_book:status:Fair"
            )
        ],
        [
            InlineKeyboardButton(
                "📄 Ko'p ishlatilgan", callback_data="add_book:status:Worn"
            )
        ],
        [InlineKeyboardButton("⬅️ Orqaga", callback_data="back")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_type_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(
                "🔄 Vaqtincha (30 kun muddatli)", callback_data="add_book:type:Borrow"
            )
        ],
        [
            InlineKeyboardButton(
                "🎁 Doimiy berib yuborish", callback_data="add_book:type:Permanent"
            )
        ],
        [
            InlineKeyboardButton(
                "🔀 Ikkalasi ham mumkin", callback_data="add_book:type:Both"
            )
        ],
        [InlineKeyboardButton("⬅️ Orqaga", callback_data="back")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_book_action_keyboard(book_id):
    keyboard = [
        [InlineKeyboardButton("🎁 Kitobni Ulashish", callback_data=f"share:{book_id}")],
        [InlineKeyboardButton("⬅️ Orqaga", callback_data="back")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_book_request_keyboard(book_id):
    keyboard = [
        [
            InlineKeyboardButton(
                "✅ Kitobni olish", callback_data=f"request:{book_id}"
            ),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_back():
    keyboard = [[InlineKeyboardButton("⬅️ Orqaga", callback_data="back")]]
    return InlineKeyboardMarkup(keyboard)
