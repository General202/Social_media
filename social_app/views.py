from django.shortcuts import render

# Create your views here.
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.shortcuts import get_object_or_404, redirect

from auth_system.models import CustomUser
from .models import Post, Comment, Like, FriendRequest, Friendship, Message, Notification
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all().order_by('-timestamp')
        context['notifications'] = self.request.user.notifications.filter(read=False)
        return context
    

class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'message/profile.html'
    context_object_name = 'profile_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = self.get_object()
        context['posts'] = Post.objects.filter(author=profile_user).order_by('-timestamp')
        context['is_friend'] = Friendship.objects.filter(
            (Q(user1=self.request.user) & Q(user2=profile_user)) |
            (Q(user1=profile_user) & Q(user2=self.request.user))
        ).exists()
        context['friend_requests_sent'] = FriendRequest.objects.filter(sender=self.request.user, recipient=profile_user).exists()
        context['friend_requests_received'] = FriendRequest.objects.filter(sender=profile_user, recipient=self.request.user).exists()
        return context
    

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
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
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
    fields = ['content', 'image']
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
    model = Comment
    fields = ['content']
    template_name = 'comment/comment_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('home')
    
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'comment/comment_delete.html'

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

    def get_success_url(self):
        return reverse('home')
    
class NotificationReadView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        notification = get_object_or_404(Notification, pk=kwargs['pk'], user=request.user)
        notification.read = True
        notification.save()
        return redirect('notifications')
    


    