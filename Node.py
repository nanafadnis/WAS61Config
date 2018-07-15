##############################################################################
# Project:	WebSphere 6.1 Automation - Core Library
# Package: 	was61core
# Module: 	Node
# Authors: 	Nana Fadnis & Leao Fernandes
# Start Date: 	01/01/2008
###############################################################################
import re
import sys
import Admin
import Utils
###############################################################################
class NodeError(Utils.Error):
  
  def __init__(self,msg=''):
    msg = "NodeError: %s" % msg
    Utils.Error.__init__(self,msg)

###############################################################################
#  get Functions
###############################################################################
"""
FUNCTION:       getId
ARGS:           admBeans, nodeName, cellName
RETURNS:        ID of the Node
DESCRIPTION:    Returns the ID of the Node identified by 'nodeName'.
                The cellName argument is optional. If not specified it is
                set to ''. 
"""
def getId (admBeans, nodeName, cellName=''):

  # Get a reference to the AdminConfig object from the first argument
  # which is a HashMap, and then use that to get node id.

  AdminConfig = admBeans['AdminConfig']
  return AdminConfig.getid('/Cell:%s/Node:%s/' % (cellName, nodeName))

#end getId
#-------------------------------------------------------------------------------
"""
FUNCTION:       getServers
ARGS:           admBeans, nodeName, cellName
RETURNS:        HashMap
DESCRIPTION:    Returns the HashMap with serverNames contained in the node 
		(identified by nodeName) as the keys, and the corresponding 
		IDs as the values.  The cellName argument is optional. 
"""
def getServers (admBeans, nodeName, cellName=''):
		
  serverMap = {}

  # Get a reference to the AdminConfig object from the first argument
  AdminConfig = admBeans['AdminConfig']

  # Get a list of all the servers defined in this node, and get their names and IDs
  # to populate the HashMap object.
  srvrIdList = AdminConfig.getid('/Cell:%s/Node:%s/Server:/' % (cellName, nodeName)).splitlines()
  for id in srvrIdList:
	if not id:
		 continue
	srvrName = AdminConfig.showAttribute(id, 'name')
	serverMap[srvrName] = id

  return serverMap

#end getServers
#-------------------------------------------------------------------------------
"""
FUNCTION:       getVariables
ARGS:           admBeans, nodeName, cellName
RETURNS:        HashMap
DESCRIPTION:    Returns the HashMap with VariableNames contained in the node 
		(identified by nodeName) as the keys, and the corresponding 
		the values as the values.  The cellName argument is optional. 
"""
def getVariables(admBeans, nodeName, cellName=''):
		
  variableMap = {}

  # Get a reference to the AdminConfig object from the first argument
  AdminConfig = admBeans['AdminConfig']

  # Get an ID of VariableMap object defined on this node and extract the 
  # variable name-value pairs from it to populate the HashMap object to be returned. 
  # For the latter step code calls a reusable function defined in Admin module.
  varmapId = AdminConfig.getid('/Cell:%s/Node:%s/VariableMap:/' % (cellName, nodeName))
  variableMap = {}
  if varmapId:
  	variableMap = Admin.getVarmapFromID(admBeans, varmapId)
  return variableMap

#end getVariables
#-------------------------------------------------------------------------------
"""
FUNCTION:       getJDBCProviders
ARGS:           admBeans, nodeName, cellName
RETURNS:        HashMap
DESCRIPTION:    Returns the HashMap with JDBCProviderNames contained in the node 
		(identified by nodeName) as the keys, and the corresponding 
		IDs as the values.  The cellName argument is optional. 
"""
def getJDBCProviders (admBeans, nodeName, cellName=''):
		
  JDBCProviderMap = {}

  # Get a reference to the AdminConfig object from the first argument
  AdminConfig = admBeans['AdminConfig']

  # Get a list of all the JDBCProviders defined in this node, and get their names and IDs
  # to populate the HashMap object.
  jdbcIdList = AdminConfig.getid('/Cell:%s/Node:%s/JDBCProvider:/' % (cellName, nodeName)).splitlines()
  for id in jdbcIdList:
	if not id:
		 continue
	jdbcName = AdminConfig.showAttribute(id, 'name')
	JDBCProviderMap[jdbcName] = id

  return JDBCProviderMap

