from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import PostForm
from .models import Post

@login_required(login_url="/login")
def PostFormView(request):
    form = PostForm(request.POST, request=request.user)
    if form.is_valid():
        post = form.save()
        messages.success(request, 'Success!')
        return redirect('/groups/%s' %form.getGroup())
    return render(request, 'Post/post.html', {'form': form})

@login_required(login_url="/login")
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    group = post.group
    post.delete()
    messages.success(request, 'Post deleted!')
    return redirect('/groups/%s' %group)