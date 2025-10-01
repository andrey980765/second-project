from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from .forms import SettingsForm, EventForm
from .models import Event, Notification

# ---- helper: get settings from cookies
def get_user_settings_from_cookies(request):
    theme = request.COOKIES.get('theme', 'light')
    language = request.COOKIES.get('language', 'ru')
    notifications = request.COOKIES.get('notifications', 'true')
    recent = request.COOKIES.get('recent_pages', '')
    recent_list = [int(x) for x in recent.split(',') if x.isdigit()]
    return {'theme': theme, 'language': language, 'notifications': (notifications == 'true'), 'recent_pages': recent_list}

# ---- helper: generate reminder notifications for upcoming events
def generate_reminder_notifications(window_minutes=60):
    now = timezone.now()
    window_end = now + timezone.timedelta(minutes=window_minutes)
    events_due = Event.objects.filter(date_time__gte=now, date_time__lte=window_end)
    created = []
    for ev in events_due:
        exists = Notification.objects.filter(event=ev, notif_type='reminder').exists()
        if not exists:
            msg = f"Напоминание: {ev.title} в {ev.date_time.strftime('%Y-%m-%d %H:%M')}"
            n = Notification.objects.create(event=ev, notif_type='reminder', message=msg)
            created.append(n)
    return created

# ---- index: список событий, генерируем reminders и показываем уведомления
def index(request):
    settings = get_user_settings_from_cookies(request)
    if settings['notifications']:
        generate_reminder_notifications(window_minutes=1)

    events = Event.objects.order_by('date_time')
    response = render(request, 'planner/index.html', {'events': events, 'settings': settings})
    recent = request.COOKIES.get('recent_pages', '')
    rec_list = [x for x in recent.split(',') if x]
    rec_list = (rec_list + ['0'])[-5:]
    response.set_cookie('recent_pages', ','.join(rec_list), max_age=30*24*3600)
    return response

# ---- event detail
def event_detail(request, pk):
    settings = get_user_settings_from_cookies(request)
    event = get_object_or_404(Event, pk=pk)
    response = render(request, 'planner/event_detail.html', {'event': event, 'settings': settings})
    recent = request.COOKIES.get('recent_pages', '')
    rec_list = [x for x in recent.split(',') if x]
    rec_list = (rec_list + [str(pk)])[-5:]
    response.set_cookie('recent_pages', ','.join(rec_list), max_age=30*24*3600)
    return response

# ---- create event
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            ev = form.save()
            Notification.objects.create(event=ev, notif_type='created', message=f"Создано событие: {ev.title}")
            return redirect('planner:event_detail', pk=ev.pk)
    else:
        form = EventForm()
    return render(request, 'planner/event_form.html', {'form': form, 'action': 'Создать событие'})

# ---- edit event
def event_edit(request, pk):
    ev = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=ev)
        if form.is_valid():
            ev = form.save()
            Notification.objects.create(event=ev, notif_type='created', message=f"Событие обновлено: {ev.title}")
            return redirect('planner:event_detail', pk=ev.pk)
    else:
        form = EventForm(instance=ev)
    return render(request, 'planner/event_form.html', {'form': form, 'action': 'Редактировать событие'})

# ---- delete event
def event_delete(request, pk):
    ev = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        ev_title = ev.title
        ev.delete()
        Notification.objects.create(event=None, notif_type='created', message=f"Событие удалено: {ev_title}")
        return redirect('planner:index')
    return render(request, 'planner/event_confirm_delete.html', {'event': ev})
# ---- settings
def settings_view(request):
    if request.method == "POST":
        form = SettingsForm(request.POST)
        if form.is_valid():
            response = redirect('planner:index')
            response.set_cookie('theme', form.cleaned_data['theme'], max_age=30*24*3600)
            response.set_cookie('language', form.cleaned_data['language'], max_age=30*24*3600)
            response.set_cookie('notifications', 'true' if form.cleaned_data.get('notifications') else 'false', max_age=30*24*3600)
            return response
    else:
        initial = {
            'theme': request.COOKIES.get('theme', 'light'),
            'language': request.COOKIES.get('language', 'ru'),
            'notifications': request.COOKIES.get('notifications', 'true') == 'true'
        }
        form = SettingsForm(initial=initial)
    return render(request, 'planner/settings.html', {'form': form})

# ---- notification endpoints
def notifications_list(request):
    notifs = Notification.objects.filter(seen=False).order_by('-created_at')[:20]
    data = [{'id': n.id, 'message': n.message, 'created_at': n.created_at.strftime('%Y-%m-%d %H:%M')} for n in notifs]
    return JsonResponse({'count': notifs.count(), 'items': data})

def notifications_poll(request):
    return notifications_list(request)

def notifications_mark_seen(request):
    if request.method == 'POST':
        ids = request.POST.getlist('ids[]')
        Notification.objects.filter(id__in=ids).update(seen=True)
        return JsonResponse({'ok': True})
    return JsonResponse({'ok': False}, status=400)

def notifications_delete_all(request):
    """Удалить все уведомления"""
    Notification.objects.all().delete()
    return JsonResponse({'ok': True})

def mark_all_read(request):
    if request.method == "POST":
        Notification.objects.filter(read=False).update(read=True)
        return JsonResponse({"status": "ok", "unread_count": 0})
    return JsonResponse({"status": "error"})