#end getJDBCProviders
#-------------------------------------------------------------------------------
"""
FUNCTION:       getDataSources
ARGS:           admBeans, nodeName, cellName
RETURNS:        HashMap
DESCRIPTION:    Returns the HashMap with DataSourceNames contained in the node 
		(identified by nodeName) as the keys, and the corresponding 
		IDs as the values.  The cellName argument is optional. 
"""
def getDataSources (admBeans, nodeName, cellName=''):
		
  DataSourceMap = {}

  # Get a reference to the AdminConfig object from the first argument
  AdminConfig = admBeans['AdminConfig']

  # Get a list of all the DataSources defined in this node, and get their names and IDs
  # to populate the HashMap object to be returned.
  dsIdList = AdminConfig.getid('/Cell:%s/Node:%s/JDBCProvider:/DataSource:/' % (cellName, nodeName)).splitlines()
  for id in dsIdList:
	if not id:
		 continue
	dsName = AdminConfig.showAttribute(id, 'name')
	DataSourceMap[dsName] = id

  return DataSourceMap

#end getDataSources
#-------------------------------------------------------------------------------
"""
FUNCTION:       getJMSProviders
ARGS:           admBeans, nodeName, cellName
RETURNS:        HashMap
DESCRIPTION:    Returns the HashMap with JMSProviderNames contained in the node 
		(identified by nodeName) as the keys, and the corresponding 
		IDs as the values.  The cellName argument is optional. 
"""
def getJMSProviders (admBeans, nodeName, cellName=''):
		
  JMSProviderMap = {}

  # Get a reference to the AdminConfig object from the first argument
  AdminConfig = admBeans['AdminConfig']

  # Get a list of all the JMSProviders defined in this node, and get their names and IDs
  # to populate the HashMap object to be returned.
  jmsIdList = AdminConfig.getid('/Cell:%s/Node:%s/JMSProvider:/' % (cellName, nodeName)).splitlines()
  for id in jmsIdList:
	if not id:
		 continue
	jmsName = AdminConfig.showAttribute(id, 'name')
	JMSProviderMap[jmsName] = id

  return JMSProviderMap

#end getJMSProviders
#-------------------------------------------------------------------------------
"""
FUNCTION:       getMQQueueConnectionFactories
ARGS:           admBeans, nodeName, cellName
RETURNS:        HashMap
DESCRIPTION:    Returns the HashMap with MQQueueConnectionFactoryNames contained in the node 
		(identified by nodeName) as the keys, and the corresponding 
		IDs as the values.  The cellName argument is optional. 
"""
def getMQQueueConnectionFactories (admBeans, nodeName, cellName=''):
		
  MQQueueConnectionFactoryMap = {}

  # Get a reference to the AdminConfig object from the first argument
  AdminConfig = admBeans['AdminConfig']

  # Get a list of all the MQQueueConnectionFactories defined in this node, and get their names and IDs
  # to populate the HashMap object to be returned.
  mqqcfIdList = AdminConfig.getid('/Cell:%s/Node:%s/JMSProvider:/MQQueueConnectionFactory:/' % (cellName, nodeName)).splitlines()
  for id in mqqcfIdList:
	if not id:
		 continue
	mqqcfName = AdminConfig.showAttribute(id, 'name')
	MQQueueConnectionFactoryMap[mqqcfName] = id

  return MQQueueConnectionFactoryMap

#end getMQQueueConnectionFactories
#-------------------------------------------------------------------------------
"""
FUNCTION:       getMQQueues
ARGS:           admBeans, nodeName, cellName
RETURNS:        HashMap
DESCRIPTION:    Returns the HashMap with MQQueueNames contained in the node 
		(identified by nodeName) as the keys, and the corresponding 
		IDs as the values.  The cellName argument is optional. 
"""
def getMQQueues (admBeans, nodeName, cellName=''):
		
  MQQueueMap = {}

  # Get a reference to the AdminConfig object from the first argument
  AdminConfig = admBeans['AdminConfig']

  # Get a list of all the MQQueues defined in this node, and get their names and IDs
  # to populate the HashMap object to be returned.
  mqqIdList = AdminConfig.getid('/Cell:%s/Node:%s/JMSProvider:/MQQueue:/' % (cellName, nodeName)).splitlines()
  for id in mqqIdList:
	if not id:
		 continue
	mqqName = AdminConfig.showAttribute(id, 'name')
	MQQueueMap[mqqName] = id

  return MQQueueMap

