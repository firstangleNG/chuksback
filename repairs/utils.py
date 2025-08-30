import threading
import socket
from smtplib import SMTPException
from django.core.mail import EmailMultiAlternatives, BadHeaderError
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

class EmailSender:
    def __init__(self, subject, from_email=settings.EMAIL_HOST_USER):
        self.subject = subject
        self.from_email = from_email

    def send_email_async(self, html_content, text_content, to):
        try:
            email = EmailMultiAlternatives(self.subject, text_content, self.from_email, [to])
            email.attach_alternative(html_content, "text/html")
            email.send()
            print(f"Email successfully sent to {to}")
        except (BadHeaderError, SMTPException, socket.gaierror, TimeoutError, ConnectionError) as e:
            print(f"Email sending failed: {e}")

    def send_ticket_to_customer_email(self, endpoint, email, customer, ticket,device_proper,payment_details,invoices,descriptions):
        """
        Sends an email with ticket details.
        """
        try:
            html_content = render_to_string('email_tickets.html', {
                'endpoint': endpoint,
                'email': email,
                'customer': customer,
                'ticket': ticket,
                'device_proper': device_proper,
                'payment_details':payment_details,
                'invoices':invoices,
                "descriptions":descriptions
            })
            text_content = strip_tags(html_content)

            # Start email in a separate thread (if not using Celery)
            email_thread = threading.Thread(target=self.send_email_async, args=(html_content, text_content, email))
            email_thread.start()

        except Exception as e:
            print(f"Failed to send email to {email}. Error: {e}")


from django.db import transaction

class TaskWithOnCommit:
    def __init__(self, task):
        """
        Initializes the wrapper class with a Celery task.
        :param task: A Celery task function.
        """
        self.task = task

    def delay_on_commit(self, *args, **kwargs):
        """
        Schedules the task to run after the transaction is committed.
        :param args: Arguments to be passed to the task.
        :param kwargs: Keyword arguments to be passed to the task.
        """
        # Use Django's transaction.on_commit to delay the task execution
        transaction.on_commit(lambda: self.task.delay(*args, **kwargs))