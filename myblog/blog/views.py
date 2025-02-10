
from django.shortcuts import render
from blog.models import Post
from django.http import Http404
from django.shortcuts import get_object_or_404 
from django.views.generic import ListView, DetailView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
        # Постраничная разбивка с 3 постами на страницу
    paginator = Paginator(post_list, 2  )
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.get_page(page_number)
    except PageNotAnInteger:
        posts = paginator.get_page(1)
    except EmptyPage:
        posts = paginator.get_page(paginator.num_pages)
        
    
   
    return render(request, 'blog/post/list.html', {'posts': posts, 'tag': tag})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'blog/post/list.html'
    
    
        
def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status = Post.Status.PUBLISCHED,
        slug = post,
        publish__year = year, publish__month = month, publish__day = day
    )
    # Список активных коментариев к этому посту
    comments = post.comments.filter(active=True)
    # Форма для коментирования пользователями
    form = CommentForm()
    return render(request, 'blog/post/detail.html', {'post':post, 'form':form, 'comments':comments})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(
        Post,
        id = post_id,
        status = Post.Status.PUBLISCHED
    )
    comment = None
    
    # коментарий был отправлен
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Создать обект класса Comment но не сохранять его
        comment = form.save(commit=False)
        # назначить пост коментарию
        comment.post = post
        # Сохранить коментарий в базе данных
        comment.save()
    return render(request, 'blog/post/comment.html', {'post': post, 'comment':comment, 'form': form})



"""
def post_list(request):
    post_list = Post.published.all()
   #posts = Post.published.all()
   #постраничная  разбивка с 3 постами на страницу
    paginator = Paginator(Post.published.all(), 2)
    page_number = request.GET.get('page')
    
    posts = paginator.get_page(page_number)
        
    
    return render(request, 'blog/post/list.html', {'posts': posts,  'post_list':  post_list})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status = Post.Status.PUBLISCHED,
        slug = post, publish__year = year, publish__month = month, publish__day = day
    )
    return render(request, 'blog/post/detail.html', {'post':post})


    применение функции сокращенного доступа
       get_object_or_404() она эквивалентна функции ниже
    

#def post_detail(request, id):
#    try:
#        post = Post.published.get(id=id)
#    except Post.DoesNotExist:
#        raise Http404("No Post found.")
#    return render(request, 'blog/post/detail.html', {'post':post})

"""


def post_schare(request, post_id):
    # извлечь пост по индификатору
    
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISCHED)
    sent = False
    
    if request.method =='POST':
        # форма была передана на обработку
        form = EmailPostForm(request.POST)
        if form.is_valid():
        # Поля формы прошли успешно валидацию
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = (
                f"{cd['name']} recommends you read "
                f"{post.title}"
            )
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}\'s comments:{cd['comments']}"
            )
            send_mail(
                subject,
                message,
                'ted20121983@gmail.com',
                [cd['to']]
            )
            sent = True
        # /// отправить электронное письмо
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form , 'sent': sent})

