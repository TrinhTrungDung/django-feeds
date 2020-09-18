from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import Item, Category


class ItemAdminForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name=_("Categories"),
            is_stacked=False
        )
    )

    class Meta:
        model = Item
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ItemAdminForm, self).__init__(*args, **kwargs)

        if self.instance.id:
            self.fields["categories"].initial = self.instance.categories.all()

    def save(self, commit=True):
        article = super(ItemAdminForm, self).save(commit=False)
        if self.cleaned_data["categories"]:
            article.save()
            article.categories.set(self.cleaned_data["categories"])
        if commit:
            article.save()
            article.save_m2m()

        return article


class ItemCreationForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = Item
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ItemCreationForm, self).__init__(*args, **kwargs)

        if self.instance.id:
            self.fields["categories"].initial = self.instance.categories.all()

    def save(self, commit=True):
        article = super(ItemCreationForm, self).save(commit=False)
        if self.cleaned_data["categories"]:
            article.save()
            article.categories.set(self.cleaned_data["categories"])
        if commit:
            article.save()

        return article
