import asyncio
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

WELCOME_TEXT = (
    "👋 <b>Bienvenue {name} !</b>\n\n"
    "Tu viens d'entrer dans <b>CLUB JM</b> — la communauté où le parrainage "
    "te fait gagner des <b>coupons de paris exclusifs</b>. 🎟️\n\n"
    "📌 <b>Comment ça marche ?</b>\n"
    "1️⃣ Ouvre l'application avec le bouton ci-dessous\n"
    "2️⃣ Invite tes amis avec ton lien de parrainage\n"
    "3️⃣ Monte en classe et débloque des coupons de plus en plus puissants\n\n"
    "⚠️ <b>Important :</b> tu dois être membre de notre canal officiel "
    "pour profiter de toutes les fonctionnalités.\n\n"
    "👇 Choisis une option pour commencer :"
)

ABOUT_TEXT = (
    "🏆 <b>QU'EST-CE QUE CLUB JM ?</b>\n\n"
    "CLUB JM est une communauté privée qui récompense ses membres "
    "avec des <b>coupons de paris exclusifs</b>. Plus tu invites d'amis, "
    "plus tu montes en classe, et plus les récompenses sont grandes. 💎\n\n"
    "🎖️ <b>Les 4 classes :</b>\n"
    "🟢 <b>Starter</b> — 0 à 29 parrainages · les coupons de base\n"
    "🔵 <b>Loki</b> — 30 à 49 parrainages · coupons intermédiaires\n"
    "🟣 <b>Blaise</b> — 50 à 79 parrainages · coupons avancés\n"
    "🔴 <b>Master</b> — 80+ parrainages · TOUS les coupons débloqués\n\n"
    "🎯 <b>Le principe est simple :</b>\n"
    "• Chaque ami qui rejoint avec ton lien = 1 parrainage actif\n"
    "• Ta classe évolue automatiquement selon tes parrainages\n"
    "• Les nouveaux coupons sont publiés régulièrement dans l'app\n"
    "• Tu es notifié dès qu'un nouveau coupon est disponible 🔔\n\n"
    "💎 <b>Le VIP :</b> un accès à vie aux coupons premium et au canal privé.\n\n"
    "Prêt à commencer ? Ouvre l'app et invite tes premiers amis ! 🚀"
)


