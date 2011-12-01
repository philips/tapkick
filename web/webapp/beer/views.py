import datetime
import json
import md5

from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models import Count, Sum
from beer.models import User, Beer, Access
from beer.forms import SearchForm, UserForm

def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            user = form.user()
            return HttpResponseRedirect(reverse(user_edit,
                       args=[user.rfid]))
    else:
        form = SearchForm() # An unbound form

    return render_to_response('search.html', {
        'form': form,
        }, context_instance=RequestContext(request))

def user_edit(request, rfid_id):
    if request.method == 'POST':
        user = User.objects.get(rfid=rfid_id)
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect(reverse(search))

    user = get_object_or_404(User, rfid=rfid_id, private=False)
    context = {'user': user}
    return render_to_response(
            'user_edit.html', context,
            context_instance=RequestContext(request))

def user_list(request):
    user_list = User.objects.filter(private=False)
    context = {
        'user_list': user_list,
    }
    return render_to_response(
            'user_list.html', context,
            context_instance=RequestContext(request))


def user_detail(request, rfid_id):
    user = get_object_or_404(User, rfid=rfid_id, private=False)
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
        'user__name', 'user__email').order_by('user').annotate(total=Sum('amount')).order_by('-total')
    user_amount2 = Access.objects.filter(beer=tap2_beer).values('user',
        'user__name', 'user__email').order_by('user').annotate(total=Sum('amount')).order_by('-total')

    highest_consumption1 = get_highest_consumption(user_amount1)
    highest_consumption2 = get_highest_consumption(user_amount2)

    user_time1 = Access.objects.filter(beer=tap1_beer).values('user',
        'user__name', 'user__email', 'time').order_by('user', '-time')
    user_time2 = Access.objects.filter(beer=tap2_beer).values('user',
        'user__name', 'user__email', 'time').order_by('user', '-time')

    fastest_beer1 = get_fastest_beer(user_time1)
    fastest_beer2 = get_fastest_beer(user_time2)

    now = datetime.datetime.now()

    # This step is needed in order to use the "timesince" templatetag
    if fastest_beer1:
        fastest_beer1['time'] = now - fastest_beer1['time']
    if fastest_beer2:
        fastest_beer2['time'] = now - fastest_beer2['time']

    context = {
        'now': now,
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

    if highest_consumption:
        return highest_consumption[0]
    return None


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
            user_accesses.append({
                'user': access['user'],
                'user__name': access['user__name'],
                'user__email': access['user__email'],
                'time': time})
            done_flg = True

    access = sorted(user_accesses, key=lambda access: access['time'])
    if access:
        return access[0]
    return None

# For ajax(json) #
def json_response(data, code=200, mimetype='application/json'):
    resp = HttpResponse(data, mimetype)
    resp.code = code
    return resp

# values, total
def get_graph(request, tap_number):
    tap_beer = get_object_or_404(Beer, tap_number=tap_number, active=True)
    tap_graph = get_graph_array(tap_beer)
    user_list = Access.objects.filter(beer=tap_beer).values('user').annotate(Count('user')).order_by()
    result = {
        'values': tap_graph,
        'total': len(user_list)}
    data = json.dumps(result)
    return json_response(data)


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

# level, name, amout_left, age, volume, ibu, abv
def get_tap(request, tap_number):
    tap_beer = get_object_or_404(Beer, tap_number=tap_number, active=True)
    now = datetime.datetime.now()
    age = (now - tap_beer.start_date).days
    if age > -1:
        if age == 1:
            age_string = "1 day"
        else:
            age_string = "%s days" % age
    else:
        age_string = "0 days"
    volume = '%s/%sL' % (tap_beer.amount_left, tap_beer.size)
    result = {
        'level': tap_beer.percent_left(),
        'name': tap_beer.name,
        'amountLeft': tap_beer.cups_left(),
        'age': age_string,
        'volume': volume,
        'ibu': tap_beer.ibu,
        'abv': tap_beer.abv}
     
    data = json.dumps(result)
    return json_response(data)

# name, time, gravitar_url
def get_last(request, tap_number):
    tap_beer = get_object_or_404(Beer, tap_number=tap_number, active=True)
    drinker_list_tap = Access.objects.filter(beer=tap_beer).order_by('-time')
    result = {}
    if drinker_list_tap:
        last_to_drink = drinker_list_tap[0]
        now = datetime.datetime.now()
        time = now - last_to_drink.time
        time = get_formatted_date(time) + ' ago'
        result = {
            'name': last_to_drink.user.name,
            'time': time,
            'email': get_url_of_gravitar(last_to_drink.user.email)}
    data = json.dumps(result)
    return json_response(data)

# name, amount, gravitar_url
def get_highest(request, tap_number):
    tap_beer = get_object_or_404(Beer, tap_number=tap_number, active=True)
    users = Access.objects.filter(beer=tap_beer).values('user', 'user__name',
        'user__email').order_by('user').annotate(total=Sum('amount')).order_by('-total')
    highest_user = get_highest_consumption(users)
    result = {}
    if highest_user:
        result = {
            'name': highest_user['user__name'],
            'amount': '%s L' % highest_user['total'],
            'email': get_url_of_gravitar(highest_user['user__email'])}
    data = json.dumps(result)
    return json_response(data)

# name, time, gravitar_url
def get_fastest(request, tap_number):
    tap_beer = get_object_or_404(Beer, tap_number=tap_number, active=True)
    user_time = Access.objects.filter(beer=tap_beer).values('user',
        'user__name', 'user__email', 'time').order_by('user', '-time')
    fastest_beer = get_fastest_beer(user_time)

    result = {}
    if fastest_beer:
        time = get_formatted_date(fastest_beer['time'])
        result = {
            'name': fastest_beer['user__name'],
            'time': time,
            'email': get_url_of_gravitar(fastest_beer['user__email'])}
    data = json.dumps(result)
    return json_response(data)


def get_url_of_gravitar(email):
    return 'http://www.gravatar.com/avatar/' + md5.new(email).hexdigest() + '.jpg?s=40'


def get_formatted_date(date):
    days = date.days
    day = days % 7
    week = days / 7
    seconds = date.seconds
    min = seconds / 60 % 60
    hour = seconds / 60 / 60
    formatted_date = ''
    if week != 0:
        if week == 1:
            formatted_date = formatted_date + '%s week, ' % week
        else:
            formatted_date = formatted_date + '%s weeks, ' % week
    if day != 0:
        if day == 1:
            formatted_date = formatted_date + '%s day, ' % day
        else:
            formatted_date = formatted_date + '%s days, ' % day
    if hour != 0:
        if hour == 1:
            formatted_date = formatted_date + '%s hour, ' % hour
        else:
            formatted_date = formatted_date + '%s hours, ' % hour
    if min != 0:
        if min == 1:
            formatted_date = formatted_date + '%s min ' % min
        else:
            formatted_date = formatted_date + '%s mins ' % min
    else:
        formatted_date = formatted_date + '0 mins'

    return formatted_date
