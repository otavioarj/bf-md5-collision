"""Rate limiting configuration."""
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


def setup_rate_limiter(app):
    """Configure rate limiting."""
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"],
        storage_uri="memory://",  # Use Redis in production
    )
    
    return limiter