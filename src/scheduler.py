"""Educational social media content scheduler; no external API calls."""
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import json
from pathlib import Path

SUPPORTED_PLATFORMS = {'instagram', 'facebook', 'linkedin', 'x', 'pinterest'}

@dataclass
class Post:
    platform: str
    content: str
    publish_at: str
    status: str = 'scheduled'


def schedule_post(platform: str, content: str, publish_at: str) -> Post:
    platform = platform.lower().strip()
    if platform not in SUPPORTED_PLATFORMS:
        raise ValueError(f'Unsupported platform: {platform}')
    if not content.strip():
        raise ValueError('Content cannot be empty')
    dt = datetime.fromisoformat(publish_at.replace('Z', '+00:00'))
    if dt.tzinfo is None:
        raise ValueError('publish_at must contain timezone information')
    if dt.astimezone(timezone.utc) <= datetime.now(timezone.utc):
        raise ValueError('publish_at must be in the future')
    return Post(platform, content.strip(), publish_at)


def save_posts(posts: list[Post], path: str) -> None:
    Path(path).write_text(json.dumps([asdict(post) for post in posts], indent=2), encoding='utf-8')
