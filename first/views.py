import datetime
import copy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render


# Create your views here.
from first.forms import PointsForm, TimeForm, InterestForm
from first.models import Way


class Polygon:
    def __init__(self, name, number, rep, tegs=[], edges=[]):
        self.name = name
        self.number = number
        self.rep = rep
        self.edges = edges

        if type(tegs) == type(""):
            self.tegs = [tegs]
        else:
            self.tegs = tegs

    def repPlus(self):
        self.rep += 1

    def repMinus(self):
        self.rep -= 1


p = open("first/dist.txt", "r")
n = len(open("first/dist.txt", "r").readlines())
pols = []
for i in range(n):
    reader = p.readline().replace(";", " ").split()
    tmp = Polygon(name=reader[0].replace("_", " "),
                  number=i,
                  tegs=reader[1].replace("_", " ").split(),
                  rep=int(reader[2].replace("_", " ")),
                  edges=[])

    for i in range(3, len(reader), 2):
        tmp.edges += [[int(reader[i]), int(reader[i + 1])]]
    pols += [copy.deepcopy(tmp)]
g = [[-1 for i in range(len(pols))] for i in range(len(pols))]

for i in range(len(pols)):
    g[i][i] = 0
for p in range(len(pols)):
    for i in pols[p].edges:
        g[p][i[0] - 1] = i[1]


def safe(pols):
    p = open("first/dist.txt", "w")
    for i in pols:
        tmp = ""
        tmp += i.name.replace(" ", "_") + ";"
        for k in i.tegs:
            tmp += k
            if k != i.tegs[-1]:
                tmp += "-"
        tmp += ";" + str(i.rep) + ";"
        for k in i.edges:
            tmp += str(k[0]) + " " + str(k[1]) + " "
        if i != pols[-1]:
            tmp += "\n"
        p.write(tmp)

counter = 0
for x in range(len(g)):
    for y in range(len(g)):
        if g[x][y] != g[y][x]:
            counter += 1


# Модифицированная деикстра
def findWay(g, s, f):
    n = len(g)
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
        return [-1, [s, f]]
    else:
        return [dist[f], way[f]]


# Оптимизация алгоритма нахождения пути и растоянии путем генерации всевозможных маршрутов
WayArr = [[[[]] for i in range(n)] for j in range(n)]
for s in range(n):
  for f in range(n):
    WayArr[s][f] = findWay(g, s, f)


# Генератор маршрутор
def routeGenerator(g, s, l, pols, fav=[], notfav=[]):
  #Генерация репутации
  if fav != [] or notfav != []:
    inf = 10**10
    for i in range(len(pols)):
      for j in fav:
        if j in pols[i].tegs:
          pols[i].rep = inf
      for j in notfav:
        if j in pols[i].tegs:
          pols[i].rep = -inf

  #Инцилизация переменных
  n = len(g)
  way = [[-1]] * n
  way[s] = [s + 1]

  inf = 10**10

  dist = [inf] * n
  dist[s] = 0

  rep = [-1] * n
  rep[s] = pols[s].rep

  v = [False] * n

  #Оснавная часть
  while True:
    m = -inf
    for j in range(n):
      if not v[j] and rep[j] > m:
        m = rep[j]
        md = j
    if m == -inf:
      break
    i = md
    v[i] = True
    for k in range(n):
      if rep[i] + pols[i].rep > rep[k] and dist[i] + g[i][k] <= l and g[i][
          k] > 0:
        dist[k] = dist[i] + g[i][k]
        way[k] = way[i] + [k + 1]
        rep[k] = rep[i] + pols[i].rep
        if (k + 1) in way[:-1]:
          rep[k] -= 10**5

  max = 0
  for i in range(n):
    if (rep[i] > rep[max]):
      max = i

  return [dist[max], way[max]]


def Main_page(request):
    context = {}

    return render(request, 'index.html', context)


def Info_page(request):
    context = {}

    return render(request, 'info.html', context)


@login_required
def History_page(request):
    context = {}

    history = list(Way.objects.filter(user=request.user))
    history.reverse()
    context['history'] = history
    return render(request, 'history.html', context)


def Route_menu_page(request):
    context = {}

    return render(request, 'route_menu.html', context)


def Route_points_page(request):
    context = {}

    if request.method == "POST":
        form = PointsForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start'] - 1
            finish = form.cleaned_data['finish'] - 1

            res = WayArr[start][finish]
            dist = res[0]
            way_arr = [(str(i + 1) + " - " + pols[i].name) for i in res[1]]

            if dist != -1:
                context['dist'] = "Время прохождения маршрута: " + str(dist) + " мин."
                w_distance = str(dist*66) + " м."
                time = str(dist) + " мин."
                context['way_arr'] = way_arr
                s_arr = str(pols[res[1][0]].name) + " -> " + str(pols[res[1][-1]].name)
                if request.user.is_authenticated:
                    record = Way(user=request.user, arr=s_arr, created_at=datetime.datetime.now(), time=time,
                                 distance=w_distance)
                    record.save()
            else:
                context['dist'] = "Такой маршрут невозможно построить"
                context['way_arr'] = []

    else:
        form = PointsForm()

    context['form'] = form

    return render(request, 'points_route.html', context)


def Route_time_page(request):
    context = {}

    if request.method == "POST":
        form = TimeForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start']
            time = form.cleaned_data['time']
            theme = form.cleaned_data['vote_type']

            res = routeGenerator(g, start - 1, time, copy.deepcopy(pols), [theme])[1]
            context['way_arr'] = [(str(i) + " - " + pols[i-1].name) for i in res]
            res = [pols[i-1].name for i in res]
            w_distance = str(time * 66) + " м."
            time = str(time) + " мин."
            s_arr = str(res[0]) + " -> " + str(res[-1])
            if request.user.is_authenticated:
                record = Way(user=request.user, arr=s_arr, created_at=datetime.datetime.now(), time=time,
                             distance=w_distance)
                record.save()
    else:
        form = TimeForm()

    context['form'] = form

    return render(request, 'time_route.html', context)


def Route_interest_page(request):
    context = {}

    context['way1'] = [1, 2, 3, 5, 6, 7, 8, 11, 12, 16, 18, 19, 20, 21, 22, 23, 25, 26, 27, 28, 30, 31, 32, 33, 34, 35, 37]
    context['way2'] = [4, 5, 6, 7, 8, 10, 12, 13, 14, 20]
    context['way3'] = [19, 27, 32, 34]

    return render(request, 'static_route.html', context)