# core/management/commands/seed_simplove.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.models import Profile
from matches.models import Evaluation, Match
from random import Random, randint, choice
from datetime import date
import json, os

# Optional inline presets; edit as you wish
PREDEFINED = [
    {"username":"alice","email":"alice@example.com","password":"test1234","profile":{"language":"FR","phone_number":"0600000001","birth_date":[1995,5,1]}},
    {"username":"bob","email":"bob@example.com","password":"test1234","profile":{"language":"EN","phone_number":"0600000002","birth_date":[1993,9,20]}},
    {"username":"carol","email":"carol@example.com","password":"test1234","profile":{"language":"FR","phone_number":"0600000003","birth_date":[1990,1,15]}},
]

def ensure_user_with_profile(User, row):
    u, _ = User.objects.get_or_create(
        username=row["username"],
        defaults={"email": row.get("email", f'{row["username"]}@example.com')}
    )
    if row.get("password") and not u.check_password(row["password"]):
        u.set_password(row["password"]); u.save()
    p = row.get("profile", {})
    # allow profile.birth_date as [YYYY, M, D] or "YYYY-MM-DD"
    bd = p.get("birth_date")
    if isinstance(bd, (list, tuple)) and len(bd) == 3:
        p["birth_date"] = date(*bd)
    Profile.objects.update_or_create(user=u, defaults={
        "language": p.get("language", "FR"),
        "phone_number": p.get("phone_number", ""),
        "birth_date": p.get("birth_date", date(1990,1,1)),
    })
    return u

class Command(BaseCommand):
    help = "Seed users/profiles/evaluations/matches (random + optional predefined)."

    def add_arguments(self, parser):
        parser.add_argument("--n", type=int, default=20, help="Random users to create")
        parser.add_argument("--mutual_prob", type=float, default=0.25,
                            help="Probability that a pair becomes a mutual like")
        parser.add_argument("--seed", type=int, default=42, help="RNG seed")
        parser.add_argument("--with-predefined", action="store_true",
                            help="Also create predefined users from the inline list")
        parser.add_argument("--from_json", type=str, default="",
                            help="Path to JSON file with predefined users")

    def handle(self, *args, **opts):
        rng = Random(opts["seed"])
        User = get_user_model()
        users = []

        # 1) Predefined (inline or from JSON)
        if opts["with_predefined"]:
            for row in PREDEFINED:
                users.append(ensure_user_with_profile(User, row))

        if opts["from_json"]:
            path = opts["from_json"]
            if not os.path.exists(path):
                raise SystemExit(f"JSON file not found: {path}")
            data = json.load(open(path, "r", encoding="utf-8"))
            if not isinstance(data, list):
                raise SystemExit("JSON must be a list of user dicts")
            for row in data:
                users.append(ensure_user_with_profile(User, row))

        # 2) Random users
        for i in range(1, opts["n"] + 1):
            u, _ = User.objects.get_or_create(
                username=f"user{i}", defaults={"email": f"user{i}@example.com"}
            )
            if not u.has_usable_password():
                u.set_password("test1234"); u.save()
            Profile.objects.get_or_create(user=u, defaults={
                "language": "FR", "phone_number": "", "birth_date": date(1990,1,1)
            })
            users.append(u)

        # Deduplicate
        users = list({u.id: u for u in users}.values())

        # 3) Evaluations + Matches
        for i, a in enumerate(users):
            for b in users[i+1:]:
                if rng.random() < opts["mutual_prob"]:
                    Evaluation.objects.update_or_create(evaluator=a, target=b,
                                                    defaults={"status": Evaluation.LIKE})
                    Evaluation.objects.update_or_create(evaluator=b, target=a,
                                                    defaults={"status": Evaluation.LIKE})
                    u1, u2 = sorted([a, b], key=lambda u: u.id)
                    Match.objects.get_or_create(user1=u1, user2=u2, defaults={"is_active": True})
                else:
                    liker = rng.choice([a, b]); other = b if liker is a else a
                    status = Evaluation.LIKE if rng.random() < 0.5 else Evaluation.UNLIKE
                    Evaluation.objects.update_or_create(evaluator=liker, target=other,
                                                    defaults={"status": status})

        self.stdout.write(self.style.SUCCESS(
            f"Seed complete. Users total: {len(users)}"
        ))


