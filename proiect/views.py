from proiect.models import Comp
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import CompForm

import sqlite3

from django.contrib.auth import authenticate, login

import platform
from datetime import datetime
import psutil
import os

@login_required
def index(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html")


@login_required
def infocollect(request):
    if request.method == 'POST':
        form1 = CompForm(request.POST)
        if form1.is_valid():
            form1.save()
            return redirect('infoprint')

    else:
        form1 = CompForm()

    return render(request,'infocollect.html', {'form1':form1})


@login_required
def infoprint(request):
    con = sqlite3.connect('db.sqlite3')
    username = []
    architecture = []
    systemname = []
    nocores = []
    nothreads = []
    maxfrq = []
    minfrq = []
    memory = []
    memoryavailable = []
    memoryused = []
    i = 0
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM proiect_comp")
        for row in cur:
            username.append(row[0])
            architecture.append(row[1])
            systemname.append(row[2])
            nocores.append(row[3])
            nothreads.append(row[4])
            maxfrq.append(row[5])
            minfrq.append(row[6])
            memory.append(row[7])
            memoryavailable.append(row[8])
            memoryused.append(row[9])
            i = i + 1
    
    antet = []
    for x in range(i):
        antet.append('User ' + str(x))
    output = {
        'User Number': antet,
        'User Name': username,
        'Architecture': architecture,
        'System Name': systemname,
        'No Cores': nocores,
        'No Threads': nothreads,
        'Max Frq': maxfrq,
        'Min Frq': minfrq,
        'Memory': memory,
        'Memory Available': memoryavailable,
        'Memory Used': memoryused
    }

    return render(request, 'infoprint.html', { 'output': output.items() })


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
	
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def about(request: HttpRequest) -> HttpResponse:

    boot_time = datetime.fromtimestamp(psutil.boot_time())

    #with open("/proc/uptime", "r") as f:
    #    uptime = f.read().split(" ")[0].strip()

    #uptime = int(float(uptime))
    #uptime_hours = uptime // 3600
    #uptime_minutes = (uptime % 3600) // 60
    #pids = []
    #for subdir in os.listdir('/proc'):
    #    if subdir.isdigit():
    #        pids.append(subdir)

    cpu_frequency = psutil.cpu_freq()

    def bytes_to_GB(bytes):
        gb = bytes/(1024*1024*1024)
        gb = round(gb, 2)
        return gb

    virtual_memory = psutil.virtual_memory()
    swap = psutil.swap_memory()
    disk_rw = psutil.disk_io_counters()
    net_io = psutil.net_io_counters()
    battery = psutil.sensors_battery()

    data = {
        "Architecture": platform.architecture()[0],
        "Machine": platform.machine(),
        "Operating System Release": platform.release(),
        "System Name": platform.system(),
    #    "Operating System Version": platform.version(),
    #    "Node": platform.node(),
    #    "Platform": platform.platform(),
        "Processor": platform.processor(),
        "System Boot Time": boot_time,
        #"System Uptime": str(uptime_hours) + ":" + str(uptime_minutes) + " hours",
        #"Total number of processes": len(pids),
        "Number of Physical cores": psutil.cpu_count(logical=False),
        "Number of Total cores": psutil.cpu_count(logical=True),
        "Max Frequency": cpu_frequency.max,
        "Min Frequency": cpu_frequency.min,
        "Current Frequency": cpu_frequency.current,
        "Total Memory present": str(bytes_to_GB(virtual_memory.total)) + " Gb",
        "Total Memory Available": str(bytes_to_GB(virtual_memory.available)) + " Gb",
        "Total Memory Used": str(bytes_to_GB(virtual_memory.used)) + "Gb",
        "Percentage Used": str(virtual_memory.percent) + "%",
        "Total swap memory": bytes_to_GB(swap.total),
        "Free swap memory": bytes_to_GB(swap.free),
        "Used swap memory": bytes_to_GB(swap.used),
        "Percentage Used": str(swap.percent) + "%",
        "Total Read since boot": str(bytes_to_GB(disk_rw.read_bytes)) + "GB",
        "Total Write sice boot": str(bytes_to_GB(disk_rw.write_bytes)) + "GB",
        "Total Bytes Sent": bytes_to_GB(net_io.bytes_sent),
        "Total Bytes Received": bytes_to_GB(net_io.bytes_recv),
        "Battery Percentage": str(round(battery.percent, 1)) + "%",
        "Battery time left": str(round(battery.secsleft/3600, 2)) + "hr",
        "Power Plugged": battery.power_plugged
    }

    return render(request, "about.html", { 'data':data.items() })





class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"
