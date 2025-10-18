from django.shortcuts import render

# Create your views here.
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.shortcuts import get_object_or_404, redirect

from auth_system.models import CustomUser
from social_app.forms import CommentForm, PostForm
from .models import Post, Comment, Like, FriendRequest, Friendship, Message, Notification
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q


class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'posts'
    ordering = ['-timestamp']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context
    

class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'message/profile.html'
    context_object_name = 'profile_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = self.get_object()
        context['posts'] = Post.objects.filter(author=profile_user).order_by('-timestamp')

        if self.request.user.is_authenticated:
            context['is_friend'] = Friendship.objects.filter(
                (Q(user1=self.request.user) & Q(user2=profile_user)) |
                (Q(user1=profile_user) & Q(user2=self.request.user))
            ).exists()
            context['friend_requests_sent'] = FriendRequest.objects.filter(sender=self.request.user, recipient=profile_user).exists()
            context['friend_requests_received'] = FriendRequest.objects.filter(sender=profile_user, recipient=self.request.user).exists()
        else:
            context['is_friend'] = False
            context['friend_requests_sent'] = False
            context['friend_requests_received'] = False

        return context
    

class EditProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ['bio', 'cover_image', 'profile_image', 'birth_date']  # Можеш додати інші
    template_name = 'message/edit_profile.html'
    success_url = reverse_lazy('home')  # або назад на profile

    def get_object(self):
        return self.request.user
    

class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'message/messages.html'
    context_object_name = 'messages'

    def get_queryset(self):
        return Message.objects.filter(Q(sender=self.request.user) | Q(recipient=self.request.user)).order_by('-timestamp')
    

class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ['recipient', 'content']
    template_name = 'message/message_create.html'
    success_url = reverse_lazy('messages')

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super().form_valid(form)
    
class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Message
    template_name = 'message/message_delete.html'
    success_url = reverse_lazy('messages')

    def test_func(self):
        message = self.get_object()
        return message.sender == self.request.user or message.recipient == self.request.user
    
class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'message/notifications.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        return self.request.user.notifications.all().order_by('-timestamp')
    

class LikePostView(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if not created:
            like.delete()
        return redirect('home')
    
class SendFriendRequestView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        recipient = get_object_or_404(CustomUser, pk=kwargs['pk'])
        if recipient != request.user and not FriendRequest.objects.filter(sender=request.user, recipient=recipient).exists():
            FriendRequest.objects.create(sender=request.user, recipient=recipient)
        return redirect('profile', pk=recipient.pk)
    
class AcceptFriendRequestView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        friend_request = get_object_or_404(FriendRequest, pk=kwargs['pk'], recipient=request.user)
        Friendship.objects.create(user1=friend_request.sender, user2=friend_request.recipient)
        friend_request.accepted = True
        friend_request.save()
        return redirect('profile', pk=friend_request.sender.pk)
    
class DeclineFriendRequestView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        friend_request = get_object_or_404(FriendRequest, pk=kwargs['pk'], recipient=request.user)
        friend_request.delete()
        return redirect('profile', pk=friend_request.sender.pk)
    
class RemoveFriendView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        friend = get_object_or_404(CustomUser, pk=kwargs['pk'])
        friendship = Friendship.objects.filter(
            (Q(user1=request.user) & Q(user2=friend)) |
            (Q(user1=friend) & Q(user2=request.user))
        ).first()
        if friendship:
            friendship.delete()
        return redirect('profile', pk=friend.pk)
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post/post_create.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post/post_delete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user
    
class CommentCreateView(LoginRequiredMixin, CreateView):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
        return redirect('home')
    
class NotificationReadView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        notification = get_object_or_404(Notification, pk=kwargs['pk'], user=request.user)
        notification.read = True
        notification.save()
        return redirect('notifications')
    


    