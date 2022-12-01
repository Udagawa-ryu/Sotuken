from django.shortcuts import redirect,render
from .models import MO2_store
    
    
def login_required_store(func):
    # お店のログイン
    def checker(request, *args, **kwargs):
        if request.session.get('storeLogin') == None:
            return redirect('store:storeLogin')
        else:
            c_email = request.session['storeLogin']
            return func(request,c_email, *args, **kwargs)
    return checker