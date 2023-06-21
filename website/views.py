from django.shortcuts import render, redirect, get_object_or_404
# retornar o response como json
from django.db import connection
from django.http import HttpResponse
from django.http import JsonResponse
import json
from django.core import serializers
from django.shortcuts import render
# fim
# from django.template import loader
from django.contrib import messages
from django.views import View
from django.views.generic.edit import CreateView
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.db.models import Count, Q
# from .models import Carro, Fabricante
# from fabricante.forms import FabricanteForm
# from carro.forms import CarroForm
from consoles.models import Console
from media_files.models import MediaFile
from emulators.models import Emulator
from games.models import Game
# from media_files.models import MediaFile
# import os
from django.db.models import OuterRef, Subquery


# Create your views here.
def elements(request):
    return render(request, 'elements.html')


def generic(request):
    return render(request, 'generic.html')


def testes(request):
    cursor = connection.cursor()
    cursor.execute('''SELECT g.*, c.short_name console FROM games_game g
                    join games_game_console gc on gc.game_id = g.id
                    join consoles_console c on c.id = gc.console_id
                    ''')

    response = []
    for id, name, short_name, console in cursor:
        r = {}
        r['id'] = id
        r['name'] = name
        r['short_name'] = short_name
        r['console'] = console
        # response.append(dict(r))
        response.append(r)
    cursor.close()

    data = json.dumps(response)
    return HttpResponse(data, content_type='application/json')
    # return JsonResponse(data)


def testes2(request):
    with connection.cursor() as cursor:
        query = """
            SELECT g.*, c.short_name console FROM games_game g
            join games_game_console gc on gc.game_id = g.id
            join consoles_console c on c.id = gc.console_id
        """
        cursor.execute(query)
        # cursor.rowfactory = lambda *args: dict(zip([d[0] for d in curs.description], args))
        # columns = [col[0] for col in cursor.description]
        # cursor.rowfactory = lambda *args: dict(zip(columns, args))
        # data = cursor.fetchall()
        columns = [str.lower(i[0]) for i in cursor.description]
        response = [dict(zip(columns, row)) for row in cursor]
        data = json.dumps(response)
        return HttpResponse(data, content_type='application/json')


# Function based view
def myView(request):
    with connection.cursor() as cursor:
        query = """ SELECT g.*, c.short_name console FROM games_game g join games_game_console gc on gc.game_id = g.id join consoles_console c on c.id = gc.console_id """
        cursor.execute(query)
        columns = [str.lower(i[0]) for i in cursor.description]
        data = [dict(zip(columns, row)) for row in cursor]
        return HttpResponse(json.dumps(data), content_type="application/json")


# Class based view
class MyView(View):
    def get(self, request):
        with connection.cursor() as cursor:
            query = """ SELECT g.*, c.short_name console FROM games_game g join games_game_console gc on gc.game_id = g.id join consoles_console c on c.id = gc.console_id """
            # query = """ SELECT c.*, m.* FROM consoles_console c left join media_files_mediafile m on m.console_id = c.id """
            cursor.execute(query)
            columns = [str.lower(i[0]) for i in cursor.description]
            data = [dict(zip(columns, row)) for row in cursor]
            return HttpResponse(json.dumps(data), content_type="application/json")


def show_tables(request):
    with connection.cursor() as cursor:
        data = cursor.execute(""" SELECT table_name FROM all_tables WHERE owner='ADMIN' ORDER BY table_name """)
        response = [str.lower(d[0]) for d in data if d[0] != "PYTAB"]
        # columns = [str.lower(i[0]) for i in cursor.description]
        # data =  [dict(zip(columns, row)) for row in cursor]
        return HttpResponse(json.dumps(response), content_type="application/json")


from django.template.defaultfilters import slugify


def home(request):
    games = Game.objects.order_by('-id')
    for q in games:
        q.media_files = MediaFile.objects.filter(game_id=q.id)
    context = {'games': games, 'emulators_nav': emulators_nav, 'games_nav': games_nav, }
    # if request.META['HTTP_ACCEPT'] == 'application/json':
    #     response = serializers.serialize('json', games)
    #     return HttpResponse(response, content_type='application/json')
    # else:
    #     context = {'games': games}
    #     return render(request, 'index.html', context)
    return render(request, 'index.html', context)


# class HomeIndex(ListView):
#     model = Game
#     template_name = 'index.html'
#     paginate_by = 10
#     context_object_name = 'games'

