from admin_honeypot.signals import honeypot
from django.dispatch import receiver

from behind import jarvis


@receiver(honeypot)
def honeypot_login_attempt_callback(instance, request, **kwargs):
    jarvis.send_slack(
        f'''Someone tried to login to fake admin: 
        Username: {instance}
        IP: {instance.ip_address}
        Session key: {instance.session_key}
        User-agent: {instance.user_agent}
        Path: {instance.path}
        ''',
        channel='#monitoring'
    )
