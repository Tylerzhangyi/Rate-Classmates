from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid
import django.core.validators


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Badge",
            fields=[
                ("badge_id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True)),
                ("badge_type", models.CharField(choices=[("student", "student"), ("school", "school")], max_length=10)),
                ("rule_desc", models.TextField(blank=True)),
            ],
            options={
                "db_table": "badge",
                "indexes": [
                    models.Index(fields=["badge_type"], name="badge_badge__ada96f_idx"),
                    models.Index(fields=["name"], name="badge_name_f0d0e9_idx"),
                ],
            },
        ),
        migrations.CreateModel(
            name="Leaderboard",
            fields=[
                ("leaderboard_id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255)),
                ("type", models.CharField(max_length=50)),
                ("formula", models.TextField(help_text="榜单评分计算规则描述")),
            ],
            options={
                "db_table": "leaderboard",
                "indexes": [
                    models.Index(fields=["type"], name="leaderboard_type_5c53c5_idx"),
                    models.Index(fields=["name"], name="leaderboard_name_6ca6b2_idx"),
                ],
            },
        ),
        migrations.CreateModel(
            name="School",
            fields=[
                ("school_id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("school_name", models.CharField(max_length=255, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "db_table": "school",
                "indexes": [
                    models.Index(fields=["school_name"], name="school_school__9551b2_idx"),
                ],
            },
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                ("user_id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("account", models.CharField(max_length=255, unique=True)),
                ("password", models.CharField(max_length=255)),
                ("role", models.CharField(choices=[("user", "user"), ("admin", "admin")], default="user", max_length=10)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "db_table": "user",
                "indexes": [
                    models.Index(fields=["account"], name="user_account_4bb44e_idx"),
                ],
            },
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                ("student_id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255)),
                ("grade", models.IntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("school", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="students", to="core.school")),
            ],
            options={
                "db_table": "student",
                "indexes": [
                    models.Index(fields=["school", "grade"], name="student_school__f3c9b4_idx"),
                    models.Index(fields=["name"], name="student_name_6eaa1e_idx"),
                ],
            },
        ),
        migrations.CreateModel(
            name="RatingSummary",
            fields=[
                ("target", models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    primary_key=True,
                    related_name="rating_summary",
                    serialize=False,
                    to="core.student",
                )),
                ("avg_score", models.DecimalField(decimal_places=2, default=0, max_digits=3)),
                ("rating_count", models.PositiveIntegerField(default=0)),
                ("last_update", models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                "db_table": "rating_summary",
                "indexes": [
                    models.Index(fields=["avg_score"], name="rating_su_avg_sco_01cfa8_idx"),
                    models.Index(fields=["rating_count"], name="rating_su_rating__6a0b1d_idx"),
                ],
            },
        ),
        migrations.CreateModel(
            name="Rating",
            fields=[
                ("rating_id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("score", models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, message="评分不得低于1"), django.core.validators.MaxValueValidator(5, message="评分不得高于5")])),
                ("comment", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("rater", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="ratings_given", to="core.user")),
                ("target", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="ratings_received", to="core.student")),
            ],
            options={
                "db_table": "rating",
                "indexes": [
                    models.Index(fields=["rater"], name="rating_rater__8f4480_idx"),
                    models.Index(fields=["target"], name="rating_target_4045f8_idx"),
                    models.Index(fields=["-created_at"], name="rating_created_f933a6_idx"),
                ],
                "constraints": [
                    models.UniqueConstraint(fields=("rater", "target"), name="unique_rating_per_target"),
                ],
            },
        ),
        migrations.CreateModel(
            name="SchoolBadge",
            fields=[
                ("school_badge_id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("period", models.CharField(max_length=50)),
                ("awarded_at", models.DateTimeField(auto_now_add=True)),
                ("badge", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="school_badges", to="core.badge")),
                ("school", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="badges", to="core.school")),
            ],
            options={
                "db_table": "school_badge",
                "indexes": [
                    models.Index(fields=["school"], name="school_bad_school__3d1f84_idx"),
                    models.Index(fields=["badge"], name="school_bad_badge_i_83d6cf_idx"),
                    models.Index(fields=["period"], name="school_bad_period_37b727_idx"),
                ],
                "constraints": [
                    models.UniqueConstraint(fields=("school", "badge", "period"), name="unique_school_badge_period"),
                ],
            },
        ),
        migrations.CreateModel(
            name="StudentBadge",
            fields=[
                ("student_badge_id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("period", models.CharField(max_length=50)),
                ("awarded_at", models.DateTimeField(auto_now_add=True)),
                ("badge", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="student_badges", to="core.badge")),
                ("student", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="badges", to="core.student")),
            ],
            options={
                "db_table": "student_badge",
                "indexes": [
                    models.Index(fields=["student"], name="student_ba_student_d4b486_idx"),
                    models.Index(fields=["badge"], name="student_ba_badge_i_3f1c62_idx"),
                    models.Index(fields=["period"], name="student_ba_period_0ad1b9_idx"),
                ],
                "constraints": [
                    models.UniqueConstraint(fields=("student", "badge", "period"), name="unique_student_badge_period"),
                ],
            },
        ),
        migrations.CreateModel(
            name="LeaderboardEntry",
            fields=[
                ("entry_id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("rank", models.IntegerField()),
                ("score_snapshot", models.DecimalField(decimal_places=2, max_digits=4)),
                ("leaderboard", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="entries", to="core.leaderboard")),
                ("student", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="leaderboard_entries", to="core.student")),
            ],
            options={
                "db_table": "leaderboard_entry",
                "indexes": [
                    models.Index(fields=["leaderboard", "rank"], name="leaderboar_leaderbo_b7df72_idx"),
                    models.Index(fields=["student"], name="leaderboar_student_6bcf6c_idx"),
                ],
                "constraints": [
                    models.UniqueConstraint(fields=("leaderboard", "student"), name="unique_leaderboard_student"),
                ],
            },
        ),
        migrations.CreateModel(
            name="SchoolApplication",
            fields=[
                ("application_id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("school_name", models.CharField(max_length=255)),
                ("contact", models.CharField(max_length=255)),
                ("reason", models.TextField()),
                ("status", models.CharField(choices=[("pending", "pending"), ("approved", "approved"), ("rejected", "rejected")], default="pending", max_length=10)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("applicant", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="school_applications", to="core.user")),
            ],
            options={
                "db_table": "school_application",
                "indexes": [
                    models.Index(fields=["applicant"], name="school_app_applican_40a5fd_idx"),
                    models.Index(fields=["status"], name="school_app_status_d8b030_idx"),
                    models.Index(fields=["-created_at"], name="school_app_created_852a98_idx"),
                ],
            },
        ),
        migrations.CreateModel(
            name="StudentApplication",
            fields=[
                ("application_id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("student_name", models.CharField(max_length=255)),
                ("grade", models.IntegerField()),
                ("reason", models.TextField()),
                ("status", models.CharField(choices=[("pending", "pending"), ("approved", "approved"), ("rejected", "rejected")], default="pending", max_length=10)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("applicant", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="student_applications", to="core.user")),
                ("school", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="student_applications", to="core.school")),
            ],
            options={
                "db_table": "student_application",
                "indexes": [
                    models.Index(fields=["applicant"], name="student_ap_applican_087657_idx"),
                    models.Index(fields=["school"], name="student_ap_school_i_438531_idx"),
                    models.Index(fields=["status"], name="student_ap_status_e1031d_idx"),
                    models.Index(fields=["-created_at"], name="student_ap_created_280f06_idx"),
                ],
            },
        ),
    ]

