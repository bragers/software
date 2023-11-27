# polls/management/commands/populate_articles.py
import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from polls.models import Location, Language, Article


class Command(BaseCommand):
    help = 'Populate articles for testing'

    def handle(self, *args, **options):
        # Create locations and languages
        locations = ['Norway', 'Sweden', 'Denmark']
        languages = ['English', 'Norwegian']

        for location_name in locations:
            Location.objects.get_or_create(name=location_name)

        for language_name in languages:
            Language.objects.get_or_create(name=language_name)

        # Create sample articles
        for i in range(50):
            Article.objects.create(
                title=f"Article {i + 1}",
                pub_date=timezone.now(),
                for_kids=random.choice([True, False]),
                high_activity=random.choice([True, False]),
                location=Location.objects.get(name=random.choice(locations)),
                language=Language.objects.get(name=random.choice(languages)),
                free=random.choice([True, False]),
                slot1_remaining_count=20,  # Adjust this based on your requirements
                slot2_remaining_count=20,
                slot3_remaining_count=20,
                # Add more fields as needed
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated articles'))
