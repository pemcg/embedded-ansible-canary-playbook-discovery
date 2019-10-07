#!/usr/bin/python

# Copyright: (c) 2019, Andrew J. Huffman <ahuffman@redhat.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: application_id
short_description: Identifies running applications by a scoring system
version_added: "2.8"
description:
    - "A set of users, groups, processes, ports, paths, packages, and services, along with collected ansible_facts, the application name and description to tag with, and acceptable scores for each category are passed into the module"
    - "This module returns the application name and description as ansible_facts['discovered_apps'].  If ansible_facts['discovered_apps'] already exists, this module will take the existing value and append any new values to it, otherwise the module will skip making no changes if an application is not identified with the scoring criteria provided."
application:
    description:
        - Information to "tag" a system with if the system meets all conditions from the scores option.  This is a dictionary with a name and desc field.
    type: dictionary
    default: {}
    required: True
application.name:
    description:
        - Name of the application to tag the system with if all conditions from the scores parameter are satisfied.
    type: string
    required: True
application.desc:
    description:
        - Description of the application to tag the system with if all conditions from the scores parameter are satisfied.
    type: string
    required: True
users:
    description:
        - List of users to check when identifying a running application.
    type: list
    default: []
    required: True
groups:
    description:
        - List of groups to check when identifying a running application.
    type: list
    default: []
    required: True
packages:
    description:
        - List of packages to check when identifying a running application.
    type: list
    default: []
    required: True
paths:
    description:
        - List of paths to check when identifying a running application.
    type: list
    default: []
    required: True
ports:
    description:
        - List of listening ports to check when identifying a running application.
    type: list
    default: []
    required: True
processes:
    description:
        - List of processes to check when identifying a running application.  Can be a partial process name to keep generic across OS platforms.
    type: list
    default: []
    required: True
services:
    description:
        - List of services to check when identifying a running application.
    type: list
    default: []
    required: True
facts:
    description:
        - Dictionary of collected ansible_facts to perform the application identification against.  The expected format is based on ansible-fact and Ansible Migration Factory's discovery process.
    type: dictionary
    default: {}
    required: True
scores:
    description:
        - Dictionary of scores required to properly identify the running application.  Each category requires an integer that represents the minimum count that will satisfy a >= evaluation.
        - As an example, if there are 2 users that could be present, but only 1 required to be present to identify an application, set the scores.users value to "1".
    type: dictionary
    default: {}
    required: True
scores.groups:
    description:
        - Integer that represents the minimum number of groups that must be present in order to identify an application.  The evaluation is performed by a >= check of this score.
    type: integer
    default: None
    required: True
scores.users:
    description:
        - Integer that represents the minimum number of users that must be present in order to identify an application.  The evaluation is performed by a >= check of this score.
    type: integer
    default: None
    required: True
scores.paths:
    description:
        - Integer that represents the minimum number of paths that must be present in order to identify an application.  The evaluation is performed by a >= check of this score.
    type: integer
    default: None
    required: True
scores.ports:
    description:
        - Integer that represents the minimum number of ports that must be present in order to identify an application.  The evaluation is performed by a >= check of this score.
    type: integer
    default: None
    required: True
scores.packages:
    description:
        - Integer that represents the minimum number of packages that must be present in order to identify an application.  The evaluation is performed by a >= check of this score.
    type: integer
    default: None
    required: True
scores.processes:
    description:
        - Integer that represents the minimum number of processes that must be present in order to identify an application.  The evaluation is performed by a >= check of this score.
    type: integer
    default: None
    required: True
scores.services:
    description:
        - Integer that represents the minimum number of services that must be present in order to identify an application.  The evaluation is performed by a >= check of this score.
    type: integer
    default: None
    required: True
author:
    - Andrew J. Huffman (@ahuffman)
'''

EXAMPLES = '''
# Identify Oracle Database
- name: "Identify Oracle Database Server"
  application_id:
    facts: "{{ ansible_facts }}"
    services: []
    users:
      - "oracle"
    groups:
      - "dba"
    paths:
      - "/etc/oratab"
      - "/etc/oraInst.loc"
    packages: []
    ports: []
    processes:
      - "ora_mmon_"
      - "ora_pmon_"
      - "ora_smon_"
      - "tnslsnr"
    application:
      name: "Oracle Database"
      desc: "Hosts identified as Oracle Database Servers"
    scores:
      users: 0
      groups: 0
      paths: 1
      packages: 0
      ports: 0
      processes: 3
      services: 0
