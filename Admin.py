##############################################################################
# Project:	WebSphere 6.1 Automation - Core Library
# Package: 	was61core
# Module: 	Admin
# Authors: 	Nana Fadnis & Leao Fernandes
# Start Date: 	01/01/2008
###############################################################################
import re
import Utils
###############################################################################
# Classes
###############################################################################
class AdminError(Utils.Error):
  
  def __init__(self,msg=''):
    msg = "AdminError: %s" % msg
    Utils.Error.__init__(self,msg)

###############################################################################
# Functions
###############################################################################
"""
FUNCTION:       setAdminBeans
ARGS:           AdminConfig, AdminControl, AdminApp, AdminTask, Help
RETURNS:        Hash Map object containing references to the above 5 MBeans
DESCRIPTION:    This is a utility function that takes references to 5 MBean
                objects that are available to the main script (that is passed
                to 'wsadmin' interface), and creates and returns  a Hash Map object
                containing these references. This map object is then passed as
                the first argument to any other function from the coreWasFuncs
                module that may be invoked by the main script.
"""
def setAdminBeans(AdminConfig, AdminControl, AdminApp, AdminTask, Help):
  admBeans = {}
  admBeans['AdminConfig'] = AdminConfig
  admBeans['AdminControl'] = AdminControl
  admBeans['AdminApp'] = AdminApp
  admBeans['AdminTask'] = AdminTask
  admBeans['Help'] = Help
  return admBeans
#end setAdminBeans
#-------------------------------------------------------------------------------
"""
FUNCTION:       showObject
ARGS:           admBeans, objID
RETURNS:        Shows attributes of the object
DESCRIPTION:    This function calls show function of AdminConfig object
"""
def showObject(admBeans, objId):
  AdminConfig = admBeans['AdminConfig']
  return AdminConfig.show(objId)
#end showObject
#-------------------------------------------------------------------------------
"""
FUNCTION:       getVarmapFromID
ARGS:           admBeans (HashMap object), varmapID
RETURNS:        Hash Map object containing name-value pairs in the VariableMap
DESCRIPTION:    The process to get the name-value pairs out of a VariableMap at 
		any of the four scopes: Cell,Node,Cluster,Server, is a little bit
		unintuitive. This function isolates that process, and is called
		from within getVariables function  defined in Cell, Node, Cluster
		and Server modules.
"""
def getVarmapFromID(admBeans, mapId):

  AdminConfig = admBeans['AdminConfig']
  entries = AdminConfig.showAttribute(mapId, 'entries')

  #take off open and close brackets 
  entries = re.sub(r'^\[|\]$', '', entries)

  variableMap = {}
  if entries:
    entries = entries.split(' ')
    for entry in entries:
      name = AdminConfig.showAttribute( entry, 'symbolicName' )
      value = AdminConfig.showAttribute( entry, 'value' )
      variableMap[name] = value
  return variableMap
#end getVarmapFromID
#-------------------------------------------------------------------------------
"""
FUNCTION:       getTemplateIdFromName
ARGS:           admBeans (HashMap object), objectType, templateName
RETURNS:        ID of the template of object type specified 'objectType' argument
		and 'name' attribute matching the 'templateName' argument.
DESCRIPTION:    For this to work you must specify the exact name of the template.
"""
def getTemplateIdFromName(admBeans, objectType, templateName):

  # Get reference to AdminConfig object.
  AdminConfig = admBeans['AdminConfig']

  # Get a list of templates and from that choose the one that matches the name.
  tmpltId = ''
  tmpltIdList = AdminConfig.listTemplates(objectType, templateName).splitlines()
  for tId in tmpltIdList:
    if AdminConfig.showAttribute(tId, 'name') == templateName:
      tmpltId = tId
      break
  
  return tmpltId

#end getTemplateIdFromName
#-------------------------------------------------------------------------------
"""
FUNCTION:       createCluster
ARGS:           admBeans, propMap, parentId
RETURNS:        ID of the newly created Cluster.
DESCRIPTION:    Used to create a new Cluster in given the cellId
"""
def createCluster(admBeans, propMap, parentId):

  # required attributes.
  if not propMap.has_key('name') or not propMap['name']:
    raise AdminError("In createCluster: Required attribute 'name' is missing.")
  name =  propMap['name']
  attrList = [['name',  name]]

  # Other attributes.
  if propMap.has_key('description'):
    attrList.append(['description', propMap['description']])
  if propMap.has_key('stateManagement.initialState'):
    attrList.append(['stateManagement', [['initialState', propMap['stateManagement.initialState']]]])

  # Get reference to AdminConfig object
  AdminConfig = admBeans['AdminConfig']

  # Now Create the Cluster. 
  return AdminConfig.create('ServerCluster', parentId, attrList)

