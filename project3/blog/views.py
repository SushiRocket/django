from django.db.models import Q
from django.shortcuts import get_object_or_404,redirect
from django.views import generic
from .forms import CommentCreateForm
from .models import Post,Category,Comment


class IndexView(generic.ListView):
    model = Post
    paginate_by = 1

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
        
        #category = get_object_or_404(Category,pk=self.kwargs['pk'])
        #queryset = Post.objects.order_by('-created_at').filter(category=category)
        

        category_pk = self.kwargs['pk']
        queryset = Post.objects.order_by('-created_at').filter(category__pk=category_pk)
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
        return redirect ('blog:detail',pk=post_pk)