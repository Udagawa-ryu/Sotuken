from django.shortcuts import render,redirect
from django.views import generic
from .forms import BlogRegisterForm
from accounts.models import CustomUser,MO6_Visit_record
from django.urls import reverse_lazy
from blog.models import MO7_Blog,MO10_Fav_Blog
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from samuraiwalk.settings_common import MEDIA_ROOT
import os
# Create your views here.

# 翻訳APIをインポート
from googletrans import Translator

# Translatorクラスのインスタンスを生成
translator = Translator()

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
        (1,'private'),
    }
    user = CustomUser.objects.get(MO1_userNumber=request.user.MO1_userNumber)
    my_record = MO6_Visit_record.objects.filter(MO1_userNumber=user)
    params = {"message":'',"form":None,"user":user}
    if request.method == 'POST':
        initial_data = {
            "MO1_userID":request.POST.get("MO1_userID"),
            "MO7_blogName":request.POST.get("MO7_blogName"),
            "MO7_blogText":request.POST.get("MO7_blogText"),
            "MO7_blogImage1":request.FILES.get("MO7_blogImage1"),
            "MO6_visitRecordNumber":request.POST.get("MO6_visitRecordNumber"),
            "MO7_openRange":request.POST.get("MO7_openRange"),
        }
        form = BlogRegisterForm(request.POST or initial_data, request.FILES)
        form.fields['MO6_visitRecordNumber'].queryset = my_record
        form.fields['MO7_openRange'].choices = CHOICE
        params = {
            'form':form,
            'message' : '',
        }
        if request.POST.get('next', '') == 'confirm':
            print(form)
            if form.is_valid():
                form.save()
                return redirect("blog:blogCompletion")
            else:
                for ele in form :
                    print(ele)
                params["message"] = "入力データが正しくありません"
                # print(form)
                return render(request,"BlogRegister.html",params)
    else :
        form = BlogRegisterForm()
        form.fields['MO6_visitRecordNumber'].queryset = my_record
        form.fields['MO7_openRange'].choices = CHOICE
        form.fields['MO7_openRange'].initial = user.MO1_openRange
        params['form'] = form
        return render(request,"BlogRegister.html",params)

