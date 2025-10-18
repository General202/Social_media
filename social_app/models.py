from django.db import models

# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey('auth_system.CustomUser', on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey('auth_system.CustomUser', on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Повідомлення від {self.sender} до {self.recipient} о {self.timestamp}'
    
class Post(models.Model):
    author = models.ForeignKey('auth_system.CustomUser', on_delete=models.CASCADE, related_name='posts')
    group = models.ForeignKey('Group', on_delete=models.CASCADE, related_name='posts', null=True, blank=True)
    content = models.TextField('Контент посту', blank=True)
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    video = models.FileField(upload_to='post_videos/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f"Пост {self.author.username} — {self.content[:30]}"
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('auth_system.CustomUser', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username}: {self.content[:20]}"
    
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey('auth_system.CustomUser', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
         return f"{self.user.username} ❤️ {self.post.id}"
    
class FriendRequest(models.Model):
    sender = models.ForeignKey('auth_system.CustomUser', on_delete=models.CASCADE, related_name='sent_friend_requests')
    recipient = models.ForeignKey('auth_system.CustomUser', on_delete=models.CASCADE, related_name='received_friend_requests')
    timestamp = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'Запит у друзі від {self.sender} до {self.recipient} о {self.timestamp}'
    
class Friendship(models.Model):
    user1 = models.ForeignKey('auth_system.CustomUser', on_delete=models.CASCADE, related_name='friendships_initiated')
    user2 = models.ForeignKey('auth_system.CustomUser', on_delete=models.CASCADE, related_name='friendships_received')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f'Дружба між {self.user1} та {self.user2} з {self.timestamp}'
    
class Notification(models.Model):
    user = models.ForeignKey('auth_system.CustomUser', on_delete=models.CASCADE, related_name='notifications')
    content = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f'Сповіщення для {self.user} о {self.timestamp}'
    
class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='group_images/', null=True, blank=True)
    members = models.ManyToManyField('auth_system.CustomUser', related_name='user_groups', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    

    
