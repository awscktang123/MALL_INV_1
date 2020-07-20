#from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.
#from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User
from .forms import NewTopicForm, PostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count

'''
def home(request):
    return HttpResponse('Hello, World AR!' + 'https://simpleisbetterthancomplex.com/series/2017/09/11/a-complete-beginners-guide-to-django-part-2.html')


def home(request):
    boards = Board.objects.all()
    boards_names = list()

    for board in boards:
        boards_names.append(board.name)

    response_html = '<br>'.join(boards_names)

    return HttpResponse(response_html)
'''

def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})

def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    #return render(request, 'topics.html', {'board': board})
    topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    return render(request, 'topics.html', {'board': board, 'topics': topics})

@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user  # <- here
            topic.save()
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user  # <- and here
            )
            return redirect('topic_posts', pk=pk, topic_pk=topic.pk)  # <- here
            #return redirect('board_topics', pk=board.pk)  # TODO: redirect to the created topic page
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})
# def new_topic(request, pk):
#     board = get_object_or_404(Board, pk=pk)
#     user = User.objects.first()# TODO: get the currently logged in user
#     if request.method == 'POST':
#         '''
#         #subject = request.POST['subject']
#         #message = request.POST['message']

#         # TODO: get the currently logged in user
#         #user = User.objects.first()
#         #user = get_object_or_404(User, pk=1)

#         topic = Topic.objects.create(
#             subject=subject,
#             board=board,
#             starter=user
#         )

#         post = Post.objects.create(
#             message=message,
#             topic=topic,
#             created_by=user
#         )
#         '''
#         form = NewTopicForm(request.POST)
#         if form.is_valid():
#             topic = form.save(commit=False)
#             topic.board = board
#             topic.starter = user
#             topic.save()
#             post = Post.objects.create(
#                 message=form.cleaned_data.get('message'),
#                 topic=topic,
#                 created_by=user
#             )
#             return redirect('board_topics', pk=board.pk)  # TODO: redirect to the created topic page
#     else:
#         form = NewTopicForm()
#     return render(request, 'new_topic.html', {'board': board, 'form': form})
#     '''
#         return redirect('board_topics', pk=board.pk)  # TODO: redirect to the created topic page

#     return render(request, 'new_topic.html', {'board': board})
#     '''

def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    topic.views += 1
    topic.save()
    return render(request, 'topic_posts.html', {'topic': topic})

@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})