# ブログ内容確認画面
def BlogConfirmation(request):
    user = CustomUser.objects.get(MO1_userNumber=request.user.MO1_userNumber)
    my_record = MO6_Visit_record.objects.filter(MO1_userNumber=user)
    CHOICE = {
        (0,'publish to the public'),
        (1,'private'),
    }
    if request.method == 'POST':
        initial_data = {
            "MO1_userID":request.POST.get("MO1_userID"),
            "MO7_blogName":request.POST.get("MO7_blogName"),
            "MO7_blogText":request.POST.get("MO7_blogText"),
            "MO7_blogImage1":request.FILES.get("MO7_blogImage1"),
            "MO6_visitRecordNumber":request.POST.get("MO6_visitRecordNumber"),
            "MO7_openRange":request.POST.get("MO7_openRange"),
        }
        v_recode = MO6_Visit_record.objects.get(MO6_visitRecordNumber=request.POST.get("MO6_visitRecordNumber"))
        form = BlogRegisterForm(request.POST or initial_data, request.FILES)
        form.fields['MO6_visitRecordNumber'].queryset = my_record
        form.fields['MO7_openRange'].choices = CHOICE
        params = {"message":'',"form":form,"user":user,"recode":v_recode}
        if request.POST.get('next', '') == 'confirm':
            img = request.FILES.get("MO7_blogImage1")
            if img is not None:
                static_paht = MEDIA_ROOT[0]
                file_paht = static_paht+"/"+str(user.MO1_userNumber)+"alias_img"
                os.makedirs(file_paht, exist_ok=True)
                file_name = str(user.MO1_userNumber)+"user.jpg"
                paht = os.path.join(file_paht, file_name)
                print("ここ",file_paht)
                with open(paht, "wb+") as f:
                    for chunk in img.chunks():
                        f.write(chunk)
            return render(request,"BlogConfirmation.html",params)
        if request.POST.get('next', '') == 'back':
            return render(request,"BlogRegister.html",params)
        if request.POST.get('next', '') == 'create':
            # img_path = MEDIA_ROOT[0]+"/"+str(user.MO1_userNumber)+"alias_img/"+str(user.MO1_userNumber)+"user.jpg"
            # print("ここ",img_path)
            # form.fields['MO7_blogImage1'] = open(img_path,"r")
            if form.is_valid():
                form.save()
                return redirect("blog:blogCompletion")
            else:
                for ele in form :
                    print(ele)
                params["message"] = "入力データが正しくありません"
                # print(form)
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
        blog = MO7_Blog.objects.get(MO7_blogNumber=self.kwargs['pk'])
        mydata = CustomUser.objects.get(MO1_userNumber = self.request.user.MO1_userNumber)
        context['blog'] = MO7_Blog.objects.filter(MO7_blogNumber=self.kwargs['pk'])
        img_list = list()
        if bool(blog.MO7_blogImage1) == True:
            img_paht = "/media/"+str(blog.MO7_blogImage1)
            img_list.append(img_paht)
        if bool(blog.MO7_blogImage2) == True:
            img_paht = "/media/"+str(blog.MO7_blogImage2)
            img_list.append(img_paht)
        if bool(blog.MO7_blogImage3) == True:
            img_paht = "/media/"+str(blog.MO7_blogImage3)
            img_list.append(img_paht)
        print(img_list)
        context['img'] = img_list
        context['login_user'] = self.request.user
        if MO10_Fav_Blog.objects.filter(MO7_blogNumber=blog.MO7_blogNumber,MO1_userNumber=mydata.MO1_userNumber).exists():
            fav = 1
        else:
            fav = 0
        context['fav'] = fav
        context['trans_name'] = translator.translate(str(blog.MO7_blogName),dest="en",str="auto").text
        context['trans_contents'] = translator.translate(str(blog.MO7_blogText),dest="en",str="auto").text
        # context['trans_recode'] = translator.translate(str(blog.MO6_visitRecordNumber),dest="en",str="auto").text
        return context

# ブログ編集画面
# class BlogEditView(generic.TemplateView):
#     template_name = "BlogEdit.html"

# class BlogEditView(LoginRequiredMixin, generic.UpdateView):
#     model = MO7_Blog
#     template_name = 'BlogEdit.html'

#     def visit_record(self):
#         form = BlogRegisterForm
#         my_record = MO6_Visit_record.objects.filter(MO1_userNumber=self.request.user)
#         form.fields['MO6_visitRecordNumber'].queryset = my_record
#         return form

#     form_class = 

#     def get_success_url(self,form):
#         my_record = MO6_Visit_record.objects.filter(MO1_userNumber=self.request.user)
#         form.fields['MO6_visitRecordNumber'].queryset = my_record
#         return reverse_lazy('blog:blogDetail', kwargs={'pk': self.kwargs['pk']})

#     def form_valid(self, form):
#         messages.success(self.request, 'ブログを更新しました。')
#         return super().form_valid(form)

#     def form_invalid(self, form):
#         messages.error(self.request, 'ブログの更新に失敗しました。')
#         return super().form_invalid(form)

