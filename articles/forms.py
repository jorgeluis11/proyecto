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
    titulo = forms.CharField(max_length=108,error_messages={"required":"Titulo Es Requerido"},
                            widget=forms.TextInput(attrs={"id":"titleNews",
                            "data-content":"contenido"}))
    contenido = forms.CharField(max_length=2500,error_messages={"required":"Contenido Es Requerido"},widget=forms.Textarea(attrs={"id":"contentNews"}))
    foto = forms.ImageField(required=False, widget= forms.ClearableFileInput())

class QuoteForm(forms.Form):
    autor = forms.CharField(error_messages={"required":"Autor Es Requerido"},max_length=35, widget=forms.TextInput)
    frase = forms.CharField(error_messages={"required":"Frase Es Requerida"}, max_length=255, widget=forms.TextInput(attrs={"style":"height:48px; width: 220px;padding:0;text-align: top; vertical-align:top;"}))


class MovieForm(forms.Form):
    titulo = forms.CharField(error_messages={"required":"Titulo Es Requerido"}, widget=forms.TextInput, max_length= 72)
    review = forms.CharField(error_messages={"required":"Contenido Es Requerido"}, widget=forms.Textarea, label="Contenido")
    foto = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={"id": "id-photo-movie"}))

class ComentaryForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'height': 2,}),
     label='Deja Tu Comentario')    
