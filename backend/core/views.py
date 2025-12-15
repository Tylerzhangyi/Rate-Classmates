import uuid
from decimal import Decimal
from typing import Any

from django.db import transaction
from django.db.models import Avg, Count, F, Sum
from django.http import HttpRequest
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import (
    Badge,
    Leaderboard,
    LeaderboardEntry,
    Rating,
    RatingSummary,
    School,
    SchoolApplication,
    SchoolBadge,
    Student,
    StudentApplication,
    StudentBadge,
    User,
)
from .utils import allow_methods, api_response, parse_json


def _user_payload(user: User) -> dict[str, Any]:
    return {
        "user_id": str(user.user_id),
        "account": user.account,
        "role": user.role,
    }


@csrf_exempt
@allow_methods(["POST"])
def register_view(request: HttpRequest):
    payload = parse_json(request)
    account = payload.get("account")
    password = payload.get("password")
    if not account or not password:
        return api_response(400, "account 和 password 必填", status=400)
    if User.objects.filter(account=account).exists():
        return api_response(400, "账号已存在", status=400)
    user = User.objects.create(account=account, password=password)
    return api_response(200, "注册成功", _user_payload(user))


@csrf_exempt
@allow_methods(["POST"])
def login_view(request: HttpRequest):
    payload = parse_json(request)
    account = payload.get("account")
    password = payload.get("password")
    try:
        user = User.objects.get(account=account, password=password)
    except User.DoesNotExist:
        return api_response(401, "账号或密码错误", status=401)
    return api_response(200, "登录成功", _user_payload(user))


def school_list(request: HttpRequest):
    schools = list(School.objects.all().order_by("created_at").values("school_id", "school_name", "created_at"))
    for item in schools:
        item["school_id"] = str(item["school_id"])
    return api_response(data=schools)


def _student_to_dict(student: Student) -> dict[str, Any]:
    summary = getattr(student, "rating_summary", None)
    return {
        "student_id": str(student.student_id),
        "name": student.name,
        "grade": student.grade,
        "school_id": str(student.school_id),
        "school_name": student.school.school_name if student.school else "",
        "avg_score": float(summary.avg_score) if summary else 0.0,
        "rating_count": summary.rating_count if summary else 0,
    }


def student_list(request: HttpRequest):
    qs = Student.objects.select_related("school", "rating_summary").all()
    school_id = request.GET.get("school_id")
    grade = request.GET.get("grade")
    if school_id:
        qs = qs.filter(school_id=school_id)
    if grade:
        qs = qs.filter(grade=grade)
    students = [_student_to_dict(s) for s in qs]
    return api_response(data=students)


def student_detail(request: HttpRequest, student_id: uuid.UUID):
    try:
        student = Student.objects.select_related("school", "rating_summary").get(student_id=student_id)
    except Student.DoesNotExist:
        return api_response(404, "student not found", status=404)
    return api_response(data=_student_to_dict(student))


def student_ratings(request: HttpRequest, student_id: uuid.UUID):
    ratings = (
        Rating.objects.filter(target_id=student_id)
        .select_related("rater")
        .order_by("-created_at")
        .values("rating_id", "rater_id", "rater__account", "score", "comment", "created_at")
    )
    result = [
        {
            "rating_id": str(item["rating_id"]),
            "rater_id": str(item["rater_id"]),
            "rater_name": item["rater__account"],
            "target_id": str(student_id),
            "score": item["score"],
            "comment": item["comment"],
            "created_at": item["created_at"].isoformat(),
        }
        for item in ratings
    ]
    return api_response(data=result)


