from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import PostForm

@login_required(login_url="/login")
def PostFormView(request):
    form = PostForm(request.POST, request=request.user)
    if form.is_valid():
        post = form.save()
        messages.success(request, 'Success!')
        return redirect('/groups')
    return render(request, 'Post/post.html', {'form': form})