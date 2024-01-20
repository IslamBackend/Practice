from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from anime.forms import CommentCreateForm, AnimeCreateForm
from anime.models import Anime, Comment, HashTag
from django.conf import settings


def main_view(request):
    if request.method == 'GET':
        return render(request, 'layouts/index.html')


def anime_list_view(request):
    if request.method == 'GET':
        anime_list = Anime.objects.all()
        search = request.GET.get('search')
        order = request.GET.get('order')
        page = int(request.GET.get('page', 1))

        if search is not None:
            anime_list = anime_list.filter(title__icontains=search)

        if order == 'created_at':
            anime_list = anime_list.order_by('created_at')
        elif order == '-created_at':
            anime_list = anime_list.order_by('-created_at')

        max_page = anime_list.__len__() / settings.PAGE_SIZE

        if max_page > round(max_page):
            max_page = round(max_page) + 1
        else:
            max_page = round(max_page)

        start = (page - 1) * settings.PAGE_SIZE
        end = page * settings.PAGE_SIZE

        anime_list = anime_list[start:end]

        context = {
            'anime_list': anime_list,
            'pages': range(1, max_page + 1),
        }

        return render(request, 'anime/anime_list.html', context)


def anime_detail_view(request, anime_id):
    anime = get_object_or_404(Anime, id=anime_id)
    if request.method == 'GET':
        # comments = Comment.objects.filter(anime=anime)
        comments = anime.comments.all()
        hashtags = anime.hashtags.all()
        context = {
            'anime': anime,
            'hashtags': hashtags,
            'comments': comments,
            'form': CommentCreateForm
        }
        return render(request, 'anime/anime_detail.html', context)

    elif request.method == 'POST':
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.anime = anime
            comment.save()
            return redirect(f'/anime/{anime_id}')
        else:
            return render(request, 'anime/anime_detail.html', {'form': form})


def anime_create_view(request):
    if request.method == 'GET':
        form = AnimeCreateForm()
        context = {
            'form': form
        }
        return render(request, 'anime/anime_create.html', context)

    elif request.method == 'POST':
        form = AnimeCreateForm(request.POST, request.FILES)
        if form.is_valid():
            anime_instance = form.save()
            hashtags_data = form.cleaned_data.get('hashtags')
            if hashtags_data:
                anime_instance.hashtags.set(hashtags_data)
            return redirect('/anime/')
        else:
            context = {
                'form': form
            }
            return render(request, 'anime/anime_create.html', context)


def anime_update_view(request, anime_id):
    anime = get_object_or_404(Anime, id=anime_id)
    if request.method == 'GET':
        context = {
            'form': AnimeCreateForm(instance=anime)
        }
        return render(request, 'anime/anime_update.html', context)

    if request.method == 'POST':
        form = AnimeCreateForm(request.POST, request.FILES, instance=anime)
        if form.is_valid():
            form.save()
            return redirect('/anime/')

        context = {
            'form': form
        }
        return render(request, 'anime/anime_update.html', context)


def anime_delete_view(request, anime_id):
    anime = get_object_or_404(Anime, id=anime_id)
    if request.method == 'GET':
        anime.delete()
        return redirect('/anime/')
    return HttpResponse('LOL ERROR!')
