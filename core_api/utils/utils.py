from graphql_relay import from_global_id


def get_object_id(global_id):

    object_id = from_global_id(global_id).id

    if len(object_id) == 0:
        raise Exception("Incorrect global ID was provided.")

    return object_id