def main_keyboard(mini_app_url: str) -> InlineKeyboardMarkup:
    """Clavier principal du /start"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎟️ Ouvrir CLUB JM",
                    web_app=WebAppInfo(url=mini_app_url),
                )
            ],
            [
                InlineKeyboardButton(text="📖 À propos", callback_data="about"),
                InlineKeyboardButton(text="🔗 Mon lien", callback_data="my_ref"),
            ],
            [
                InlineKeyboardButton(text="📢 Canal officiel", url=CHANNEL_LINK),
                InlineKeyboardButton(text="💬 Support", url=SUPPORT_LINK),
            ],
        ]
    )


@dp.message(CommandStart())
async def start_handler(message: types.Message):
    """Handle /start command"""
    user = message.from_user
    referral_code = None

    if message.text:
        parts = message.text.split()
        if len(parts) > 1:
            referral_code = parts[1]

    mini_app_url = f"{FRONTEND_URL}?utm_source=telegram_bot"
    if referral_code:
        mini_app_url += f"&startParam={referral_code}"

    await message.answer(
        WELCOME_TEXT.format(name=user.first_name),
        reply_markup=main_keyboard(mini_app_url),
        parse_mode="HTML",
    )


@dp.callback_query(F.data == "about")
async def about_handler(query: types.CallbackQuery):
    """Handle about button"""
    await query.answer()

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎟️ Ouvrir CLUB JM",
                    web_app=WebAppInfo(url=f"{FRONTEND_URL}?utm_source=telegram_bot"),
                )
            ],
            [InlineKeyboardButton(text="← Retour", callback_data="back_to_start")],
        ]
    )

    await query.message.edit_text(
        ABOUT_TEXT,
        reply_markup=keyboard,
        parse_mode="HTML",
    )


@dp.callback_query(F.data == "my_ref")
async def my_ref_handler(query: types.CallbackQuery):
    """Handle referral link button - fetch real code from DB"""
    await query.answer()

    from app.database import AsyncSessionLocal
    from app import crud

    async with AsyncSessionLocal() as session:
        db_user = await crud.get_or_create_user(
            session,
            query.from_user.id,
            query.from_user.first_name or "User",
            query.from_user.username,
        )
        ref_code = db_user.referral_code
        active = db_user.active_invites
        total = db_user.total_invites
        user_class = db_user.user_class

    me = await bot.get_me()
    link = f"https://t.me/{me.username}?start=ref_{ref_code}"

    ref_text = (
        "🔗 <b>TON LIEN DE PARRAINAGE</b>\n\n"
        f"<code>{link}</code>\n\n"
        "👆 Appuie sur le lien pour le copier, puis partage-le à tes amis.\n\n"
        f"📊 <b>Tes statistiques :</b>\n"
        f"• Classe actuelle : <b>{user_class}</b>\n"
        f"• Parrainages actifs : <b>{active}</b>\n"
        f"• Invitations totales : <b>{total}</b>\n\n"
        "💡 Chaque ami qui rejoint CLUB JM avec ton lien te rapproche "
        "de la classe supérieure et de nouveaux coupons !"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📤 Partager mon lien",
                    url=f"https://t.me/share/url?url={link}&text=Rejoins%20CLUB%20JM%20avec%20mon%20lien%20et%20gagne%20des%20coupons%20exclusifs%20!",
                )
            ],
            [InlineKeyboardButton(text="← Retour", callback_data="back_to_start")],
        ]
    )

    await query.message.edit_text(
        ref_text,
        reply_markup=keyboard,
        parse_mode="HTML",
    )


@dp.callback_query(F.data == "back_to_start")
async def back_to_start(query: types.CallbackQuery):
    """Go back to start menu"""
    await query.answer()

    await query.message.edit_text(
        WELCOME_TEXT.format(name=query.from_user.first_name),
        reply_markup=main_keyboard(f"{FRONTEND_URL}?utm_source=telegram_bot"),
        parse_mode="HTML",
    )


@dp.message(Command("about"))
async def about_command(message: types.Message):
    """Handle /about command"""
    await message.answer(ABOUT_TEXT, parse_mode="HTML")


@dp.message(Command("ref"))
async def ref_command(message: types.Message):
    """Handle /ref command - real referral link from DB"""
    from app.database import AsyncSessionLocal
    from app import crud

    async with AsyncSessionLocal() as session:
        db_user = await crud.get_or_create_user(
            session,
            message.from_user.id,
            message.from_user.first_name or "User",
            message.from_user.username,
        )
        ref_code = db_user.referral_code
        active = db_user.active_invites

    me = await bot.get_me()
    link = f"https://t.me/{me.username}?start=ref_{ref_code}"

    await message.answer(
        "🔗 <b>Ton lien de parrainage :</b>\n\n"
        f"<code>{link}</code>\n\n"
        f"👥 Parrainages actifs : <b>{active}</b>\n\n"
        "Partage ce lien avec tes amis pour monter en classe "
        "et débloquer des coupons exclusifs ! 🎟️",
        parse_mode="HTML",
    )


@dp.message(Command("help"))
async def help_command(message: types.Message):
    """Handle /help command"""
    help_text = (
        "📖 <b>COMMANDES DISPONIBLES</b>\n\n"
        "/start — Menu principal du bot\n"
        "/about — Découvrir CLUB JM et les classes\n"
        "/ref — Obtenir ton lien de parrainage\n"
        "/help — Afficher cette aide\n\n"
        "💬 <b>Besoin d'aide ?</b>\n"
        f"Contacte le support : {SUPPORT_LINK}\n\n"
        f"📢 <b>Canal officiel :</b>\n{CHANNEL_LINK}"
    )

    await message.answer(help_text, parse_mode="HTML")


@dp.message()
async def echo_handler(message: types.Message):
    """Echo unknown messages"""
    await message.answer(
        "🤔 Je n'ai pas compris cette commande.\n"
        "Tape /help pour voir les commandes disponibles."
    )


async def check_user_subscription(user_id: int) -> bool:
    """Check if user is member of channel"""
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in [
            "member",
            "administrator",
            "creator",
            "restricted",
        ]
    except Exception as e:
        logger.error(f"Error checking subscription: {e}")
        return False


async def broadcast_new_coupon(coupon_text: str, coupon_image_url: str | None = None):
    """Notify all users when a new coupon is published"""
    from app.database import AsyncSessionLocal
    from app import crud

    async with AsyncSessionLocal() as session:
        users = await crud.get_all_users(session)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎟️ Voir le coupon",
                    web_app=WebAppInfo(url=f"{FRONTEND_URL}?utm_source=coupon_notif"),
                )
            ]
        ]
    )

    notif_text = (
        "🔥 <b>NOUVEAU COUPON DISPONIBLE !</b>\n\n"
        f"🎟️ {coupon_text}\n\n"
        "⚡ Ouvre l'application maintenant pour le récupérer "
        "avant qu'il ne soit épuisé !"
    )

    sent = 0
    failed = 0
    for u in users:
        try:
            if coupon_image_url and coupon_image_url.startswith("http"):
                await bot.send_photo(
                    u.telegram_id,
                    photo=coupon_image_url,
                    caption=notif_text,
                    reply_markup=keyboard,
                    parse_mode="HTML",
                )
            else:
                await bot.send_message(
                    u.telegram_id,
                    notif_text,
                    reply_markup=keyboard,
                    parse_mode="HTML",
                )
            sent += 1
        except Exception as e:
            # User blocked the bot or deleted account
            failed += 1
            logger.warning(f"Broadcast failed for {u.telegram_id}: {e}")

        # Rate limit: max ~25 messages/second
        await asyncio.sleep(0.05)

    logger.info(f"Coupon broadcast done: {sent} sent, {failed} failed")
