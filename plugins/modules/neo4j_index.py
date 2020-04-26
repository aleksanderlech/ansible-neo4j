#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.0.0',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: neo4j_index

short_description: Ensures the index existence in Neo4j database

description:
    - "This is will ensure that Neo4j database has an index defined matching provided parameters."
    - "If the index does not exist it will be created."
    - "If the index exist but does not match the current parameters it won't be dropped. You should manually remove it first."

options:
    neo4j_host:
        description:
            - Target Neo4j database host
        default: "localhost"
    neo4j_port:
        description:
            - Target Neo4j database port
        default: 7687
    neo4j_user:
        description:
            - Target Neo4j database user name
        required: "true"
    neo4j_password:
        description:
            - Target Neo4j database user password
        required: "true"
    neo4j_index_name:
    index_label:
        description:
            - The index desired node label that should be included in the index
        required: "true"    
    index_properties:
        description:
            - The full text index desired node properties to be indexed
        required: "true"
author:
    - Aleksander Lech (me@aleksander-lech.com)
'''

from ansible.module_utils.basic import *
from ansible_collections.community.neo4j.plugins.module_utils.utils import Neo4jExecutor


def main():
    # Define module

    module_args = dict(
        neo4j_host=dict(type='str', default="localhost"),
        neo4j_port=dict(type='int', default=7687),
        neo4j_user=dict(type='str', required=True),
        neo4j_password=dict(type='str', required=True, no_log=True),
        index_label=dict(type='str', required=True),
        index_properties=dict(type='list', required=True)
    )
    module = AnsibleModule(argument_spec=module_args)

    # Read parameters

    neo4j_host = module.params['neo4j_host']
    neo4j_port = module.params['neo4j_port']
    neo4j_user = module.params['neo4j_user']
    neo4j_password = module.params['neo4j_password']
    index_label = module.params['index_label']
    index_properties = module.params['index_properties']

    executor = Neo4jExecutor(neo4j_host, neo4j_port, neo4j_user, neo4j_password)

    result = executor.execute(lambda session: session.run(f"CREATE INDEX ON :{index_label}({','.join(index_properties)})"))
    added = result.summary().counters.indexes_added == 1

    executor.close()
    module.exit_json(changed=added)


if __name__ == '__main__':
    main()
