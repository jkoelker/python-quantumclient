# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2011 OpenStack LLC
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import json
import urlparse

import requests


class Client(object):
    def __init__(self, host='localhost', port=9696, ssl=False,
            verify_ssl=False):
        self.verify_ssl = verify_ssl

        headers = {'Content-Type': 'application/json'}
        self.session = requests.session(headers=headers)

        scheme = 'http'
        if ssl:
            scheme = 'https'

        netloc = '%s:%s' % (host, port)
        path = '/v1.1/tenants/'

        self.url = urlparse.urlunsplit((scheme, netloc, path, None, None))

    def _do(self, method, path, body=dict(), headers=dict(),
            params=dict()):
        args = dict(headers=headers, data=body, params=params)
        with self.session as c:
            return getattr(c, method.lower())(**args)

    def _list(self, tenant_id, what, filters=None, detail=False):
        url = urlparse.urljoin(self.url, '%s/%s/' % (tenant_id, what))
        if detail:
            url = urlparse.urljoin(url, 'detail')

        r = self._do('get', url, params=filters)
        r.raise_for_status()
        return json.loads(r.text)[what]

    def _get(self, tenant_id, what, uuid, detail=False):
        url = urlparse.urljoin(self.url, '%s/%s/%s/' % (tenant_id, what,
                                                        uuid))
        if detail:
            url = urlparse.urljoin(url, 'detail')

        r = self._do('get', url)
        r.raise_for_status()
        return json.loads(r.text)['network']

    def _create(self, tenant_id, what, **kwargs):
        url = urlparse.urljoin(self.url, '%s/%s/' % (tenant_id, what))
        r = self._do('post', url, body=kwargs)
        r.raise_for_status()
        return json.loads(r.text)[what]

    def _delete(self, tenant_id, what, uuid):
        url = urlparse.urljoin(self.url, '%s/%s/%s/' % (tenant_id, what,
                                                        uuid))
        r = self._do('delete', url)
        r.raise_for_status()

    def list_networks(self, tenant_id, filters=None, detail=False):
        return self._list(tenant_id, 'networks', filters, detail)

    def get_network(self, tenant_id, uuid, filters=None, detail=False):
        return self._get(tenant_id, 'networks', filters, detail)

    def create_network(self, tenant_id, name):
        return self._create(tenant_id, 'networks', name=name)

    def delete_network(self, tenant_id, uuid):
        return self._delete(tenant_id, 'networks', uuid)

    def list_ports(self, tenant_id, filters=None, detail=False):
        return self._list(tenant_id, 'ports', filters, detail)

    def get_port(self, tenant_id, uuid, filters=None, detail=False):
        return self._get(tenant_id, 'ports', filters, detail)

#    def create_port(self, tenant_id, state, attach=True):
#        port = self._create(tenant_id, 'ports', state=state)
#        if attach:
#            args = (tenant_id, 'ports', port['id'])
#            url = urlparse.urljoin(self.url, '%s/%s/%s/attachment' % args)
#            r = self._do('get', url, body=port)
#            r.raise_for_status()
