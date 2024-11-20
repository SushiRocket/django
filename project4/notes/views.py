from django.db.models import Q
from django.shortcuts import get_object_or_404,redirect,render
from django.views import generic,View
from django.views.generic import TemplateView
from.forms import CommentCreateForm,ContactForm
from .models import Post,Category,Comment
from django.core.mail import send_mail


class IndexView(generic.ListView):
    model = Post
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Post.objects.order_by('-created_at')
        keyword = self.request.GET.get('keyword')
        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword)|Q(text__icontains=keyword)
            )
        return queryset
    
class CategoryView(generic.ListView):
    model = Post
    paginate_by = 10

    def get_queryset(self):
        category = get_object_or_404(Category,pk=self.kwargs['pk'])
        queryset = Post.objects.order_by('-created_at').filter(category=category)
        return queryset
    
class DetailView(generic.DetailView):
    model = Post

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
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            send_mail(
                '新しいお問い合わせ',
                f'名前: {name}\nメールアドレス: {email}\nメッセージ: {message}',
                email,
                ['support@example.com'],
                fail_silently=False,
            )

            return redirect('notes/contact_success.html')

        else:
            form = ContactForm()

            return render(request, 'notes/contact_form.html', {'form': form})