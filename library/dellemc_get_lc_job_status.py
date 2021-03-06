#!/usr/bin/python
# _*_ coding: utf-8 _*_

#
# Dell EMC OpenManage Ansible Modules
# Version 1.0
# Copyright (C) 2018 Dell Inc.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries.
# Other trademarks may be trademarks of their respective owners.
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: dellemc_get_lc_job_status
short_description: Get the status of a Lifecycle Controller Job.
version_added: "2.3"
description: Get the status of a Lifecycle Controller job using its JOB ID.
options:
    idrac_ip:
        required: True
        description: iDRAC IP Address.
    idrac_user:
        required: True
        description: iDRAC username.
    idrac_pwd:
        required: True
        description: iDRAC user password.
    idrac_port:
        required: False
        description: iDRAC port.
        default: 443
    job_id:
        required: True
        description: JOB ID in the format "JID_123456789012".

requirements:
    - "omsdk"
    - "python >= 2.7.5"
author: "Rajeev Arakkal (@rajeevarakkal)"

"""

EXAMPLES = """
---
- name: Get LC Job Status
  dellemc_get_lc_job_status:
       idrac_ip:   "xx.xx.xx.xx"
       idrac_user: "xxxx"
       idrac_pwd:  "xxxxxxxx"
       job_id:     "JID_1234567890"
"""

RETURNS = """
dest:
    description: Displays the status of a Lifecycle Controller job.
    returned: success
    type: string
"""


from ansible.module_utils.dellemc_idrac import iDRACConnection
from ansible.module_utils.basic import AnsibleModule


def run_get_lc_job_status(idrac, module):
    """
    Get status of a Lifecycle Controller Job given a JOB ID

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """
    msg = {}
    msg['failed'] = False
    msg['changed'] = False
    err = False

    try:
        # idrac.use_redfish = True
        msg['msg'] = idrac.job_mgr.get_job_status(module.params['job_id'])

    except Exception as e:
        err = True
        msg['msg'] = "Error: %s" % str(e)
        msg['failed'] = True
    return msg, err


# Main
def main():
    module = AnsibleModule(
        argument_spec=dict(

            # iDRAC Credentials
            idrac_ip=dict(required=True, type='str'),
            idrac_user=dict(required=True, type='str'),
            idrac_pwd=dict(required=True,
                           type='str', no_log=True),
            idrac_port=dict(required=False, default=443, type='int'),

            # JOB ID
            job_id=dict(required=True, type='str')
        ),

        supports_check_mode=False)

    # Connect to iDRAC
    idrac_conn = iDRACConnection(module)
    idrac = idrac_conn.connect()
    msg, err = run_get_lc_job_status(idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)


if __name__ == '__main__':
    main()
