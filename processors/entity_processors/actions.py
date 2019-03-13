import colors

def process_actions(entity, entities):
    """Check for something on the ground and maybe pick it up?"""
    if entity['Action'] == 'PICKUP':
        pickupables = []
        for ent in entities:
            # TODO: dang this is a crappy check
            if ('Map' in ent) or (not 'Position' in ent) or (not 'Position' in entity) or (ent == entity) or ('ContainedBy' in ent and ent['ContainedBy'] == entity):
                continue
            if ent['Position']['x'] == entity['Position']['x'] and ent['Position']['y'] == entity['Position']['y']:
                pickupables.append(ent['Name'])
                entity['Inventory']['items'].append(ent)
                ent['Obscured'] = True
                del ent['Position']
                ent['ContainedBy'] = entity
        entity['Action'] = ''
        if len(pickupables) == 0:
            return [{
                'notification': {
                    'text': 'There is nothing here to pick up.',
                    'color': colors.white
                }
            }]
        return [{
            'pickupables': pickupables
        }]
    if entity['Action'] == 'DROP':
        return [{
            'droppables': entity['Inventory']['items']
        }]
    return []
