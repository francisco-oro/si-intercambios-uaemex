import logging

import os
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string

logger = logging.getLogger(__name__)


class EmailService:
    @staticmethod
    def send_activation_email(user):
        logger.info(f"Preparing activation email for user: {user.email}")
        try:
            activation_code = get_random_string(32)
            logger.debug(f"Generated activation code for user {user.email}")

            # Store the activation code in user model or separate table
            user.activation_code = activation_code
            user.save()
            logger.debug(f"Saved activation code for user {user.email}")

            subject = 'Activate your account'
            context = {
                'user': user,
                'activation_code': activation_code,
                'frontend_url': os.getenv('FRONTEND_URL')
            }

            try:
                message = render_to_string('emails/activation.html', context)
                logger.debug(f"Email template rendered successfully for user {user.email}")
            except Exception as e:
                logger.error(f"Template rendering failed: {str(e)}")
                raise

            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=os.getenv('DEFAULT_FROM_EMAIL'),
                    recipient_list=[user.email],
                    html_message=message
                )
                logger.info(f"Activation email sent successfully to {user.email}")
            except Exception as e:
                logger.error(f"Failed to send activation email to {user.email}: {str(e)}")
                raise

        except Exception as e:
            logger.error(f"Error in send_activation_email for user {user.email}: {str(e)}")
            raise
