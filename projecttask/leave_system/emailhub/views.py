from django.core.mail import send_mail
from django.http import HttpResponse

def test_email(request):
    try:
        send_mail(
            'Hello from Django',
            'This is a test email sent from Django app.',
            'your_email@gmail.com',  # from
            ['recipient@example.com'],  # to
            fail_silently=False,
        )
        return HttpResponse("Email sent successfully")
    except Exception as e:
        return HttpResponse(f"Error occurred: {e}")
