from django.urls import path

from . import views

urlpatterns = [
    path("auth/login", views.login_view),
    path("auth/register", views.register_view),
    path("auth/logout", views.logout_view),
    path("auth/check", views.check_auth_view),
    path("schools", views.school_list),
    path("students", views.student_list),
    path("students/<uuid:student_id>", views.student_detail),
    path("students/<uuid:student_id>/ratings", views.student_ratings),
    path("ratings", views.ratings_view),
    path("leaderboard", views.leaderboard_view),
    path("badges", views.badge_list),
    path("student-badges/<uuid:student_id>", views.student_badge_list),
    path("school-applications", views.school_applications_view),
    path("school-applications/<uuid:application_id>", views.school_application_detail_view),
    path("student-applications", views.student_applications_view),
    path("student-applications/<uuid:application_id>", views.student_application_detail_view),
]

