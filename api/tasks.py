from celery import shared_task
from django.utils.timezone import now
from django.core.mail import send_mail
from .models import Borrow
from django.contrib.auth import get_user_model

User = get_user_model()
# @shared_task
# def send_due_date_notifications():
#     today = now().date()
#     borrows_due_today = Borrow.objects.filter(due_date=today, return_date__isnull=True)

#     for borrow in borrows_due_today:
#         user = borrow.user
#         book = borrow.book
#         send_mail(
#             subject="📚 Book Due Reminder",
#             message=f"Dear {user.username}, your borrowed book '{book.title}' is due today.",
#             from_email=None,
#             recipient_list=[user.email],
#         )

@shared_task
def send_due_date_notifications():
    """
    Test task: sends a verification email to every active user.
    """
    # Fetch all active users
    users = User.objects.filter(is_active=True)
    
    for user in users:
        send_mail(
            subject="✅ Test Email from Library System",
            message=(
                f"Hello {user.username},\n\n"
                "This is a test email sent via Celery to verify that "
                "email delivery is working correctly.\n\n"
                "Cheers,\n"
                "Your Library Team"
            ),
            from_email=None,            # uses DEFAULT_FROM_EMAIL
            recipient_list=[user.email],
            fail_silently=False,
        )