#end createCluster
#-------------------------------------------------------------------------------
"""
FUNCTION:       createClusterMember
ARGS:           admBeans, propMap, clusterId, nodeId
RETURNS:        ID of the newly-created ClusterMember.
DESCRIPTION:    Used to create a new ClusterMember given the clusterId and nodeId
"""
def createClusterMember(admBeans, propMap, clusterId, nodeId):

  # required attributes.
  if not propMap.has_key('memberName') or not propMap['memberName']:
    raise AdminError("In createClusterMember: Required attribute 'memberName' is missing.")
  memberName =  propMap['memberName']
  attrList = [['memberName',  memberName]]

  # Other attributes.

  # Get reference to AdminConfig object
  AdminConfig = admBeans['AdminConfig']

  # Now Create the Library. 
  return AdminConfig.createClusterMember(clusterId, nodeId, attrList)

#end createClusterMember
#-------------------------------------------------------------------------------
"""
FUNCTION:       createJDBCProvider
ARGS:           admBeans, propMap, parentId 
RETURNS:        ID of the newly created JDBCProvider.
DESCRIPTION:    Used to create a new JDBCProvider at any scope identified
		by the parentId. 
"""
def createJDBCProvider(admBeans, propMap, parentId):

  # Check required parameters.
  if not propMap.has_key('name') or not propMap['name']:
    raise AdminError("In createJDBCProvider: Required attribute 'name' is missing.")
  name =  propMap['name']

  if not propMap.has_key('templateName') or not propMap['templateName']:
    if not propMap.has_key('implementationClassName') or not propMap['implementationClassName']:
      raise AdminError("In createJDBCProvider: One of 'implementationClassName' or 'templateName' must be specified.")
    else:
      templateName = ''
      implementationClassName = propMap['implementationClassName']
  else:
      templateName = propMap['templateName']
      implementationClassName = ''

  # Get reference to AdminConfig object.
  AdminConfig = admBeans['AdminConfig']

  # Set attribute list
  attrList = [['name',  name]]
  
  if propMap.has_key('classpath'):
    attrList.append(['classpath', propMap['classpath']])

  # Create a new JDBCProvider
  if templateName:
    tmpltId = getTemplateIdFromName(admBeans,'JDBCProvider',templateName)
    if not tmpltId:
      raise AdminError("In createJDBCProvider: Null id for template \'%s\'." % templateName)
    print "Creating JDBCProvider %s using template %s" % (name, templateName)
    id = AdminConfig.createUsingTemplate('JDBCProvider', parentId, attrList, tmpltId)
  else:
    attrList.append(['implementationClassName', implementationClassName])
    if propMap.has_key('xa') and propMap['xa']:
      attrList.append(['xa', propMap['xa']])
    id = AdminConfig.create('JDBCProvider', parentId, attrList)

  return id

