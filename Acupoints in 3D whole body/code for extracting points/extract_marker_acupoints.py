from cmlibs.utils.zinc.general import ChangeManager
from cmlibs.utils.zinc.field import findOrCreateFieldStoredMeshLocation, getGroupList
from cmlibs.zinc.context import Context
from cmlibs.zinc.field import Field, FieldFindMeshLocation

node_identifier_offset = 10000
context = Context("offset_data")
region = context.getDefaultRegion()
region.readFile("boxWithAcupoints.exf") # Read in file containing acupoint geometric marker coordinates
fieldmodule = region.getFieldmodule()
# for efficiency, suppress change messages until all changes completed
with ChangeManager(fieldmodule):
    # remove all elements
    for dimension in range(3, 0, -1):
        mesh = fieldmodule.findMeshByDimension(dimension)
        mesh.destroyAllElements()
    
    # remove all nodes not in marker_group
    # groups are a special kind of field which return non-zero/true on objects in them
            
    marker_group = fieldmodule.findFieldByName("marker").castGroup()
    nodes = fieldmodule.findNodesetByFieldDomainType(Field.DOMAIN_TYPE_NODES)
    nodes.destroyNodesConditional(fieldmodule.createFieldNot(marker_group))
    # tricky loop to renumber marker nodes, since can't iterate over them while renumbering
    # assumes there is at least one node and all node identifiers are under the offset value
    print(nodes.getSize())
    while True:
       node = nodes.createNodeiterator().next()
       node_identifier = node.getIdentifier()
       # print(node_identifier)
       if node_identifier >= node_identifier_offset:
           break
       node.setIdentifier(node_identifier + node_identifier_offset)

    fitted_marker_coordinates = fieldmodule.findFieldByName("marker coordinates")  # read earlier
    region.readFile("Geometry_Fitter_Wholebody.exf") # Read in scaffold file fitted to whole body
    mesh_coordinates = fieldmodule.findFieldByName("fitted coordinates")  # read above, whatever it's called
    mesh3d = fieldmodule.findMeshByDimension(3)
    find_marker_location = fieldmodule.createFieldFindMeshLocation(fitted_marker_coordinates, mesh_coordinates, mesh3d)
    find_marker_location.setSearchMode(FieldFindMeshLocation.SEARCH_MODE_NEAREST)  # in case point is slightly outside
    
    # assign the found location into the stored location
    marker_location = fieldmodule.findFieldByName("marker_location")
       
    fieldassignment = marker_location.createFieldassignment(find_marker_location)
    fieldassignment.setNodeset(marker_group.getNodesetGroup(nodes))
    print(fieldassignment.isValid())
    fieldassignment.assign()
        

# this is the new male body with the offset marker data
region.writeFile("3DWholeBody_acupoints.exf")
