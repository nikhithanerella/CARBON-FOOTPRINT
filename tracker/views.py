from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import SignUpForm, FootprintForm
from .models import FootprintEntry, UserProfile
from .utils import predict_footprint, get_suggestions
from django.contrib.auth import logout


def custom_logout(request):
    logout(request)   # clears the session
    return redirect('login')  # send user back to login page

# -----------------------------
# Leaderboard view
# -----------------------------
def leaderboard(request):
    top_users = UserProfile.objects.order_by('-total_footprint')[:10]
    return render(request, 'tracker/leaderboard.html', {'top_users': top_users})

# -----------------------------
# Add footprint entry
# -----------------------------
@login_required
def add_entry(request):
    if request.method == 'POST':
        form = FootprintForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            # calculate footprint
            entry.prediction = predict_footprint(entry)
            entry.save()

            # update or create user profile
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            profile.total_footprint += entry.prediction
            profile.save()

            return redirect('dashboard')
    else:
        form = FootprintForm()
    return render(request, 'tracker/predict_form.html', {'form': form})

# -----------------------------
# Register new user
# -----------------------------
from .models import UserProfile

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create UserProfile automatically
            UserProfile.objects.create(user=user, total_footprint=0)
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'tracker/register.html', {'form': form})


# -----------------------------
# Dashboard view
# -----------------------------
@login_required
def dashboard(request):
    entries = FootprintEntry.objects.filter(user=request.user).order_by('created_at')
    dates = [e.created_at.strftime("%Y-%m-%d") for e in entries]
    predictions = [e.prediction for e in entries]
    latest = entries.last()
    pie_data = {
        'transport': latest.transport_km if latest else 0,
        'electricity': latest.electricity_kwh if latest else 0,
        'food': (latest.food_meat + latest.food_dairy + latest.food_plant) if latest else 0,
        'waste': latest.waste_kg if latest else 0
    }
    suggestions = get_suggestions(latest, latest.prediction) if latest else []
    return render(request, 'tracker/dashboard.html', {
        'entries': entries,
        'dates': dates,
        'predictions': predictions,
        'pie_data': pie_data,
        'suggestions': suggestions
    })

# -----------------------------
# Predict view (alternative to add_entry)
# -----------------------------
@login_required
def predict(request):
    if request.method == 'POST':
        form = FootprintForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.prediction = predict_footprint(entry)
            entry.save()

            # Update UserProfile total
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            profile.total_footprint += entry.prediction
            profile.save()

            return redirect('dashboard')
    else:
        form = FootprintForm()
    return render(request, 'tracker/predict_form.html', {'form': form})

    