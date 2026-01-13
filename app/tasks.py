import time
from app.celery_app import celery_app
from datetime import datetime

#  docker compose logs -f worker
# @celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=5, retry_kwargs={"max_retries": 3})
# def send_email(self, email: str):
#     print(f"📨 {datetime.now()} Wysyłam maila do {email}")
#     time.sleep(30)
#     print(f"✅ {datetime.now()} Mail wysłany")
#     return {"status": "ok", "email": email}

@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 3},
)
def send_email(self, email: str):
    # ETAP 1
    self.update_state(
        state="PROGRESS",
        meta={
            "step": "Rozpoczęcie wysyłki",
            "email": email,
            "progress": 0,
        },
    )

    print(f"📨 {datetime.now()} Wysyłam maila do {email}")

    # ETAP 2
    self.update_state(
        state="PROGRESS",
        meta={
            "step": "Łączenie z serwerem SMTP",
            "progress": 30,
        },
    )
    time.sleep(10)

    # ETAP 3
    self.update_state(
        state="PROGRESS",
        meta={
            "step": "Wysyłanie treści wiadomości",
            "progress": 70,
        },
    )
    time.sleep(20)

    print(f"✅ {datetime.now()} Mail wysłany")

    return {
        "status": "ok",
        "email": email,
        "progress": 100,
    }