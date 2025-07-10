from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Bug
import json
# Create your views here.

@csrf_exempt
def bug_list_api(request):
    if request.method == "GET":
        bugs = Bug.objects.all().order_by('-created_at')
        bug_list = []
        for bug in bugs:
            bug_list.append({
                "id": bug.id,
                "title": bug.title,
                "description": bug.description,
                "status": bug.status,
                "created_by": bug.created_by,
                "created_at": bug.created_at.strftime("%Y-%m-%d %H:%M:%S")
            })
        return JsonResponse({"status": True, "data": bug_list})

    elif request.method == "POST":
        try:
            data = json.loads(request.body)

            bug = Bug.objects.create(
                title=data["title"],
                description=data.get("description", ""),
                status=data.get("status", "OPEN"),
                created_by=data["created_by"]
            )

            return JsonResponse({
                "status": True,
                "message": "Bug created",
                "bug_id": bug.id
            }, status=201)

        except Exception as e:
            return JsonResponse({"status": False, "message": str(e)}, status=400)

    return JsonResponse({"status": False, "message": "Method not allowed"}, status=405)

