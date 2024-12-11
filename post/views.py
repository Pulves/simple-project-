from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Post, Notification
from notify.models import User
from .forms import CreatePostForm
from django.http import JsonResponse


# Create your views here.
def feed(request):
    posts = Post.objects.all().order_by('date')
    feed = [{
        'author': post.author.username,
        'title': post.title,
        'content': post.content
    } for post in posts]

    return render(request, 'feed.html', {'posts': feed})

def create_post(request):
    form = CreatePostForm()
    
    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            print(f'[*] Log User: {request.user}')
            try:
                user = User.objects.filter(username=request.user.username).get()
                print(f'user: {user.username}')
                post = Post.objects.create(author=user, title=title, content=content)
                post.save()

                notification = Notification()
                notification.send_notification(sender=user, content=f"new post of the {user.username}", receiver=User.objects.first())
                
                return redirect('feed')
            
            except Exception as error:
                print(f'[*] Log error in create post -> {error}')
        else:
            messages.error(request, 'form is not valid!')

    return render(request, 'create_post.html', {'form': form})


def notifications(request):
    user = request.user
    notify = Notification.objects.filter(receiver=User.objects.first()).all()
    
    data = {
        'owner': notify.first().sender.username,
        'read': notify.first().is_read,
        'content': notify.first().content
    }

    return JsonResponse(data)