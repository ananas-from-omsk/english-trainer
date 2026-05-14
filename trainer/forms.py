"""Forms module for trainer app"""

from django import forms

from .models import Word


class WordForm(forms.ModelForm):
    """Form for creating and validating Word objects"""

    class Meta:
        """Meta configuration for WordForm"""
        model = Word
        fields = ["english", "russian", "example"]

    def clean_english(self):
        """Validate English word"""
        value = self.cleaned_data["english"]

        if len(value.strip()) < 2:
            raise forms.ValidationError("Слишком короткое английское слово")

        return value

    def clean_russian(self):
        """Validate Russian translation"""
        value = self.cleaned_data["russian"]

        if len(value.strip()) < 2:
            raise forms.ValidationError("Слишком короткий перевод")

        return value