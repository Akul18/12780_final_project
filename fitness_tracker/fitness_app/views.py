import openpyxl

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods

from .models import Exercise, SessionSet


def dashboard(request):
    exercises = Exercise.objects.all().order_by("name")
    return render(
        request,
        "dashboard.html",
        {
            "exercises": exercises,
            "error": request.GET.get("error"),
            "success": request.GET.get("success"),
        },
    )


def add_exercise(request):
    name = (request.POST.get("name") or "").strip()
    muscle_group = (request.POST.get("muscle_group") or "").strip()

    # Use %20 instead of spaces in URLs.

    # Missing an attribute
    if not name or not muscle_group:
        return redirect("/?error=Name%20and%20muscle%20group%20are%20required.")

    # Attribute already exists
    if Exercise.objects.filter(name__iexact=name).exists():
        return redirect("/?error=That%20exercise%20already%20exists.")

    Exercise.objects.create(name=name, muscle_group=muscle_group)
    return redirect("/")


def log_session(request):
    exercise_id = request.POST.get("exercise")
    performed_at = (request.POST.get("performed_at") or "").strip()

    weight_raw = (request.POST.get("weight") or "").strip()
    reps_raw = (request.POST.get("reps") or "").strip()

    if not exercise_id or not performed_at:
        return redirect("/?error=Exercise%20and%20date%20are%20required.")

    try:
        exercise = get_object_or_404(Exercise, id=int(exercise_id))
        weight = float(weight_raw) if weight_raw else None
        reps = int(reps_raw) if reps_raw else None

        SessionSet.objects.create(
            exercise=exercise,
            performed_at=performed_at,  
            weight=weight,
            reps=reps,
        )
        return redirect("/")
    except ValueError:
        return redirect("/?error=Invalid%20number%20entered%20(weight%20or%20reps).")


def chart_data(request):
    exercise_id = request.GET.get("exercise_id")
    metric = (request.GET.get("metric") or "weight").strip()

    qs = SessionSet.objects.order_by("performed_at", "id")
    if exercise_id:
        try:
            qs = qs.filter(exercise_id=int(exercise_id))
        except ValueError:
            return JsonResponse({"error": "Invalid exercise_id."}, status=400)

    labels = []
    data = []
    for s in qs:
        labels.append(s.performed_at.isoformat())
        data.append(getattr(s, metric))

    return JsonResponse({"labels": labels, "data": data, "metric": metric}) # To be used in javascript for chart js


def export_xlsx(request):
    exercise_id = request.GET.get("exercise_id")

    qs = SessionSet.objects.select_related("exercise").order_by("-performed_at", "-id")
    filename = "fitness_data.xlsx"

    if exercise_id:
        try:
            ex_id_int = int(exercise_id)
            ex = get_object_or_404(Exercise, id=ex_id_int)
            qs = qs.filter(exercise_id=ex_id_int)
            filename = f"fitness_data_{ex.name.replace(' ', '_')}.xlsx"
        except ValueError:
            return HttpResponse("Invalid exercise_id", status=400)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "SessionSets"

    headers = ["performed_at", "exercise", "muscle_group", "weight", "reps"]
    ws.append(headers)

    for s in qs:
        ws.append(
            [
                s.performed_at.isoformat(),
                s.exercise.name,
                s.exercise.muscle_group,
                s.weight,
                s.reps,
            ]
        )

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    wb.save(response)
    return response
