from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

metrics_service_app = FastAPI()
templates = Jinja2Templates(directory = '/app/frontend/templates')
metrics_service_app.mount(
    '/static',
    StaticFiles(directory = '/app/frontend/static'),
    name = 'static'
)

@metrics_service_app.get('/')
async def index_page(request: Request):
    return templates.TemplateResponse(
        request = request,
        name = 'index.html',
        context = {'request' : request}
    )

@metrics_service_app.get('/health')
async def health_check():
    return {
        'status' : 'ok'
    }