import uuid

from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator


class User(models.Model):
    class Role(models.TextChoices):
        USER = "user", "user"
        ADMIN = "admin", "admin"

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)  # 按需求存明文
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.USER)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user"
        indexes = [
            models.Index(fields=["account"]),
        ]

    def __str__(self) -> str:
        return self.account


class School(models.Model):
    school_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    school_name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "school"
        indexes = [
            models.Index(fields=["school_name"]),
        ]

    def __str__(self) -> str:
        return self.school_name


class Student(models.Model):
    student_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="students")
    name = models.CharField(max_length=255)
    grade = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "student"
        indexes = [
            models.Index(fields=["school", "grade"]),
            models.Index(fields=["name"]),
        ]

    def __str__(self) -> str:
        return self.name


class Rating(models.Model):
    rating_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rater = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ratings_given")
    target = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="ratings_received")
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, message="评分不得低于1"),
            MaxValueValidator(5, message="评分不得高于5"),
        ]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "rating"
        constraints = [
            models.UniqueConstraint(fields=["rater", "target"], name="unique_rating_per_target"),
        ]
        indexes = [
            models.Index(fields=["rater"]),
            models.Index(fields=["target"]),
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.rater_id} -> {self.target_id}"


class RatingSummary(models.Model):
    target = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="rating_summary",
    )
    avg_score = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    rating_count = models.PositiveIntegerField(default=0)
    last_update = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "rating_summary"
        indexes = [
            models.Index(fields=["avg_score"]),
            models.Index(fields=["rating_count"]),
        ]

    def __str__(self) -> str:
        return f"{self.target_id} summary"


class Badge(models.Model):
    class BadgeType(models.TextChoices):
        STUDENT = "student", "student"
        SCHOOL = "school", "school"

    badge_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    badge_type = models.CharField(max_length=10, choices=BadgeType.choices)
    rule_desc = models.TextField(blank=True)

    class Meta:
        db_table = "badge"
        indexes = [
            models.Index(fields=["badge_type"]),
            models.Index(fields=["name"]),
        ]

    def __str__(self) -> str:
        return self.name


class StudentBadge(models.Model):
    student_badge_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="badges")
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name="student_badges")
    period = models.CharField(max_length=50)
    awarded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "student_badge"
        indexes = [
            models.Index(fields=["student"]),
            models.Index(fields=["badge"]),
            models.Index(fields=["period"]),
        ]
        constraints = [
            models.UniqueConstraint(fields=["student", "badge", "period"], name="unique_student_badge_period"),
        ]

    def __str__(self) -> str:
        return f"{self.student_id}-{self.badge_id}"


class SchoolBadge(models.Model):
    school_badge_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="badges")
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name="school_badges")
    period = models.CharField(max_length=50)
    awarded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "school_badge"
        indexes = [
            models.Index(fields=["school"]),
            models.Index(fields=["badge"]),
            models.Index(fields=["period"]),
        ]
        constraints = [
            models.UniqueConstraint(fields=["school", "badge", "period"], name="unique_school_badge_period"),
        ]

    def __str__(self) -> str:
        return f"{self.school_id}-{self.badge_id}"


class Leaderboard(models.Model):
    leaderboard_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50)
    formula = models.TextField(help_text="榜单评分计算规则描述")

    class Meta:
        db_table = "leaderboard"
        indexes = [
            models.Index(fields=["type"]),
            models.Index(fields=["name"]),
        ]

    def __str__(self) -> str:
        return self.name


class LeaderboardEntry(models.Model):
    entry_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    leaderboard = models.ForeignKey(Leaderboard, on_delete=models.CASCADE, related_name="entries")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="leaderboard_entries")
    rank = models.IntegerField()
    score_snapshot = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        db_table = "leaderboard_entry"
        constraints = [
            models.UniqueConstraint(fields=["leaderboard", "student"], name="unique_leaderboard_student"),
        ]
        indexes = [
            models.Index(fields=["leaderboard", "rank"]),
            models.Index(fields=["student"]),
        ]

    def __str__(self) -> str:
        return f"{self.leaderboard_id}#{self.rank}"


class SchoolApplication(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "pending"
        APPROVED = "approved", "approved"
        REJECTED = "rejected", "rejected"

    application_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="school_applications")
    school_name = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "school_application"
        indexes = [
            models.Index(fields=["applicant"]),
            models.Index(fields=["status"]),
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.school_name} ({self.status})"


class StudentApplication(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "pending"
        APPROVED = "approved", "approved"
        REJECTED = "rejected", "rejected"

    application_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="student_applications")
    student_name = models.CharField(max_length=255)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="student_applications")
    grade = models.IntegerField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "student_application"
        indexes = [
            models.Index(fields=["applicant"]),
            models.Index(fields=["school"]),
            models.Index(fields=["status"]),
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.student_name} ({self.status})"

