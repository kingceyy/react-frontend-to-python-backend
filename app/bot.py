import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from app.config import settings

logger = logging.getLogger(__name__)

bot = Bot(token=settings.telegram_bot_token)
dp = Dispatcher()

FRONTEND_URL = settings.frontend_url
CHANNEL_ID = settings.telegram_channel_id
CHANNEL_LINK = "https://t.me/+gpImJ4tj2BUxMzE0"
SUPPORT_LINK = "https://t.me/JMDAVEKKKK"


@dp.message(CommandStart())
async def start_handler(message: types.Message):
    """Handle /start command"""
    user = message.from_user
    referral_code = None
    
    # Check if there's a start parameter (referral)
    if message.text:
        parts = message.text.split()
        if len(parts) > 1:
            referral_code = parts[1]

    # Build mini app URL
    mini_app_url = f"{FRONTEND_URL}?utm_source=telegram_bot"
    if referral_code:
        mini_app_url += f"&startParam={referral_code}"

    # Create inline keyboard
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎮 Ouvrir l'app",
                    web_app=WebAppInfo(url=mini_app_url),
                )
            ],
            [
                InlineKeyboardButton(
                    text="📖 À propos",
                    callback_data="about",
                )
            ],
            [
                InlineKeyboardButton(
                    text="👥 Rejoindre le canal",
                    url=CHANNEL_LINK,
                )
            ],
            [
                InlineKeyboardButton(
                    text="💬 Support",
                    url=SUPPORT_LINK,
                )
            ],
        ]
    )

    await message.answer(
        f"Bienvenue {user.first_name}! 👋\n\n"
        "Je suis le bot officiel de **Club JM**. "
        "Cliquez sur les boutons ci-dessous pour commencer.",
        reply_markup=keyboard,
        parse_mode="Markdown",
    )


@dp.callback_query(F.data == "about")
async def about_handler(query: types.CallbackQuery):
    """Handle about button"""
    await query.answer()
    
    about_text = (
        "🏆 **À propos de CLUB JM**\n\n"
        "Club JM est une communauté exclusive de parrainage "
        "avec un système de récompenses progressif.\n\n"
        "**Les classes d'utilisateurs:**\n"
        "🟢 **Starter** - Débutant (0-29 parrainages)\n"
        "🔵 **Loki** - Intermédiaire (30-49 parrainages)\n"
        "🟣 **Blaise** - Avancé (50-79 parrainages)\n"
        "🔴 **Master** - Expert (80+ parrainages)\n\n"
        "**Système de parrainage:**\n"
        "• Parrainez des amis et gagnez des points\n"
        "• Déverrouillez des coupons exclusifs\n"
        "• Montez en classe et accédez à plus de récompenses\n"
        "• Devenez VIP pour plus d'avantages\n\n"
        "Rejoignez-nous maintenant!"
    )
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="← Retour",
                    callback_data="back_to_start",
                )
            ]
        ]
    )
    
    await query.message.edit_text(
        about_text,
        reply_markup=keyboard,
        parse_mode="Markdown",
    )


@dp.callback_query(F.data == "back_to_start")
async def back_to_start(query: types.CallbackQuery):
    """Go back to start"""
    await query.answer()
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎮 Ouvrir l'app",
                    web_app=WebAppInfo(url=f"{FRONTEND_URL}?utm_source=telegram_bot"),
                )
            ],
            [
                InlineKeyboardButton(
                    text="📖 À propos",
                    callback_data="about",
                )
            ],
            [
                InlineKeyboardButton(
                    text="👥 Rejoindre le canal",
                    url=CHANNEL_LINK,
                )
            ],
            [
                InlineKeyboardButton(
                    text="💬 Support",
                    url=SUPPORT_LINK,
                )
            ],
        ]
    )
    
    await query.message.edit_text(
        f"Bienvenue! 👋\n\n"
        "Je suis le bot officiel de **Club JM**. "
        "Cliquez sur les boutons ci-dessous pour commencer.",
        reply_markup=keyboard,
        parse_mode="Markdown",
    )


@dp.message(Command("about"))
async def about_command(message: types.Message):
    """Handle /about command"""
    about_text = (
        "🏆 **À propos de CLUB JM**\n\n"
        "Club JM est une communauté exclusive de parrainage "
        "avec un système de récompenses progressif.\n\n"
        "**Les classes d'utilisateurs:**\n"
        "🟢 **Starter** - Débutant (0-29 parrainages)\n"
        "🔵 **Loki** - Intermédiaire (30-49 parrainages)\n"
        "🟣 **Blaise** - Avancé (50-79 parrainages)\n"
        "🔴 **Master** - Expert (80+ parrainages)\n\n"
        "**Système de parrainage:**\n"
        "• Parrainez des amis et gagnez des points\n"
        "• Déverrouillez des coupons exclusifs\n"
        "• Montez en classe et accédez à plus de récompenses\n"
        "• Devenez VIP pour plus d'avantages\n\n"
        "Rejoignez-nous maintenant!"
    )
    
    await message.answer(about_text, parse_mode="Markdown")


@dp.message(Command("ref"))
async def ref_command(message: types.Message):
    """Handle /ref command - show referral info"""
    user = message.from_user
    
    # In real implementation, fetch from database
    referral_text = (
        f"🎯 **Votre lien de parrainage:**\n\n"
        f"`https://t.me/{(await bot.get_me()).username}?start=ref_YOUR_CODE`\n\n"
        f"Partagez ce lien avec vos amis et obtenez des récompenses!"
    )
    
    await message.answer(referral_text, parse_mode="Markdown")


@dp.message(Command("help"))
async def help_command(message: types.Message):
    """Handle /help command"""
    help_text = (
        "📖 **Commandes disponibles:**\n\n"
        "/start - Démarrer le bot\n"
        "/about - À propos de Club JM\n"
        "/ref - Voir votre lien de parrainage\n"
        "/help - Afficher cette aide\n\n"
        "Ou utilisez les boutons de l'application."
    )
    
    await message.answer(help_text, parse_mode="Markdown")


@dp.message()
async def echo_handler(message: types.Message):
    """Echo unknown messages"""
    await message.answer(
        "Je n'ai pas compris cette commande. "
        "Tapez /help pour voir les commandes disponibles."
    )


async def check_user_subscription(user_id: int) -> bool:
    """Check if user is member of channel"""
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        # Check if user is member, admin, creator, etc. (not restricted or left)
        return member.status in [
            "member",
            "administrator",
            "creator",
            "restricted",  # Restricted but still member
        ]
    except Exception as e:
        logger.error(f"Error checking subscription: {e}")
        return False
