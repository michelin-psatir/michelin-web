from django import forms
from django.utils.translation import gettext_lazy as _

class SearchForm(forms.Form):
    search = forms.CharField(max_length='100', required=True, label="", widget=forms.TextInput(
        attrs={'class' : 'block w-full p-4 pl-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-white-50 hover:ring-gray-400 hover:border-gray-400 focus:ring-blue-500 focus:border-blue-500 truncate',
        'type' : "text",
        'placeholder' : "Search Restaurants...",
        'id' : "michelin-search",
          }))

      