def BlogEdit(request, pk):
    user = CustomUser.objects.get(MO1_userNumber=request.user.MO1_userNumber)
    my_record = MO6_Visit_record.objects.filter(MO1_userNumber=user)
    CHOICE = {
        (0,'publish to the public'),
        (1,'private'),
    }
    params = {"message":'',"form":None,"user":user}
    blog = MO7_Blog.objects.get(MO7_blogNumber=pk)
    if request.method == 'POST':
        initial_data = {
            "MO1_userID":request.POST.get("MO1_userID"),
            "MO7_blogName":request.POST.get("MO7_blogName"),
            "MO7_blogText":request.POST.get("MO7_blogText"),
            "MO7_blogImage1":request.FILES.get("MO7_blogImage1"),
            "MO7_blogImage2":request.FILES.get("MO7_blogImage2"),
            "MO7_blogImage3":request.FILES.get("MO7_blogImage3"),
            "MO6_visitRecordNumber":request.POST.get("MO6_visitRecordNumber"),
            "MO7_openRange":request.POST.get("MO7_openRange"),
        }
        if request.POST.get('next', '') == 'update':
            form = BlogRegisterForm(request.POST,request.FILES,instance=blog)
            form.fields['MO6_visitRecordNumber'].queryset = my_record
            form.fields['MO7_openRange'].choices = CHOICE
            print(form)
            if form.is_valid():
                form.save()
                if blog.MO7_openRange == 1:
                    fav = MO10_Fav_Blog.objects.filter(MO7_blogNumber=blog.MO7_blogNumber).delete()
                return redirect("blog:blogDetail", pk=pk)
            return render(request,"BlogEdit.html",params)
    else :
        # initial_dict = dict(MO1_userID=blog.MO1_userID,MO7_blogName=blog.MO7_blogName,MO7_blogText=blog.MO7_blogText,MO7_blogImage1=blog.MO7_blogImage1,MO7_blogImage2=blog.MO7_blogImage2,MO7_blogImage3=blog.MO7_blogImage3,MO6_visitRecordNumber=blog.MO6_visitRecordNumber,MO7_openRange=blog.MO7_openRange)
        form = BlogRegisterForm(instance=blog)
        form.fields['MO6_visitRecordNumber'].queryset = my_record
        form.fields['MO7_openRange'].choices = CHOICE
        params['form'] = form
        return render(request,"BlogEdit.html",params)

# ブログ削除画面
# class BlogDeleteView(generic.TemplateView):
#     template_name = "BlogDelete.html"

class BlogDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = MO7_Blog
    template_name = "BlogDelete.html"
    success_url = reverse_lazy('blog:blogList')

    def get_context_data(self, **kwargs):
        blog = MO7_Blog.objects.get(MO7_blogNumber=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context['blog'] = MO7_Blog.objects.filter(MO7_blogNumber=self.kwargs['pk'])
        img_list = list()
        if bool(blog.MO7_blogImage1) == True:
            img_paht = "/media/"+str(blog.MO7_blogImage1)
            img_list.append(img_paht)
        if bool(blog.MO7_blogImage2) == True:
            img_paht = "/media/"+str(blog.MO7_blogImage2)
            img_list.append(img_paht)
        if bool(blog.MO7_blogImage3) == True:
            img_paht = "/media/"+str(blog.MO7_blogImage3)
            img_list.append(img_paht)
        print(img_list)
        context['img'] = img_list

        return context

# マイブログ公開範囲設定入力画面
class OpenRangeRegisterView(generic.TemplateView):
    template_name = "OpenRangeRegister.html"

# 他ユーザのブログ画面
# class OtherBlogListView(generic.TemplateView):
#     template_name = "OtherBlogList.html"

class OtherBlogListView(LoginRequiredMixin, generic.ListView):
    model = MO7_Blog
    template_name = "OtherBlogList.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = CustomUser.objects.get(MO1_userNumber=self.kwargs['pk'])
        user_or = user.MO1_openRange
        if user_or == 0:
            context['blogs'] = MO7_Blog.objects.filter(MO1_userID=user,MO7_openRange=0).order_by('-MO7_createDate')
        return context

@login_required
def FavBlog(request,pk):
    if request.method == 'POST':
        page_blog = MO7_Blog.objects.get(MO7_blogNumber = pk)
        mydata = CustomUser.objects.get(MO1_userNumber = request.user.MO1_userNumber)
        result, created = MO10_Fav_Blog.objects.get_or_create(MO7_blogNumber = page_blog,MO1_userNumber=mydata)
        if created :
            return redirect("blog:blogDetail", pk=pk)
        else:
            result.delete()
            return redirect("blog:blogDetail", pk=pk)
    return redirect("blog:blogDetail", pk=pk)