#     def get_queryset(self):
#         qs = super().get_queryset()
#         for q in qs:
#             q.media_files = MediaFile.objects.filter(game_id=q.id)
#         return qs
#     def get_context_data(self, **kwargs):
#         context = super(GameIndex, self).get_context_data(**kwargs)
#         context['emulators_nav']=emulators_nav
#         context['games_nav']=games_nav
#         return context

# class NavMenuIndex(ListView):
#     model = Emulator
#     # template_name = 'consoles/console.hml'
#     # context_object_name = 'consoles'
#     queryset = model.objects.all()

#     def get_context_data(self, **kwargs):
#         # context = super(ConsoleIndex, self).get_context_data(**kwargs)
#         # context['consoles'] = Console.objects.all()
#         context['emulators'] = self.queryset
#         return context    

class ConsoleIndex(ListView):
    model = Console
    template_name = 'consoles/consoles.html'
    paginate_by = 10
    context_object_name = 'consoles'

    def get_queryset(self):
        qs = super().get_queryset()
        # qs = qs.select_related('modelo')
        qs = qs.prefetch_related('mediafiles').order_by('name').filter()
        qs = [list(console.mediafiles.filter(console_id__in=qs.values('id'))) for console in qs]
        return qs

    def get_context_data(self, **kwargs):
        # context = super(ConsoleIndex, self).get_context_data(**kwargs)
        # consoles = Console.objects.all().order_by('name')
        # consoles = Console.objects.filter(id=2)
        # media_files = MediaFile.objects.all()
        # media_files = MediaFile.objects.filter(console__name="id")
        # media_files = MediaFile.objects.filter(console=consoles)
        # media_files = MediaFile.objects.filter(console=OuterRef('id'))
        # media_files = MediaFile.objects.filter(console=consoles.values('id'))
        # consoles.media_files = media_files
        # console = Console.objects.all().prefetch_related(media_files).order_by('-id') # MANYTOMANY
        # Console.objects.select_related('media_files')#FOREIGNKEY
        # media_files = MediaFile.objects.select_related(None)
        # console.media_files=media_files
        # consoles =MediaFile.objects.select_related('console')#FOREIGNKEY
        # consoles = Console.objects.all().order_by('name')
        # media_files = MediaFile.objects.filter(console__in=consoles).order_by('pk').distinct()
        # media_files = Console.objects.get(id=1).mediafile_set.all()
        # consoles = Console.objects.all().prefetch_related('mediafile')
        # media_files = MediaFile.objects.select_related().filter(console_id__in=consoles.values('id'))
        # mediafiles = MediaFile.objects.select_related().filter(console_id__in=console.values('id'))
        # print({'consoles': consoles, 'interviews': MediaFile.objects.filter(console_id__in=consoles)})
        # console = serializers.serialize('json', console)
        # print(str(mediafiles.query))
        # print(str(console))
        # console.mediafiles.all()
        # console = Console.objects.all().order_by('name')

        # consoles = Console.objects.all().order_by('name').prefetch_related('mediafiles')
        # console_list = [list(console.mediafiles.filter(console_id__in=consoles.values('id'))) for console in consoles]

        # json = serializers.serialize('json', asd)
        # print(str(mediafiles.query))
        # print(json)
        # consoles = []
        # for e in console:
        #     print(e.name)
        # for c in console:
        #     print(c)
        #     consoles['consoles']={c}
        #     for m in mediafiles:
        #         media=[]
        #         if c.id == m.console:
        #             media.append(m)
        #         consoles['media_files']={media}
        # context['console_list'] = console_list
        # context['media_files'] = MediaFile.objects.all()
        # context['emulators_nav'] = emulators_nav
        # context['games_nav'] = games_nav
        # context = {'console_list': console_list, 'emulators_nav':emulators_nav, 'games_nav':games_nav, }
        # context = super().get_context_data(**kwargs)
        # context = super(ConsoleIndex, self).get_context_data(**kwargs)
        # context = {'consoles': self.get_queryset(), 'emulators_nav':emulators_nav, 'games_nav':games_nav, }
        context = super(ConsoleIndex, self).get_context_data(**kwargs)
        console_list = list(self.get_queryset())
        context['data'] = zip(console_list)
        context['emulators_nav'] = emulators_nav
        context['games_nav'] = games_nav
        return context


