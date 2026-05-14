from django import forms
from .models import Word


class WordForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = ["english", "russian", "example"]

    def clean_english(self):
        value = self.cleaned_data["english"]
        if len(value.strip()) < 2:
            raise forms.ValidationError("Слишком короткое английское слово")
        return value

    def clean_russian(self):
        value = self.cleaned_data["russian"]
        if len(value.strip()) < 2:
            raise forms.ValidationError("Слишком короткий перевод")
        return value