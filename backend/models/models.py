from pydantic import BaseModel

from datetime import datetime

class BaseMetrics(BaseModel):
    event_type: str
    timestamp: datetime

class PageViewMetric(BaseMetrics):
    event_type: str = 'page_view'
    url: str
    path: str
    title: str
    referrer: str
    screen_width: float
    screen_height: float
    user_agent: str

class ClickViewMetric(BaseMetrics):
    event_type: str = 'click'
    target: str
    target_text: str
    target_id: str
    target_class: str
    url: str