@csrf_exempt
@allow_methods(["GET", "POST"])
def ratings_view(request: HttpRequest):
    if request.method == "GET":
        rater_id = request.GET.get("rater_id")
        if not rater_id:
            return api_response(400, "缺少 rater_id", status=400)
        ratings = (
            Rating.objects.filter(rater_id=rater_id)
            .select_related("target")
            .order_by("-created_at")
            .values(
                "rating_id",
                "target_id",
                "target__name",
                "score",
                "comment",
                "created_at",
            )
        )
        data = [
            {
                "rating_id": str(r["rating_id"]),
                "target_id": str(r["target_id"]),
                "target_name": r["target__name"],
                "score": r["score"],
                "comment": r["comment"],
                "created_at": r["created_at"].isoformat(),
            }
            for r in ratings
        ]
        return api_response(data=data)

    # POST 评分创建/更新
    payload = parse_json(request)
    rater_id = payload.get("rater_id")
    target_id = payload.get("target_id")
    score = payload.get("score")
    comment = payload.get("comment", "")
    if not (rater_id and target_id and score):
        return api_response(400, "rater_id, target_id, score 必填", status=400)
    try:
        rater = User.objects.get(user_id=rater_id)
        target = Student.objects.get(student_id=target_id)
    except (User.DoesNotExist, Student.DoesNotExist):
        return api_response(404, "用户或学生不存在", status=404)

    with transaction.atomic():
        rating, _created = Rating.objects.update_or_create(
            rater=rater,
            target=target,
            defaults={"score": score, "comment": comment},
        )
        # 更新汇总
        agg = Rating.objects.filter(target=target).aggregate(
            avg=Avg("score"),
            cnt=Count("rating_id"),
        )
        RatingSummary.objects.update_or_create(
            target=target,
            defaults={
                "avg_score": Decimal(agg["avg"] or 0).quantize(Decimal("0.01")),
                "rating_count": agg["cnt"] or 0,
                "last_update": timezone.now(),
            },
        )

    return api_response(data={"rating_id": str(rating.rating_id)})


def badge_list(request: HttpRequest):
    badges = list(
        Badge.objects.all()
        .order_by("badge_type", "name")
        .values("badge_id", "name", "description", "badge_type", "rule_desc")
    )
    for item in badges:
        item["badge_id"] = str(item["badge_id"])
    return api_response(data=badges)


def student_badge_list(request: HttpRequest, student_id: uuid.UUID):
    badges = (
        StudentBadge.objects.filter(student_id=student_id)
        .select_related("badge")
        .values(
            "student_badge_id",
            "badge_id",
            "badge__name",
            "period",
            "awarded_at",
        )
    )
    result = [
        {
            "id": str(item["student_badge_id"]),
            "badge_id": str(item["badge_id"]),
            "badge_name": item["badge__name"],
            "period": item["period"],
            "awarded_at": item["awarded_at"].isoformat(),
        }
        for item in badges
    ]
    return api_response(data=result)


@csrf_exempt
@allow_methods(["GET", "POST"])
def school_applications_view(request: HttpRequest):
    if request.method == "GET":
        status = request.GET.get("status")
        applicant_id = request.GET.get("applicant_id")
        qs = SchoolApplication.objects.all().order_by("-created_at")
        if status:
            qs = qs.filter(status=status)
        if applicant_id:
            qs = qs.filter(applicant_id=applicant_id)
        data = [
            {
                "application_id": str(app.application_id),
                "applicant_id": str(app.applicant_id),
                "school_name": app.school_name,
                "contact": app.contact,
                "reason": app.reason,
                "status": app.status,
                "created_at": app.created_at.isoformat(),
                "updated_at": app.updated_at.isoformat() if app.updated_at else None,
            }
            for app in qs
        ]
        return api_response(data=data)

    # POST 创建申请
    payload = parse_json(request)
    required = ["applicant_id", "school_name", "contact"]
    if any(not payload.get(k) for k in required):
        return api_response(400, "缺少必填字段", status=400)
    try:
        applicant = User.objects.get(user_id=payload["applicant_id"])
    except User.DoesNotExist:
        return api_response(404, "applicant 不存在", status=404)
    app = SchoolApplication.objects.create(
        applicant=applicant,
        school_name=payload["school_name"],
        contact=payload["contact"],
        reason=payload.get("reason") or "",
    )
    return api_response(data={"application_id": str(app.application_id)})


@csrf_exempt
@allow_methods(["PATCH"])
def school_application_detail_view(request: HttpRequest, application_id: uuid.UUID):
    try:
        app = SchoolApplication.objects.get(application_id=application_id)
    except SchoolApplication.DoesNotExist:
        return api_response(404, "申请不存在", status=404)

    payload = parse_json(request)
    status = payload.get("status")
    if status not in {"pending", "approved", "rejected"}:
        return api_response(400, "非法状态", status=400)

    with transaction.atomic():
        app.status = status
        app.save(update_fields=["status", "updated_at"])

        # 审核通过时，如学校不存在则创建
        if status == "approved":
            exists = School.objects.filter(school_name__iexact=app.school_name).exists()
            if not exists:
                School.objects.create(school_name=app.school_name)

    return api_response(data={"application_id": str(app.application_id), "status": app.status})


