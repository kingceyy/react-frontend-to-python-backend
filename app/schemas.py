from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


# User Schemas
class UserBase(BaseModel):
    first_name: str
    username: Optional[str] = None
    photo_url: Optional[str] = None


class UserProfile(BaseModel):
    telegram_id: int
    first_name: str
    username: Optional[str] = None
    photo_url: Optional[str] = None
    user_class: str
    is_vip: bool
    is_admin: bool
    referral_code: str
    active_invites: int
    total_invites: int
    next_threshold: Optional[int] = None
    joined_at: datetime

    class Config:
        from_attributes = True


# Coupon Schemas
class CouponCreate(BaseModel):
    text: str
    image_url: str
    code: str
    min_class: str = "Starter"
    expires_at: Optional[datetime] = None
    quantity: Optional[int] = None


class CouponResponse(BaseModel):
    id: str
    image_url: str
    text: str
    code: str
    min_class: str
    expires_at: Optional[datetime] = None
    quantity_left: Optional[int] = None
    locked: bool
    created_at: datetime

    class Config:
        from_attributes = True


# History Schemas
class HistoryEntry(BaseModel):
    id: str
    coupon_id: str
    coupon_text: str
    code: str
    validated_at: datetime

    class Config:
        from_attributes = True


# Leaderboard Schemas
class LeaderboardEntry(BaseModel):
    rank: int
    display_name: str
    active_invites: int
    user_class: str
    is_vip: bool


# Referee Schemas
class Referee(BaseModel):
    id: int
    display_name: str
    joined_at: datetime
    active: bool


# VIP Schemas
class VipInfo(BaseModel):
    is_vip: bool
    price_label: str = "49 € (accès à vie)"
    channel_url: Optional[str] = None


# Admin Schemas
class AdminUserRow(BaseModel):
    telegram_id: int
    display_name: str
    user_class: str
    is_vip: bool
    active_invites: int

    class Config:
        from_attributes = True


class AdminStats(BaseModel):
    total_users: int
    per_class: dict
    vip_users: int
    vip_conversion: float


# Auth Schemas
class AuthRequest(BaseModel):
    init_data: str
    start_param: Optional[str] = None


class AuthResponse(BaseModel):
    token: str
    profile: UserProfile
    is_member: bool = True
