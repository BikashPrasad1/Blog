from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from blogs.models import Blog, Category


class Command(BaseCommand):
    help = "Seed sample categories and blog posts"

    def handle(self, *args, **options):
        User = get_user_model()

        user, user_created = User.objects.get_or_create(
            username="demo_author",
            defaults={
                "email": "demo_author@example.com",
                "first_name": "Demo",
                "last_name": "Author",
            },
        )

        if user_created:
            user.set_password("demo12345")
            user.save(update_fields=["password"])
            self.stdout.write(self.style.SUCCESS("Created demo author: demo_author / demo12345"))

        category_names = [
            "Technology",
            "Web Development",
            "Productivity",
            "Design",
            "Lifestyle",
        ]

        categories = {}
        for name in category_names:
            category, _ = Category.objects.get_or_create(category_name=name)
            categories[name] = category

        seed_posts = [
            {
                "title": "How to Build a Django Blog That Scales",
                "category": "Technology",
                "short_description": "A practical checklist to structure your Django blog app for speed, clarity, and maintainability.",
                "blog_body": "Start by separating app concerns clearly: content models, query logic, and templates. Then optimize ORM queries with select_related and prefetch_related where needed. Use caching for frequently visited pages, and keep templates component-oriented for easier UI changes.",
                "is_featured": True,
            },
            {
                "title": "Modern CSS Patterns for Cleaner Layouts",
                "category": "Web Development",
                "short_description": "Use CSS variables, spacing systems, and reusable card components to keep styles predictable.",
                "blog_body": "Define a global token system for colors, spacing, and typography. Build reusable utility classes for common layout patterns. Avoid over-specific selectors and keep responsive behavior deliberate using breakpoint-based overrides.",
                "is_featured": True,
            },
            {
                "title": "5 Deep Work Habits for Developers",
                "category": "Productivity",
                "short_description": "Simple habits that reduce context switching and improve output quality during coding sessions.",
                "blog_body": "Batch notifications, set clear sprint goals, and work in focused time blocks. Keep a short task queue and close unrelated tabs before coding. End each session by writing the next actionable step.",
                "is_featured": False,
            },
            {
                "title": "Designing Blog Pages That Feel Premium",
                "category": "Design",
                "short_description": "Typography, contrast, and spacing decisions that make blog content easier and more enjoyable to read.",
                "blog_body": "Use one expressive heading font with a neutral body font. Maintain generous line-height and whitespace. Prioritize reading flow by reducing visual clutter and keeping action buttons secondary to content.",
                "is_featured": False,
            },
            {
                "title": "Morning Routines That Actually Stick",
                "category": "Lifestyle",
                "short_description": "Build a low-friction routine that supports focus and consistency without overcomplicating your day.",
                "blog_body": "Anchor your routine to one non-negotiable habit, then expand only when it feels automatic. Keep the system simple and measurable. Consistency beats intensity when building sustainable routines.",
                "is_featured": False,
            },
        ]

        created_count = 0
        for index, post_data in enumerate(seed_posts, start=1):
            slug = slugify(post_data["title"])
            _, created = Blog.objects.get_or_create(
                slug=slug,
                defaults={
                    "title": post_data["title"],
                    "category": categories[post_data["category"]],
                    "author": user,
                    "featured_image": f"upload/seed/post-{index}.jpg",
                    "short_description": post_data["short_description"],
                    "blog_body": post_data["blog_body"],
                    "status": "Published",
                    "is_featured": post_data["is_featured"],
                },
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f"Seed complete. Created {created_count} new post(s)."))
