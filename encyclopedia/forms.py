from django import forms


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100)
    content = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'textarea'}), label="Content")
