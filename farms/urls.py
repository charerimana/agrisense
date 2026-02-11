from django.urls import path, include
from django.contrib.auth.views import LogoutView, LoginView

from rest_framework.routers import DefaultRouter

from .views import (
    FarmViewSet,
    SensorViewSet,
    SensorReadingViewSet,
    NotificationPreferenceViewSet,
    NotificationViewSet,
    DashboardDataView,
    dashboard_view,
    CustomLoginView,
    farm_list_view,
    farm_upsert,
    farm_delete,
    manage_preferences
)

router = DefaultRouter()

router.register(r'farms', FarmViewSet, basename='farm')
router.register(r'sensors', SensorViewSet, basename='sensor')
router.register(r'readings', SensorReadingViewSet, basename='reading')
router.register(r'notification-preferences', NotificationPreferenceViewSet, basename='notification-preference')
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/dashboard-data/', DashboardDataView.as_view(), name='dashboard-data'),
    path('dashboard/', dashboard_view, name='dashboard'),

    path('farms/', farm_list_view, name='farm-manage'),
    path('farms/add/', farm_upsert, name='farm_add'),
    path('farms/edit/<int:pk>/', farm_upsert, name='farm_edit'),
    path('farms/delete/<int:pk>/', farm_delete, name='farm_delete'),

    path('notifications/preferences/', manage_preferences, name='preferences'),

    path('login/', CustomLoginView.as_view(), name='login'),
    # path('login/', LoginView.as_view(template_name='farms/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
