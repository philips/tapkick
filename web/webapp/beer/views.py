from django.template import Context, loader
from django.http import HttpResponse
from beer.models import User

def user_index(request):
    user_list = User.objects.all()
    t = loader.get_template('user_index.html')
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
