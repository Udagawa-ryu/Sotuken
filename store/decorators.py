from django.shortcuts import redirect,render
from .models import MO2_storer
    
    
def login_required_store(func):
    # お店のログイン
    def checker(request, *args, **kwargs):
        if request.session.get('store_login') == None:
            return redirect('store:storeLogin')
        else:
            c_email = request.COOKIES.get('store_login')
            return func(request,c_email, *args, **kwargs)
    return checker