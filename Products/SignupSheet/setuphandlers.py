from Products.CMFCore.utils import getToolByName

_PROPERTIES = [
    dict(name='traverse_to_thankyou', type_='boolean', value=False),
    dict(name='first_last_name_order', type_='string', value='fl'),
]


def setupVarious(context):
    if context.readDataFile('products_signupsheet_various.txt') is None:
        return
    
    portal = context.getSite()
    
    # Adding a property sheet, specific for enabling/disabling the traverse to the
    # thankyou page. This fix BAD Varnish problem and privacy issue
    ptool = portal.portal_properties
    props = ptool.signupsheet_properties

    for prop in _PROPERTIES:
        if not props.hasProperty(prop['name']):
            props.manage_addProperty(prop['name'], prop['value'], prop['type_'])

    
    # Add a form controller that traverse to the post page so the proper state can be set
    # on the registrant.  Should be part of Generic Setup but examples for CMFFormController are missings   
    controller = getToolByName(portal, 'portal_form_controller')
    controller.addFormAction('validate_integrity','success','Registrant', None, 'traverse_to', 'string:registrant_post')
                                 
    # Remove from use_folder_tabs
    properties = getToolByName(portal, 'portal_properties')
    siteProperties = properties.site_properties
    
    useFolderTabs = list(siteProperties.getProperty('use_folder_tabs', []))
    if 'SignupSheet' in useFolderTabs:
        useFolderTabs.remove('SignupSheet')
    siteProperties.manage_changeProperties(use_folder_tabs = useFolderTabs)

    # Remove from typesLinkToFolderContentsInFC 
    typesLinkToFolderContentsInFC = list(siteProperties.getProperty('typesLinkToFolderContentsInFC'))
    if 'SignupSheet' in typesLinkToFolderContentsInFC:
        typesLinkToFolderContentsInFC.remove('SignupSheet')
    siteProperties.manage_changeProperties(typesLinkToFolderContentsInFC = typesLinkToFolderContentsInFC)

    # Add SignupSheet to kupu's linkable and media
    # types
    kupuTool = getToolByName(portal, 'kupu_library_tool', None)
    if kupuTool is not None:
        linkable = list(kupuTool.getPortalTypesForResourceType('linkable'))
        mediaobject = list(kupuTool.getPortalTypesForResourceType('mediaobject'))
        if 'SignupSheet' not in linkable:
            linkable.append('SignupSheet')
        # kupu_library_tool has an idiotic interface, basically written purely to
        # work with its configuration page. :-(
        kupuTool.updateResourceTypes(({'resource_type' : 'linkable',
                                       'old_type'      : 'linkable',
                                       'portal_types'  :  linkable},
                                      {'resource_type' : 'mediaobject',
                                       'old_type'      : 'mediaobject',
                                       'portal_types'  :  mediaobject},))

    install_dependencies(portal)                                       
                                       
def install_dependencies(portal):
    """ATSENG does not a have a GS profile to user for install"""
    qi = getToolByName(portal,'portal_quickinstaller')
    qi.installProducts(('ATSchemaEditorNG',))
    
