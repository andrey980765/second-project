from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import SettingsForm
from . import data

# вспомогательная функция:
# вытаскивает текущие настройки пользователя из cookies (тема, язык, уведомления, последние страницы)
def get_user_settings_from_cookies(request):
    theme = request.COOKIES.get('theme', 'light')
    language = request.COOKIES.get('language', 'ru')
    notifications = request.COOKIES.get('notifications', 'true')  # строка 'true'/'false'
    recent = request.COOKIES.get('recent_pages', '')  # список id через запятую
    recent_list = [int(x) for x in recent.split(',') if x.isdigit()]
    return {
        'theme': theme,
        'language': language,
        'notifications': (notifications == 'true'),
        'recent_pages': recent_list
    }

# главная страница: показывает список событий и сохраняет факт её посещения в cookies
def index(request):
    settings = get_user_settings_from_cookies(request)
    events = data.EVENTS  
    response = render(request, 'planner/index.html', {'events': events, 'settings': settings})

    # обновляем cookie с последними посещёнными страницами (кодируем главную как "0")
    recent = request.COOKIES.get('recent_pages', '')
    rec_list = [x for x in recent.split(',') if x]
    rec_list = (rec_list + ['0'])[-5:]   # храним только последние 5
    response.set_cookie('recent_pages', ','.join(rec_list), max_age=30*24*3600)
    return response

# страница конкретного события: ищет событие по id, показывает его и сохраняет в cookies факт посещения
def event_detail(request, event_id):
    settings = get_user_settings_from_cookies(request)
    event = next((e for e in data.EVENTS if e['id'] == event_id), None)
    if not event:
        return HttpResponse('Event not found', status=404)

    response = render(request, 'planner/event_detail.html', {'event': event, 'settings': settings})

    # обновляем список последних посещённых страниц (сюда попадёт id события)
    recent = request.COOKIES.get('recent_pages', '')
    rec_list = [x for x in recent.split(',') if x]
    rec_list = (rec_list + [str(event_id)])[-5:]
    response.set_cookie('recent_pages', ','.join(rec_list), max_age=30*24*3600)
    return response

# страница с формой настроек: при GET показывает форму, при POST сохраняет настройки в cookies
def settings_view(request):
    initial = get_user_settings_from_cookies(request)

    if request.method == 'POST':
        form = SettingsForm(request.POST)
        if form.is_valid():
            theme = form.cleaned_data.get('theme') or 'light'
            language = form.cleaned_data.get('language') or 'ru'
            notifications = form.cleaned_data.get('notifications')

            # после сохранения настроек перенаправляем на главную страницу
            resp = redirect('planner:index')
            resp.set_cookie('theme', theme, max_age=365*24*3600) 
            resp.set_cookie('language', language, max_age=365*24*3600)
            resp.set_cookie('notifications', 'true' if notifications else 'false', max_age=365*24*3600)
            return resp
    else:
        # при первом открытии форма подставляется с текущими настройками
        form = SettingsForm(initial={
            'theme': initial['theme'],
            'language': initial['language'],
            'notifications': initial['notifications']
        })

    settings = initial
    return render(request, 'planner/settings.html', {'form': form, 'settings': settings})


# Create your views here.
