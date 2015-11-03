# -*- coding: utf-8 -*-
from __future__ import print_function

import json

from django.conf import settings

from elvanto_subgroups.utils import retry_request


class ElvantoApiException(Exception):
    pass


def e_api(end_point, **kwargs):
    base_url = 'https://api.elvanto.com/v1/'
    e_url = '{0}{1}.json'.format(base_url, end_point)
    resp = retry_request(e_url, 'post',
                         json=kwargs,
                         auth=(settings.ELVANTO_KEY, '_'))
    data = json.loads(resp.text)
    if data['status'] == 'ok':
        return data
    else:
        raise ElvantoApiException(data['error'])


def refresh_elvanto_data():
    """
    """
    from elvanto_subgroups.models import ElvantoGroup, ElvantoPerson
    print('Pulling Elvanto groups')
    ElvantoGroup.pull()
    print('Pulling Elvanto people')
    ElvantoPerson.pull()
    print('Populating groups')
    ElvantoGroup.populate()
