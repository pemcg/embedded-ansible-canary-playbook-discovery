# amf-seed-coalmine
An Ansible role to seed the Coalmine web-service.

## Role Variables
| Variable Name | Default Value | Description | Type |
|---|---|---|:---:|
|tower_user|""|Tower username with access to read inventories|string|
|tower_pass|""|Tower password for `tower_user`|string|
|tower_url|""|URL to the Tower server|string|
|tower_verify_ssl|False|Whether or not to validate the Tower server's SSL certificate|boolean|
|tower_legacy_inventory_name|""|Name of the inventory that the Ansible Migration Factory discovery playbook targets, to obtain a list of hosts and seed the webservice database with|string|
|pg_user|"postgres"|Username of the postgres user for the Coalmine web-service|string|
|pg_group|"postgres"|Groupname of the postgres user for the Coalmine web-service|string|
|pg_home|"/var/lib/postgres"|Home directory of the postgres user for the Coalmine web-service|string|

## License
[MIT](LICENSE)

## Author Information
[Andrew J. Huffman](mailto:ahuffman@redhat.com)
