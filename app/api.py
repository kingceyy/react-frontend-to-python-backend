import asyncio
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.database import get_session
from app.auth import verify_telegram_init_data, create_jwt_token, verify_jwt_token
from app.config import settings
from app.models import User, Coupon, CouponUsage
from app.schemas import (
    AuthRequest,
    AuthResponse,
    UserProfile,
    CouponResponse,
    CouponCreate,
    HistoryEntry,
    LeaderboardEntry,
    Referee,
    VipInfo,
    AdminUserRow,
    AdminStats,
)
from app import crud

router = APIRouter(prefix="/api", tags=["api"])


async def get_current_user(
    authorization: str = Header(None),
    session: AsyncSession = Depends(get_session),
):
    """Get current user from JWT token"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")

    token = authorization[7:]
    user_id = verify_jwt_token(token)

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await crud.get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.post("/auth/telegram", response_model=AuthResponse)
async def auth_telegram(
    request: AuthRequest,
    session: AsyncSession = Depends(get_session),
):
    """Authenticate user with Telegram InitData"""
    user_data = verify_telegram_init_data(request.init_data, settings.telegram_bot_token)
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid InitData")

    telegram_id = user_data.get("id")
    first_name = user_data.get("first_name", "User")
    username = user_data.get("username")
    photo_url = user_data.get("photo_url")
    language_code = user_data.get("language_code")

    user = await crud.get_or_create_user(
        session,
        telegram_id,
        first_name,
        username,
        photo_url,
        language_code,
    )

    # Auto-promote admins listed in ADMIN_IDS env var
    if telegram_id in settings.admin_ids and not user.is_admin:
        user.is_admin = True
        session.add(user)
        await session.commit()

    # Handle referral via start_param
    if request.start_param and request.start_param.startswith("ref_"):
        ref_code = request.start_param[4:]
        referrer = await crud.get_user_by_referral_code(session, ref_code)
        if referrer and user.referrer_id is None and referrer.id != user.id:
            await crud.add_referral(session, referrer.telegram_id, user.telegram_id)

    token = create_jwt_token(user.telegram_id)

    return AuthResponse(
        token=token,
        profile=_user_to_profile(user),
    )


@router.get("/me", response_model=UserProfile)
async def get_me(user = Depends(get_current_user)):
    """Get current user profile"""
    return _user_to_profile(user)


@router.get("/coupons", response_model=list[CouponResponse])
async def get_coupons(
    user = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Get available coupons"""
    coupons = await crud.get_coupons_for_user(session, user)
    return coupons


