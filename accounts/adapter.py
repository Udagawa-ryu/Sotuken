from allauth.account.adapter import DefaultAccountAdapter
from .models import *


class AccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, form, user, commit=True):
        """
        This is called when saving user via allauth registration.
        We override this to set additional data on user object.
        """
        from allauth.account.utils import user_email
        # Do not persist the user yet so we pass commit=False
        # (last argument
        user = super(AccountAdapter, self).save_user(
            request, user, form, commit=False)
        email = user.get('email')
        user_email(user, email)
        if 'password1' in user:
           user.set_password(user["password1"])
        user.username = user.get('username')
        user.MO1_homeCountry = user.get('MO1_homeCountry')
        user.MO1_language = user.get('MO1_language')
        user.MO1_openRange = user.get('MO1_openRange')
        user.save()