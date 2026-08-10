from django.urls import path

from .views import (
    DustbinListView,
    CreateDustbinView,
    ReportDustbinView,
    ReportedDustbinListView
)


urlpatterns = [

    # ==========================================
    # LIST ACTIVE DUSTBINS
    # ==========================================

    path(
        "",
        DustbinListView.as_view(),
        name="dustbin-list"
    ),


    # ==========================================
    # ADMIN CREATE DUSTBIN
    # ==========================================

    path(
        "create/",
        CreateDustbinView.as_view(),
        name="create-dustbin"
    ),


    # ==========================================
    # REPORT DUSTBIN FULL
    # ==========================================

    path(
        "<int:id>/report/",
        ReportDustbinView.as_view(),
        name="report-dustbin"
    ),


    # ==========================================
    # ADMIN REPORTED DUSTBINS
    # ==========================================

    path(
        "reported/",
        ReportedDustbinListView.as_view(),
        name="reported-dustbins"
    ),

]