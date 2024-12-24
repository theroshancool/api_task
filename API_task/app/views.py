from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import App


@csrf_exempt
def add_app(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            required_fields = ["app_name", "version", "description"]
            for field in required_fields:
                if field not in data or not data[field].strip():
                    return JsonResponse({"error": f"Missing or empty field: {field}"}, status=400)

            app = App.objects.create(
                app_name=data["app_name"],
                version=data["version"],
                description=data["description"],
            )
            return JsonResponse({"message": "App created successfully", "id": app.id}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid HTTP method"}, status=405)


def get_app(request, id):
    if request.method == "GET":
        app = get_object_or_404(App, id=id)
        return JsonResponse(app.to_dict(), status=200)
    return JsonResponse({"error": "Invalid HTTP method"}, status=405)


@csrf_exempt
def delete_app(request, id):
    if request.method == "DELETE":
        app = get_object_or_404(App, id=id)
        app.delete()
        return JsonResponse({"message": "App deleted successfully"}, status=200)
    return JsonResponse({"error": "Invalid HTTP method"}, status=405)
