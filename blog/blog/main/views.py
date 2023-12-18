from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, TemplateView, DeleteView, UpdateView
from .forms import CustomUserForm, ChangeUserInfoForm, CreatePost, CommentForm
from .models import CustomUser, Post, Comment


def index(request):
    all_posts = Post.objects.order_by('-created_at')[:50]
    paginator = Paginator(all_posts, 10)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'main/index.html', {'posts': posts})


class LoginViewUser(LoginView):
    template_name = 'main/login.html'


def logout_view(request):
    logout(request)
    return render(request, 'main/logout.html')


@login_required
def profile(request):
    user_posts = Post.objects.filter(user=request.user)
    return render(request, 'main/profile.html', {'user_posts': user_posts})


class UserRegister(CreateView):
    model = CustomUser
    form_class = CustomUserForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('main:register_done')

    def form_valid(self, form):
        response = super().form_valid(form)
        avatar = self.request.FILES.get('avatar')
        if avatar:
            self.object.avatar = avatar
            self.object.save()
        return response


def create_post(request):
    if request.method == 'POST':
        form = CreatePost(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('main:profile')
    else:
        form = CreatePost()

    return render(request, 'main/post_create-form.html', {'form': form})


class RegisterDone(TemplateView):
    template_name = 'registration/register_done.html'


def edit_user(request):
    if request.method == 'POST':
        form = ChangeUserInfoForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            if 'delete_avatar' in request.POST:
                request.user.avatar.delete(save=True)
            form.save()
            return redirect('main:profile')

    else:
        form = ChangeUserInfoForm(instance=request.user)

    return render(request, 'main/change_user_info.html', {'form': form})


@login_required
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)
        return redirect('main:index')
    return render(request, 'main/delete_user-accounts.html')


@method_decorator(login_required, name='dispatch')
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'main/delete_post_confirm.html'
    success_url = reverse_lazy('main:profile')

    def get_object(self, queryset=None):
        post = super().get_object(queryset=queryset)
        if post.user != self.request.user:
            raise get_object_or_404(Post, id=post.id, user=self.request.user)
        return post


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    form_class = CreatePost
    template_name = 'main/edit_post.html'
    success_url = reverse_lazy('main:profile')

    def get_object(self, queryset=None):
        post = super().get_object(queryset=queryset)
        if post.user != self.request.user:
            raise get_object_or_404(Post, id=post.id, user=self.request.user)
        return post


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).order_by('created_at')
    comment_count = comments.count()

    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            form = CommentForm()
    else:
        form = CommentForm()

    return render(request, 'main/post_detail.html', {'post': post, 'comments': comments, 'form': form, 'comment_count': comment_count})


def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user == comment.user:
        comment.delete()

    return redirect('main:post_detail', post_id=comment.post.id)
