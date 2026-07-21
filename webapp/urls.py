from django.urls import path

from simulator import views

urlpatterns = [
    path('', views.index, name='index'),
    path('set-quantum/', views.set_quantum, name='set_quantum'),
    path('add-process/', views.add_process, name='add_process'),
    path('load-sample/', views.load_sample, name='load_sample'),
    path('step/', views.step, name='step'),
    path('run-all/', views.run_all, name='run_all'),
    path('reset/', views.reset, name='reset'),
]
