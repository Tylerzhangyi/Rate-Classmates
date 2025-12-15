from django.contrib import admin

from . import models


@admin.register(
    models.User,
    models.School,
    models.Student,
    models.Rating,
    models.RatingSummary,
    models.Badge,
    models.StudentBadge,
    models.SchoolBadge,
    models.Leaderboard,
    models.LeaderboardEntry,
    models.SchoolApplication,
    models.StudentApplication,
)
class CoreAdmin(admin.ModelAdmin):
    pass

