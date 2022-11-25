from django.shortcuts import render
from django.views import generic
from .models import *
from .froms import *
# Create your views here.

class IndexView(generic.TemplateView):
    template_name= "index.html"


def storeRequest(request):
    params = {'message': '仮登録が完了しました。メールが届くまでお待ちください。', 'form': None,}
    if request.method == 'POST':
        form = StoreCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'StoreLogin.html', params)
        else:
            params['message'] = '再入力して下さい'
            params['form'] = form
    else:
        params['form'] =  StoreCreateForm(request.POST)
        params['message'] = ''
    return render(request, 'StoreRequest.html', params)

