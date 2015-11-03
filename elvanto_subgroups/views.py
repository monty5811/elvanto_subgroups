# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from elvanto_subgroups.mixins import LoginRequiredMixin
from elvanto_subgroups.models import Link


class Index(LoginRequiredMixin, TemplateView):
    template_name = 'elvanto_subgroups/index.html'


class LinkCreate(LoginRequiredMixin, CreateView):
    model = Link
    fields = ['main_group', 'sub_groups']
    success_url = '/'


class LinkUpdate(LoginRequiredMixin, UpdateView):
    model = Link
    fields = ['main_group', 'sub_groups']
    success_url = '/'


class LinkDelete(LoginRequiredMixin, DeleteView):
    model = Link
    success_url = '/'
