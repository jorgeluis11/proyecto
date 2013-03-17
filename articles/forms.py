from django import forms


class NewsForm(forms.Form):
    categories = (
        (1, "Deporte"),
        (2, "Economia"),
        (3, "Entretenimiento"),
        (4, "Internacionales"),
        (5, "Local"),
        (6, "Politica"),
        (7, "Tecnologia"),
        (8, "Vida"),
    )

    categoria = forms.ChoiceField(choices=categories)
    titulo = forms.CharField(widget=forms.TextInput)
    contenido = forms.CharField(widget=forms.Textarea)
    image = forms.ImageField()
