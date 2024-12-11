from django.db import models
from django.utils.translation import gettext_lazy as _
from notify.models import User
# Create your models here.

class Post(models.Model):
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name=_('Author'))
    title = models.CharField(_('Title of the post'), max_length=50)
    content = models.TextField(_('Content of the post'))
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username}: {self.content[:10]}'
    
    def set_author(self, author):
        if not isinstance(author, User):
            return -1
        self.author = author
    

class Notification(models.Model):

    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name=_('Origin_Notification'))
    content = models.CharField(_('Content of notification'), max_length=100)
    read = models.BooleanField(_('read status'), default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name=_('Destination_Notification'))

    @property
    def is_read(self):
        return self.read
    
    @is_read.setter
    def is_read(self, read):
        if isinstance(read, bool):
            self.read = read
    
    def send_notification(self, sender, content, receiver):
        #type verification of the attributes
        if not isinstance(sender, User) and not isinstance(content, str) and not isinstance(receiver, User):
            return -1
        
        self.sender = sender
        self.content = content
        self.receiver = receiver  

        self.save()        
    
    def get_notify(self):
        
        return {
            'sender': self.sender,
            'content': self.content,
            'receiver': self.receiver,
            'date': self.create_at,
            'read': self.is_read()
        }
    
    