#end createJDBCProvider
#-------------------------------------------------------------------------------
"""
FUNCTION:       createDataSource
ARGS:           admBeans, propMap, parentId
RETURNS:        ID of the newly created DataSource.
DESCRIPTION:    Used to create a new DataSource in a scope given in terms of
		the parentId
"""
def createDataSource(admBeans, propMap, parentId):

  # required attributes.
  if not propMap.has_key('name') or not propMap['name']:
    raise AdminError("In createDataSource: Required attribute 'name' is missing.")
  name =  propMap['name']
  attrList = [['name',  name]]

  if not propMap.has_key('jndiName') or not propMap['jndiName']:
    raise AdminError("In createJDBCProvider: Required attribute 'jndiName' is missing.")
  attrList.append(['jndiName', propMap['jndiName']])

  # Other attributes.
  if propMap.has_key('description'):
    attrList.append(['description', propMap['description']])
  if propMap.has_key('statementCacheSize'):
    attrList.append(['statementCacheSize', propMap['statementCacheSize']])
  if propMap.has_key('authDataAlias'):
    attrList.append(['authDataAlias', propMap['authDataAlias']])
  if propMap.has_key('datasourceHelperClassname'):
    attrList.append(['datasourceHelperClassname', propMap['datasourceHelperClassname']])

  # ConnectionPool settings
  cpAttrList = []
  if propMap.has_key('connectionPool.minConnections'):
    cpAttrList.append(['minConnections', propMap['connectionPool.minConnections']])
  if propMap.has_key('connectionPool.maxConnections'):
    cpAttrList.append(['maxConnections', propMap['connectionPool.maxConnections']])
  if propMap.has_key('connectionPool.connectionTimeout'):
    cpAttrList.append(['connectionTimeout',propMap['connectionPool.connectionTimeout']])
  if propMap.has_key('connectionPool.unusedTimeout'):
    cpAttrList.append(['unusedTimeout', propMap['connectionPool.unusedTimeout']])
  if propMap.has_key('connectionPool.unusedTimeout'):
    cpAttrList.append(['agedTimeout', propMap['connectionPool.agedTimeout']])
  if propMap.has_key('connectionPool.reapTime'):
    cpAttrList.append(['reapTime', propMap['connectionPool.reapTime']])
  if propMap.has_key('connectionPool.purgePolicy'):
    cpAttrList.append(['purgePolicy', propMap['connectionPool.purgePolicy']])
  if len(cpAttrList) > 0:
    attrList.append(['connectionPool', cpAttrList])

  # Custom properties
  rpAttrsList = []
  patt = re.compile(r'^customProperty\.(.+)$')
  for k in propMap.keys():
    match = patt.search(k)
    if match:
      name = match.group(1)
      value = propMap[k]
      rpAttrsList.append([['name',name],['value',value]])
  if len(rpAttrsList) > 0:
    attrList.append(['propertySet', [['resourceProperties', rpAttrsList]]])

  # Get reference to AdminConfig object
  AdminConfig = admBeans['AdminConfig']

  # Now Create the DataSource. Check if the template had been specified, if
  # yes get its id and use it to create, otherwise create without template.
  #templateName = ''
  #if propMap.has_key('templateName'):
  #  templateName = propMap['templateName']
  #if templateName:
  #  tmpltId = getTemplateIdFromName(admBeans,'DataSource',templateName)

  # Check if 'useTemplate' is turned off (default is to use template), and if not
  # get template ID by matching the providerType of the JDBCProvider that is the 
  # parent of this DataSource.
  tmpltId = ''
  templateName = ''
  if not propMap.has_key('useTemplate') or not propMap['useTemplate'] == 'false':
    prvdrType = AdminConfig.showAttribute(parentId, 'providerType')
    if prvdrType:
      tList = AdminConfig.listTemplates('DataSource').splitlines()
      for tid in tList:
        if not tid:
          continue		
	if AdminConfig.showAttribute(tid, 'providerType') == prvdrType:
	  templateName = AdminConfig.showAttribute(tid, 'name')
          tmpltId = tid
	  break
  if tmpltId:
    print "Creating DataSource %s using template %s" % (name, templateName)
    id = AdminConfig.createUsingTemplate('DataSource', parentId, attrList, tmpltId)
  else:
    print "Creating DataSource %s without using a template" % name
    id = AdminConfig.create('DataSource', parentId, attrList)
  return id

#end createDataSource
#-------------------------------------------------------------------------------
"""
FUNCTION:       createLibrary
ARGS:           admBeans, propMap, parentId
RETURNS:        ID of the newly created Library.
DESCRIPTION:    Used to create a new Library in a scope given in terms of
		the parentId
"""
def createLibrary(admBeans, propMap, parentId):

  # required attributes.
  if not propMap.has_key('name') or not propMap['name']:
    raise AdminError("In createLibrary: Required attribute 'name' is missing.")
  name =  propMap['name']
  attrList = [['name',  name]]

  # description attribute.
  if propMap.has_key('description'):
    attrList.append(['description', propMap['description']])  

  # classpath attribute.
  cp = []
  patt = re.compile(r'^classpath\d{0,}$')
  for k in propMap.keys():
    match = patt.search(k)
    if match:
      cp.append(propMap[k])
  if len(cp) > 0:
    cp.reverse()
    cpStr = ";".join(cp)
    attrList.append(['classPath', cpStr])

  # nativepath attribute.
  np = []
  patt = re.compile(r'^nativepath\d{0,}$')
  for k in propMap.keys():
    match = patt.search(k)
    if match:
      np.append(propMap[k])
  if len(np) > 0:
    np.reverse()
    npStr = ";".join(np)
    attrList.append(['nativePath', npStr])

  # Get reference to AdminConfig object
  AdminConfig = admBeans['AdminConfig']

  # Now Create the Library. 
  return AdminConfig.create('Library', parentId, attrList)

