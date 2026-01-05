from django.core.management.base import BaseCommand
from Posts.models import News

class Command(BaseCommand):
    help = "Seed default news for sidebar"

    def handle(self, *args, **kwargs):
        news_data = [
            ("Django 5 Released", "django", "Performance & ORM improvements"),
            ("Python Hiring Boom", "python", "Top companies hiring"),
            ("AI in Web Development", "ai", "AI tools trending"),
            ("Internships 2026", "intern", "Fresh opportunities"),
            ("Remote Jobs Rise", "jobs", "Remote roles increasing"),
        ]

        for title, tag, desc in news_data:
            News.objects.get_or_create(
                title=title,
                tag=tag,
                description=desc
            )

        self.stdout.write("✅ Default news added successfully")
