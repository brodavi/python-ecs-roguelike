components = {}

def getComponent(componentName):
    """Given a component name, return the actual list"""
    return components[componentName]

def registerComponent(name):
    """Create a component (really just a dict of IDs to data)"""
    entities = []
    # maybe do a check to see if the data matches the existing structure?
    # base case is componentData = None and set it
    components[name] = entities

def createProcessor(name, selectionList, process):
    """Give it a name, a selection list, and a function, and it will return a processor"""
    entities = []
    return {
      'entities': entities,
      'selectionList': selectionList,
      'name': name,
      'process': process
    }

def runProcessor(processorName):
    """Provide the name of the processor, and it will run"""
    # NOTE: we are assuming that the 'entities' attribute here is full of
    # entityIDs (ints) and the processor process function only accesses the
    # components as specified in the selectionList... automate constraint?
    # or trust the user to keep track of it?

    # NOTE: when an entity is given a component, at that point, maybe we check
    # all the components where the entity is listed, and if it matches all the
    # selectionList of any processors, add the entity to that processor's
    # entity list
    processor = processors[processorName]
    for entity in processor['entities']:
        processor['process'](entity)

lastID = 0
def createEntity(dict):
    """A function to create an entity with all its components all at once"""
    lastID += 1
    for componentName in dict:
        setComponentData(lastID, componentName, dict[key])
    return lastID # this is really all the entity is

def getComponentData(entity, componentName):
    """Given an entity and a component, get the associated data"""
    component = getComponent(componentName)
    return component[entity]

def setComponentData(entity, componentName, value):
    """Modify component data for an entity"""
    component = getComponent(componentName)
    component[entity] = value

def removeComponent(entity, componentName):
    """Remove a component to an entity (actually just removing the entityID from the component list)"""
    component = getComponent(componentName)
    del component[entity]
