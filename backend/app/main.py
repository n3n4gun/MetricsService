from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import ValidationError
from loguru import logger

from models import PageViewMetric, ClickViewMetric, BaseMetrics

metrics_service_app = FastAPI()
templates = Jinja2Templates(directory = '/app/frontend/templates')
metrics_service_app.mount(
    '/static',
    StaticFiles(directory = '/app/frontend/static'),
    name = 'static'
)

metrics_service_app.middleware(
    CORSMiddleware(
        app = metrics_service_app,
        allow_origins = ['http://localhost:8080'],
        allow_methods = ['POST'],
        allow_headers = ['*']
    )
)

@metrics_service_app.get('/')
async def index_page(request: Request):
    return templates.TemplateResponse(
        request = request,
        name = 'index.html',
        context = {'request' : request}
    )

@metrics_service_app.post('/api/collect')
async def user_event(user_event : dict):
    try:
        event = BaseMetrics(**user_event)

    except ValidationError as base_validation_error:
        raise HTTPException(
            status_code = 400,
            detail = f'Base validation ERROR: {base_validation_error.errors()}'
        )
    
    else:
        try:
            if event.event_type == 'page_view':
                validated_data = PageViewMetric(**user_event)
            elif event.event_type == 'click':
                validated_data = ClickViewMetric(**user_event)
            else:
                raise HTTPException(
                    status_code = 400,
                    detail = f'Unkown event type: {event.event_type}'
                )

        except ValidationError as validation_error:
            raise HTTPException(
                status_code = 400,
                detail = f'Validation ERROR for {event.event_type}: {validation_error.errors()}'
            )
        
        else:
            logger.info(f'Successfull validation: {validated_data}')
            return {
                'status' : 'ok',
                'event_type' : event.event_type
            }

@metrics_service_app.get('/health')
async def health_check():
    return {
        'status' : 'ok'
    }