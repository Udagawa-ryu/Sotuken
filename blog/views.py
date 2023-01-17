from django.shortcuts import render,redirect
from django.views import generic
from .forms import BlogRegisterForm
from accounts.models import CustomUser,MO6_Visit_record
from django.urls import reverse_lazy
from blog.models import MO7_Blog
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
# Create your views here.

# ブログ一覧画面
class BlogListView(LoginRequiredMixin, generic.ListView):
    model = MO7_Blog
    template_name = "BlogList.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blogs'] = MO7_Blog.objects.filter(MO1_userID=self.request.user).order_by('-MO7_createDate')
        return context

# ブログ新規作成画面
# class BlogRegisterView(generic.CreateView):
#     template_name = "BlogRegister.html"
#     form_class = BlogRegisterForm
#     model = MO6_Visit_record
#     success_url = reverse_lazy('blog:blogList')
#     def get_form(self,form_class=None):
#         form = super().get_form(form_class=form_class)
#         CHOICE = {
#             (0,'OPEN'),
#             (1,'HIDDEN'),
#         }
#         user = CustomUser.objects.get(MO1_userNumber=self.request.user.MO1_userNumber)
#         my_record = MO6_Visit_record.objects.filter(MO1_userNumber=user)
#         form.fields['MO6_visitRecordNumber'].queryset = my_record
#         form.fields['MO7_openRange'].choices = CHOICE
#         return form

#     def form_valid(self, form):
#         params = {'message':'','form': form}
#         if self.request.POST.get('next', '') == 'confirm':
#             return render(self.request,"BlogConfirmation.html",params)
#         if self.request.POST.get('next', '') == 'back':
#             return render(self.request,"BlogRegister.html",params)
#         if self.request.POST.get('next', '') == 'create':
#             return super().form_valid(form)
#         else:
#             # 正常動作ではここは通らない。エラーページへの遷移でも良い
#             return redirect(reverse_lazy('base:top'))


def BlogRegister(request):
    CHOICE = {
        (0,'publish to the public'),
        (1,'publish only default spots'),
        (2,'private'),
    }
    user = CustomUser.objects.get(MO1_userNumber=request.user.MO1_userNumber)
    my_record = MO6_Visit_record.objects.filter(MO1_userNumber=user)
    params = {"message":'初期メッセージ',"form":None,"user":user}
    if request.method == 'POST':
        initial_data = {
            "MO1_userID":request.POST.get("MO1_userID"),
            "MO7_blogName":request.POST.get("MO7_blogName"),
            "MO7_blogText":request.POST.get("MO7_blogText"),
            "MO6_visitRecordNumber":request.POST.get("MO6_visitRecordNumber"),
            "MO7_openRange":request.POST.get("MO7_openRange"),
        }
        form = BlogRegisterForm(request.POST or initial_data)
        form.fields['MO6_visitRecordNumber'].queryset = my_record
        form.fields['MO7_openRange'].choices = CHOICE
        params = {
            'form':form,
            'message' : '',
        }
        return render(request, 'BlogRegister.html', params)
    else :
        form = BlogRegisterForm()
        form.fields['MO6_visitRecordNumber'].queryset = my_record
        form.fields['MO7_openRange'].choices = CHOICE
        params['form'] = form
        return render(request,"BlogRegister.html",params)
    


# ブログ内容確認画面
def BlogConfirmation(request):
    user = CustomUser.objects.get(MO1_userNumber=request.user.MO1_userNumber)
    my_record = MO6_Visit_record.objects.filter(MO1_userNumber=user)
    CHOICE = {
        (0,'publish to the public'),
        (1,'publish only default spots'),
        (2,'private'),
    }
    if request.method == 'POST':
        initial_data = {
            "MO1_userID":request.POST.get("MO1_userID"),
            "MO7_blogName":request.POST.get("MO7_blogName"),
            "MO7_blogText":request.POST.get("MO7_blogText"),
            "MO6_visitRecordNumber":request.POST.get("MO6_visitRecordNumber"),
            "MO7_openRange":request.POST.get("MO7_openRange"),
        }
        form = BlogRegisterForm(request.POST or initial_data)
        form.fields['MO6_visitRecordNumber'].queryset = my_record
        form.fields['MO7_openRange'].choices = CHOICE
        params = {"message":'',"form":form,"user":user}
        if request.POST.get('next', '') == 'confirm':
            return render(request,"BlogConfirmation.html",params)
        if request.POST.get('next', '') == 'back':
            return render(request,"BlogRegister.html",params)
        if request.POST.get('next', '') == 'create':
            if form.is_valid():
                form.save()
                return redirect("blog:blogCompletion")
            else:
                params["message"] = "入力データが正しくありません"
                print(form)
                return render(request,"BlogRegister.html",params)
        else:
            # 正常動作ではここは通らない。エラーページへの遷移でも良い
            return redirect(reverse_lazy('base:top'))
    return redirect("blog:blogRegister")

# ブログ登録完了画面
class BlogCompletionView(generic.TemplateView):
    template_name = "BlogCompletion.html"

# ブログ詳細画面
# class BlogDetailView(generic.TemplateView):
#     template_name = "BlogDetail.html"

class BlogDetailView(LoginRequiredMixin, generic.DetailView):
    model = MO7_Blog
    template_name = "BlogDetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blog'] = MO7_Blog.objects.filter(MO7_blogNumber=self.kwargs['pk'])
        return context

# ブログ編集画面
# class BlogEditView(generic.TemplateView):
#     template_name = "BlogEdit.html"

class BlogEditView(LoginRequiredMixin, generic.UpdateView):
    model = MO7_Blog
    template_name = 'BlogEdit.html'
    form_class = BlogRegisterForm
    def visit_recode(request):
        user = CustomUser.objects.get(MO1_userNumber=request.user.MO1_userNumber)
        my_record = MO6_Visit_record.objects.filter(MO1_userNumber=user)
        form = BlogRegisterForm()
        form.fields['MO6_visitRecordNumber'].queryset = my_record
        return 

    def get_success_url(self):
        return reverse_lazy('blog:blogDetail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        messages.success(self.request, 'ブログを更新しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'ブログの更新に失敗しました。')
        return super().form_invalid(form)

# ブログ削除画面
# class BlogDeleteView(generic.TemplateView):
#     template_name = "BlogDelete.html"

class BlogDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = MO7_Blog
    template_name = "BlogDelete.html"
    success_url = reverse_lazy('blog:blogList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blog'] = MO7_Blog.objects.filter(MO7_blogNumber=self.kwargs['pk'])
        return context

# マイブログ公開範囲設定入力画面
class OpenRangeRegisterView(generic.TemplateView):
    template_name = "OpenRangeRegister.html"

# 他ユーザのブログ画面
# class OtherBlogListView(generic.TemplateView):
#     template_name = "OtherBlogList.html"

class OtherBlogListView(LoginRequiredMixin, generic.DetailView):
    model = MO7_Blog
    template_name = "OtherBlogList.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blog'] = MO7_Blog.objects.filter(MO7_blogNumber=self.kwargs['pk'])
        print(context['blog'])
        return context