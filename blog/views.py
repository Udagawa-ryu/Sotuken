from django.shortcuts import render
from django.views import generic
from .forms import *
from accounts.models import CustomUser
# Create your views here.

# ブログ一覧画面
class BlogListView(generic.FormView):
    template_name = "BlogList.html"

# ブログ新規作成画面
class BlogRegisterView(generic.View):
    template_name = "BlogRegister.html"
    form_class = BlogRegisterForm
    def get(self, request, *args, **kwargs):
        params = {"message":'',}
        user = CustomUser.object.get(MO1_userNumber=request.user.MO1_userNumber)
        form = self.form_class()
        my_record = MO6_Visit_record.objects.filter(MO1_userNumber=user)
        form.fields['category'].queryset = my_record
        return render(request,"BlogList.html",)


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