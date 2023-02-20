from django.conf import settings
def constant_text(request):
    return {
        'GOOGLE_API': settings.GOOGLE_APIKEY,
    }