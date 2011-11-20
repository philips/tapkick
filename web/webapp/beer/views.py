import datetime

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import Http404
from django.http import HttpResponse
from django.db.models import Count 
from django.db.models import Sum
from beer.models import User
from beer.models import Access
from beer.models import Beer
import json

def user_list(request):
    user_list = User.objects.filter(private=False)
    context = {
        'user_list': user_list,
    }
    return render_to_response(
            'user_list.html', context,
            context_instance=RequestContext(request))


def user_detail(request, rfid_id):
    try:
        user = User.objects.get(rfid=rfid_id)
    except User.DoesNotExist:
        raise Http404
    context = {
        'user': user,
    }
    return render_to_response(
            'user_detail.html', context,
            context_instance=RequestContext(request))


def front_page(request):
    tap1_beer, c1 = Beer.objects.get_or_create(tap_number=1, active=True)
    if c1:
        tap1_beer.name = "PBR"
        tap1_beer.slug = "pbr"
        tap1_beer.save()
    tap2_beer, c2 = Beer.objects.get_or_create(tap_number=2, active=True)
    if c2:
        tap2_beer.name = "PBR"
        tap2_beer.slug = "pbr"
        tap2_beer.save()

    last_to_drink1 = None
    last_to_drink2 = None

    drinker_list_tap1 = Access.objects.filter(beer=tap1_beer).order_by('-time')
    if drinker_list_tap1:
        last_to_drink1 = drinker_list_tap1[0]
    drinker_list_tap2 = Access.objects.filter(beer=tap2_beer).order_by('-time')
    if drinker_list_tap2:
        last_to_drink2 = drinker_list_tap2[0]

    user_amount1 = Access.objects.filter(beer=tap1_beer).values('user',
        'user__name').order_by('user').annotate(total=Sum('amount')).order_by('-total')
    user_amount2 = Access.objects.filter(beer=tap2_beer).values('user',
        'user__name').order_by('user').annotate(total=Sum('amount')).order_by('-total')

    highest_consumption1 = get_highest_consumption(user_amount1)
    highest_consumption2 = get_highest_consumption(user_amount2)

    user_time1 = Access.objects.filter(beer=tap1_beer).values('user',
        'user__name', 'time').order_by('user', '-time')
    user_time2 = Access.objects.filter(beer=tap2_beer).values('user',
        'user__name', 'time').order_by('user', '-time')

    fastest_beer1 = get_fastest_beer(user_time1)
    fastest_beer2 = get_fastest_beer(user_time2)

    context = {
        'now': datetime.datetime.now(),
        'tap1_beer': tap1_beer,
        'tap2_beer': tap2_beer,
        'last_to_drink1': last_to_drink1,
        'last_to_drink2': last_to_drink2,
        'highest_consumption1': highest_consumption1,
        'highest_consumption2': highest_consumption2,
        'fastest_beer1': fastest_beer1,
        'fastest_beer2': fastest_beer2,
    }
    return render_to_response(
            'index.html', context,
            context_instance=RequestContext(request))


def get_highest_consumption(user_amount):
    highest_consumption = []
    max_amount = 0

    for amount in user_amount:
        if max_amount <= amount['total']:
            max_amount = amount['total']
            highest_consumption.append(amount)
        else:
            break

    return highest_consumption


def get_fastest_beer(user_time):
    user_accesses = []
    current_user = 0
    done_flg = True

    for access in user_time:
        if not current_user == access['user']:
            done_flg = False
            current_user = access['user']
            latest_time = access['time']
        elif current_user == access['user'] and not done_flg:
            time = latest_time - access['time']
            user_accesses.append({'user': access['user'], 'user__name': access['user__name'],
                'time': time})
            done_flg = True

    access = sorted(user_accesses, key=lambda access: access['time'])
    if access:
        return access[0]
    return None


def get_graph(request, tap_number):
    tap_beer = Beer.objects.get(tap_number=tap_number, active=True)
    tap_graph = get_graph_array(tap_beer)
    
    mimetype = 'application/javascript'
    data = json.dumps(tap_graph)
    return HttpResponse(data,mimetype)

def get_graph_array(beer):
        array = []
        select_data = {"d": "strftime('%%Y-%%m-%%dT%%H:00:00.000', time)"}
        tap_counts = Access.objects.filter(beer=beer).extra(select=select_data).values('d').annotate(Count('user')).order_by()    
        if tap_counts:
            for data in tap_counts:
                for k, v in data.iteritems():
                    if k == 'user__count':
                        array.append(v)
    
            return array
        else:
            pass

def get_tap(request, tap_number):
    tap_beer = Beer.objects.get(tap_number=tap_number, active=True)
    percent_left = tap_beer.percent_left()
        
    mimetype = 'application/javascript'
    data = json.dumps(percent_left)
    return HttpResponse(data,mimetype)

