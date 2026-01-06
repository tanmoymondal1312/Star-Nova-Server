from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from utils.translator import translate_text

@csrf_exempt  # Only needed if testing without CSRF token
def api_translate(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            text = data.get("text")
            source = data.get("source")
            target = data.get("target")
            
            # Check if any required field is missing
            if not text or not source or not target:
                return JsonResponse(
                    {"error": "Please provide 'text', 'source', and 'target'."},
                    status=400
                )
            
            translated = translate_text(text, source, target)
            return JsonResponse({"translated": translated})
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "POST request required"}, status=405)





