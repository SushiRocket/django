from django.db.models import Q,Count
from django.shortcuts import get_object_or_404,redirect,render
from django.views import generic,View
from django.views.generic import TemplateView
from.forms import CommentCreateForm,ContactForm
from .models import Post,Category,Comment,Like
from django.core.mail import send_mail
import random
from.forms import SignUpForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib.auth.views import LogoutView,LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from taggit.models import Tag
from django.contrib.contenttypes.models import ContentType

class IndexView(generic.ListView):
    model = Post
    paginate_by = 10
    context_object_name = 'post_list'


    def get_queryset(self):
        queryset = Post.objects.order_by('-created_at')
        keyword = self.request.GET.get('keyword')
        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword)|Q(text__icontains=keyword)
            )

        return queryset

    def get_context_data(self, **kwargs):
        # 親クラスのcontextを取得
        context = super().get_context_data(**kwargs)

        # タグの取得
        post_list = context['post_list']
        post_ids = post_list.values_list('id', flat=True)
        post_content_type = ContentType.objects.get_for_model(Post)

        context['tags'] = Tag.objects.filter(
            taggit_taggeditem_items__content_type=post_content_type,
            taggit_taggeditem_items__object_id__in=post_ids
        ).distinct()

        # ピックアップ記事を取得（ランダムに3件選ぶ）
        all_pickups = list(Post.objects.order_by('-created_at')[:10])  # 最新10件をリストに変換
        random_pickups = random.sample(all_pickups, min(len(all_pickups), 3))  # ランダムに3件選択
        context['pickups'] = random_pickups

        user = self.request.user
        if user.is_authenticated:
            liked_posts = Like.objects.filter(user=user).values_list('post_id', flat=True)
            context['liked_posts'] = liked_posts
        else:
            context['liked_posts'] = []

        ranked_posts = Post.objects.annotate(likes_count=Count('likes')).order_by('-likes_count') #(<新しいフィールド名>=<計算式>)
        context['ranked_posts'] = ranked_posts

        return context

class CategoryView(generic.ListView):
    model = Post
    paginate_by = 10
    template_name = 'notes/category.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        category = get_object_or_404(Category,pk=self.kwargs['pk'])
        queryset = Post.objects.order_by('-created_at').filter(category=category)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category = get_object_or_404(Category, pk=self.kwargs['pk'])
        context['category'] = category

        all_pickups = list(Post.objects.order_by('-created_at')[:10])
        random_pickups = random.sample(all_pickups, min(len(all_pickups), 3))
        context['pickups'] = random_pickups

        context['ranked_posts'] = Post.objects.annotate(likes_count=Count('likes')).order_by('-likes_count')[:3]

        context['all_categories'] = Category.objects.all()

        user = self.request.user
        if user.is_authenticated:
            liked_posts = Like.objects.filter(user=user).values_list('post_id', flat=True)
            context['liked_posts'] = list(liked_posts)
        else:
            context['liked_posts'] = []

        context['current_sort'] = self.request.GET.get('sort', 'created_at')

        return context

class TaggedPostView(generic.ListView):
    model = Post
    paginate_by = 10
    context_object_name = 'post_list'
    template_name = 'notes/post_tagged.html'

    def get_queryset(self):

        #URLパラメータからタグのスラッグを取得し、そのタグに関連する投稿をフィルタリングします。
        self.tag = get_object_or_404(Tag, pk=self.kwargs['pk'])
        queryset = Post.objects.filter(tags__pk=self.tag.pk).order_by('-created_at').select_related('category').prefetch_related('tags')
        return queryset

    def get_context_data(self, **kwargs):

        #コンテキストデータにタグ情報を追加します。
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        context['tags'] = Tag.objects.all()
        # 他に必要なコンテキストデータがあればここに追加
        return context

class DetailView(generic.DetailView):
    model = Post

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        post = self.get_object()
        post.views += 1
        post.save()
        return response

class CommentView(generic.CreateView):
    model = Comment
    form_class = CommentCreateForm

    def form_valid(self,form):
        post_pk = self.kwargs['post_pk']
        comment = form.save(commit=False)
        comment.post = get_object_or_404(Post,pk=post_pk)
        comment.save()
        return redirect('notes:detail',pk=post_pk)

class AboutView(TemplateView):
    template_name = 'notes/about.html'


class ContactView(View):
    def get(self,request):
        form = ContactForm()
        return render(request, 'notes/contact_form.html', {'form':form})

    def post(self,request):
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            company = form.cleaned_data.get('company','')
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            return render(request,'notes/contact_confirm.html', {
                'form': form,
                'name': name,
                'company':company,
                'email': email,
                'message': message,
            })

        else:
            form = ContactForm()

            return render(request, 'notes/contact_form.html', {'form': form})

class ContactConfirmView(View):
    def post(self, request):
        # 確認画面で「送信」ボタンが押されたときの処理
        name = request.POST.get('name')
        company = request.POST.get('company','')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # メール送信処理
        send_mail(
            '新しいお問い合わせ',
            f'名前: {name}\nメールアドレス: {email}\nメッセージ: {message}',
            email,
            ['kentamori27@gmail.com'],  # 宛先
            fail_silently=False,
        )

        # 送信後に完了画面へリダイレクト
        return redirect('notes:contact_success')

class ContactSuccessView(TemplateView):
    template_name = 'notes/contact_success.html'

class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'notes/signup.html'

class LikeToggleView(LoginRequiredMixin,View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        user = request.user

        # 既に「いいね」しているか確認
        like, created = Like.objects.get_or_create(post=post, user=user)

        if not created:
            # 「いいね」を解除
            like.delete()
            result = 'unliked'
        else:
            # 「いいね」を追加
            result = 'liked'

        # 最新の「いいね」数を取得
        likes_count = post.likes_count()

        return JsonResponse({'result': result, 'likes_count': likes_count})

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('notes:index')

class CustomLoginView(LoginView):
    template_name = 'notes/login.html'
    authentication_form = AuthenticationForm

    def form_valid(self, form):

        messages.success(self.request, 'ログインに成功しました！')

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('notes:index')