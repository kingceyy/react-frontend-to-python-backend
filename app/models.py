from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False, index=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=True)
    username = Column(String(255), nullable=True)
    photo_url = Column(String(500), nullable=True)
    language_code = Column(String(10), nullable=True)

    # User status
    user_class = Column(String(50), default="Starter", nullable=False)
    is_vip = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)

    # Referral system
    referral_code = Column(String(50), unique=True, nullable=False, index=True)
    referrer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    active_invites = Column(Integer, default=0)
    total_invites = Column(Integer, default=0)

    # Timestamps
    joined_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    referees = relationship(
        "User",
        backref="referrer",
        remote_side=[id],
        foreign_keys=[referrer_id],
    )
    coupons_used = relationship("CouponUsage", back_populates="user")

    def __repr__(self):
        return f"<User {self.telegram_id} {self.first_name}>"


class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(String(50), primary_key=True)
    image_url = Column(String(500), nullable=False)
    text = Column(Text, nullable=False)
    code = Column(String(100), unique=True, nullable=False, index=True)
    min_class = Column(String(50), default="Starter", nullable=False)

    # Limits
    expires_at = Column(DateTime, nullable=True)
    quantity_left = Column(Integer, nullable=True)

    # Status
    locked = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    usages = relationship("CouponUsage", back_populates="coupon")

    def __repr__(self):
        return f"<Coupon {self.code}>"


class CouponUsage(Base):
    __tablename__ = "coupon_usages"

    id = Column(String(50), primary_key=True)
    coupon_id = Column(String(50), ForeignKey("coupons.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    validated_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    coupon = relationship("Coupon", back_populates="usages")
    user = relationship("User", back_populates="coupons_used")

    def __repr__(self):
        return f"<CouponUsage {self.coupon_id} {self.user_id}>"
