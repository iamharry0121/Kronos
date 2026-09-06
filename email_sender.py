import os
import resend

resend.api_key = os.getenv('RESEND_API_KEY')

FROM_ADDRESS = 'onboarding@resend.dev'

def send_reminder_email(to_email, task_text, due_date):
    formatted_due_date = due_date.strftime('%b %d, %Y at %I:%M %p')
    subject = f'Reminder: "{task_text}" is due soon'

    html_body = (
        '<div style="background-color:#0B0B0B;color:#F5F5F5;padding:32px;'
        'font-family:sans-serif;">'
        '<h2 style="color:#D4AF37;">Task Reminder</h2>'
        f'<p style="font-size:1.1rem;"><strong>{task_text}</strong></p>'
        f'<p style="color:#cfcfcf;">Due: {formatted_due_date}</p>'
        '</div>'
    )

    text_body = f'Reminder: "{task_text}" is due {formatted_due_date}'
 
    params = {
        "from": FROM_ADDRESS,
        "to": [to_email],
        "subject": subject,
        "html": html_body,
        "text": text_body,
    }

    try:
        response = resend.Emails.send(params)
        return True, response
    except Exception as error:
        print(f'failed to send reminder email to {to_email}: {error}')
        return False, str(error)



