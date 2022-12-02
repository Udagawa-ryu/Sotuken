from django.shortcuts import render,redirect
from django.views import generic
from .forms import BlogRegisterForm
from accounts.models import CustomUser,MO6_Visit_record
from django.urls import reverse_lazy
# Create your views here.

# ブログ一覧画面
class BlogListView(generic.TemplateView):
    template_name = "BlogList.html"

# ブログ新規作成画面
class BlogRegisterView(generic.CreateView):
    template_name = "BlogRegister.html"
    form_class = BlogRegisterForm
    model = MO6_Visit_record
    success_url = reverse_lazy('blog:blogList')
    def get_form(self,form_class=None):
        form = super().get_form(form_class=form_class)
        CHOICE = {
            (0,'OPEN'),
            (1,'HIDDEN'),
        }
        user = CustomUser.objects.get(MO1_userNumber=self.request.user.MO1_userNumber)
        my_record = MO6_Visit_record.objects.filter(MO1_userNumber=user)
        form.fields['MO6_visitRecordNumber'].queryset = my_record
        form.fields['MO7_openRange'].choices = CHOICE
        return form

    def form_valid(self, form):
        params = {'message':'','form': form}
        if self.request.POST.get('next', '') == 'confirm':
            return render(self.request,"BlogConfirmation.html",params)
        if self.request.POST.get('next', '') == 'back':
            return render(self.request,"BlogRegister.html",params)
        if self.request.POST.get('next', '') == 'create':
            return super().form_valid(form)
        else:
            # 正常動作ではここは通らない。エラーページへの遷移でも良い
            return redirect(reverse_lazy('base:top'))
# def BlogRegisterView(request):
#     CHOICE = {
#         (0,'OPEN'),
#         (1,'HIDDEN'),
#     }
#     params = {"message":'初期メッセージ',"form":None}
#     user = CustomUser.objects.get(MO1_userNumber=request.user.MO1_userNumber)
#     my_record = MO6_Visit_record.objects.filter(MO1_userNumber=user)
#     if request.method == 'POST':
#         print(request.POST)
#         post_form = BlogRegisterForm(request.POST)
#         post_form.fields['MO6_visitRecordNumber'].queryset = my_record
#         post_form.fields['MO7_openRange'].choices = CHOICE
#         if post_form.is_valid():
#             params['form'] = post_form
#             params['message'] = "Please check your entries"
#             if request.POST.get('next', '') == 'confirm':
#                 return render(request,"BlogConfirmation.html",params)
#             if request.POST.get('next', '') == 'back':
#                 return render(request,"BlogRegister.html",params)
#             if request.POST.get('next', '') == 'create':
#                 post_form.save()
#                 return redirect("BlogList.html")
#         else:
#             params['form'] = post_form
#             print(post_form)
#             params['message'] = '再入力して下さい'
#             return render(request, 'BlogRegister.html', params)
#     else :
#         form = BlogRegisterForm()
#         form.fields['MO6_visitRecordNumber'].queryset = my_record
#         form.fields['MO7_openRange'].choices = CHOICE
#         params['form'] = form
#         return render(request,"BlogRegister.html",params)
    


# ブログ内容確認画面
class BlogConfirmationView(generic.TemplateView):
    template_name = "BlogConfirmation.html"

# ブログ登録完了画面
class BlogCompletionView(generic.TemplateView):
    template_name = "BlogCompletion.html"

# ブログ詳細画面
class BlogDetailView(generic.TemplateView):
    template_name = "BlogDetail.html"

# ブログ編集画面
class BlogEditView(generic.TemplateView):
    template_name = "BlogEdit.html"

# ブログ削除画面
class BlogDeleteView(generic.TemplateView):
    template_name = "BlogDelete.html"

# マイブログ公開範囲設定入力画面
class OpenRangeRegisterView(generic.TemplateView):
    template_name = "OpenRangeRegister.html"

# 他ユーザのブログ画面
class OtherBlogListView(generic.TemplateView):
    template_name = "OtherBlogList.html"