'''

RETURN = '''
ansible_facts['discovered_apps']:
  - name: "Oracle Database"
    desc: "Hosts identified as Oracle Database Servers"
'''

from ansible.module_utils.basic import AnsibleModule
from os.path import exists
import jmespath


def main():
    module_args = dict(
        services=dict(
            type='list',
            default=list(),
            required=False
        ),
        users=dict(
            type='list',
            default=list(),
            required=False
        ),
        groups=dict(
            type='list',
            default=list(),
            required=False
        ),
        paths=dict(
            type='list',
            default=list(),
            required=False
        ),
        packages=dict(
            type='list',
            default=list(),
            required=False
        ),
        processes=dict(
            type='list',
            default=list(),
            required=False
        ),
        ports=dict(
            type='list',
            default=list(),
            required=False
        ),
        application=dict(
            type='dict',
            default=dict(
                name="",
                desc=""
            ),
            required=False
        ),
        scores=dict(
            type='dict',
            default=dict(
                users=0,
                groups=0,
                services=0,
                paths=0,
                packages=0,
                processes=0,
                ports=0
            ),
            required=False
        ),
        facts=dict(
            type='dict',
            required=True
        )
    )

    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    params = module.params

    # if params['output_ps_stdout_lines']:
    #     processes['ps_stdout_lines'] = raw_procs['stdout']
    # if params['output_parsed_processes']:
    #     processes['total_running_processes'] = raw_procs['total_running_processes']
    #     processes['processes'] = proc_data
    # result = {'ansible_facts': {'running_processes': processes}}
    #
    # module.exit_json(**result)

    # init counters
    svc_count = 0
    user_count = 0
    group_count = 0
    path_count = 0
    pkg_count = 0
    proc_count = 0
    port_count = 0

    chk_services = params['services']
    chk_users = params['users']
    chk_groups = params['groups']
    chk_paths = params['paths']
    chk_packages = params['packages']
    chk_processes = params['processes']
    chk_ports = params['ports']
    app_id = params['application']
    scores = params['scores']
    facts = params['facts']

    # check services
    if len(chk_services) > 0 and facts.get('services'):
        for s in chk_services:
            if facts['services'][s]:
                svc_count += 1

    # check users
    if len(chk_users) > 0 and facts.get('local_users'):
        user_expression = jmespath.compile('[*].user')
        for u in chk_users:
            if u in user_expression.search(facts['local_users']):
                user_count += 1

    # check groups
    if len(chk_groups) > 0 and facts.get('local_groups'):
        group_expression = jmespath.compile('[*].group')
        for g in chk_groups:
            if g in group_expression.search(facts['local_groups']):
                group_count += 1

    # check packages
    if len(chk_packages) > 0 and facts.get('packages'):
        for p in chk_packages:
            if facts['packages'][p]:
                pkg_count += 1

    # check processes
    if len(chk_processes) > 0 and len(facts['running_processes']['processes']) > 0:
        proc_expression = jmespath.compile('[*].command')
        for p in chk_processes:
            for proc in proc_expression.search(facts['running_processes']['processes']):
                if str(p) in str(proc):
                    proc_count += 1

    # check ports
    # if len(chk_ports) > 0:
    #     for p in chk_ports:

    # check paths
    if len(chk_paths) > 0:
        for p in chk_paths:
            if exists(p):
                path_count += 1

    # Scoring
    if svc_count >= scores['services'] and user_count >= scores['users'] and \
        group_count >= scores['groups'] and path_count >= scores['paths'] and \
        pkg_count >= scores['packages'] and proc_count >= scores['processes'] and \
        port_count >= scores['ports']:
        # App is identified
        if facts.get('discovered_apps') is None:
            discovered_apps = [app_id]
        else:
            discovered_apps = facts['discovered_apps']
            discovered_apps.append(app_id)
        result = {'ansible_facts': {'discovered_apps': discovered_apps}, 'changed': True, 'msg': {'user_count': user_count, 'group_count': group_count,'svc_count': svc_count, 'port_count': port_count, 'proc_count': proc_count, 'pkg_count': pkg_count, 'path_count': path_count}}
        module.exit_json(**result)
    else:
        # not identified
        result['msg'] = {'user_count': user_count, 'group_count': group_count,'svc_count': svc_count, 'port_count': port_count, 'proc_count': proc_count, 'pkg_count': pkg_count, 'path_count': path_count, 'proc_query': proc_expression.search(facts['running_processes']['processes'])}
        result['skipped'] = True
        module.exit_json(**result)
if __name__ == '__main__':
    main()
