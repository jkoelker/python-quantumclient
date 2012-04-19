# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2011 OpenStack LLC
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the 'License'); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an 'AS IS' BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from cement2.core import foundation, controller, handler


class Base(controller.CementBaseController):
    class Meta:
        label = 'base'
        interface = controller.IController
        description = 'Quantum CLI'
        defaults = dict(host='localhost', port='9696', ssl=False,
                        verify=False)
        arguments = [
            (['--url'], dict(help=('Quantum URL (default: '
                                   'http://localhost:9696/'),
                             default='http://localhost:9696/')),
            (['--noverify'], dict(action='store_true', default=False,
                                  help='Verify ssl certificate')),
            ]

    @controller.expose(hide=True, help='Quantum')
    def default(self):
        print self.app.__dict__


class Network(controller.CementBaseController):
    class Meta:
        label = 'network'
        interface = controller.IController
        stacked_on = 'base'
        description = 'network resources'
        defaults = dict()
        arguments = [
            (['-t', '--tenant'], dict(help='Tenant to act upon')),
            ]

    @controller.expose(help='create something yo')
    def create(self):
        self.render(dict(hi='there'))


def main():
    app = foundation.CementApp('example', base_controller=Base)
    handler.register(Network)
    app.setup()
    app.run()
