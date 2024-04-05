from django.shortcuts import render
from .models import Post
from django.http import JsonResponse
from .forms import PostForm
from profiles.models import Profile
# from django.core import serializers
# Create your views here.

def post_list_and_create(request):
    form = PostForm(request.POST or None)
    # qs = Post.objects.all()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if form.is_valid():
            author = Profile.objects.get(user=request.user)
            instance = form.save(commit=False)
            instance.author = author
            instance.save()
            data = {
                'id': instance.id,
                'title': instance.title,
                'body': instance.body,
                'author': instance.author.user.username,
                # Add any other post data you want to send to the template
            }
            return JsonResponse(data, safe=False)
        else:
            return JsonResponse({'error': form.errors}, status=400)
            

    context = {
        'form': form,
    }

    return render(request, 'posts/main.html', context)

def post_detail(request, pk):
    obj = Post.objects.get(pk=pk)
    form = PostForm()

    context = {
        'obj': obj,
        'form': form,
    } 

    return render(request, 'posts/detail.html', context)   

def load_post_data_view(request, num_posts):
        visible = 3
        upper = num_posts
        lower = upper - visible
        size = Post.objects.all().count()

        qs = Post.objects.all()
        data = []
        for obj in qs:
            item = {
                'id': obj.id,
                'title': obj.title,
                'body': obj.body,
                'liked': 'True' if request.user in obj.liked.all() else 'False',  
                'count': obj.like_count,  
                'author': obj.author.user.username  
            }
            data.append(item)

        return JsonResponse({'data': data[lower:upper], 'size': size})     