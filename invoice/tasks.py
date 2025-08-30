from celery import shared_task
from .utils import EmailSender,TaskWithOnCommit
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_email_invoice(endpoint, email, invoices):
    email_sender_obj = EmailSender("Computer Hub United Kingdom Sales Invoice ")
    try:
        success = email_sender_obj.send_ticket_to_customer_email(
            endpoint=endpoint, 
            email=email,
            invoices=invoices
        )
        if not success:
            raise Exception("Failed to send email")

        return f"Email successfully sent to {email}"
    except Exception as e:

         error_message = f"Failed to send email to {email}. Error: {e}"
    print(f"ERROR: {error_message}")
         # Optionally, you can log the error or handle it as needed  
    raise Exception(error_message)

@shared_task(bind=True)
def send_email_invoice_task(self, endpoint, email, invoices):
    """
    This is the actual Celery task that will be executed.
    """
    # Call the core logic
    return _send_email_invoice_logic(endpoint, email, invoices)

# This code defines a Celery task to send an email with invoice details.
# invoice/tasks.py
#import logging
#from celery import shared_task
#from django.core.mail import send_mail
#from django.template.loader import render_to_string
#from django.conf import settings

#logger = logging.getLogger(__name__)

#@shared_task
#def send_email_invoice(invoice_id, recipient_email):
 #   try:
        # Get invoice object (assuming you fetch it by ID)
        # from .models import Invoice # Or wherever your Invoice model is
        # invoice = Invoice.objects.get(id=invoice_id)

        # Example: Render an email template
        # subject = f"Invoice #{invoice.invoice_number}"
        # message = render_to_string('emails/invoice.html', {'invoice': invoice})

        # For testing, just a simple message
  #      subject = f"Invoice #00001 (Test)"
   #     message = f"Dear customer, here is your invoice #00001."

    #    send_mail(
     #       subject,
      #      message,
       #     settings.DEFAULT_FROM_EMAIL,
        #    [recipient_email],
         #   fail_silently=False,
        #)
        #logger.info(f"Successfully sent invoice {invoice_id} to {recipient_email}")
        #return True
    #except Exception as e:
     #   logger.error(f"Failed to send invoice {invoice_id} to {recipient_email}: {e}", exc_info=True)
        # Re-raise the exception if you want Celery to mark the task as failed
      #  raise