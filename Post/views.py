from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic.edit import FormView

from .forms import PostForm
from .models import Post
from Groups.models import Group

@login_required(login_url="/login")
def PostView(request, pk):
    form = PostForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.group = Group.objects.get(pk=pk)
        post.user = request.user
        post.checkTaboo()
        post.save()
        messages.success(request, 'Post was successful!')
        return redirect('/groups/%s' %pk)
    return render(request, 'Post/post.html', {'form': form})


@login_required(login_url="/login")
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    group = post.group.pk
    post.delete()
    messages.success(request, 'Post deleted!')
    return redirect('/groups/%s' %group)