# Copyright (c) 2015 OpenStack Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from neutron import context
from neutron.tests.unit import testlib_api

from baremetal_network_provisioning.db import bm_nw_provision_db as db
from baremetal_network_provisioning.db import bm_nw_provision_models as models


class NetworkProvisionDBTestCase(testlib_api.SqlTestCase):

    def setUp(self):
        super(NetworkProvisionDBTestCase, self).setUp()
        self.ctx = context.get_admin_context()

    def _get_switch_port_dict(self):
        rec_dict = {'id': "phy1234",
                    'switch_id': "test_switch1",
                    'port_name': "Tengig0/1",
                    'lag_id': None}
        return rec_dict

    def _get_switch_lag_port_dict(self):
        rec_dict = {'id': "lag1234",
                    'external_lag_id': "extlag123"}
        return rec_dict

    def _get_ironic_switch_port_map_dict(self):
        rec_dict = {'neutron_port_id': "n1234",
                    'switch_port_id': None,
                    'lag_id': None,
                    'access_type': "access",
                    'segmentation_id': 100,
                    'bind_requested': True}
        return rec_dict

    def test_add_hp_switch_port(self):
        rec_dict = self._get_switch_port_dict()
        db.add_hp_switch_port(self.ctx, rec_dict)
        count = self.ctx.session.query(models.HPSwitchPort).count()
        self.assertEqual(1, count)

    def test_delete_hp_switch_port(self):
        rec_dict = self._get_switch_port_dict()
        db.add_hp_switch_port(self.ctx, rec_dict)
        db.delete_hp_switch_port(self.ctx, rec_dict)
        count = self.ctx.session.query(models.HPSwitchPort).count()
        self.assertEqual(count, 0)

    def test_add_hp_switch_lag_port(self):
        rec_dict = self._get_switch_lag_port_dict()
        db.add_hp_switch_lag_port(self.ctx, rec_dict)
        count = self.ctx.session.query(models.HPSwitchLAGPort).count()
        self.assertEqual(1, count)

    def test_delete_hp_switch_lag_port(self):
        rec_dict = self._get_switch_lag_port_dict()
        db.add_hp_switch_lag_port(self.ctx, rec_dict)
        db.delete_hp_switch_lag_port(self.ctx, rec_dict)
        count = self.ctx.session.query(models.HPSwitchLAGPort).count()
        self.assertEqual(count, 0)

    def test_add_hp_ironic_switch_port_mapping(self):
        rec_dict = self._get_ironic_switch_port_map_dict()
        db.add_hp_ironic_switch_port_mapping(self.ctx, rec_dict)
        count = self.ctx.session.query(
            models.HPIronicSwitchPortMapping).count()
        self.assertEqual(1, count)

    def test_delete_hp_ironic_switch_port_mapping(self):
        rec_dict = self._get_ironic_switch_port_map_dict()
        db.add_hp_ironic_switch_port_mapping(self.ctx, rec_dict)
        db.delete_hp_ironic_switch_port_mapping(self.ctx, rec_dict)
        count = self.ctx.session.query(
            models.HPIronicSwitchPortMapping).count()
        self.assertEqual(count, 0)

    def test_get_hp_switch_port_by_switchid_portname(self):
        with self.ctx.session.begin(subtransactions=True):
            entry = models.HPSwitchPort(
                id="phy1234",
                switch_id="switch1",
                port_name="Tengig0/1",
                lag_id=None)
            self.ctx.session.add(entry)
        result = db.get_hp_switch_port_by_switchid_portname(
            self.ctx,
            {'switch_id': "switch1", 'port_name': "Tengig0/1"})
        self.assertEqual(entry, result)

    def test_get_hp_switch_lag_port_by_id(self):
        with self.ctx.session.begin(subtransactions=True):
            entry = models.HPSwitchLAGPort(
                id="lag1234",
                external_lag_id="extlag123")
            self.ctx.session.add(entry)
        result = db.get_hp_switch_lag_port_by_id(
            self.ctx, {'id': "lag1234"})
        self.assertEqual(entry, result)

    def test_get_hp_ironic_switch_port_mapping_by_neutron_port_id(self):
        with self.ctx.session.begin(subtransactions=True):
            entry = models.HPIronicSwitchPortMapping(
                neutron_port_id="n1234",
                switch_port_id=None,
                lag_id=None,
                access_type="access",
                segmentation_id=100,
                bind_requested=True)
            self.ctx.session.add(entry)
        result = db.get_hp_ironic_switch_port_mapping_by_neutron_port_id(
            self.ctx, {'neutron_port_id': "n1234"})
        self.assertEqual(entry, result)