#end createLibrary
#-------------------------------------------------------------------------------
"""
FUNCTION:       createSIBJMSConnectionFactory
ARGS:           admBeans, propMap, scopeId
RETURNS:        ID of the newly created SIBJMSConnectionFactory.
DESCRIPTION:    Used to create a new SIBJMSConnectionFactory in a scope given in terms of
		the scopeId
"""
def createSIBJMSConnectionFactory(admBeans, propMap, scopeId):

  # required attributes.
  if not propMap.has_key('name') or not propMap['name']:
    raise AdminError("In createSIBJMSConnectionFactory: Required attribute 'name' is missing.")
  name =  propMap['name']
  attrList = ['-name',  name]

  if not propMap.has_key('jndiName') or not propMap['jndiName']:
    raise AdminError("In createSIBJMSConnectionFactory: Required attribute 'jndiName' is missing.")
  attrList.extend(['-jndiName', propMap['jndiName']])

  if not propMap.has_key('busName') or not propMap['busName']:
    raise AdminError("In createSIBJMSConnectionFactory: Required attribute 'busName' is missing.")
  attrList.extend(['-busName', propMap['busName']])

  # Other attributes
  #----------------------
  if propMap.has_key('description'):
    attrList.extend(['-description', propMap['description']])

  # Get reference to AdminConfig object
  AdminTask = admBeans['AdminTask']

  # Create
  #----------------------
  print "Creating a new createSIBJMSConnectionFactory \'%s\'." % name
  return AdminTask.createSIBJMSConnectionFactory(scopeId, attrList)

#end createSIBJMSConnectionFactory
#-------------------------------------------------------------------------------
"""
FUNCTION:       createSIBJMSQueue
ARGS:           admBeans, propMap, scopeId
RETURNS:        ID of the newly created SIBJMSQueue.
DESCRIPTION:    Used to create a new SIBJMSQueue in a scope given in terms of
		the scopeId
"""
def createSIBJMSQueue(admBeans, propMap, scopeId):

  # required attributes.
  if not propMap.has_key('name') or not propMap['name']:
    raise AdminError("In createSIBJMSQueue: Required attribute 'name' is missing.")
  name =  propMap['name']
  attrList = ['-name',  name]

  if not propMap.has_key('jndiName') or not propMap['jndiName']:
    raise AdminError("In createSIBJMSQueue: Required attribute 'jndiName' is missing.")
  attrList.extend(['-jndiName', propMap['jndiName']])

  if not propMap.has_key('queueName') or not propMap['queueName']:
    raise AdminError("In createSIBJMSQueue: Required attribute 'queueName' is missing.")
  attrList.extend(['-queueName', propMap['queueName']])

  # Other attributes
  #----------------------
  if propMap.has_key('description'):
    attrList.extend(['-description', propMap['description']])

  # Get reference to AdminConfig object
  AdminTask = admBeans['AdminTask']

  # Create
  #----------------------
  print "Creating a new SIBJMSQueue \'%s\'." % name
  return AdminTask.createSIBJMSQueue(scopeId, attrList)

#end createSIBJMSQueue
#-------------------------------------------------------------------------------
"""
FUNCTION:       createMQQueueConnectionFactory
ARGS:           admBeans, propMap, parentId
RETURNS:        ID of the newly created MQQueueConnectionFactory.
DESCRIPTION:    Used to create a new MQQueueConnectionFactory in a scope given in terms of
		the parentId
"""
def createMQQueueConnectionFactory(admBeans, propMap, parentId):

  # required attributes.
  if not propMap.has_key('name') or not propMap['name']:
    raise AdminError("In createMQQueueConnectionFactory: Required attribute 'name' is missing.")
  name =  propMap['name']
  attrList = [['name',  name]]
  if not propMap.has_key('jndiName') or not propMap['jndiName']:
    raise AdminError("In createMQQueueConnectionFactory: Required attribute 'jndiName' is missing.")
  attrList.append(['jndiName', propMap['jndiName']])

  # Other attributes
  #----------------------
  if propMap.has_key('description'):
    attrList.append(['description', propMap['description']])
  if propMap.has_key('authDataAlias'):
    attrList.append(['authDataAlias', propMap['authDataAlias']])
  if propMap.has_key('queueManager'):
    attrList.append(['queueManager', propMap['queueManager']])
  if propMap.has_key('host'):
    attrList.append(['host', propMap['host']])
  if propMap.has_key('port'):
    attrList.append(['port', propMap['port']])
  if propMap.has_key('channel'):
    attrList.append(['channel', propMap['channel']])
  if propMap.has_key('msgRetention'):
    attrList.append(['msgRetention', propMap['msgRetention']])
  if propMap.has_key('XAEnabled'):
    attrList.append(['XAEnabled', propMap['XAEnabled']])
  if propMap.has_key('transportType'):
    attrList.append(['transportType', propMap['transportType']])
  if propMap.has_key('useConnectionPooling'):
    attrList.append(['useConnectionPooling', propMap['useConnectionPooling']])
  if propMap.has_key('mappingConfigAlias'):
    attrList.append(['mapping', [['mappingConfigAlias', propMap['mappingConfigAlias']]]])

  # Get reference to AdminConfig object
  AdminConfig = admBeans['AdminConfig']

  # Create
  #----------------------
  print "Creating a new MQQueueConnectionFactory \'%s\'." % name
  return AdminConfig.create('MQQueueConnectionFactory', parentId, attrList)
