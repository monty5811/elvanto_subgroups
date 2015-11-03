# -*- coding: utf-8 -*-
from rest_framework import serializers

from elvanto_subgroups.models import ElvantoGroup, ElvantoPerson, Link


class LinkSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='main_group.name')
    sub_groups = serializers.StringRelatedField(many=True)
    url = serializers.CharField(source='get_absolute_url')
    delete_url = serializers.CharField(source='get_delete_url')

    class Meta:
        model = Link
        fields = (
            'name',
            'main_group',
            'sub_groups',
            'last_sync',
            'url',
            'delete_url',
            'pk',
        )


class ElvantoPersonSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField()

    class Meta:
        model = ElvantoPerson
        fields = (
            'e_id',
            'full_name',
            'first_name',
            'last_name',
            'pk',
        )


class ElvantoGroupSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url')
    last_pulled = serializers.DateTimeField(format='%d %b %H:%M')

    class Meta:
        model = ElvantoGroup
        fields = (
            'e_id',
            'name',
            'google_email',
            'pk',
        )
