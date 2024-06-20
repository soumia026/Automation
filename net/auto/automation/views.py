
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from . import functions
from django.views.decorators.csrf import csrf_exempt
from tabulate import tabulate
import re


# Create your views here.
# def home(request):
#     return HttpResponse(render(request,"shabaka.html"))

# def about(request):
#     return HttpResponse(render(request,"about.html"))

# def index(request):
#     return HttpResponse(render(request,"index.html"))

# @csrf_exempt
# def ping(request):
#     x = ''
#     for i in functions.ping(request.GET['host'],request.GET['address']).split("\n"):
#         x +='<pre>'+i+'</pre>'
#     return HttpResponse(x)    

# @csrf_exempt
# def show_ospf(request):
#     headers = re.sub(' +', ' ',functions.get_ospf_neighboor(request.GET['router']).split("\n")[0]).strip().split(' ')
#     table = []
#     for i in functions.get_ospf_neighboor(request.GET['router']).split("\n")[1::]:
#         table.append(re.sub(' +',' ',i).strip().split(' '))
#     x = ''
#     for i in tabulate(table,headers=headers).split("\n"):
#         x +='<pre>'+i+'</pre>'
#     return HttpResponse(x)


# @csrf_exempt
# def set_ip_pc(request):
#     if(request.POST["gateway"]==""):
#         if(request.POST["pc"]=='5006' or request.POST["pc"]=='5002'):
#             res = functions.set_ip_for_pc(request.POST['pc'],request.POST['ip'],"192.168.1.1")
#         else:
#             res = functions.set_ip_for_pc(request.POST['pc'],request.POST['ip'],"192.168.2.1")
#     else:
#         res = functions.set_ip_for_pc(request.POST['pc'],request.POST['ip'],request.POST['gateway'])
#     return HttpResponse(res+'<br/><br/><a href="../../index">go back</a>')


@csrf_exempt
def set_dhcp(request):
    functions.set_dhcp(request.POST['router'] )
    return HttpResponse()


@csrf_exempt
def get_dhcp_binding(request):
    x = ''
    for i in functions.get_dhcp_binding(request.GET['router']).split('\n'):
        x+= '<pre>'+i+'</pre>'
    return HttpResponse(x)