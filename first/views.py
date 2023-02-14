import datetime
import copy
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render


# Create your views here.
from first.forms import FindForm
from first.models import Pavilion, Way

g = []
f = open("first/dist.txt", "r")
for i in range(8):
  g.append(list(map(int, f.readline().split())))


def findWay(s, f, n=8):
  way = [[-1]] * n
  way[s] = [s]
  inf = 10 ** 9
  dist = [inf] * n
  dist[s] = 0
  v = [False] * n
  while True:
    m = inf
    for j in range(n):
      if not v[j] and dist[j] < m:
        m = dist[j]
        md = j
    if m == inf:
      break
    i = md
    v[i] = True
    for k in range(n):
      if dist[i] + g[i][k] < dist[k] and g[i][k] != -1:
        dist[k] = dist[i] + g[i][k]
        way[k] = way[i] + [k]
  if dist[f] == inf:
    return [-1, -1]
  else:
    return [dist[f], way[f]]


def Main_page(request):
    context = {}

    return render(request, 'index.html', context)


def Info_page(request):
    context = {}

    return render(request, 'info.html', context)


def History_page(request):
    context = {}

    history = list(Way.objects.filter(user=request.user))
    history.reverse()
    context['history'] = history
    return render(request, 'history.html', context)


def Route_page(request):
    context = {}

    if request.method == "POST":
        form = FindForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start']
            finish = form.cleaned_data['finish']
            way = findWay(start, finish)
            dist = way[0]
            way_arr = way[1]
            context['dist'] = dist
            context['way_arr'] = way_arr
            s_arr = str(way_arr[0]) + " -> " + str(way_arr[-1])
            if request.user.is_authenticated:
                record = Way(user=request.user, arr=s_arr, created_at=datetime.datetime.now(), time=dist)
                record.save()

    else:
        form = FindForm()

    context['form'] = form

    return render(request, 'create_route.html', context)