import datetime
import copy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render

# Create your views here.
from first.forms import PointsForm, TimeForm, InterestForm
from first.models import Way
from sys import setrecursionlimit

setrecursionlimit(20000)

class Polygon:
    """
    Класс Polygon для хранения информации о павильонах

    :param name: Название павильона
    :param number: Номер на карте
    :param rep: репутация (для расчета интересных путей)
    :param tegs: Тема павильона
    :param edges: Список павильонов, с котырыми соединен, и растояние между ними
    """

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


p = open('first/dist.txt', "r")
n = len(open("first/dist.txt",
             "r").readlines())  # Считывание информации о павильонах из текстового документа и заполнение массива
pols = []
for i in range(n):
  reader = p.readline().replace(";", " ").split()
  tmp = Polygon(name=reader[0].replace("_", " "),
                number=i,
                tegs=reader[1].replace("-", " ").split(),
                rep=int(reader[2].replace("_", " ")),
                edges=[])

  for i in range(3, len(reader), 2):
    tmp.edges += [[int(reader[i]), int(reader[i + 1])]]
  pols += [copy.deepcopy(tmp)]
g = [[-1 for i in range(len(pols))] for i in range(len(pols))]  # Генерация графа по времени между соседними павильонами

for i in range(len(pols)):
    g[i][i] = 0
for p in range(len(pols)):
    for i in pols[p].edges:
        g[p][i[0] - 1] = i[1]


def save(pols):
    """
    Функция save

    :param pols: Список павильонов
    Перебирает все елементы массива, сохраняя их в удобном для считывании формате, в текстовый файл ``dist.txt``
    """
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
    """
    Функция findWay

    :param g: Граф
    :param s: Номер точки начала маршрута
    :param f: Номер точки конца маршрута
    :return: Длина до искомой точки и маршрут до нее (список павильонов)

    *За основу взят алгоритм Деикстры*
    """
    n = len(g)  # Объявление констант, а также массива растояний, массива маршрутов и массива посещенных вершин
    way = [[-1]] * n
    way[s] = [s]
    inf = 10 ** 9
    dist = [inf] * n
    dist[s] = 0
    v = [False] * n
    while True:  # Пока существуют непосещенные вершины:
        m = inf
        for j in range(n):
            if not v[j] and dist[j] < m:  # Если существует длина пути меньше текущей:
                m = dist[j]  # Обновление длины и маршрута
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
def routeGenerator(g, s, length, pols, fav=[]):
    """
    Функция routeGenerator

    :param g: Граф
    :param s: Номер точки начала маршрута
    :param l: Максимальное время прохождения пути
    :param fav: Список интересующих типов павильонов
    :param notfav: Список не интересующих типов павильонов
    :return: Лучший маршрут (список павильонов) и его длину

    *За основу взят алгоритм Деикстры*
    """
    inf = 10 ** 10
    pols = pols[::1]

    for j in fav:
        for i in range(len(pols)):
            if j in pols[i].tegs:
                pols[i].rep = inf

    if length > 0:
        tmp = pols[s].rep
        pols[s].rep = -inf
        choice = []
        n = 0
        for i in range(len(g[s])):
            if g[s][i] > 0 and pols[i].rep > -10 ** 5 and length - g[s][i] > 0:
                n += 1
                choice += [routeGenerator(g, i, length - g[s][i], pols)]
        maxInd = 0
        if n == 0:
            return [tmp, [s + 1]]

        for i in range(0, n):
            if choice[i][0] > choice[maxInd][0]:
                maxInd = i
        return [tmp + choice[maxInd][0], [s + 1] + choice[maxInd][1]]
    elif length == 0:
        return [pols[s].rep, [s + 1]]
    else:
        return [0, []]


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
                w_distance = str(dist * 66) + " м."
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
            context['way_arr'] = [(str(i) + " - " + pols[i - 1].name) for i in res]
            res = [pols[i - 1].name for i in res]
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

    context['way_arr_v'] = ['Павильон № 36 «Переработка продукции сельского хозяйства»', 'Павильон № 29 «Цветоводство и озеленение»', 'Павильон № 25 «Нефтяная промышленность»', 'Строящийся аквапарк с океанариумом', 'Павильон № 21 «Газовая промышленность»', 'Павильон № 26 «Транспорт»', 'Павильон № 32 «Космос»', 'Павильон № 55 «Электрификация»', 'Площадь Промышленности', 'Павильон № 20 «Химическая промышленность»']
    context['way_arr_s'] = ['Павильон № 18 «Белоруссия»', 'Павильон № 15 «Радиоэлектроника и связь»', 'Павильон № 14 «Вычислительная техника»', 'Павильон № 13 «Здоровье»', 'Павильон № 12 «Профсоюзы»', 'Павильон № 11 «Металлургия» («Казахстан»)', 'Павильон № 10 «Стандарты»', 'Фонтан «Дружба народов СССР»', 'Павильон № 68 «Армения»', 'Павильон № 67 «Советская печать»', 'Павильон № 66 «Культура»']
    context['way_arr_n'] = ['Павильон №19 Планируемая область застройки', 'Павильон № 25 «Нефтяная промышленность»', 'Павильон № 29 «Цветоводство и озеленение»', 'Павильон № 32 «Космос»']

    return render(request, 'static_route.html', context)
