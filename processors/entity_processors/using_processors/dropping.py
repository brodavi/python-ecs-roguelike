import colors

def process_dropping(entity):
    """Just dropping something.. give it ContainedBy's x and y"""
    results = []

    print('we are going to drop: ', entity)

    entity['Position'] = {'x': 0, 'y': 0}
    entity['Position']['x'] = entity['ContainedBy']['Position']['x']
    entity['Position']['y'] = entity['ContainedBy']['Position']['y']

    entity['ContainedBy']['Inventory']['items'].remove(entity)

    del entity['Obscured']
    del entity['ContainedBy']

    return results
