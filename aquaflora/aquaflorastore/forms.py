from django import forms


class SearchForm(forms.Form):
    search_terms = forms.CharField(
        label="",
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "search-input", "placeholder": "Pesquisar...", "label" : " - ",}
        ),
    )

    def filter_results(self, query):
        search_terms = self.cleaned_data["search_terms"]
        search_terms = search_terms.split(" ")
        for term in search_terms:
            query = query.filter(livro_nome__icontains=term)
        return query
