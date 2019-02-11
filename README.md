# Ansible Migration Factory Discovery Playbook
An Ansible playbook to conduct system discoveries on Unix/Linux systems with Ansible Tower.

## Variables
See the `discovered_hosts_inventory` role for many variables that can be overridden.

### Required Variables
|tower_user|yes|Ansible Tower user with access to create inventories|""|string|
|tower_pass|yes|Password to the Ansible Tower user.|""|string|
|tower_org|yes|Organization of the Ansible Tower, where the new discovery inventory will be created|""|string|
|tower_url|yes|URL to the Ansible Tower server starting with 'https://'|""|string|
|tower_verify_ssl|yes|Validate the Ansible Tower Server's SSL certificate|False|boolean|


## License
[MIT](LICENSE)

## Author Information
[Andrew J. Huffman](mailto:ahuffman@redhat.com)