@router.get("/coupons/history", response_model=list[HistoryEntry])
async def get_coupons_history(
    user = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Get coupon usage history"""
    stmt = (
        select(CouponUsage)
        .options(selectinload(CouponUsage.coupon))
        .where(CouponUsage.user_id == user.id)
        .order_by(CouponUsage.validated_at.desc())
    )
    result = await session.execute(stmt)
    usages = result.scalars().all()

    return [
        HistoryEntry(
            id=usage.id,
            coupon_id=usage.coupon_id,
            coupon_text=usage.coupon.text,
            code=usage.coupon.code,
            validated_at=usage.validated_at,
        )
        for usage in usages
    ]


@router.get("/leaderboard", response_model=list[LeaderboardEntry])
async def get_leaderboard(
    session: AsyncSession = Depends(get_session),
):
    """Get leaderboard"""
    stmt = select(User).order_by(User.active_invites.desc()).limit(100)
    result = await session.execute(stmt)
    users = result.scalars().all()

    return [
        LeaderboardEntry(
            rank=i + 1,
            display_name=user.first_name,
            active_invites=user.active_invites,
            user_class=user.user_class,
            is_vip=user.is_vip,
        )
        for i, user in enumerate(users)
    ]


@router.get("/referees", response_model=list[Referee])
async def get_referees(
    user = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Get list of referees"""
    stmt = select(User).where(User.referrer_id == user.id)
    result = await session.execute(stmt)
    referees = result.scalars().all()

    return [
        Referee(
            id=ref.telegram_id,
            display_name=ref.first_name,
            joined_at=ref.joined_at,
            active=True,
        )
        for ref in referees
    ]


@router.get("/vip", response_model=VipInfo)
async def get_vip_info(user = Depends(get_current_user)):
    """Get VIP info"""
    channel_url = None
    if user.is_vip:
        channel_url = "https://t.me/+vip_canal_demo"  # Update with real channel

    return VipInfo(
        is_vip=user.is_vip,
        price_label="49 € (accès à vie)",
        channel_url=channel_url,
    )


@router.post("/vip/purchase")
async def vip_purchase(user = Depends(get_current_user)):
    """Initiate VIP purchase"""
    return {
        "redirect_url": "https://t.me/JMDAVEKKKK"
    }


@router.post("/forcesub/check")
async def forcesub_check(
    user = Depends(get_current_user),
):
    """Check if user is member of channel via bot getChatMember"""
    from app.bot import check_user_subscription
    is_member = await check_user_subscription(user.telegram_id)
    return {"is_member": is_member}


# Admin routes
@router.post("/admin/coupons", response_model=CouponResponse)
async def admin_create_coupon(
    payload: CouponCreate,
    user = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Create new coupon (admin only) and notify all users"""
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin only")

    coupon = await crud.create_coupon(
        session,
        payload.text,
        payload.image_url,
        payload.code,
        payload.min_class,
        payload.expires_at,
        payload.quantity,
    )

    # Broadcast notification to all users (in background, non-blocking)
    from app.bot import broadcast_new_coupon
    asyncio.create_task(broadcast_new_coupon(coupon.text, coupon.image_url))

    return coupon


@router.patch("/admin/coupons/{coupon_id}/validate")
async def admin_validate_coupon(
    coupon_id: str,
    user = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Validate coupon (admin only)"""
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin only")

    success = await crud.validate_coupon(session, coupon_id, user.id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to validate coupon")

    return {"ok": True}


@router.get("/admin/coupons")
async def admin_get_coupons(
    user = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Get all coupons (admin only)"""
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin only")

    stmt = select(Coupon).order_by(Coupon.created_at.desc())
    result = await session.execute(stmt)
    return result.scalars().all()


@router.get("/admin/users", response_model=list[AdminUserRow])
async def admin_get_users(
    search: str = None,
    user = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Get users, with optional name search (admin only)"""
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin only")

    if search:
        users = await crud.search_users(session, search)
    else:
        users = await crud.get_all_users(session)

    return [
        AdminUserRow(
            telegram_id=u.telegram_id,
            display_name=u.first_name,
            user_class=u.user_class,
            is_vip=u.is_vip,
            active_invites=u.active_invites,
        )
        for u in users
    ]


@router.patch("/admin/users/{user_id}")
async def admin_update_user(
    user_id: int,
    payload: dict,
    current_user = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Update user (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin only")

    # Only allow safe fields
    allowed_fields = {"user_class", "is_vip", "is_admin", "active_invites", "total_invites"}
    safe_payload = {k: v for k, v in payload.items() if k in allowed_fields}

    updated = await crud.update_user(session, user_id, **safe_payload)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")

    return AdminUserRow(
        telegram_id=updated.telegram_id,
        display_name=updated.first_name,
        user_class=updated.user_class,
        is_vip=updated.is_vip,
        active_invites=updated.active_invites,
    )


@router.get("/admin/stats", response_model=AdminStats)
async def admin_get_stats(
    user = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Get stats (admin only)"""
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin only")

    return await crud.get_admin_stats(session)


def _user_to_profile(user) -> UserProfile:
    """Convert user model to profile schema"""
    next_threshold = crud.get_next_class_threshold(user.active_invites)
    return UserProfile(
        telegram_id=user.telegram_id,
        first_name=user.first_name,
        username=user.username,
        photo_url=user.photo_url,
        user_class=user.user_class,
        is_vip=user.is_vip,
        is_admin=user.is_admin,
        referral_code=user.referral_code,
        active_invites=user.active_invites,
        total_invites=user.total_invites,
        next_threshold=next_threshold,
        joined_at=user.joined_at,
    )
