from django.shortcuts import render
from .models import Post, Photo
from django.http import JsonResponse, HttpResponse
from .forms import PostForm
from profiles.models import Profile
from .utils import action_permission
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
    

def post_detail_data_view(request, pk):
    obj = Post.objects.get(pk=pk)
    data = {
        'id': obj.id,
        'title': obj.title,
        'body': obj.body,
        'author': obj.author.user.username,
        'logged_in': request.user.username,
    }
    return JsonResponse({'data': data})
    


def like_unlike_post(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # This is an AJAX request
        pk = request.POST.get('pk')
        obj = Post.objects.get(pk=pk)
        if request.user in obj.liked.all():
            liked=False
            obj.liked.remove(request.user)
        else:
            liked=True
            obj.liked.add(request.user)
        return JsonResponse({'liked': liked, 'count': obj.like_count})
    else:
        # This is not an AJAX request
        return JsonResponse({'error': 'Not an AJAX request'}, status=400) 
    


def update_post(request, pk):
    obj = Post.objects.get(pk=pk)
    
    # Manually check for 'X-Requested-With' header
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        new_title = request.POST.get('title')
        new_body = request.POST.get('body')
        obj.title = new_title
        obj.body = new_body
        obj.save()
        
        return JsonResponse({
            'title': new_title,
            'body': new_body,
        })
    else:
        return HttpResponseBadRequest('Not an AJAX request')


@action_permission
def delete_post(request, pk):
    obj = Post.objects.get(pk=pk)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        obj.delete()
        return JsonResponse({'post has been deleted'})
    else:
        # Handle the case for non-AJAX requests, if necessary
        return HttpResponseBadRequest('Not an AJAX request')


def image_upload_view(request):
    if request.method == 'POST':
        img = request.FILES.get('file')
        new_post_id = request.POST.get('new_post_id')
        post = Post.objects.get(id=new_post_id)
        Photo.objects.create(image=img, post=post)
    return HttpResponse()    