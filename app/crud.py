import uuid
from datetime import datetime
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User, Coupon, CouponUsage
from app.schemas import AdminStats


class CLASS_THRESHOLDS:
    """Class progression thresholds"""
    STARTER = 0
    LOKI = 30
    BLAISE = 50
    MASTER = 80


def get_user_class(active_invites: int) -> str:
    """Calculate user class based on active invites"""
    if active_invites >= CLASS_THRESHOLDS.MASTER:
        return "Master"
    elif active_invites >= CLASS_THRESHOLDS.BLAISE:
        return "Blaise"
    elif active_invites >= CLASS_THRESHOLDS.LOKI:
        return "Loki"
    else:
        return "Starter"


def get_next_class_threshold(current_invites: int) -> int | None:
    """Get next class threshold"""
    if current_invites < CLASS_THRESHOLDS.LOKI:
        return CLASS_THRESHOLDS.LOKI
    elif current_invites < CLASS_THRESHOLDS.BLAISE:
        return CLASS_THRESHOLDS.BLAISE
    elif current_invites < CLASS_THRESHOLDS.MASTER:
        return CLASS_THRESHOLDS.MASTER
    else:
        return None


# User CRUD
async def get_or_create_user(
    session: AsyncSession,
    telegram_id: int,
    first_name: str,
    username: str | None = None,
    photo_url: str | None = None,
    language_code: str | None = None,
    referral_code: str | None = None,
) -> User:
    """Get existing user or create new one"""
    stmt = select(User).where(User.telegram_id == telegram_id)
    result = await session.execute(stmt)
    user = result.scalars().first()

    if user:
        return user

    # Create new user
    if not referral_code:
        referral_code = f"JM{telegram_id}{uuid.uuid4().hex[:6].upper()}"

    user = User(
        telegram_id=telegram_id,
        first_name=first_name,
        username=username,
        photo_url=photo_url,
        language_code=language_code,
        referral_code=referral_code,
    )

    session.add(user)
    await session.commit()
    return user


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    """Get user by telegram_id"""
    stmt = select(User).where(User.telegram_id == user_id)
    result = await session.execute(stmt)
    return result.scalars().first()


async def get_user_by_referral_code(session: AsyncSession, code: str) -> User | None:
    """Get user by referral code"""
    stmt = select(User).where(User.referral_code == code)
    result = await session.execute(stmt)
    return result.scalars().first()


async def add_referral(
    session: AsyncSession,
    referrer: User,
    referee: User,
) -> bool:
    """Add a referral. referrer_id (FK) doit pointer vers users.id (PK interne),
    pas vers telegram_id — d'ou l'usage direct des objets User deja charges."""
    if not referrer or not referee or referee.referrer_id:
        return False

    referee.referrer_id = referrer.id
    referrer.total_invites += 1
    referrer.active_invites += 1

    # Update class
    referrer.user_class = get_user_class(referrer.active_invites)

    session.add(referrer)
    session.add(referee)
    await session.commit()
    return True


# Coupon CRUD
async def create_coupon(
    session: AsyncSession,
    text: str,
    image_url: str,
    code: str,
    min_class: str = "Starter",
    expires_at: datetime | None = None,
    quantity: int | None = None,
) -> Coupon:
    """Create new coupon"""
    coupon = Coupon(
        id=f"c{uuid.uuid4().hex[:12]}",
        text=text,
        image_url=image_url,
        code=code,
        min_class=min_class,
        expires_at=expires_at,
        quantity_left=quantity,
    )

    session.add(coupon)
    await session.commit()
    return coupon


async def get_coupons_for_user(session: AsyncSession, user: User) -> list[Coupon]:
    """Get available coupons for user"""
    stmt = select(Coupon).where(
        (Coupon.expires_at.is_(None) | (Coupon.expires_at > datetime.utcnow()))
    )
    result = await session.execute(stmt)
    coupons = result.scalars().all()

    # Apply lock logic
    CLASS_ORDER = ["Starter", "Loki", "Blaise", "Master"]
    user_class_rank = CLASS_ORDER.index(user.user_class)

    for coupon in coupons:
        coupon_class_rank = CLASS_ORDER.index(coupon.min_class)
        coupon.locked = user_class_rank < coupon_class_rank

    return coupons


async def get_coupon_by_id(session: AsyncSession, coupon_id: str) -> Coupon | None:
    """Get coupon by id"""
    stmt = select(Coupon).where(Coupon.id == coupon_id)
    result = await session.execute(stmt)
    return result.scalars().first()


async def validate_coupon(
    session: AsyncSession,
    coupon_id: str,
    user_id: int,
) -> bool:
    """Validate coupon for user"""
    coupon = await get_coupon_by_id(session, coupon_id)
    if not coupon:
        return False

    # Create usage record
    usage = CouponUsage(
        id=f"h{uuid.uuid4().hex[:12]}",
        coupon_id=coupon_id,
        user_id=user_id,
    )

    # Decrease quantity if limited
    if coupon.quantity_left is not None:
        if coupon.quantity_left <= 0:
            return False
        coupon.quantity_left -= 1

    session.add(usage)
    session.add(coupon)
    await session.commit()
    return True


# Admin CRUD
async def get_all_users(session: AsyncSession) -> list[User]:
    """Get all users"""
    stmt = select(User).order_by(User.active_invites.desc())
    result = await session.execute(stmt)
    return result.scalars().all()


async def search_users(session: AsyncSession, search_term: str) -> list[User]:
    """Search users by name or username"""
    search_like = f"%{search_term}%"
    stmt = select(User).where(
        (User.first_name.ilike(search_like))
        | (User.last_name.ilike(search_like))
        | (User.username.ilike(search_like))
    )
    result = await session.execute(stmt)
    return result.scalars().all()


async def update_user(
    session: AsyncSession,
    user_id: int,
    **kwargs,
) -> User | None:
    """Update user"""
    user = await get_user_by_id(session, user_id)
    if not user:
        return None

    for key, value in kwargs.items():
        if hasattr(user, key):
            setattr(user, key, value)

    session.add(user)
    await session.commit()
    return user


async def get_admin_stats(session: AsyncSession) -> AdminStats:
    """Get admin statistics"""
    # Total users
    total_stmt = select(func.count(User.id))
    total_result = await session.execute(total_stmt)
    total_users = total_result.scalar() or 0

    # Per class
    class_stmt = select(User.user_class, func.count(User.id)).group_by(User.user_class)
    class_result = await session.execute(class_stmt)
    per_class = {
        "Starter": 0,
        "Loki": 0,
        "Blaise": 0,
        "Master": 0,
    }
    for row in class_result:
        per_class[row[0]] = row[1]

    # VIP users
    vip_stmt = select(func.count(User.id)).where(User.is_vip.is_(True))
    vip_result = await session.execute(vip_stmt)
    vip_users = vip_result.scalar() or 0

    vip_conversion = vip_users / total_users if total_users > 0 else 0.0

    return AdminStats(
        total_users=total_users,
        per_class=per_class,
        vip_users=vip_users,
        vip_conversion=vip_conversion,
    )