#end getMQQueues
#-------------------------------------------------------------------------------
"""
FUNCTION:       getMQTopicConnectionFactories
ARGS:           admBeans, nodeName, cellName
RETURNS:        HashMap
DESCRIPTION:    Returns the HashMap with MQTopicConnectionFactoryNames contained in the node 
		(identified by nodeName) as the keys, and the corresponding 
		IDs as the values.  The cellName argument is optional. 
"""
def getMQTopicConnectionFactories (admBeans, nodeName, cellName=''):
		
  MQTopicConnectionFactoryMap = {}

  # Get a reference to the AdminConfig object from the first argument
  AdminConfig = admBeans['AdminConfig']

  # Get a list of all the MQTopicConnectionFactories defined in this node, and get their names and IDs
  # to populate the HashMap object to be returned.
  mqtcfIdList = AdminConfig.getid('/Cell:%s/Node:%s/JMSProvider:/MQTopicConnectionFactory:/' % (cellName, nodeName)).splitlines()
  for id in mqtcfIdList:
	if not id:
		 continue
	mqtcfName = AdminConfig.showAttribute(id, 'name')
	MQTopicConnectionFactoryMap[mqtcfName] = id

  return MQTopicConnectionFactoryMap

#end getMQTopicConnectionFactories
#-------------------------------------------------------------------------------
"""
FUNCTION:       getMQTopics
ARGS:           admBeans, nodeName, cellName
RETURNS:        HashMap
DESCRIPTION:    Returns the HashMap with MQTopicNames contained in the node 
		(identified by nodeName) as the keys, and the corresponding 
		IDs as the values.  The cellName argument is optional. 
"""
def getMQTopics (admBeans, nodeName, cellName=''):
		
  MQTopicMap = {}

  # Get a reference to the AdminConfig object from the first argument
  AdminConfig = admBeans['AdminConfig']

  # Get a list of all the MQTopics defined in this node, and get their names and IDs
  # to populate the HashMap object to be returned.
  mqtIdList = AdminConfig.getid('/Cell:%s/Node:%s/JMSProvider:/MQTopic:/' % (cellName, nodeName)).splitlines()
  for id in mqtIdList:
	if not id:
		 continue
	mqtName = AdminConfig.showAttribute(id, 'name')
	MQTopicMap[mqtName] = id

  return MQTopicMap

#end getMQTopics
#-------------------------------------------------------------------------------
"""
FUNCTION:       getWorkManagers
ARGS:           admBeans, nodeName, cellName
RETURNS:        HashMap
DESCRIPTION:    Returns the HashMap with WorkManagerNames contained in the node 
		(identified by nodeName) as the keys, and the corresponding 
		IDs as the values.  The cellName argument is optional. 
"""
def getWorkManagers (admBeans, nodeName, cellName=''):
		
  WorkManagerMap = {}

  # Get a reference to the AdminConfig object from the first argument
  AdminConfig = admBeans['AdminConfig']

  # Get a list of all the WorkManagers defined in this node, and get their names and IDs
  # to populate the HashMap object to be returned.
  wrkmgrIdList = AdminConfig.getid('/Cell:%s/Node:%s/WorkManagerProvider:/WorkManagerInfo:/' % 
                                    (cellName, nodeName)).splitlines()
  for id in wrkmgrIdList:
	if not id:
		 continue
	wrkmgrName = AdminConfig.showAttribute(id, 'name')
	WorkManagerMap[wrkmgrName] = id

  return WorkManagerMap

