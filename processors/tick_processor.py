from processors.entity_processors.death import process_death
from processors.entity_processors.using import process_using
from processors.entity_processors.actions import process_actions
from processors.entity_processors.ai import process_ai
from processors.entity_processors.movement import process_movement
from processors.entity_processors.memory import process_memory

def process_tick(entity, entities, fov_map, mouse):
    """A convenience function to apply several tick processor functions to entities"""
    death_actions = []
    using_actions = []
    action_actions = []
    ai_actions = []
    movement_actions = []
    memory_actions = []
    # you should really try to be clear on what your processors need and expect
    # NOTE: Health should come first, because if something is dead, no sense in having it think or move
    if 'Health' in entity:
        death_actions = process_death(entity, fov_map)
    if 'Using' in entity or 'Dropping' in entity:
        using_actions = process_using(entity, entities, fov_map)
    if 'Action' in entity:
        action_actions = process_actions(entity, entities)
    # NOTE: AI should come next, as it might inform the movement processing
    if 'Goal' in entity:
        ai_actions = process_ai(entity, entities, fov_map)
    # NOTE: Movement should come before position, as it might inform memory
    if 'Movement' in entity:
        movement_actions = process_movement(entity, entities, fov_map)
    if 'Seen' in entity:
        memory_actions = process_memory(entity, fov_map)

    return death_actions + using_actions + action_actions + movement_actions + memory_actions + ai_actions
