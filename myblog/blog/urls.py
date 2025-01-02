
from django.urls import path, include
from . import views




blog_patterns = (
[
    path('blog/', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
],
'blog',
) 

urlpatterns = [
    path("", include(blog_patterns)),
]