#end createMQQueueConnectionFactory
#-------------------------------------------------------------------------------
"""
FUNCTION:       createMQQueue
ARGS:           admBeans, propMap, parentId
RETURNS:        ID of the newly created MQQueue.
DESCRIPTION:    Used to create a new MQQueue in a scope given in terms of
		the parentId
"""
def createMQQueue(admBeans, propMap, parentId):

  # required attributes.
  if not propMap.has_key('name') or not propMap['name']:
    raise AdminError("In createMQQueue: Required attribute 'name' is missing.")
  name =  propMap['name']
  attrList = [['name',  name]]
  if not propMap.has_key('jndiName') or not propMap['jndiName']:
    raise AdminError("In createMQQueue: Required attribute 'jndiName' is missing.")
  attrList.append(['jndiName', propMap['jndiName']])
  if not propMap.has_key('baseQueueName'):
    raise AdminError("In createMQQueue: Required attribute 'baseQueueName' is missing.")
  baseQueueName = propMap['baseQueueName']
  attrList.append(['baseQueueName', baseQueueName])

  # Other attributes
  #----------------------
  if propMap.has_key('description'):
    attrList.append(['description', propMap['description']])
  if propMap.has_key('userName'):
    attrList.append(['userName', propMap['userName']])
  if propMap.has_key('password'):
    attrList.append(['password', propMap['password']])
  if propMap.has_key('category'):
    attrList.append(['category', propMap['category']])
  if propMap.has_key('baseQueueName'):
    attrList.append(['baseQueueName', propMap['baseQueueName']])
  if propMap.has_key('baseQueueManagerName'):
    attrList.append(['baseQueueManagerName', propMap['baseQueueManagerName']])
  if propMap.has_key('persistence'):
    attrList.append(['persistence', propMap['persistence']])
  if propMap.has_key('priority'):
    attrList.append(['priority', propMap['priority']])
  if propMap.has_key('expiry'):
    attrList.append(['expiry', propMap['expiry']])
  if propMap.has_key('specifiedPriority'):
    attrList.append(['specifiedPriority', propMap['specifiedPriority']])
  if propMap.has_key('specifiedExpiry'):
    attrList.append(['specifiedExpiry', propMap['specifiedExpiry']])
  if propMap.has_key('decimalEncoding'):
    attrList.append(['decimalEncoding', propMap['decimalEncoding']])
  if propMap.has_key('integerEncoding'):
    attrList.append(['integerEncoding', propMap['integerEncoding']])
  if propMap.has_key('floatingPointEncoding'):
    attrList.append(['floatingPointEncoding', propMap['floatingPointEncoding']])
  if propMap.has_key('targetClient'):
    attrList.append(['targetClient', propMap['targetClient']])
  if propMap.has_key('queueManagerHost'):
    attrList.append(['queueManagerHost', propMap['queueManagerHost']])
  if propMap.has_key('queueManagerPort'):
    attrList.append(['queueManagerPort', propMap['queueManagerPort']])
  if propMap.has_key('serverConnectionChannelName'):
    attrList.append(['serverConnectionChannelName', propMap['serverConnectionChannelName']])

  # Get reference to AdminConfig object
  AdminConfig = admBeans['AdminConfig']

  # Create
  #----------------------
  print "Creating a new MQQueue \'%s\'." % name
  return AdminConfig.create('MQQueue', parentId, attrList)
