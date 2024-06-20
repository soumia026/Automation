from django.urls import path

from . import views

urlpatterns = [
    # path('ping/', views.ping, name='ping'),
    # path('setip/pc/',views.set_ip_pc,name="set_ip_for_pc"),
    path('dhcp/set/',views.set_dhcp,name="set_dhcp"),
    path('dhcp/binding/',views.get_dhcp_binding,name="get_dhcp_binding"),
]