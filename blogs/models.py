from django.db import models

from taggit.managers import TaggableManager

from helpers.models import BaseModel
from users.models import User

class Post(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False)
    content = models.TextField()
    image = models.ImageField(blank=True, null=True)
    #공감버튼
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    tags = TaggableManager()

    # 매직 메소드
    def __str__(self):
        return '%s - %s' % (self.id, self.title)

    def total_likes(self):
        #공감 갯수
        return self.likes.count()

#댓글
class Comment(BaseModel):
    # 각각의 댓글이 쓰여져야 해서 ForeignKey 사용함
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    
    # 게시판 리스트로 보여줄 필드
    def __str__(self):
        return '%s - %s' % (self.id, self.user)
