#
# Project Ginger
#
# Copyright IBM Corp, 2016
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA

from wok.control.base import Collection, Resource
from wok.control.utils import model_fn, UrlSubNode


DASDDEV_REQUESTS = {
    'POST': {
        'format': "GINDASD0001L"
    },
}


@UrlSubNode('dasddevs', True)
class DASDdevs(Collection):
    """
    Collections representing the DASD devices on the system
    """
    def __init__(self, model):
        super(DASDdevs, self).__init__(model)
        self.role_key = 'storage'
        self.admin_methods = ['GET', 'POST', 'DELETE']
        self.resource = DASDdev

    def _get_resources(self, flag_filter):
        """
        Overriden this method, here get_list should return list dict
        which will be set to the resource, this way we avoid calling lookup
        and hence avoiding lsdasd -l command execution again for each device.
        :param flag_filter:
        :return: list of resources.
        """
        try:
            get_list = getattr(self.model, model_fn(self, 'get_list'))
            idents = get_list(*self.model_args, **flag_filter)
            res_list = []
            for ident in idents:
                # internal text, get_list changes ident to unicode for sorted
                args = self.resource_args + [ident]
                res = self.resource(self.model, *args)
                res.info = ident
                res_list.append(res)
            return res_list
        except AttributeError:
            return []


class DASDdev(Resource):
    """
    Resource representing a single DASD device
    """
    def __init__(self, model, ident):
        super(DASDdev, self).__init__(model, ident)
        self.role_key = 'storage'
        self.admin_methods = ['GET', 'POST', 'DELETE']
        self.uri_fmt = "/dasddevs/%s"
        self.format = self.generate_action_handler_task('format', ['blk_size'])
        self.info = {}

        # set user log messages and make sure all parameters are present
        self.log_map = DASDDEV_REQUESTS
        self.log_args.update({'blk_size': ''})

    @property
    def data(self):
        return self.info
