# Imoirt Pagination staf
from django.core.paginator import Paginator

from django.core.paginator import Paginator, PageNotAnInteger
from django.shortcuts import render
from blog.models import Post
from django.http import Http404
from django.shortcuts import get_object_or_404 


def post_list(request):
    # post_list = Post.published.all()
    
    post_list = Post.published.all()
   #posts = Post.published.all()
   #постраничная  разбивка с 3 постами на страницу
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page')
    
    try:
        
        posts = paginator.page(page_number)
        
    except PageNotAnInteger:
        
        posts =paginator.page(1)
    
    return render(request, 'blog/post/list.html', {'posts': posts})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status = Post.Status.PUBLISCHED,
        slug = post, publish__year = year, publish__month = month, publish__day = day
    )
    return render(request, 'blog/post/detail.html', {'post':post})


    """применение функции сокращенного доступа
       get_object_or_404() она эквивалентна функции ниже
    """

#def post_detail(request, id):
#    try:
#        post = Post.published.get(id=id)
#    except Post.DoesNotExist:
#        raise Http404("No Post found.")
#    return render(request, 'blog/post/detail.html', {'post':post})
