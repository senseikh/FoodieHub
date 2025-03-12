from django.contrib.auth import get_user_model

from django_rest_passwordreset.signals import reset_password_token_created
from django.dispatch import receiver 
from django.urls import reverse 
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags

User = get_user_model()

class EmailAuthBackend: 
    def authenticate(self, request, email=None, password=None):
        try: 
            user = User.objects.get(email=email)
            if user.check_password(password): 
                return user 
        except User.DoesNotExist:
            return None
        
    def get_user(self, user_id): 
        try: 
            return User.objects.get(pk=user_id)
        except User.DoesNotExist: 
            return None
        

@receiver(reset_password_token_created)
def password_reset_token_created(reset_password_token, *args, **kwargs):
    sitelink = "https://foodhub-156e0.web.app/"
    token = "{}".format(reset_password_token.key)
    full_link = str(sitelink)+str("password-reset/")+str(token)

    print(token)
    print(full_link)

    context = {
        'full_link': full_link,
        'email_adress': reset_password_token.user.email
    }

    html_message = render_to_string("backend/email.html", context=context)
    plain_message = strip_tags(html_message)

    msg = EmailMultiAlternatives(
        subject = "Request for resetting password for {title}".format(title=reset_password_token.user.email), 
        body=plain_message,
        from_email = "hillarykisera@gmail.com", 
        to=[reset_password_token.user.email]
    )

    msg.attach_alternative(html_message, "text/html")
    msg.send()