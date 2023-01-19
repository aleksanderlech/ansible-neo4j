# Neo4j Collection
This collection helps to create indexes in Neo4j using Ansible.

## Tested with

- Ansible 2.9.7, 2.13.4
- Neo4 4.0.4, 5.2, 5.3

## Compatibility Matrix

| Version | No4j |
|---------|------|
| 1.0.0   | 3.x  |
| 1.1.0   | 4.x  |
| 1.2.0   | 5.x  |

## External requirements

- neo4j [pip]

## Using this collection

    - name: Ensure the name index
      community.neo4j.neo4j_index:
          neo4j_host: "{{ neo4j_host }}"
          neo4j_user: "{{ neo4j_user }}"
          neo4j_password: "{{ neo4j_password }}"
          index_label: 'Customer'
          index_properties: ['name']

See [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## Contributing to this collection

Any contributions welcomed. Currently just a basic module supporting few schema operations.
[Ansible Community Guide](https://docs.ansible.com/ansible/latest/community/index.html).

## More information

<!-- List out where the user can find additional information, such as working group meeting times, slack/IRC channels, or documentation for the product this collection automates. At a minimum, link to: -->

- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)

## Licensing

GNU General Public License v3.0 or later.

See [LICENCE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
