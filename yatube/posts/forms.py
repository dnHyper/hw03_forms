from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')


class FeedBackForm(forms.Form):
    name = forms.CharField(max_length=40,
                           required=True,
                           label='Как вас величать?')
    email = forms.EmailField(required=True, label='E-Mail')
    text = forms.CharField(widget=forms.Textarea,
                           required=True,
                           label='Ваши слова',
                           help_text='И что таки ви хотите мне сказать?')
