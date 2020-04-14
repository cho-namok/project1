from django.contrib import admin

from .models import Post, Comment

admin.site.register(Post) #블로그 글쓰기
admin.site.register(Comment) # 댓글
