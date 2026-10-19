import unittest
from datetime import datetime, timedelta, timezone
from tempfile import TemporaryDirectory
from pathlib import Path
from src.scheduler import schedule_post, save_posts


class SchedulerTests(unittest.TestCase):
    def setUp(self):
        self.tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()

    def test_valid_post(self):
        post = schedule_post('LinkedIn', 'Hello world', self.tomorrow)
        self.assertEqual(post.platform, 'linkedin')
        self.assertEqual(post.status, 'scheduled')

    def test_invalid_platform(self):
        with self.assertRaises(ValueError):
            schedule_post('unknown', 'Hello', self.tomorrow)

    def test_empty_content(self):
        with self.assertRaises(ValueError):
            schedule_post('linkedin', '  ', self.tomorrow)

    def test_naive_datetime(self):
        with self.assertRaises(ValueError):
            schedule_post('linkedin', 'Hello', '2030-01-01T12:00:00')

    def test_past_datetime(self):
        with self.assertRaises(ValueError):
            schedule_post('linkedin', 'Hello', '2020-01-01T12:00:00Z')

    def test_json_output(self):
        with TemporaryDirectory() as folder:
            path = str(Path(folder) / 'posts.json')
            save_posts([schedule_post('linkedin', 'Hello', self.tomorrow)], path)
            self.assertIn('Hello', Path(path).read_text())


if __name__ == '__main__':
    unittest.main()
