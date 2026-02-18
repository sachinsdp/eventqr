import qrcode
import os
import re
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from .models import Participant, MealScan
from io import BytesIO
from django.http import HttpResponse
from django.db.models import Count


EVENT_PREFIX = "EVENT2026"


def dashboard(request):

    stats = (
        MealScan.objects
        .values("day", "meal")
        .annotate(total=Count("id"))
        .order_by("day")
    )

    return render(request, "dashboard.html", {"stats": stats})

def generate_qr(request):

    if request.method == "POST":
        name = request.POST.get("name").strip()
        reg_no = request.POST.get("reg_no").strip()

        # Check if reg_no exists
        participant, created = Participant.objects.get_or_create(reg_no=reg_no)

        # ALWAYS update name
        participant.name = name
        participant.save()

        qr_data = f"{EVENT_PREFIX}|{participant.id}"

        # Generate QR
        qr = qrcode.make(qr_data)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")

        # Safe filename
        safe_name = re.sub(r'[^A-Za-z0-9]+', '_', participant.name).strip('_')
        if not safe_name:
            safe_name = "Participant"

        filename = f"{safe_name}_{participant.reg_no}.png"

        response = HttpResponse(buffer.getvalue(), content_type="image/png")
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        return response

    return render(request, "generate.html")

def scanner_page(request):
    return render(request, "scanner.html")


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Participant, MealScan

EVENT_PREFIX = "EVENT2026"

# Allowed structure
ALLOWED_MEALS = {
    "1": ["snack1", "lunch", "snack2", "dinner"],
    "2": ["snack1", "lunch", "snack2"],
    "3": ["snack1", "lunch", "snack2"],
}


@csrf_exempt  # only if you are using fetch() without CSRF token
def verify_scan(request):

    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Invalid request method"})

    qr_data = request.POST.get("qr_data")
    day = request.POST.get("day")
    meal = request.POST.get("meal")

    # Basic validation
    if not qr_data or not day or not meal:
        return JsonResponse({"status": "error", "message": "Missing data"})

    try:
        prefix, participant_id = qr_data.split("|")

        # Validate event
        if prefix != EVENT_PREFIX:
            return JsonResponse({"status": "error", "message": "Invalid QR Code"})

        # Validate participant
        participant = Participant.objects.get(id=participant_id)

        # Validate day
        if day not in ALLOWED_MEALS:
            return JsonResponse({"status": "error", "message": "Invalid Day Selected"})

        # Validate meal for that day
        if meal not in ALLOWED_MEALS[day]:
            return JsonResponse({
                "status": "error",
                "message": f"{meal.title()} not available on Day {day}"
            })

        # Prevent duplicate scan
        if MealScan.objects.filter(
            participant=participant,
            day=day,
            meal=meal
        ).exists():
            return JsonResponse({
                "status": "duplicate",
                "message": f"{participant.name} already used Day {day} {meal.title()}"
            })

        # Save scan
        MealScan.objects.create(
            participant=participant,
            day=day,
            meal=meal
        )

        return JsonResponse({
            "status": "success",
            "message": f"{participant.name} allowed for Day {day} {meal.title()}"
        })

    except Participant.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Participant not found"})

    except ValueError:
        return JsonResponse({"status": "error", "message": "Invalid QR format"})

    except Exception as e:
        return JsonResponse({"status": "error", "message": "Something went wrong"})
