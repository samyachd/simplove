from django.test import TestCase

# Create your tests here.

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from .models import Like, Match

User = get_user_model()

class LikeMatchTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username="alice", password="x")
        self.bob   = User.objects.create_user(username="bob",   password="x")

    def test_like_unique_per_pair(self):
        Like.objects.create(user=self.alice, target=self.bob)
        with self.assertRaises(IntegrityError):
            Like.objects.create(user=self.alice, target=self.bob)

    def test_mutual_like_creates_match(self):
        Like.objects.create(user=self.alice, target=self.bob)
        self.assertFalse(Match.objects.exists())
        Like.objects.create(user=self.bob, target=self.alice)
        self.assertEqual(Match.objects.count(), 1)
        m = Match.objects.first()
        self.assertTrue(m.is_active)
        # ordering enforced
        self.assertLess(m.user1_id, m.user2_id)

    def test_unlike_deactivates_match(self):
        # make it mutual
        Like.objects.create(user=self.alice, target=self.bob)
        Like.objects.create(user=self.bob,   target=self.alice)
        m = Match.objects.first()
        self.assertTrue(m.is_active)
        # alice unlikes bob -> deactivate
        Like.objects.get(user=self.alice, target=self.bob).delete()
        m.refresh_from_db()
        self.assertFalse(m.is_active)
