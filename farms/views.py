from django.shortcuts import render, get_object_or_404
from django.utils.timezone import localtime
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.db import transaction
from django.db.models import Q

from django.db.models import Prefetch
from collections import defaultdict

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Farm,
    Sensor,
    SensorReading,
    Notification,
    NotificationPreference
)
from .serializers import (
    FarmSerializer,
    SensorSerializer,
    SensorReadingSerializer,
    NotificationPreferenceSerializer,
    NotificationSerializer
)
from .utils import send_alert
from .permissions import IsOwnerOrSuperUser
from .forms import FarmSensorForm, NotificationPreferenceForm

class FarmViewSet(ModelViewSet):
    serializer_class = FarmSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrSuperUser]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Farm.objects.all()
        return Farm.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SensorViewSet(ModelViewSet):
    serializer_class = SensorSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrSuperUser]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Sensor.objects.all()
        return Sensor.objects.filter(farm__owner=self.request.user)


class SensorReadingViewSet(ModelViewSet):
    serializer_class = SensorReadingSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrSuperUser]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return SensorReading.objects.all()
        return SensorReading.objects.filter(
            sensor__farm__owner=self.request.user
        )

    def perform_create(self, serializer):
        reading = serializer.save()

        sensor = reading.sensor
        reading.is_valid = sensor.min_temp <= reading.temperature <= sensor.max_temp
        reading.save()

        if not reading.is_valid:
            send_alert(sensor.farm.owner, reading)


class NotificationPreferenceViewSet(ModelViewSet):
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return NotificationPreference.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class NotificationViewSet(ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrSuperUser]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Notification.objects.all()
        return Notification.objects.filter(user=self.request.user)


class DashboardDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        farm_id = request.query_params.get('farm_id')
        
        # Base Query
        sensor_qs = Sensor.objects.filter(farm__owner=user).select_related('farm')
        if farm_id:
            sensor_qs = sensor_qs.filter(farm_id=farm_id)
            
        sensors = sensor_qs.prefetch_related(
            Prefetch('readings', queryset=SensorReading.objects.order_by('recorded_at'))
        )

        # --- 1. Line Chart Data (Existing) ---
        all_labels = set()
        line_datasets = []
        colors = ['#0d6efd', '#198754', '#dc3545', '#ffc107']

        # --- 2. Pie Chart Data (New) ---
        volume_labels = []
        volume_counts = []
        health_stats = []

        for i, sensor in enumerate(sensors):
            readings = sensor.readings.all()
            count = readings.count()
            
            # Line data
            farm_points = []
            out_of_range = 0
            for r in readings:
                ts = localtime(r.recorded_at).strftime("%Y-%m-%d %H:%M")
                all_labels.add(ts)
                farm_points.append({'x': ts, 'y': r.temperature})
                # Check range for Pie Stats
                if r.temperature < sensor.min_temp or r.temperature > sensor.max_temp:
                    out_of_range += 1

            line_datasets.append({
                "label": sensor.farm.name,
                "data": farm_points,
                "borderColor": colors[i % len(colors)],
                "tension": 0.3
            })

            # Pie: Volume
            volume_labels.append(sensor.farm.name)
            volume_counts.append(count)

            # Pie: Health
            health_stats.append({
                "name": sensor.farm.name,
                "in": count - out_of_range,
                "out": out_of_range
            })

        return Response({
            "line_data": {
                "labels": sorted(list(all_labels)),
                "datasets": line_datasets
            },
            "volume_data": {
                "labels": volume_labels,
                "counts": volume_counts
            },
            "health_stats": health_stats
        })



class CustomLoginView(LoginView):
    template_name = 'farms/login.html'

    def get_success_url(self):
        return reverse_lazy('dashboard')

# Render Dashboard Page
@login_required
def dashboard_view(request):
    # Only show farms owned by the logged-in user
    farms = Farm.objects.filter(owner=request.user) 
    
    context = {
        'farms': farms,
    }
    return render(request, 'farms/dashboard.html', context)

@login_required
def farm_list_view(request):
    query = request.GET.get('q', '')
    farms = Farm.objects.filter(owner=request.user).select_related('sensor').order_by('-id')

    if query:
        # Search by farm name OR location name
        farms = farms.filter(
            Q(name__icontains=query) | 
            Q(location__icontains=query)
        )

    context = {
        'farms': farms,
        'query': query
    }
    return render(request, 'farms/farm_manage.html', context)

def farm_upsert(request, pk=None):
    if pk:
        farm = get_object_or_404(Farm, pk=pk, owner=request.user)
    else:
        farm = Farm(owner=request.user)

    if request.method == 'POST':
        form = FarmSensorForm(request.POST, instance=farm)
        if form.is_valid():
            with transaction.atomic(): # Ensure both save or neither saves
                farm = form.save()
                # Update or Create the OneToOne Sensor
                Sensor.objects.update_or_create(
                    farm=farm,
                    defaults={
                        'min_temp': form.cleaned_data['min_temp'],
                        'max_temp': form.cleaned_data['max_temp'],
                        'sensor_type': 'TEMP'
                    }
                )
            return JsonResponse({'success': True})
        else:
            html = render_to_string('farms/partials/farm_form.html', {'form': form}, request=request)
            return JsonResponse({'success': False, 'html': html})
    
    form = FarmSensorForm(instance=farm)
    return render(request, 'farms/partials/farm_form.html', {'form': form})

def farm_delete(request, pk):
    if request.method == 'POST':
        farm = get_object_or_404(Farm, pk=pk, owner=request.user)
        farm.delete()
        return JsonResponse({'success': True})

@login_required
def manage_preferences(request):
    # Get or create preferences for the current user
    prefs, created = NotificationPreference.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = NotificationPreferenceForm(request.POST, instance=prefs)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            html = render_to_string('farms/partials/pref_form.html', {'form': form}, request=request)
            return JsonResponse({'success': False, 'html': html})
            
    form = NotificationPreferenceForm(instance=prefs)
    return render(request, 'farms/partials/pref_form.html', {'form': form})