@csrf_exempt
@allow_methods(["GET", "POST"])
def student_applications_view(request: HttpRequest):
    if request.method == "GET":
        status = request.GET.get("status")
        applicant_id = request.GET.get("applicant_id")
        qs = StudentApplication.objects.select_related("school").all().order_by("-created_at")
        if status:
            qs = qs.filter(status=status)
        if applicant_id:
            qs = qs.filter(applicant_id=applicant_id)
        data = [
            {
                "application_id": str(app.application_id),
                "applicant_id": str(app.applicant_id),
                "student_name": app.student_name,
                "school_id": str(app.school_id),
                "school_name": app.school.school_name if app.school else "",
                "grade": app.grade,
                "reason": app.reason,
                "status": app.status,
                "created_at": app.created_at.isoformat(),
                "updated_at": app.updated_at.isoformat() if app.updated_at else None,
            }
            for app in qs
        ]
        return api_response(data=data)

    # POST 创建申请
    payload = parse_json(request)
    required = ["applicant_id", "student_name", "school_id", "grade"]
    if any(not payload.get(k) for k in required):
        return api_response(400, "缺少必填字段", status=400)
    try:
        applicant = User.objects.get(user_id=payload["applicant_id"])
        school = School.objects.get(school_id=payload["school_id"])
    except (User.DoesNotExist, School.DoesNotExist):
        return api_response(404, "applicant 或 school 不存在", status=404)
    app = StudentApplication.objects.create(
        applicant=applicant,
        student_name=payload["student_name"],
        school=school,
        grade=payload["grade"],
        reason=payload.get("reason") or "",
    )
    return api_response(data={"application_id": str(app.application_id)})


@csrf_exempt
@allow_methods(["PATCH"])
def student_application_detail_view(request: HttpRequest, application_id: uuid.UUID):
    try:
        app = StudentApplication.objects.select_related("school").get(application_id=application_id)
    except StudentApplication.DoesNotExist:
        return api_response(404, "申请不存在", status=404)

    payload = parse_json(request)
    status = payload.get("status")
    if status not in {"pending", "approved", "rejected"}:
        return api_response(400, "非法状态", status=400)

    with transaction.atomic():
        app.status = status
        app.save(update_fields=["status", "updated_at"])

        # 通过时若学生不存在则添加
        if status == "approved":
            exists = Student.objects.filter(
                name=app.student_name,
                school_id=app.school_id,
                grade=app.grade,
            ).exists()
            if not exists:
                Student.objects.create(
                    school=app.school,
                    name=app.student_name,
                    grade=app.grade,
                )

    return api_response(data={"application_id": str(app.application_id), "status": app.status})


def leaderboard_view(request: HttpRequest):
    lb_type = request.GET.get("type", "all")
    if lb_type == "school":
        data = (
            Student.objects.select_related("school", "rating_summary")
            .values("school_id", "school__school_name")
            .annotate(
                total_score=Sum(F("rating_summary__avg_score") * F("rating_summary__rating_count")),
                total_count=Sum("rating_summary__rating_count"),
            )
        )
        result = []
        for item in data:
            total_count = item["total_count"] or 0
            avg = (item["total_score"] / total_count) if total_count else 0
            result.append(
                {
                    "school_id": str(item["school_id"]),
                    "school_name": item["school__school_name"],
                    "avg_score": float(Decimal(avg).quantize(Decimal("0.01"))) if total_count else 0,
                    "rating_count": total_count,
                }
            )
        result.sort(key=lambda x: (-x["avg_score"], -x["rating_count"]))
        return api_response(data=result[:10])

    # 综合榜：按 avg_score 与 rating_count 排序
    students = (
        Student.objects.select_related("rating_summary", "school")
        .filter(rating_summary__rating_count__gt=0)
        .order_by("-rating_summary__avg_score", "-rating_summary__rating_count")[:10]
    )
    result = [
        {
            **_student_to_dict(s),
            "rank": idx + 1,
        }
        for idx, s in enumerate(students)
    ]
    return api_response(data=result)

