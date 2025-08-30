# from celery import shared_task
# from .utils import TaskWithOnCommit, EmailSender

# @shared_task
# def send_email_ticket(endpoint, email, customer, ticket, device_proper):  # Changed property → device_proper
#     email_sender_obj = EmailSender('Firststore Repairs Ticket')

#     try:
#         email_sender_obj.send_ticket_to_customer_email(
#             endpoint=endpoint,
#             email=email,
#             customer=customer,
#             ticket=ticket,
#             device_proper=device_proper  # Updated key
#         )
#         return f"Sending email to {email}"
#     except Exception as exc:
#         return f"Failed to send email to {email}. Exception occurred: {exc}"

# send_email_ticket = TaskWithOnCommit(send_email_ticket)




from celery import shared_task
from .utils import EmailSender,TaskWithOnCommit

@shared_task
def send_email_ticket(endpoint, email, customer, ticket, device_proper,payment_details,invoices,descriptions):
    email_sender_obj = EmailSender("Computer Hub United Kingdom Repairs Ticket")
    try:
        email_sender_obj.send_ticket_to_customer_email(
            endpoint=endpoint, email=email, customer=customer, ticket=ticket, device_proper=device_proper,payment_details=payment_details,invoices=invoices,descriptions=descriptions
        )
        return f"Email successfully sent to {email}"
    except Exception as e:
        return f"Failed to send email to {email}. Error: {e}"
send_email_ticket = TaskWithOnCommit(send_email_ticket)