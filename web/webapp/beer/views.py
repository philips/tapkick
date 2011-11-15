from django.template import RequestContext, Context, loader
from django.http import HttpResponse
from django.db.models import Sum
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
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise Http404
    t = loader.get_template('user_detail.html')
    c = Context({
        'rfid': user.rfid,
        'name': user.name,
    })
    return HttpResponse(t.render(c))

def front_page(request):
    tap1_beer = Beer.objects.get(tap_number=1, active=True)
    tap2_beer = Beer.objects.get(tap_number=2, active=True)

    last_to_drink1 = Access.objects.filter(beer=tap1_beer).order_by('-time')[0]
    last_to_drink2 = Access.objects.filter(beer=tap2_beer).order_by('-time')[0]
    
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

    return sorted(user_accesses, key=lambda access: access['time'])[0]
        

