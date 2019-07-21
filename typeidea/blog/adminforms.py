from django import forms


'''作用于后台的Form，不是前端的Form'''


class PostAdminForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False)  # 摘要显示多行多列