#end getWorkManagers
#-------------------------------------------------------------------------------
"""
FUNCTION:       getLibraries
ARGS:           admBeans, nodeName, cellName
RETURNS:        HashMap
DESCRIPTION:    Returns the HashMap with LibraryNames contained in the node 
		(identified by nodeName) as the keys, and the corresponding 
		IDs as the values.  The cellName argument is optional. 
"""
def getLibraries (admBeans, nodeName, cellName=''):
		
  LibraryMap = {}

  # Get a reference to the AdminConfig object from the first argument
  AdminConfig = admBeans['AdminConfig']

  # Get a list of all the Libraries defined in this node, and get their names and IDs
  # to populate the HashMap object to be returned.
  libIdList = AdminConfig.getid('/Cell:%s/Node:%s/Library:/' % (cellName, nodeName)).splitlines()
  for id in libIdList:
	if not id:
		 continue
	libName = AdminConfig.showAttribute(id, 'name')
	LibraryMap[libName] = id

  return LibraryMap

#end getLibraries
#-------------------------------------------------------------------------------
#  create Functions
#-------------------------------------------------------------------------------
"""
FUNCTION:       createServer
ARGS:           admBeans, propMap, nodeName, cellName
RETURNS:        ID (String) of the server created
DESCRIPTION:    Creates an ApplicationServer with a given Node as a parent.
		Sets required attributes, and some additional attributes
		of ApplicationServer specified in propMap (HashMap) object.
"""
def createServer (admBeans, propMap, nodeName, cellName=''):

  # Get a reference to the AdminConfig object from the first argument
  AdminConfig = admBeans['AdminConfig']

  # Check the required attributes
  if not propMap.has_key('name') or not propMap['name']:
    raise NodeError("In createServer: Required attribute 'name' is missing.")
  name = propMap['name']
  attrList = [['name', name]]
  
  # Get parent ID
  parentId = AdminConfig.getid("/Cell:%s/Node:%s/" % (cellName, nodeName))
  if not parentId:
  	raise NodeError("In createServer: Null ID returned for Parent %s/%s." % (cellName, nodeName))

  # Additional attributes
  if propMap.has_key('initialState'):
  	attrList.append(['stateManagement', [['initialState', propMap['initialState']]]])
  
  if propMap.has_key('stdout.fileName'):
  	attrList.append(['outputStreamRedirect', [['fileName', propMap['stdout.fileName']]]])
  
  # Check if Server already exists
  id = AdminConfig.getid("/Cell:%s/Node:%s/Server:%s/" % (cellName, nodeName, name))
  if id:
  	print "Server %s already exists in %s/%s." % (name, cellName, nodeName)
	return id
  
  # Create
  print "Creating a new Server %s in %s/%s." % (name, cellName, nodeName)
  id = AdminConfig.create('Server', parentId, attrList)
  
  return id

#end createServer
#-------------------------------------------------------------------------------
"""
FUNCTION:       setVar
ARGS:           admBeans, name, vaue, nodeName, cellName
RETURNS:        true/false string 
DESCRIPTION:    Used to set a WebSphere Managed Variable, defined via
                arguments name and value, at a Node scope.
"""
def setVar(admBeans, varName, varValue, nodeName, cellName=''):

  # Get a reference to AdminTask object
  AdminTask = admBeans['AdminTask']

  # set up scope srting
  scope = "Cell=%s,Node=%s" % (cellName, nodeName)
  return AdminTask.setVariable(['-variableName', varName, '-variableValue', varValue, '-scope', scope])

#end setVar
#-------------------------------------------------------------------------------
"""
FUNCTION:       createJDBCProvider
ARGS:           admBeans, propMap, nodeName, [cellName]
RETURNS:        ID of the newly created/existing JDBCProvider.
DESCRIPTION:    Used to create a new JDBCProvider at Node scope identified
		by the nodeName. The cellName argument is optional. 
"""
def createJDBCProvider(admBeans,propMap,nodeName,cellName=''):

  # Check required parameters.
  if not propMap.has_key('name') or not propMap['name']:
    raise NodeError("In createJDBCProvider: Required attribute 'name' is missing.")
  name =  propMap['name']

  # Get reference to AdminConfig object.
  AdminConfig = admBeans['AdminConfig']

  # Get parentId
  parentId = AdminConfig.getid("/Cell:%s/Node:%s/" % (cellName,nodeName))
  if not parentId:
    raise NodeError("In createJDBCProvider: Null parentId for parent %s." % nodeName)

  # Check if this JDBCProvider already exists.
  id = AdminConfig.getid("/Cell:%s/Node:%s/JDBCProvider:%s/" % (cellName,nodeName,name))
  if id:
    print "JDBCProvider %s already exists in node %s. Returing its id" % (name,nodeName)
    return id

  # Create a new JDBCProvider
  id = Admin.createJDBCProvider(admBeans,propMap,parentId)

  return id