#end createMQQueue
#-------------------------------------------------------------------------------
"""
FUNCTION:       createMQTopicConnectionFactory
ARGS:           admBeans, propMap, parentId
RETURNS:        ID of the newly created MQTopicConnectionFactory.
DESCRIPTION:    Used to create a new MQTopicConnectionFactory in a scope given in terms of
		the parentId
"""
def createMQTopicConnectionFactory(admBeans, propMap, parentId):

  # required attributes.
  if not propMap.has_key('name') or not propMap['name']:
    raise AdminError("In createMQTopicConnectionFactory: Required attribute 'name' is missing.")
  name =  propMap['name']
  attrList = [['name',  name]]
  if not propMap.has_key('jndiName') or not propMap['jndiName']:
    raise AdminError("In createMQTopicConnectionFactory: Required attribute 'jndiName' is missing.")
  attrList.append(['jndiName', propMap['jndiName']])

  # Other attributes
  #----------------------
  if propMap.has_key('description'):
    attrList.append(['description', propMap['description']])
  if propMap.has_key('authDataAlias'):
    attrList.append(['authDataAlias', propMap['authDataAlias']])
  if propMap.has_key('queueManager'):
    attrList.append(['queueManager', propMap['queueManager']])
  if propMap.has_key('brokerPubQueue'):
    attrList.append(['brokerPubQueue', propMap['brokerPubQueue']])
  if propMap.has_key('brokerVersion'):
    attrList.append(['brokerVersion', propMap['brokerVersion']])
  if propMap.has_key('msgSelection'):
    attrList.append(['msgSelection', propMap['msgSelection']])
  if propMap.has_key('host'):
    attrList.append(['host', propMap['host']])
  if propMap.has_key('port'):
    attrList.append(['port', propMap['port']])
  if propMap.has_key('channel'):
    attrList.append(['channel', propMap['channel']])
  if propMap.has_key('XAEnabled'):
    attrList.append(['XAEnabled', propMap['XAEnabled']])
  if propMap.has_key('transportType'):
    attrList.append(['transportType', propMap['transportType']])
  if propMap.has_key('useConnectionPooling'):
    attrList.append(['useConnectionPooling', propMap['useConnectionPooling']])

  # Get reference to AdminConfig object
  AdminConfig = admBeans['AdminConfig']

  # Create
  #----------------------
  print "Creating a new MQTopicConnectionFactory \'%s\'." % name
  return AdminConfig.create('MQTopicConnectionFactory', parentId, attrList)
#end createMQTopicConnectionFactory
#-------------------------------------------------------------------------------
"""
FUNCTION:       createMQTopic
ARGS:           admBeans, propMap, parentId
RETURNS:        ID of the newly created MQTopic.
DESCRIPTION:    Used to create a new MQTopic in a scope given in terms of
		the parentId
"""
def createMQTopic(admBeans, propMap, parentId):

  # required attributes.
  if not propMap.has_key('name') or not propMap['name']:
    raise AdminError("In createMQTopic: Required attribute 'name' is missing.")
  name =  propMap['name']
  attrList = [['name',  name]]
  if not propMap.has_key('jndiName') or not propMap['jndiName']:
    raise AdminError("In createMQTopic: Required attribute 'jndiName' is missing.")
  attrList.append(['jndiName', propMap['jndiName']])
  if not propMap.has_key('baseTopicName'):
    raise AdminError("In createMQTopic: Required attribute 'baseTopicName' is missing.")
  baseTopicName = propMap['baseTopicName']
  attrList.append(['baseTopicName', baseTopicName])

  # Other attributes
  #----------------------
  if propMap.has_key('description'):
    attrList.append(['description', propMap['description']])
  if propMap.has_key('baseTopicName'):
    attrList.append(['baseTopicName', propMap['baseTopicName']])
  if propMap.has_key('category'):
    attrList.append(['category', propMap['category']])
  if propMap.has_key('persistence'):
    attrList.append(['persistence', propMap['persistence']])
  if propMap.has_key('priority'):
    attrList.append(['priority', propMap['priority']])
  if propMap.has_key('expiry'):
    attrList.append(['expiry', propMap['expiry']])
  if propMap.has_key('specifiedPriority'):
    attrList.append(['specifiedPriority', propMap['specifiedPriority']])
  if propMap.has_key('specifiedExpiry'):
    attrList.append(['specifiedExpiry', propMap['specifiedExpiry']])
  if propMap.has_key('decimalEncoding'):
    attrList.append(['decimalEncoding', propMap['decimalEncoding']])
  if propMap.has_key('integerEncoding'):
    attrList.append(['integerEncoding', propMap['integerEncoding']])
  if propMap.has_key('floatingPointEncoding'):
    attrList.append(['floatingPointEncoding', propMap['floatingPointEncoding']])
  if propMap.has_key('targetClient'):
    attrList.append(['targetClient', propMap['targetClient']])

  # Get reference to AdminConfig object
  AdminConfig = admBeans['AdminConfig']

  # Create
  #----------------------
  print "Creating a new MQTopic \'%s\'." % name
  return AdminConfig.create('MQTopic', parentId, attrList)
