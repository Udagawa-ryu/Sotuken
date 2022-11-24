from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _
from .models import CustomUser
  
  
# class MyUserChangeForm(UserChangeForm):
#     class Meta:
#         model = CustomUser
#         fields = '__all__'
# class MyUserCreationForm(UserCreationForm):
#     class Meta:
#         model = CustomUser
#         fields = ('email', 'MO1_userName','password','MO1_userID' ,
#                             'MO1_homeCountry','MO1_language','MO1_openRange','MO1_point')

# class MyUserAdmin(UserAdmin):
#     fieldsets = (
#         (None, {'fields': ('email', 'MO1_userName','password','MO1_userID' ,
#                             'MO1_homeCountry','MO1_language','MO1_openRange','MO1_point')}),
#         (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email'),
#         }),
#     )
#     form = MyUserChangeForm
#     add_form = MyUserCreationForm
#     list_display = ('MO1_userNumber','email', 'MO1_userName', 'is_staff')
#     list_filter = ('is_staff', 'is_superuser', 'is_active')
#     search_fields = ('email', 'MO1_userName')
#     ordering = ('email',)
  
admin.site.register(CustomUser)