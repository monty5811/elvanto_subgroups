# -*- coding: utf-8 -*-
from django import forms

from elvanto_subgroups.models import Link


class LinkForm(forms.ModelForm):

    class Meta:
        model = Link
        fields = ['main_group', 'sub_groups']
