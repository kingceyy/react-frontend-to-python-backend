import hmac
import hashlib
import json
import logging
from datetime import datetime, timedelta
from typing import Optional
from urllib.parse import parse_qsl
import jwt
from app.config import settings

logger = logging.getLogger(__name__)


def verify_telegram_init_data(init_data: str, bot_token: str) -> Optional[dict]:
    """
    Verify Telegram InitData signature
    """
    try:
        # Parse init_data (query-string encodee : les valeurs doivent etre URL-decodees
        # avant de reconstruire le check_string, sinon le hash ne correspondra jamais)
        pairs = dict(parse_qsl(init_data, keep_blank_values=True))

        # Extract hash
        hash_value = pairs.pop("hash", None)
        if not hash_value:
            logger.warning("No hash in init_data")
            return None

        # Sort and create check string
        check_string = "\n".join(
            f"{k}={v}" for k, v in sorted(pairs.items())
        )

        # Verify signature
        secret_key = hmac.new(
            "WebAppData".encode(),
            bot_token.encode(),
            hashlib.sha256,
        ).digest()

        computed_hash = hmac.new(
            secret_key,
            check_string.encode(),
            hashlib.sha256,
        ).hexdigest()

        if computed_hash != hash_value:
            logger.warning(f"Invalid hash: {computed_hash} != {hash_value}")
            return None

        # Parse user data
        user_data = json.loads(pairs.get("user", "{}"))
        return user_data

    except Exception as e:
        logger.error(f"Error verifying init_data: {e}")
        return None


def create_jwt_token(user_id: int, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT token"""
    if expires_delta is None:
        expires_delta = timedelta(days=30)

    expire = datetime.utcnow() + expires_delta
    payload = {
        "sub": str(user_id),
        "exp": expire,
    }

    token = jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )
    return token


def verify_jwt_token(token: str) -> Optional[int]:
    """Verify JWT token and return user_id"""
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )
        user_id = int(payload.get("sub"))
        return user_id
    except Exception as e:
        logger.error(f"Error verifying token: {e}")
        return None
