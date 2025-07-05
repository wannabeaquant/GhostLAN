"""
Export API for GhostLAN SimWorld
Endpoints for exporting analytics data as JSON or CSV
"""

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse, Response
from analytics.advanced_analytics import AdvancedAnalytics

export_router = APIRouter()

analytics = AdvancedAnalytics()

@export_router.get("/export")
def export_data(format: str = Query('json', enum=['json', 'csv'])):
    data = analytics.export_data(format=format)
    if format == 'json':
        return JSONResponse(content=data)
    elif format == 'csv':
        return Response(content=data, media_type='text/csv') 