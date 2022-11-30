from django.shortcuts import render
from django.views import generic
from .forms import *
# Create your views here.

# ブログ一覧画面
class BlogListView(generic.FormView):
    template_name = "BlogList.html"
    form = BlogRegisterForm
    def get_form_kwargs(self,request):
        user = self.request.user # formへ渡す変数
        kwargs = super(BlogRegisterForm, self).get_form_kwargs()
        kwargs.update({'user': user})
        return kwargs

# ブログ新規作成画面
class BlogRegisterView(generic.View):
    template_name = "BlogRegister.html"

# ブログ内容確認画面
class BlogConfirmationView(generic.View):
    template_name = "BlogConfirmation.html"

# ブログ登録完了画面
class BlogCompletionView(generic.View):
    template_name = "BlogCompletion.html"

# ブログ詳細画面
class BlogDetailView(generic.View):
    template_name = "BlogDetail.html"

# ブログ編集画面
class BlogEditView(generic.View):
    template_name = "BlogEdit.html"

# ブログ削除画面
class BlogDeleteView(generic.View):
    template_name = "BlogDelete.html"

# マイブログ公開範囲設定入力画面ん
class OpenRangeRegisterView(generic.View):
    template_name = "OpenRangeRegister.html"

# 他ユーザのブログ画面
class OtherBlogListView(generic.View):
    template_name = "OtherBlogList.html"