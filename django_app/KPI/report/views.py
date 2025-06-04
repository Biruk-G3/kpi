import datetime
import openpyxl
from django.shortcuts import render, redirect
from .forms import KpiDetailsForm, UserRegistrationForm, KpiForm
from django.http import HttpResponse
from .models import Kpi
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto login after registration
            return redirect('home')  # Redirect to home/dashboard
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})


def home(request):
	return render(request,("home.html"),{})


def create_kpi(request):
    kpis = Kpi.objects.prefetch_related('details').order_by('-id')
    today = datetime.date.today()
    is_monday = today.weekday() == 2  # 0 means Monday

    if request.method == 'POST' and is_monday:
        form = KpiForm(request.POST)
        if form.is_valid():
            kpi = form.save(commit=False)
            kpi.created_by = request.user  # assumes your model has this field
            kpi.save()
            return render(request, 'kpi_summary.html', {'kpis': kpis})
    else:
        form = KpiForm()

    context = {
        'is_monday': is_monday,
        'form': form
    }
    return render(request, 'create_kpi.html', context)

def add_progress(request):
    if request.method == 'POST':
        form = KpiDetailsForm(request.POST, user=request.user)
        if form.is_valid():
            detail = form.save(commit=False)
            detail.created_by = request.user
            detail.save()
            return redirect('kpi_summary')  # or wherever you want
    else:
        form = KpiDetailsForm(user=request.user)
    return render(request, 'add_progress.html', {'form': form})
def kpi_summary(request):
    kpis = Kpi.objects.all().order_by('-id')

    labels = []
    plans = []
    actuals = []

    for kpi in kpis:
        labels.append(f"{kpi.kpi} (W{kpi.weeks})")
        plans.append(kpi.plan)
        detail = kpi.details.last()
        actuals.append(detail.progress if detail and detail.progress else 0)

    return render(request, 'kpi_summary.html', {
        'kpis': kpis,
        'labels': labels,
        'plans': plans,
        'actuals': actuals
    })

def export_kpi_summary(request):
    # Create a workbook and worksheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "KPI Summary"

    # Add headers
    ws.append([
        "Week", "Activity", "KPI", "Baseline", "Plan", 
        "Progress", "Achievement", "Created At"
    ])

    # Populate with data
    kpis = Kpi.objects.all().order_by('-weeks')
    for kpi in kpis:
        detail = kpi.details.first()
        ws.append([
            kpi.weeks,
            kpi.activity,
            kpi.kpi,
            kpi.baseline,
            kpi.plan,
            detail.progress if detail else "N/A",
            f"{detail.achievement:.2f}%" if detail else "N/A",
            detail.created_at.strftime('%Y-%m-%d %H:%M') if detail else "N/A",
        ])

    # Prepare HTTP response with Excel content
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename=kpi_summary.xlsx'
    wb.save(response)
    return response
