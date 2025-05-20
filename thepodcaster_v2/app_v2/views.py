from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Show, Episode
from .forms import ShowForm, EpisodeForm
from django.http import HttpResponse
from django.template.loader import render_to_string
from . import extensions
# Create your views here.

def index(request):
    return render(request, 'app_v2/index.html')

def shows(request):
    return render(request, 'app_v2/show/shows.html')

@login_required(login_url='/login/')
def dashboard(request):
    return render(request, 'app_v2/dashboard.html')

#TODO: Add more views here
#TODO: Dashboard, Shows, Episodes, Account, Settings, etc.

@login_required(login_url='/login/')
def account(request):
    return render(request, 'app_v2/account/account.html')

@login_required(login_url='/login/')
def dashboard_shows(request):
    return render(request, 'app_v2/show/dashboard_shows.html',{"shows": Show.objects.filter(author=request.user)})

@login_required(login_url='/login/')
def overview(request):
    return render(request, 'app_v2/overview.html')

@login_required(login_url='/login/')
def episodes(request):
    episodes = Episode.objects.filter(show__author=request.user)
    return render(request, 'app_v2/episode/dashboard_episodes.html', {"episodes": episodes})
    
@login_required(login_url='/login/')
def add_show(request):
    if request.method == 'POST' and request.FILES:
        form = ShowForm(request.POST, request.FILES)
        if form.is_valid():
            show = form.save(commit=False)
            show.author = request.user
            show.save()
            return redirect('dashboard-shows')
        else:
            return render(request, 'app_v2/show/show_editor.html', {'form': form, "error": form.errors.as_json()})
    else:
        form = ShowForm()
        return render(request, 'app_v2/show/show_editor.html', {'form': form})
    
@login_required(login_url='/login/')
def add_episode(request):
    if request.method == 'POST':
        form = EpisodeForm(request.POST, request.FILES)
        if form.is_valid():
            episode = form.save(commit=False)
            episode.save()
            return redirect('dashboard-episodes')
        else:
            return render(request, 'app_v2/episode/episode_editor.html', {'form': form, "error": form.errors.as_json()})
    else:
        form = EpisodeForm()
        return render(request, 'app_v2/episode/episode_editor.html', {'form': form})

@login_required(login_url='/login/')
def edit_show(request, pk):
    show = Show.objects.get(pk=pk)
    form = ShowForm(request.POST, request.FILES, instance=show)
    if request.method == 'POST':
        form = ShowForm(request.POST, request.FILES)
        if form.is_valid():
            show = form.save(commit=False)
            show.author = request.user
            show.save()
            return redirect('dashboard-shows')
        else:
            return render(request, 'app_v2/show/show_editor.html', {'form': form, "error": form.errors.as_json()})
        
    else:
        return render(request, 'app_v2/show/show_editor.html', {'form': form})

@login_required(login_url='/login/')
def edit_episode(request, pk):
    episode = Episode.objects.get(pk=pk)
    form = EpisodeForm(instance=episode)
    if request.method == 'POST':
        form = EpisodeForm(request.POST, request.FILES, instance=episode)
        if form.is_valid():
            episode = form.save(commit=False)
            
            episode.save()
            
            return redirect('dashboard-episodes')
        else:
            return render(request, 'app_v2/episode/episode_editor.html', {'form': form, "error": form.errors.as_json()})
    else:
        return render(request, 'app_v2/episode/episode_editor.html', {'form': form})

@login_required(login_url='/login/')
def dashboard_rss(request, pk):
    show = Show.objects.get(pk=pk)
    episodes = Episode.objects.filter(show=show)
    rss_content = render_to_string('app_v2/rss.xml', {'show': show, 'episodes': episodes,"request":request})
    return HttpResponse(rss_content, content_type='application/rss+xml')
    
def show_rss(request, pk):
    show = Show.objects.get(pk=pk)
    episodes = Episode.objects.filter(show=show)
    rss_content = render_to_string('app_v2/rss.xml', {'show': show, 'episodes': episodes,"request":request})
    return HttpResponse(rss_content, content_type='application/rss+xml')