#end createMQTopic
#-------------------------------------------------------------------------------
"""
FUNCTION:       createWorkManager
ARGS:           admBeans, propMap, parentId
RETURNS:        ID of the newly created WorkManager.
DESCRIPTION:    Used to create a new WorkManager in a scope given in terms of
		the parentId
"""
def createWorkManager(admBeans, propMap, parentId):

  # required attributes.
  if not propMap.has_key('name') or not propMap['name']:
    raise AdminError("In createWorkManager: Required attribute 'name' is missing.")
  name =  propMap['name']
  attrList = [['name',  name]]

  if not propMap.has_key('jndiName') or not propMap['jndiName']:
    raise AdminError("In createWorkManager: Required attribute 'jndiName' is missing.")
  attrList.append(['jndiName', propMap['jndiName']])


  # Other attributes
  #----------------------
  if propMap.has_key('description'): 
    attrList.append(['description', propMap['description']])
  if propMap.has_key('minThreads'): 
    attrList.append(['minThreads', propMap['minThreads']])
  if propMap.has_key('maxThreads'): 
    attrList.append(['maxThreads', propMap['maxThreads']])
  if propMap.has_key('numAlarmThreads'): 
    attrList.append(['numAlarmThreads', propMap['numAlarmThreads']])
  if propMap.has_key('threadPriority'): 
    attrList.append(['threadPriority', propMap['threadPriority']])
  if propMap.has_key('providerType'): 
    attrList.append(['providerType', propMap['providerType']])
  if propMap.has_key('isGrowable'): 
    attrList.append(['isGrowable', propMap['isGrowable']])
  if propMap.has_key('workTimeout'): 
    attrList.append(['workTimeout', propMap['workTimeout']])
  if propMap.has_key('workReqQSize'): 
    attrList.append(['workReqQSize', propMap['workReqQSize']])
  if propMap.has_key('category'): 
    attrList.append(['category', propMap['category']])

  # Get reference to AdminConfig object
  AdminConfig = admBeans['AdminConfig']

  # Create
  #----------------------
  print "Creating a new WorkManager \'%s\'." % name
  return AdminConfig.create('WorkManagerInfo', parentId, attrList)

#end createWorkManager
#-------------------------------------------------------------------------------
"""
FUNCTION:       createSIBus
ARGS:           admBeans, propMap 
RETURNS:        ID of the newly created SIBus.
DESCRIPTION:    Used to create a new Service Integration Bus in the cell
"""
def createSIBus(admBeans, propMap):

  # required attributes.
  if not propMap.has_key('name') or not propMap['name']:
    raise AdminError("In createSIBus: Required attribute 'name' is missing.")
  name =  propMap['name']
  attrList = ['-bus',  name]

  # Other attributes.
  if propMap.has_key('description'):
    attrList.extend(['-description', propMap['description']])
  if propMap.has_key('protocol'):
    attrList.extend(['-protocol', propMap['protocol']])
  if propMap.has_key('configurationReloadEnabled'):
    attrList.extend(['-configurationReloadEnabled', propMap['configurationReloadEnabled']])
  if propMap.has_key('busSecurity'):
    attrList.extend(['-busSecurity', propMap['busSecurity']])
  if propMap.has_key('mediationsAuthAlias'):
    attrList.extend(['-mediationsAuthAlias', propMap['mediationsAuthAlias']])
  if propMap.has_key('discardOnDelete'):
    attrList.extend(['-discardOnDelete', propMap['discardOnDelete']])
  if propMap.has_key('highMessageThreshold'):
    attrList.extend(['-highMessageThreshold', propMap['highMessageThreshold']])

  # Get reference to AdminTask object
  AdminTask = admBeans['AdminTask']

  # Now Create the Cluster. 
  return AdminTask.createSIBus(attrList)