# class ConsoleDetails(DetailView):
class ConsoleDetails(View):
    template_name = 'consoles/console.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        pk = self.kwargs.get('pk')

        console = get_object_or_404(Console, pk=pk)
        # console = console.mediafiles.filter(console_id=console.id)
        # console.mediafiles.set(console.mediafiles.filter(console_id=console.id))
        # media_files = MediaFile.objects.filter(console_id=console.id)
        media_files = console.mediafiles.filter(console_id=console.id)
        console.mediafiles.set(media_files)
        self.contexto = {
            'console': console,
            'mediafiles': media_files,
            'emulators_nav': emulators_nav,
            'games_nav': games_nav,
        }

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.contexto)


class EmulatorIndex(ListView):
    model = Emulator
    template_name = 'emulators/emulators.html'
    paginate_by = 10
    context_object_name = 'emulators'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.prefetch_related('mediafiles').order_by('name').filter()
        qs = [list(emulator.mediafiles.filter(emulator_id__in=qs.values('id'))) for emulator in qs]
        return qs

    def get_context_data(self, **kwargs):
        context = super(EmulatorIndex, self).get_context_data(**kwargs)
        emulator_list = list(self.get_queryset())
        context['data'] = zip(emulator_list)
        context['emulators_nav'] = emulators_nav
        context['games_nav'] = games_nav
        return context


class EmulatorDetails(View):
    template_name = 'emulators/emulator.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        short_name = self.kwargs.get('short_name')

        emulator = get_object_or_404(Emulator, console__short_name=short_name)
        media_files = emulator.mediafiles.filter(emulator_id=emulator.id)
        self.contexto = {
            'emulator': emulator,
            'mediafiles': media_files,
            'emulators_nav': emulators_nav,
            'games_nav': games_nav,
        }

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.contexto)


class GameIndex(ListView):
    model = Game
    template_name = 'games/games.html'
    paginate_by = 10
    context_object_name = 'games'

    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     qs = qs.prefetch_related('console', 'mediafiles').order_by('name').filter(console__id__in=qs.values('id'),mediafiles__game_id__in=qs.values('id'))
    #     # qs = qs.prefetch_related('console', 'mediafiles').order_by('name').filter()
    #     # qs = qs.prefetch_related('mediafiles').order_by('name').filter()
    #     # qs = [list(game.mediafiles.filter(game_id__in=qs.values('id'))) for game in qs]
    #     # qs = qs.prefetch_related('console').order_by('name').filter()
    #     # qs = [list(game.console.filter(id__in=qs.values('id'))) for game in qs]

    #     # qs = qs.prefetch_related('console')
    #     # qs = [list(game.console.filter(id__in=qs.values('id'))) for game in qs]
    #     qs.console = Console.objects.filter(id__in=qs.values('id')).get()
    #     qs.mediafiles = MediaFile.objects.filter(game_id__in=qs.values('id')).get()
    #     return qs

    # def get_context_data(self, **kwargs):
    #     context = super(GameIndex, self).get_context_data(**kwargs)
    #     game_list = list(self.get_queryset())
    #     print(self.get_queryset().console.short_name)
    #     # context['data'] = zip(game_list)
    #     context['data'] = self.get_queryset()
    #     # context['console'] = self.get_queryset().console
    #     # context['mediafiles'] = self.get_queryset().mediafiles
    #     context['emulators_nav']=emulators_nav
    #     context['games_nav']=games_nav
    #     return context
    def get_queryset(self):
        qs = super().get_queryset().filter()
        # qs = qs.prefetch_related('mediafiles').order_by('name').filter()
        # qs = qs.prefetch_related('console').order_by('name').filter()
        # qs.mediafiles = [list(game.mediafiles.filter(game_id__in=qs.values('id'))) for game in qs]

        # qs = qs.prefetch_related('console', 'mediafiles').order_by('name').filter(console__id__in=qs.values('id'),mediafiles__game_id__in=qs.values('id'))
        # qs.console = Console.objects.filter(id__in=qs.values('id')).get()
        # qs.mediafiles = MediaFile.objects.filter(game_id__in=qs.values('id')).get()
        for q in qs:
            q.media_files = MediaFile.objects.filter(game_id=q.id)
        # qs = qs.prefetch_related('console','mediafiles').order_by('name').filter()
        # qs.console = Console.objects.filter(id__in=qs.values('id'))
        # qs.mediafiles = MediaFile.objects.filter(game_id__in=qs.values('id'))
        # qs = qs.prefetch_related('console', 'mediafiles').order_by('name').filter(console__id__in=qs.values('id'),mediafiles__game_id__in=qs.values('id'))
        return qs

    def get_context_data(self, **kwargs):
        context = super(GameIndex, self).get_context_data(**kwargs)
        # game_list = self.get_queryset()
        # game_list = self.get_queryset().all().values("id", "console_id", "mediafiles")
        # game_list = serializers.serialize("json", self.get_queryset())
        # game_list.mediafiles = self.get_queryset().mediafiles
        # print(self.get_queryset().mediafiles[0].image_file)
        # print(self.get_queryset().name)
        # print(self.get_queryset().consoles)
        # print(game_list.mediafiles[1].image_file)
        # print(get_json_list(game_list))
        # print(context)
        # context['data'] = game_list
        context['emulators_nav'] = emulators_nav
        context['games_nav'] = games_nav
        return context


