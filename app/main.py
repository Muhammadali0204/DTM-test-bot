from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from fastadmin import fastapi_app as admin_app

from tortoise.contrib.fastapi import register_tortoise

from app.data.config import settings, DATABASE_CONFIG
from app.utils.others import send_answer_page
from app.utils.main_functions import handle_webhook, on_shutdown, on_startup



app = FastAPI(docs_url=None, redoc_url=None)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/admin", admin_app)


templates = Jinja2Templates(directory='app/templates')

register_tortoise(
    app,
    config=DATABASE_CONFIG,
    generate_schemas=True,
    add_exception_handlers=True,
)


app.add_event_handler("startup", on_startup)
app.add_event_handler("shutdown", on_shutdown)

@app.get('/answer')
async def get_answer(test_id: int, request: Request):
    return await send_answer_page(templates, test_id, request)
    

@app.post(settings.WEBHOOK_PATH)
async def webhook_endpoint(request: Request):
    return await handle_webhook(request)
