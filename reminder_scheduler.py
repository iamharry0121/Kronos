from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import database_manager as db_mgr
import email_sender


def check_and_send_reminders(app):
    """
    This function runs automatically every few minutes (see start_scheduler
    below). It looks for any task across all users that's due for a
    reminder right now, sends the email, and marks it as sent. It needs `app` 
    (the Flask app) so it can use app_context(); database queries only work 
    inside that context, and this function runs outside of a normal web request, 
    so i has to set that context up manually.
    """
    with app.app_context():
        now = datetime.utcnow()
        tasks_due = db_mgr.get_tasks_needing_reminders(now)

        for task in tasks_due:
            # task.user is available because SQLAlchemy automatically lets
            # it access the related User object through the foreign key,
            # even though i never explicitly wrote a "user" property.
            owner = db_mgr.get_user_by_id(task.user_id)
            if owner is None:
                continue

            success, _ = email_sender.send_reminder_email(
                to_email=owner.email,
                task_text=task.task,
                due_date=task.due_date
            )

            # only mark as sent if the email actually went through. If it
            # failed (e.g. Resend was briefly down), we leave reminder_sent
            # as False so the next check (a few minutes later) retries it
            if success:
                db_mgr.mark_reminder_sent(task.id)


def start_scheduler(app):
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=lambda: check_and_send_reminders(app),
        trigger='interval',
        minutes=2,
        id='reminder_check_job',
        replace_existing=True
    )
    scheduler.start()
    return scheduler