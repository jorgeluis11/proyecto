from django import forms


class NewsForm(forms.Form):
    categories = (
        ("Deportes", "Deporte"),
        ("Economia", "Economia"),
        ("Entretenimiento", "Entretenimiento"),
        ("Internacionales", "Internacional"),
        ("Local", "Local"),
        ("Politica", "Politica"),
        ("Tecnologia", "Tecnologia"),
        ("Vida", "Vida"),
    )

    categoria = forms.ChoiceField(choices=categories)
    titulo = forms.CharField(widget=forms.TextInput(attrs={"id":"titleNews","rel":"popover","data-content":"contenido"}))
    contenido = forms.CharField(widget=forms.Textarea(attrs={"id":"contentNews"}))
    foto = forms.ImageField(required=False)


class QuoteForm(forms.Form):
    autor = forms.CharField(widget=forms.TextInput)
    frase = forms.CharField(widget=forms.Textarea)


class MovieForm(forms.Form):
    titulo = forms.CharField(widget=forms.TextInput)
    contenido = forms.CharField(widget=forms.Textarea)


class ComentaryForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'height': 2,}),
     label='Deja Tu Comentario')    
