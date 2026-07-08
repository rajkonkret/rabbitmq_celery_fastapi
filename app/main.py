from fastapi import FastAPI
from app.tasks import send_email
from app.celery_app import celery_app

app = FastAPI()

@app.post("/send-email")
def send_email_endpoint(email: str):
    task = send_email.delay(email)
    return {
        "message": "Zadanie przyjęte",
        "task_id": task.id
    }


@app.get("/tasks/{task_id}")
def get_task_status(task_id: str):
    async_result = celery_app.AsyncResult(task_id)
    response = {
        "task_id": task_id,
        "state": async_result.state,
        "info": async_result.info,
    }

    # include result only when ready/success
    if async_result.ready():
        try:
            response["result"] = async_result.result
        except Exception as e:
            response["result_error"] = str(e)

    return response

print("BROKER:", celery_app.conf.broker_url)
print("BACKEND:", celery_app.conf.result_backend)