#end createSIBus
#-------------------------------------------------------------------------------
"""
FUNCTION:       addSIBusMember
ARGS:           admBeans, propMap 
RETURNS:        ?? 
DESCRIPTION:    Used to add cluster or server as a SIBus member
"""
def addSIBusMember(admBeans, propMap):

  # Get the bus name
  if not propMap.has_key('bus') or not propMap['bus']:
    raise AdminError("In addSIBusMember: Required attribute 'bus' is missing.")
  bus =  propMap['bus']
  attrList = ['-bus',  bus]

  # check bus member type (cluster/server/wmqServer) and set update the attribute string accordingly
  if propMap.has_key('cluster'):
    attrList.extend(['-cluster', propMap['cluster']])
  elif propMap.has_key('wmqServer'):
    attrList.extend(['-wmqServer', propMap['wmqServer']])
  else: 
    if not propMap.has_key('node') or not propMap['node'] or not propMap.has_key('server') or not propMap['server']:
      raise AdminError("In addSIBusMember: For busMember of type server node and server are required attributes.")
    attrList.extend(['-node', propMap['node']])
    attrList.extend(['-server', propMap['server']])
  
#-------------------------------------------------------------------------------
"""
FUNCTION:       createSIBDestination
ARGS:           admBeans, propMap 
RETURNS:        Id of the SIBDestination object created. 
DESCRIPTION:    Used to create a SIBDestination of type: queue, alias, port, Foreign
		WebService or TopicSpace. 
"""
def createSIBDestination(admBeans, propMap):

  # Check Required Parameters
  if not propMap.has_key('bus') or not propMap['bus']:
    raise AdminError("In createSIBDestination: Required attribute 'bus' is missing.")
  bus =  propMap['bus']
  attrList = ['-bus',  bus]

  if not propMap.has_key('name') or not propMap['name']:
    raise AdminError("In createSIBDestination: Required attribute 'name' is missing.")
  attrList.extend(['-name', propMap['name']])

  if not propMap.has_key('type') or not propMap['type']:
    raise AdminError("In createSIBDestination: Required attribute 'type' is missing.")
  attrList.extend(['-type', propMap['type']])

  # check bus member type (cluster/server/wmqServer) and set update the attribute string accordingly
  if propMap.has_key('cluster'):
    attrList.extend(['-cluster', propMap['cluster']])
  elif propMap.has_key('wmqServer'):
    attrList.extend(['-wmqServer', propMap['wmqServer']])
  else: 
    if not propMap.has_key('node') or not propMap['node'] or not propMap.has_key('server') or not propMap['server']:
      raise AdminError("In createSIBDestination: For busMember of type server node and server are required attributes.")
    attrList.extend(['-node', propMap['node']])
    attrList.extend(['-server', propMap['server']])
  
  # Get reference to AdminTask object
  AdminTask = admBeans['AdminTask']

  # Now add the member to the bus
  AdminTask.createSIBDestination(attrList)

#end createSIBDestination
###############################################################################
# Misc. Functions
###############################################################################
def getJdbcTemplateName(propMap):
  
  # Check required parameters
  if not propMap.has_key('dbType'):
    raise AdminError("In getJdbcTemplateName: Required attribute 'dbType' is missing.")
  dbType = propMap['dbType']

  # Check Database Type and branch off accordingly
  #######
  # DB2
  #######
  if dbType.lower() == 'db2':
    driverType = '4'
    if propMap.has_key('driverType'):
      driverType = propMap['driverType']
    XA = 'false'
    if propMap.has_key('XA'):
      XA = propMap['XA']
    if XA == 'true': 
      if driverType == '2':  
        return 'DB2 Legacy CLI-based Type 2 JDBC Driver (XA)'
      else:
        return 'DB2 Universal JDBC Driver Provider (XA)'
    else:
      if driverType == '2':  
        return 'DB2 Legacy CLI-based Type 2 JDBC Driver'
      else:
        return 'DB2 Universal JDBC Driver Provider'
  #########
  # Oracle
  #########
  elif dbType.lower() == 'oracle':
    XA = 'false'
    if propMap.has_key('XA'):
      XA = propMap['XA']
    if XA == 'true': 
      return 'Oracle JDBC Driver (XA)'
    else:
      return 'Oracle JDBC Driver'
  ############
  # SQL Server
  ############
  elif dbType.lower() == 'sql server':
    XA = 'false'
    if propMap.has_key('XA'):
      XA = propMap['XA']
    if XA == 'true': 
      return 'WebSphere embedded ConnectJDBC driver for MS SQL Server (XA)'
    else:
      return 'WebSphere embedded ConnectJDBC driver for MS SQL Server'
  ############
  # User Defined
  ############
  elif dbType.lower() == 'user-defined' or dbType.lower() == 'generic' :
    return ''
  ######################
  # Unsupported/Unknown
  ######################
  else:
    "The dbType %s is currently not supported"
    return