#end createJDBCProvider
#-------------------------------------------------------------------------------
"""
FUNCTION:       createDataSource
ARGS:           admBeans, propMap, nodeName, [cellName]
RETURNS:        ID of the newly created/existing DataSource.
DESCRIPTION:    Used to create a new DataSource at Node scope identified
		by the nodeName. The cellName argument is optional. 
"""
def createDataSource(admBeans,propMap,nodeName,cellName=''):

  # Check required parameters.
  if not propMap.has_key('name') or not propMap['name']:
    raise NodeError("In createDataSource: Required attribute 'name' is missing.")
  name =  propMap['name']
  if not propMap.has_key('jdbcProviderName') or not propMap['jdbcProviderName']:
    raise NodeError("In createDataSource: Required attribute 'jdbcProviderName' is missing.")
  jdbcProviderName =  propMap['jdbcProviderName']

  # Get reference to AdminConfig object.
  AdminConfig = admBeans['AdminConfig']

  # Get parentId
  parentId = AdminConfig.getid("/Cell:%s/Node:%s/JDBCProvider:%s/" % (cellName,nodeName,jdbcProviderName))
  if not parentId:
    raise NodeError("In createDataSource: Null parentId for parent %s." % jdbcProviderName)

  # Check if this DataSource already exists.
  id = AdminConfig.getid("/Cell:%s/Node:%s/JDBCProvider:%s/DataSource:%s/" % (cellName,nodeName,jdbcProviderName,name))
  if id:
    print "DataSource %s already exists in node %s. Returing its id" % (name,nodeName)
    return id

  # Create a new DataSource
  id = Admin.createDataSource(admBeans,propMap,parentId)

  return id

#end createDataSource
#-------------------------------------------------------------------------------
"""
FUNCTION:       createLibrary
ARGS:           admBeans, propMap, nodeName, [cellName]
RETURNS:        ID of the newly created/existing Library.
DESCRIPTION:    Used to create a new Library at Node scope identified
		by the nodeName. The cellName argument is optional. 
"""
def createLibrary(admBeans,propMap,nodeName,cellName=''):

  # Check required parameters.
  if not propMap.has_key('name') or not propMap['name']:
    raise NodeError("In createLibrary: Required attribute 'name' is missing.")
  name =  propMap['name']

  # Get reference to AdminConfig object.
  AdminConfig = admBeans['AdminConfig']

  # Get parentId
  parentId = AdminConfig.getid("/Cell:%s/Node:%s/" % (cellName,nodeName))
  if not parentId:
    raise NodeError("In createLibrary: Null parentId for parent %s." % nodeName)

  # Check if this Library already exists.
  id = AdminConfig.getid("/Cell:%s/Node:%s/Library:%s/" % (cellName,nodeName,name))
  if id:
    print "Library %s already exists in node %s. Returing its id" % (name,nodeName)
    return id

  # Create a new Library
  id = Admin.createLibrary(admBeans,propMap,parentId)

  return id

