from django import forms
from anime.models import Comment, Anime


class AnimeCreateForm(forms.ModelForm):
    class Meta:
        model = Anime
        fields = '__all__'


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
