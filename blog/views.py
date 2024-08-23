from typing import Any
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.db.models import Count
from accounts.models import Post, Comment, Account, Like
from .forms import CreatePostForm, CreateCommentForm

class FeedView(generic.ListView):
    model = Post
    template_name = "blog/feed.html"
    context_object_name = "posts"
    paginate_by = 20
    login_required = True

    ordering = ["-created_at",]

    def get_context_data(self, **kwargs):
        # Add any extra context needed in the template
        context = super().get_context_data(**kwargs)

        context["posts"] = Post.objects.get_queryset().annotate(
            likes_count=Count("likes", distinct=True),
            comments_count=Count('comments', distinct=True),
        ).order_by(*self.ordering)

        return context

class PostDetailsView(generic.DetailView, generic.FormView):
    model = Post
    template_name = "blog/post.html"
    context_object_name = "post"

    form_class = CreateCommentForm
    success_url = reverse_lazy("blog:feed")

    login_required = True

    def get_context_data(self, **kwargs):
        # Add any extra context needed in the template
        context = super().get_context_data(**kwargs)

        context['comments'] = Comment.objects.filter(post=context["post"]).order_by("-created_at")

        current_post_likes = Like.objects.get_queryset().filter(post=context["post"])
        context["like_count"] = current_post_likes.count()
        context["is_liked"] = current_post_likes.filter(user=self.request.user).exists()

        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, user=request.user, post=self.object)  # Pass the user
        message = None
        if form.is_valid():
            comment = form.save()
            if comment is None:
                message = 'There is an error when publishing your comment'
            else:
                form = self.form_class(user=request.user, post=self.object)
        else:
            message = 'There is an error when publishing your comment'


        return self.render_to_response(self.get_context_data(form=form, message=message))
    
class ProfileDetailsView(generic.DetailView):
    model = Account
    template_name = "blog/account.html"
    context_object_name = "account"
    login_required = True

    def get_object(self):
        # Retrieve the user by username
        username = self.kwargs.get('username')
        return get_object_or_404(Account, username=username)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context["posts"] = Post.objects.filter(user=context["account"]).annotate(
            likes_count=Count("likes", distinct=True),
            comments_count=Count('comments', distinct=True),
        ).order_by("-created_at")
        # print(context["posts"][0].body[:10], context["posts"][0].likes_count)

        return context

    
class CreatePostView(generic.FormView):
    form_class = CreatePostForm
    template_name = "blog/create_post.html"
    success_url = reverse_lazy("blog:feed")
    login_required = True

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES, user=request.user)  # Pass the user
        if form.is_valid():
            post = form.save()
            return redirect(self.success_url)
        
        # If form is invalid, re-render the page with the form data and error messages
        return self.form_invalid(form)

    def form_invalid(self, form):
        print(form.errors)
        return HttpResponse(f'{form.errors}')



def delete_post(request, pk):
    post = Post.objects.get(pk=pk)
    if post.user == request.user:
        post.delete()
    return redirect(reverse_lazy("blog:account", kwargs={'username': request.user.username}))

def delete_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    if comment.user == request.user:
        comment.delete()

    return redirect(request.META.get('HTTP_REFERER', '/')) 
    # return redirect(reverse_lazy("blog:account", kwargs={'username': request.user.username}))

def like_post_button(request, pk):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        post = Post.objects.get(pk=pk)

        like, created = Like.objects.get_or_create(post=post, user=request.user)

        if not created:
            like.delete()


        return get_post_liked_status(request, pk)
    return redirect(reverse_lazy("blog:feed"))

def get_post_liked_status(request, pk):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        post = Post.objects.get(pk=pk)

        post_likes = Like.objects.filter(post=post)

        liked_by_user = post_likes.filter(user=request.user).exists()

        data = {
            "liked_by_user": liked_by_user,
            "like_count": post_likes.count(),
        }

        return JsonResponse(data, status=200)
    return redirect(reverse_lazy("blog:feed"))



