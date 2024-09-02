from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone
from .models import UserLogin

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    
    UserLogin.objects.get_or_create(user=user, login_date=timezone.now().date())