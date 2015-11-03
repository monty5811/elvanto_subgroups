# -*- coding: utf-8 -*-
from django.contrib import admin

from elvanto_subgroups.models import ElvantoGroup, ElvantoPerson, Link

admin.site.register(ElvantoGroup)
admin.site.register(ElvantoPerson)
admin.site.register(Link)
