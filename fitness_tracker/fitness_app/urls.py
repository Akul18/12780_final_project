from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("exercise/add/", views.add_exercise, name="add_exercise"),
    path("log/", views.log_session, name="log_session"),
    path("chart-data/", views.chart_data, name="chart_data"),
    path("export.xlsx", views.export_xlsx, name="export_xlsx"),
]