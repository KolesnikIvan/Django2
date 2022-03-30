from urllib.parse import urljoin
from django.core.mail import send_mail
# from geekshop import settings
from django.conf import settings
from django.urls import reverse

def send_verify_mail(user):
    # verify_link = f'/user.verify/{user.email}/user.activation_key'
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key,])  
    subject = "Confirm your acccount"
    lnk = urljoin(settings.DOMAIN_NAME, verify_link)
    message = f"""
        To confirm your account {user.username} 
        at {settings.DOMAIN_NAME} 
        follow link 
        {lnk}.
    """
    send_mail(subject, message, 'noreply@localhost', [user.email,])
