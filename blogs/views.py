from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string

from blogs.models import Post, Comment

import json

# 글 목록
def posts_list(request):
    #-created_at생성 날짜가 최근 것이 앞으로 나오게
    posts = Post.objects.order_by('-created_at')

    return render(request, 'blogs/posts_list.html',  context={'posts':posts})

#글쓰기 상세페이지
def post_detail(request, post_id):
    # 404페이지
    # get_object_or_404(Post, pk=post_id)
    # 첫번째 인자: 모델, 두번째 인자: 키워드, 만약 키워드가 없으면 404에러 발생
    post = get_object_or_404(Post, pk=post_id)
    #댓글
    comments = Comment.objects.filter(post=post.id)
    # 좋아요 디폴트 false
    is_liked = False

    #request.user.id 로그인 여부 확인, exists() 글 존재 여부확인
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True

    return render(request, 'blogs/post_detail.html', context={'post':post, 'comments':comments, 'is_liked':is_liked, 'total_likes':post.total_likes()})

#글 공감, 로그인 상태에서만 공감표시
@login_required
@require_POST
def post_like(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    
    is_liked = post.likes.filter(id=request.user.id).exists()

    if is_liked:
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('post_detail', kwargs={'post_id': post.id}))

#from django.contrib.auth.decorators import login_required
#@login_required 사용자 인증 여부 체크(DEcorator)
@login_required
def post_write(request):
    errors = []
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        image = request.FILES.get('image')

        if not title:
            errors.append('제목을 입력해주세요.')

        if not content:
            errors.append('내용을 입력해주세요.')

        if not errors:
            post = Post.objects.create(user=request.user, title=title, content=content, image=image)

            return redirect(reverse('post_detail', kwargs={'post_id': post.id}))
    
    return render(request, 'blogs/post_write.html', {'user':request.user, 'errors':errors})

#로그인 한 사람만 댓글 글쓰기 가능하도록 함
@login_required
def comment_write(request):
    errors = []
    #post 데이터를 보냄, get 데이터를 가져옴
    if request.method == 'POST':
        post_id = request.POST.get('post_id', '').strip()
        content = request.POST.get('content', '').strip()

        if not content:
            errors.append('댓글을 입력해주세요.')

        if not errors:
            comment = Comment.objects.create(user=request.user, post_id=post_id, content=content)
            # redirect는 함수 부분으로 넘어감
            # path('post/<int:article_id>/<int:post_id>/', views.post_detal, name='post_detail'),
            #/post/%d/%post.id == reverse('post_detail', args=[post.id, article.id])
            return redirect(reverse('post_detail', kwargs={'post_id': comment.post.id}))
    
    return render(request, 'blogs/post_detail.html', {'user':request.user, 'errors':errors} )



@login_required
@require_POST
def like_toggle(request):
    if request.method == 'POST':
        user = request.user 
        post_id = request.POST.get('pk', '')
        post = Post.objects.get(pk=post_id)

        if post.like.filter(id=user.id).exists(): 
            post.like.remove(user) 
            message = 'Dislike'
        else:
            post.like.add(user)
            message = 'Like'

    context = {'like_count' : post.total_like, 'message' : message}
    return HttpResponse(json.dumps(context), content_type='application/json')