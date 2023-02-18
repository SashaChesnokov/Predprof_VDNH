import datetime
import copy
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render


# Create your views here.
from first.forms import FindForm
from first.models import Way


class Polygon:
    def __init__(self, name, number, rep, tegs=[], des="", edges=[]):
        self.name = name
        self.number = number
        self.rep = rep
        self.des = des
        self.edges = edges
        if type(tegs) == type(""):
            self.tegs = [tegs]
        else:
            self.tegs = tegs

# Инциализация графа
p = open("first/polygon.txt", "r")
n = len(open("first/polygon.txt", "r").readlines())
pols = []
for i in range(n):
    reader = p.readline().replace(";", " ").split()
    tmp = Polygon(name=reader[0], number=i, tegs=reader[1].replace("_", " ").split(), des=reader[2].replace("_", " "),
                  rep=1, edges=[])
    for i in range(3, len(reader), 2):
        tmp.edges += [[int(reader[i]), int(reader[i + 1])]]
    pols += [copy.deepcopy(tmp)]
g = [[-1 for i in range(len(pols))] for i in range(len(pols))]
for i in range(len(pols)):
    g[i][i] = 0
for p in range(len(pols)):
    for i in pols[p].edges:
        g[p][i[0] - 1] = i[1]

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
def routeGenerator(g, s, length, pols, fav = [], notfav = []):
  pols = pols.copy()
  inf = 10 ** 10
  if fav != [] or notfav != []:
    for i in range(len(pols)):
      for j in fav:
        if j in pols[i].tegs:
          pols[i].rep = inf
      for j in notfav:
        if j in pols[i].tegs:
          pols[i].rep = -inf
  if length > 0:
    tmp = pols[s].rep
    pols[s].rep = -inf
    choice = []
    n = 0
    for i in range(len(g[s])):
      if g[s][i] > 0:
        n += 1
        choice += [routeGenerator(g, i, length - g[s][i], pols)]
    maxInd = 0
    for i in range(1, n):
      if choice[i][0] > choice[maxInd][0]:
        maxInd = i
    return [tmp + choice[maxInd][0], [s] + choice[maxInd][1]]
  elif length == 0:
    return [pols[s].rep, [s]]
  else:
    return [0, []]


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


def Route_SF_page(request):
    context = {}

    if request.method == "POST":
        form = FindForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start']
            finish = form.cleaned_data['finish']

            res = WayArr[start][finish]
            dist = res[0]
            way_arr = [(str(i) + " - " + pols[i - 1].name) for i in res[1]]

            if dist != -1:
                context['dist'] = str(dist) + " мин."
                w_distance = str(dist*66) + " м."
                time = str(dist) + " мин."
                context['way_arr'] = way_arr
                s_arr = str(pols[res[1][0] - 1].name) + " -> " + str(pols[res[1][-1] - 1].name)
            else:
                context['dist'] = "такой маршрут невозможно построить"
                context['way_arr'] = []
                w_distance = ''
                time = ''
                s_arr = "Нет пути"

            if request.user.is_authenticated:
                record = Way(user=request.user, arr=s_arr, created_at=datetime.datetime.now(), time=time,
                             distance=w_distance)
                record.save()

    else:
        form = FindForm()

    context['form'] = form

    return render(request, 'create_route.html', context)


def Route_menu_page(request):
    context = {}

    return render(request, 'route_menu.html', context)