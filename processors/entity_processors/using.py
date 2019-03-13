import colors

from processors.entity_processors.using_processors.healing import process_healing
from processors.entity_processors.using_processors.dropping import process_dropping

def process_using(entity, entities, fov_map):
    """Bookkeeping for using objects ()"""
    healing_actions = []
    dropping_actions = []
    if 'Healing' in entity and 'ContainedBy' in entity and 'Using' in entity:
        healing_actions = process_healing(entity)
        del entity['Using'] # stop using it
    if 'Dropping' in entity:
        dropping_actions = process_dropping(entity)
        del entity['Dropping'] # stop dropping it


    return healing_actions + dropping_actions
