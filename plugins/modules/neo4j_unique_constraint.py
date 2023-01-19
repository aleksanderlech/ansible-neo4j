#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.2.0',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: neo4j_unique_constraint

short_description: Ensures the index existence in Neo4j database

description:
    - "This is will ensure that Neo4j database has an unique constraint defined matching provided parameters."
    - "If the constraint does not exist it will be created."
    - "If the constraint exist but does not match the current parameters it won't be dropped. You should manually remove it first."

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
    neo4j_encryption:
        description:
           - Whether to enable secure Neo4j connection
    constraint_label:
        description:
            - The constraint desired node label that it belongs to
        required: "true"    
    index_properties:
        description:
            - The constraint desired node properties to be unique
        required: "true"
    neo4j_encryption:
        description:
           - Whether to enable secure Neo4j connection
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
        neo4j_encryption=dict(type='bool', default=False),
        constraint_label=dict(type='str', required=True),
        constraint_property=dict(type='str', required=True)
    )
    module = AnsibleModule(argument_spec=module_args)

    # Read parameters

    neo4j_host = module.params['neo4j_host']
    neo4j_port = module.params['neo4j_port']
    neo4j_user = module.params['neo4j_user']
    neo4j_password = module.params['neo4j_password']
    neo4j_encryption = module.params['neo4j_encryption']
    constraint_label = module.params['constraint_label']
    constraint_property = module.params['constraint_property']

    executor = Neo4jExecutor(neo4j_host, neo4j_port, neo4j_user, neo4j_password, neo4j_encryption)

    if not executor.constraint_exists([constraint_label], [constraint_property]):
        executor.execute(lambda session: session.run(
            f"CREATE CONSTRAINT FOR (n:{constraint_label}) REQUIRE n.{constraint_property} IS UNIQUE"))
        changed = True
    else:
        changed = False

    executor.close()
    module.exit_json(changed=changed)


if __name__ == '__main__':
    main()
