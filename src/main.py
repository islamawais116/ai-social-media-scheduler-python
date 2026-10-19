"""Run with python -m src.main."""
from datetime import datetime, timedelta, timezone
from .scheduler import schedule_post, save_posts


def main():
    date = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()
    post = schedule_post('linkedin', 'Plan, create, and schedule social content.', date)
    save_posts([post], 'scheduled_posts.json')
    print(f'Scheduled {post.platform} post for {post.publish_at}')
    print('Saved to scheduled_posts.json (demo only; not published online).')


if __name__ == '__main__':
    main()
