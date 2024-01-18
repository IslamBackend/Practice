from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from anime.forms import CommentCreateForm, AnimeCreateForm
from anime.models import Anime, Comment, HashTag


def main_view(request):
    if request.method == 'GET':
        return render(request, 'layouts/index.html')


def anime_list_view(request):
    if request.method == 'GET':
        anime_list = Anime.objects.all()
        context = {
            'anime_list': anime_list,
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
    if request.method == 'POST':
        anime.delete()
        return redirect('/anime/')