class GameByConsole(ListView):
    model = Game
    template_name = 'games/games.html'
    # ordering = ['-name']
    paginate_by = 10
    context_object_name = 'games'

    def get_queryset(self, **kwargs):
        console_short_name = self.kwargs.get('short_name')
        # print(console_short_name)
        qs = super().get_queryset()
        games = qs

        qs = super().get_queryset().prefetch_related('mediafiles').filter(console__short_name=console_short_name).order_by('name')
        # qs = qs.prefetch_related('console', 'mediafiles').order_by('name').filter(console__id__in=qs.values('id'),
        #                                                                           mediafiles__game_id__in=qs.values(
        #                                                                               'id'))
        # qs = qs.prefetch_related('mediafiles').order_by('name').filter(mediafiles__game_id__in=qs.values('id'))
        # qs = qs.prefetch_related('mediafiles').order_by('name').filter()
        # qs.mediafiles = MediaFile.objects.filter(mediafiles__game_id__in=qs.values('id'))
        # print(qs)
        # for q in qs:
        #     print(q.mediafiles)
        #
        for q in qs:
            q.media_files = MediaFile.objects.filter(game_id=q.id)

        # for g in qs:
        #     print('for')
        #     print(MediaFile.objects.filter(game_id=g.id))
        # g.media_files = MediaFile.objects.filter(game_id=g.id)

        # qs = super(GameByConsole, self).get_queryset()
        # games = Game.objects.filter(console__short_name=console_short_name).order_by('name')
        # games = qs.filter(console__short_name=console_short_name)

        # games = qs.filter(Q(console__short_name=console_short_name)).order_by('name')

        # for g in games:
        #     print('for')
        #     print(MediaFile.objects.filter(game_id=g.id))
        #     g.media_files = MediaFile.objects.filter(game_id=g.id)

        # for q in qs:
        #     q.media_files = MediaFile.objects.filter(game_id=q.id)
        # print(games)
        return qs

    def get_context_data(self, **kwargs):
        context = super(GameByConsole, self).get_context_data(**kwargs)
        # game_list = self.get_queryset()
        # context['games']=game_list
        context['emulators_nav'] = emulators_nav
        context['games_nav'] = games_nav
        return context


class GameDetails(View):
    template_name = 'games/game.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        game_id = self.kwargs.get('game_id')

        game = get_object_or_404(Game, id=game_id)
        media_files = game.mediafiles.filter(game_id=game.id)
        self.contexto = {
            'game': game,
            'mediafiles': media_files,
            'emulators_nav': emulators_nav,
            'games_nav': games_nav,
        }

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.contexto)


def emulators_nav():
    emulators_nav = Emulator.objects.values('console__short_name').annotate(
        short_name_count=Count('console__short_name')).order_by('console__short_name')
    return emulators_nav


def games_nav():
    games_nav = Game.objects.values('console__short_name').annotate(console=Count('console__short_name')).order_by(
        'console__short_name')
    return games_nav


def rows_to_dict_list(cursor):
    columns = [i[0] for i in cursor.description]
    return [dict(zip(columns, row)) for row in cursor]


def get_json_list(query_set):
    list_objects = []
    for obj in query_set:
        dict_obj = {}
        for field in obj._meta.get_fields():
            try:
                if field.many_to_many:
                    dict_obj[field.name] = get_json_list(getattr(obj, field.name).all())
                    continue
                dict_obj[field.name] = getattr(obj, field.name)
            except AttributeError:
                continue
        list_objects.append(dict_obj)
    return list_objects