#end createLibrary
#-------------------------------------------------------------------------------
"""
FUNCTION:       createMQQueueConnectionFactory
ARGS:           admBeans, propMap, nodeName, [cellName]
RETURNS:        ID of the newly created/existing MQQueueConnectionFactory.
DESCRIPTION:    Used to create a new MQQueueConnectionFactory at Node scope identified
		by the nodeName. The cellName argument is optional. 
"""
def createMQQueueConnectionFactory(admBeans,propMap,nodeName,cellName=''):

  # Check required parameters.
  if not propMap.has_key('jmsProviderName') or not propMap['jmsProviderName']:
    raise NodeError("In createMQQueueConnectionFactory: Required attribute 'jmsProviderName' is missing.")
  jmsProviderName =  propMap['jmsProviderName']

  if not propMap.has_key('name') or not propMap['name']:
    raise NodeError("In createMQQueueConnectionFactory: Required attribute 'name' is missing.")
  name =  propMap['name']

  # Get reference to AdminConfig object.
  AdminConfig = admBeans['AdminConfig']

  # Get parentId
  parentId = AdminConfig.getid("/Cell:%s/Node:%s/JMSProvider:%s/" % (cellName,nodeName,jmsProviderName))
  if not parentId:
    raise NodeError("In createMQQueueConnectionFactory: Null parentId for parent %s." % jmsProviderName)

  # Check if this MQQueueConnectionFactory already exists.
  id = AdminConfig.getid("/Cell:%s/Node:%s/JMSProvider:%s/MQQueueConnectionFactory:%s/" % (cellName,nodeName,jmsProviderName,name))
  if id:
    print "MQQueueConnectionFactory %s already exists in node %s. Returing its id" % (name,nodeName)
    return id

  # Create a new MQQueueConnectionFactory
  id = Admin.createMQQueueConnectionFactory(admBeans,propMap,parentId)

  return id

#end createMQQueueConnectionFactory
#-------------------------------------------------------------------------------
"""
FUNCTION:       createMQQueue
ARGS:           admBeans, propMap, nodeName, [cellName]
RETURNS:        ID of the newly created/existing MQQueue.
DESCRIPTION:    Used to create a new MQQueue at Node scope identified
		by the nodeName. The cellName argument is optional. 
"""
def createMQQueue(admBeans,propMap,nodeName,cellName=''):

  # Check required parameters.
  if not propMap.has_key('jmsProviderName') or not propMap['jmsProviderName']:
    raise NodeError("In createMQQueue: Required attribute 'jmsProviderName' is missing.")
  jmsProviderName =  propMap['jmsProviderName']

  if not propMap.has_key('name') or not propMap['name']:
    raise NodeError("In createMQQueue: Required attribute 'name' is missing.")
  name =  propMap['name']

  # Get reference to AdminConfig object.
  AdminConfig = admBeans['AdminConfig']

  # Get parentId
  parentId = AdminConfig.getid("/Cell:%s/Node:%s/JMSProvider:%s/" % (cellName,nodeName,jmsProviderName))
  if not parentId:
    raise NodeError("In createMQQueue: Null parentId for parent %s." % jmsProviderName)

  # Check if this MQQueue already exists.
  id = AdminConfig.getid("/Cell:%s/Node:%s/JMSProvider:%s/MQQueue:%s/" % (cellName,nodeName,jmsProviderName,name))
  if id:
    print "MQQueue %s already exists in node %s. Returing its id" % (name,nodeName)
    return id

  # Create a new MQQueue
  id = Admin.createMQQueue(admBeans,propMap,parentId)

  return id

#end createMQQueue
#-------------------------------------------------------------------------------
"""
FUNCTION:       createMQTopicConnectionFactory
ARGS:           admBeans, propMap, nodeName, [cellName]
RETURNS:        ID of the newly created/existing MQTopicConnectionFactory.
DESCRIPTION:    Used to create a new MQTopicConnectionFactory at Node scope identified
		by the nodeName. The cellName argument is optional. 
"""
def createMQTopicConnectionFactory(admBeans,propMap,nodeName,cellName=''):

  # Check required parameters.
  if not propMap.has_key('jmsProviderName') or not propMap['jmsProviderName']:
    raise NodeError("In createMQTopicConnectionFactory: Required attribute 'jmsProviderName' is missing.")
  jmsProviderName =  propMap['jmsProviderName']

  if not propMap.has_key('name') or not propMap['name']:
    raise NodeError("In createMQTopicConnectionFactory: Required attribute 'name' is missing.")
  name =  propMap['name']

  # Get reference to AdminConfig object.
  AdminConfig = admBeans['AdminConfig']

  # Get parentId
  parentId = AdminConfig.getid("/Cell:%s/Node:%s/JMSProvider:%s/" % (cellName,nodeName,jmsProviderName))
  if not parentId:
    raise NodeError("In createMQTopicConnectionFactory: Null parentId for parent %s." % jmsProviderName)

  # Check if this MQTopicConnectionFactory already exists.
  id = AdminConfig.getid("/Cell:%s/Node:%s/JMSProvider:%s/MQTopicConnectionFactory:%s/" % (cellName,nodeName,jmsProviderName,name))
  if id:
    print "MQTopicConnectionFactory %s already exists in node %s. Returing its id" % (name,nodeName)
    return id

  # Create a new MQTopicConnectionFactory
  id = Admin.createMQTopicConnectionFactory(admBeans,propMap,parentId)

  return id

