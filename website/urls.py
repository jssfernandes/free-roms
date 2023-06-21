from django.urls import path
from . import views

urlpatterns = [
    path('elements.html', views.elements, name='elements'),
    path('generic.html', views.generic, name='generic'),
    path('testes', views.testes, name='testes'),
    path('testes2', views.testes2, name='testes2'),
    path('myView', views.myView, name='myView'),
    path('MyView', views.MyView.as_view(), name='MyView'),
    path('tables', views.show_tables, name='show_tables'),
    path('', views.home, name='home'),
    # path('index.html', views.home, name='home'),
    path('home', views.home, name='home'),
    # path('', views.HomeIndex.as_view(), name='home'),
    # path('home', views.HomeIndex.as_view(), name='home'),
    path('consoles', views.ConsoleIndex.as_view(), name='consoles'),
    path('consoles/<int:pk>', views.ConsoleDetails.as_view(), name='console_details'),
    path('emulators', views.EmulatorIndex.as_view(), name='emulators'),
    path('emulators/<short_name>', views.EmulatorDetails.as_view(), name='emulator_details'),
    path('games', views.GameIndex.as_view(), name='games'),
    path('games/<short_name>', views.GameByConsole.as_view(), name='game_list_by_console'),
    # path('games/<str:console_short_name>', views.GameDetails.as_view(), name='game_details'),
    # path('games/<int:game_id>', views.GameDetails.as_view(), name='game_details_by_id'),
    # path('games/console/<int:game_id>', views.GameDetails.as_view(), name='game_details_by_id'),
    # path('consoles/<short_name>/games', views.GameByConsole.as_view(), name='game_list_by_console'),
    # path('consoles/<short_name>/games/<name>', views.GameDetails.as_view(), name='game_details_by_game_name'),
    
    # path('consoles/<pk>', views.ConsoleDetails.as_view(), name='console_details'),
    # path('consoles/(?P<pk>[-\w]+)', views.ConsoleDetails.as_view(), name='console_details'),
    # path('consoles/<console_id>', views.ConsoleDetails.as_view(), name='console_details'),
]
