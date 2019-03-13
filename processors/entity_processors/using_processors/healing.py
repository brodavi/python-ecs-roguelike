import colors

def process_healing(entity):
    """Something which is ContainedBy (an item, probably) and has the property Healing"""
    results = []

    if 'Empty' in entity:
        return results

    if entity['ContainedBy']['Health'] == entity['ContainedBy']['MaxHealth']:
        results.append({
            'notification': {
                'text': 'You are already at full health',
                'color': colors.yellow
            }
        })
    else:
        entity['ContainedBy']['Health'] += entity['Healing']

        # clamp to max health value
        if entity['ContainedBy']['Health'] > entity['ContainedBy']['MaxHealth']:
            entity['ContainedBy']['Health'] = entity['ContainedBy']['MaxHealth']

        del entity['Healing'] # now it is just an empty bottle
        entity['Empty'] = True
        entity['Name'] = 'empty bottle'
        entity['Color'] = colors.white
        # TODO: add weight?
        results.append({
            'notification': {
                'text': 'Your wounds start to feel better!',
                'color': colors.green
            }
        })

    return results