#end createMQTopicConnectionFactory
#-------------------------------------------------------------------------------
"""
FUNCTION:       createMQTopic
ARGS:           admBeans, propMap, nodeName, [cellName]
RETURNS:        ID of the newly created/existing MQTopic.
DESCRIPTION:    Used to create a new MQTopic at Node scope identified
		by the nodeName. The cellName argument is optional. 
"""
def createMQTopic(admBeans,propMap,nodeName,cellName=''):

  # Check required parameters.
  if not propMap.has_key('jmsProviderName') or not propMap['jmsProviderName']:
    raise NodeError("In createMQTopic: Required attribute 'jmsProviderName' is missing.")
  jmsProviderName =  propMap['jmsProviderName']

  if not propMap.has_key('name') or not propMap['name']:
    raise NodeError("In createMQTopic: Required attribute 'name' is missing.")
  name =  propMap['name']

  # Get reference to AdminConfig object.
  AdminConfig = admBeans['AdminConfig']

  # Get parentId
  parentId = AdminConfig.getid("/Cell:%s/Node:%s/JMSProvider:%s/" % (cellName,nodeName,jmsProviderName))
  if not parentId:
    raise NodeError("In createMQTopic: Null parentId for parent %s." % jmsProviderName)

  # Check if this MQTopic already exists.
  id = AdminConfig.getid("/Cell:%s/Node:%s/JMSProvider:%s/MQTopic:%s/" % (cellName,nodeName,jmsProviderName,name))
  if id:
    print "MQTopic %s already exists in node %s. Returing its id" % (name,nodeName)
    return id

  # Create a new MQTopic
  id = Admin.createMQTopic(admBeans,propMap,parentId)

  return id

#end createMQTopic
#-------------------------------------------------------------------------------
"""
FUNCTION:       createWorkManager
ARGS:           admBeans, propMap, nodeName, [cellName]
RETURNS:        ID of the newly created/existing WorkManager.
DESCRIPTION:    Used to create a new WorkManager at Node scope identified
		by the nodeName. The cellName argument is optional. 
"""
def createWorkManager(admBeans,propMap,nodeName,cellName=''):

  # Check required parameters.
  if not propMap.has_key('name') or not propMap['name']:
    raise NodeError("In createWorkManager: Required attribute 'name' is missing.")
  name =  propMap['name']

  # Get reference to AdminConfig object.
  AdminConfig = admBeans['AdminConfig']

  # Get parentId
  parentId = AdminConfig.getid("/Cell:%s/Node:%s/WorkManagerProvider:WorkManagerProvider/"  
                                              % (cellName,nodeName))
  if not parentId:
    raise NodeError("In createWorkManager: Null parentId for parent WorkManagerProvider in node %s." % nodeName)

  # Check if this WorkManager already exists.
  id = AdminConfig.getid("/Cell:%s/Node:%s/WorkManagerProvider:WorkManagerProvider/WorkManagerInfo:%s/" 
                                 % (cellName,nodeName,name))
  if id:
    print "WorkManager %s already exists in node %s. Returing its id" % (name,nodeName)
    return id

  # Create a new WorkManager
  id = Admin.createWorkManager(admBeans,propMap,parentId)

  return id

#end createWorkManager
#-------------------------------------------------------------------------------
