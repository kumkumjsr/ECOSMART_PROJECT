from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from accounts.views import LoginView

from rest_framework_simplejwt.views import TokenRefreshView


def healthz(request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    # Health check
    path("healthz/", healthz, name="healthz"),

    # Admin
    path("admin/", admin.site.urls),

    # Accounts
    path("api/accounts/", include("accounts.urls")),

    # Waste / AI
    path("api/waste/", include("waste.urls")),

    # Dashboard
    path("api/dashboard/", include("dashboard.urls")),

    # JWT
    path("api/token/", LoginView.as_view(), name="token_obtain_pair"),
    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),

    # Dustbins
    path("api/dustbins/", include("dustbins.urls")),

    # Dustbin Reports
    path("api/dustbin-report/", include("dustbin_reports.urls")),

    # Tasks
    path("api/tasks/", include("tasks.urls")),

    # Notifications
    path("api/notifications/", include("notifications.urls")),

    # Employees
    path("api/employees/", include("employees.urls")),

    # Complaints
    path("api/complaints/", include("complaints.urls")),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )