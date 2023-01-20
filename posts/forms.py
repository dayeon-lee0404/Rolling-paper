from django import forms
from .models import Post, Comment
from common.models import User
from django_summernote.fields import SummernoteTextField
from django_summernote.widgets import SummernoteWidget


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # fields = '__all__'
        exclude = ('post', 'user',)


class PostWriteForm(forms.ModelForm):
    title = forms.CharField(
        label='글 제목',
        widget=forms.TextInput(
            attrs={
                'placeholder': '게시글 제목'
            }),
        required=True,
    )

    contents = SummernoteTextField()

    options = (
        ('Graduate', '축하 게시판'),
        ('consolation', '위로')
    )

    post_name = forms.ChoiceField(
        label='게시판 선택',
        widget=forms.Select(),
        choices=options
    )

    field_order = [
        'title',
        'post_name',
        'contents'
    ]

    class Meta:
        model = Post
        fields = [
            'title',
            'contents',
            'post_name'
        ]
        widgets = {
            'contents': SummernoteWidget()
        }

    def clean(self):
        cleaned_data = super().clean()

        title = cleaned_data.get('title', '')
        contents = cleaned_data.get('contents', '')
        post_name = cleaned_data.get('post_name', 'Python')

        if title == '':
            self.add_error('title', '글 제목을 입력하세요.')
        elif contents == '':
            self.add_error('contents', '글 내용을 입력하세요.')
        else:
            self.title = title
            self.contents = contents
            self.post_name = post_name
