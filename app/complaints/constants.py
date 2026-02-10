# complaints/constants.py
import json
import logging
from django.conf import settings
from pathlib import Path

logger = logging.getLogger(__name__)

CATEGORY_SCORE_MAP = {}

path = Path(settings.BASE_DIR) / "config" / "category_scores.json"

try:
    with open(path) as f:
        CATEGORY_SCORE_MAP = json.load(f)

    logger.info(
        "Category score config loaded",
        extra={
            "path": str(path),
            "entries": len(CATEGORY_SCORE_MAP),
        },
    )

except FileNotFoundError:
    logger.error(
        "Category score config file not found",
        extra={"path": str(path)},
    )

except Exception:
    logger.exception(
        "Unexpected error while loading category score config",
        extra={"path": str(path)},
    )
