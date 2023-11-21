from django.contrib.auth.views import LoginView, PasswordResetView, LogoutView
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.urls import reverse_lazy

from .models import *
from .forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_POST
# from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.search import TrigramSimilarity
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.contrib import messages
from random import randint


# from django.contrib.auth.models import User


# Create your views here.
def index(request):
    posts = Post.published.all()
    r = randint(0, len(posts)-1)
    post = posts[r]
    return render(request, 'blog/index.html', {'post': post})


def post_list(request, category=None):
    if category is not None:
        posts = Post.published.filter(category=category)
    else:
        posts = Post.published.all()
    paginator = Paginator(posts, 8)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    context = {
        "posts": posts,
        "category": category
    }
    return render(request, 'blog/list1.html', context)
# class PostListView(ListView):
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 5
#     template_name = 'blog/list.html'


def post_detail(request, id):
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
    comments = post.comments.filter(active=True)
    form = CommentForm()
    context = {
        'post': post,
        'form': form,
        'comments': comments
    }
    return render(request, 'blog/detail.html', context)


# class PostDetailView(DetailView):
#     model = Post
#     template_name = 'blog/detail.html'


def ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Ticket.objects.create(message=cd['message'], name=cd['name'], email=cd['email'],
                                  phone=cd['phone'], subject=cd['subject'])
            return redirect('blog:index')
    else:
        form = TicketForm()
    return render(request, 'forms/ticket.html', {'form': form})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    context = {
        'post': post,
        'form': form,
        'comment': comment
    }
    return render(request, 'forms/comment.html', context)


def new_post(request):
    user = request.user.username
    if request.method == 'POST':
        form = NewPostForm(request.POST)

        if form.is_valid():
            try:
                cd = form.cleaned_data
                Post.objects.create(author=request.user, title=cd['title'],
                                    reading_time=cd['reading_time'], description=cd['description'])
                return redirect('blog:index')
            except ValueError:
                error = 'کاربری یافت نشد. لطفن دوباره تلاش کنید'
                return render(request, 'forms/newpost.html', {'error': error})
    else:
        form = NewPostForm()
    return render(request, 'forms/newpost.html', {'form': form, 'user': user})


def post_search(request):
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(data=request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results1 = (Post.published.annotate(similarity=TrigramSimilarity('title', query))
                        .filter(similarity__gt=0.1))
            results2 = (Post.published.annotate(similarity=TrigramSimilarity('description', query))
                        .filter(similarity__gt=0.1))
            results3 = (Post.published.annotate(similarity=TrigramSimilarity('images__title', query))
                        .filter(similarity__gt=0.1))
            results4 = (Post.published.annotate(similarity=TrigramSimilarity('images__description', query))
                        .filter(similarity__gt=0.1))
            results = ((results1 | results2) | (results3 | results4)).order_by('-similarity')
    context = {
        'query': query,
        'results': results
    }
    return render(request, 'blog/search.html', context)


@login_required()
def profile(request):
    user = request.user
    posts = Post.published.filter(author=user)
    comment = Comment.objects.filter(post__author=user)
    paginator = Paginator(posts, 2)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    return render(request, 'blog/profile.html', {'posts': posts, 'comment': comment})


def user_profile(request, author_id, author):
    posts = Post.published.filter(author=author_id)
    user = User.objects.get(username=author)
    return render(request, 'blog/user-profile.html', {'posts': posts, 'user': user})


def create_post(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            Image.objects.create(image_file=form.cleaned_data['image1'], post=post)
            Image.objects.create(image_file=form.cleaned_data['image2'], post=post)
            return redirect('blog:profile.html')
    else:
        form = CreatePostForm()
        return render(request, 'forms/create-post.html', {'form': form})


def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:index')
    return render(request, 'forms/delete-post.html', {'post': post})


def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            Image.objects.create(image_file=form.cleaned_data['image1'], post=post)
            Image.objects.create(image_file=form.cleaned_data['image2'], post=post)
            return redirect('blog:profile.html')
    else:
        form = CreatePostForm(instance=post)
    return render(request, 'forms/create-post.html', {'form': form, 'post': post})


def delete_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    image.delete()
    return redirect('blog:profile.html')


class MyLoginView(LoginView):
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('blog:profile')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


# class MyLogoutView(LogoutView):
#     def render_to_response(self, context, **response_kwargs):
#         """
#         Return a response, using the `response_class` for this view, with a
#         template rendered with the given context.
#         Pass response_kwargs to the constructor of the response class.
#         """
#         response_kwargs.setdefault("content_type", self.content_type)
#         return self.response_class(
#             request=self.request,
#             template=self.get_template_names(),
#             context=context,
#             using=self.template_engine,
#             **response_kwargs,
#         )

# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'], password=cd['password'])
#             print(user)
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return redirect('blog:index')
#                 else:
#                     return HttpResponse('Your account is not active')
#             else:
#                 return HttpResponse('Invalid username or password')
#     else:
#         form = LoginForm()
#     return render(request, 'registration/login1.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Account.objects.create(user=user)
            return render(request, 'registration/register_done.html', {'user': user})
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def edit_account(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        account_form = UserEditAccount(request.POST, instance=request.user.account, files=request.FILES)
        if account_form.is_valid() and user_form.is_valid():
            account_form.save()
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        account_form = UserEditAccount(instance=request.user.account)
    context = {
        'account_form': account_form,
        'user_form': user_form,
    }
    return render(request, 'registration/edit_account.html', context)


