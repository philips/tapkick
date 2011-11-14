from django.template import RequestContext, Context, loader
from django.http import HttpResponse
from django.db.models import Sum
from datetime import timedelta
from beer.models import User
from beer.models import Access
from beer.models import Beer

def user_list(request):
    user_list = User.objects.all()
    t = loader.get_template('user_list.html')
    c = Context({
        'user_list': user_list,
    })
    return HttpResponse(t.render(c))

def user_detail(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    t = loader.get_template('user_detail.html')
    c = Context({
        'rfid': user.rfid,
        'name': user.name,
    })
    return HttpResponse(t.render(c))

def front_page(request):
    tap1_beer = Beer.objects.get(tap_number=1, active=True)
    tap2_beer = Beer.objects.get(tap_number=2, active=True)

    last_to_drink1 = get_last_to_drink(tap1_beer)
    last_to_drink2 = get_last_to_drink(tap2_beer)
    
    highest_consumption1 = get_highest_consumption(tap1_beer)
    highest_consumption2 = get_highest_consumption(tap2_beer)

    fastest_beer1 = get_fastest_beer(tap1_beer)
    fastest_beer2 = get_fastest_beer(tap2_beer)

    t = loader.get_template('index.html')
    c = RequestContext(request, {
        'tap1_beer': tap1_beer,
        'tap2_beer': tap2_beer,
        'last_to_drink1': last_to_drink1,
        'last_to_drink2': last_to_drink2,
        'highest_consumption1': highest_consumption1,
        'highest_consumption2': highest_consumption2,
        'fastest_beer1': fastest_beer1,
        'fastest_beer2': fastest_beer2,
    })
    return HttpResponse(t.render(c))

def get_last_to_drink(tap_beer):
    accesses = Access.objects.filter(beer=tap_beer).order_by('-time')
    if accesses:
        return accesses[0]
    else:
        return None
    

def get_highest_consumption(tap_beer):
    user_amount = Access.objects.filter(beer=tap_beer).values('user',
        'user__name').order_by('user').annotate(total=Sum('amount')).order_by('-total')
    highest_consumption = []
    max_amount = 0
    
    for amount in user_amount:
        if max_amount <= amount['total']:
            max_amount = amount['total']
            highest_consumption.append(amount)
        else:
            break

    if highest_consumption:
        return highest_consumption
    else:
        return None


def get_fastest_beer(tap_beer):
    user_time = Access.objects.filter(beer=tap_beer).values('user', 
        'user__name', 'time').order_by('user', '-time')
    user_accesses = []
    current_user = 0
    min_dif = timedelta.max.seconds

    for access in user_time:
        if not current_user == access['user']:
            current_user = access['user']
            prev_time = access['time']
        else:
            dif = (prev_time - access['time']).seconds
            if min_dif > dif:
                min_dif = dif
                time = '%s min %s sec' % (dif / 60, dif % 60)
                user_accesses.append({'user': access['user'], 
                    'user__name': access['user__name'], 'time': time, 'dif': dif})
            else:
                prev_time = access['time']

    if user_accesses:
        return sorted(user_accesses, key=lambda access: access['dif'])[0]
    else:
        return None

