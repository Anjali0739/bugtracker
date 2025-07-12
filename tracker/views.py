from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Bug
import json
from django.contrib.auth.models import User
# Create your views here.

@csrf_exempt
def bug_list_api(request):
    if request.method == "GET":
        user_id = request.GET.get("user_id")
        if user_id:
            bugs = Bug.objects.filter(created_by_id=user_id).order_by('-created_at')
        else:
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
            
            try:
                user = User.objects.get(id=data["user_id"])
            except User.DoesNotExist:
                return JsonResponse({"status": False, "message": "User not found"}, status=404)

            bug = Bug.objects.create(
                title=data["title"],
                description=data.get("description", ""),
                status=data.get("status", "OPEN"),
                created_by=user
            )

            return JsonResponse({
                "status": True,
                "message": "Bug created",
                "bug_id": bug.id
            }, status=201)

        except Exception as e:
            return JsonResponse({"status": False, "message": str(e)}, status=400)

    return JsonResponse({"status": False, "message": "Method not allowed"}, status=405)




@csrf_exempt
def update_bug_status(request, bug_id):
    if request.method=="PATCH":
        try:
            data=json.loads(request.body)
            new_status=data.get("status")

            if new_status not in ["OPEN", "IN_PROGRESS", "RESOLVED"]:
                return JsonResponse({
                    "status": False,
                    "message": "Invalid status value",
                }, status=400
                )
            bug=Bug.objects.get(id=bug_id)
            bug.status=new_status
            bug.save()

            return JsonResponse(
                {
                    "status": True,
                    "message": f"Bug status updated to {new_status}",
                    "bug_id": bug.id
                }
            )
        except Bug.DoesNotExist:
            return JsonResponse(
                {
                    "status": False,
                    "message": "Bug not found"
                }, status=404
            )
        
        except Exception as e:
            return JsonResponse(
                {
                    "status": False,
                    "message": str(e)
                }, status=500
            )
        
    elif request.method == "DELETE":
        try:
            bug = Bug.objects.get(id=bug_id)
            bug.delete()
            return JsonResponse({
                "status": True,
                "message": f"Bug {bug_id} deleted successfully"
            })

        except Bug.DoesNotExist:
            return JsonResponse({"status": False, "message": "Bug not found"}, status=404)
        except Exception as e:
            return JsonResponse({"status": False, "message": str(e)}, status=500)

    return JsonResponse({"status": False, "message": "Method not allowed"}, status=405)


