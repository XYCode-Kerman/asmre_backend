from fastapi import FastAPI

from routers.classes import router as classes_router
from routers.credits import router as credit_router
from routers.policy import router as policy_router
from routers.student import router as student_router
from routers.user import router as user_router

app = FastAPI(title='Atomic Student Manager Reborn API',
              version='0.0.1-infdev')

app.include_router(classes_router)
app.include_router(student_router)
app.include_router(credit_router)
app.include_router(user_router)
app.include_router(policy_router)


@app.get("/ping", response_model=str, tags=['杂项'], responses={
    200: {
        'description': '成功 ping',
        'content': {
            'text/plain': {
                'example': 'pong'
            }
        }
    }
})
def ping():
    return 'pong'
