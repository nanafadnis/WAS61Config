##############################################################################
# Project:	WebSphere 6.1 Automation - Core Library
# Package: 	was61core
# Module: 	Cell
# Authors: 	Nana Fadnis & Leao Fernandes
# Start Date: 	01/01/2008
###############################################################################
import re
import sys
import Admin
import Utils
###############################################################################
class CellError(Utils.Error):
  
  def __init__(self,msg=''):
    msg = "CellError: %s" % msg
    Utils.Error.__init__(self,msg)

###############################################################################
#  get Functions
###############################################################################
"""
FUNCTION:       getId
ARGS:           admBeans, cellName
RETURNS:        ID of the cell
DESCRIPTION:    Returns the ID of the Cell identified by 'cellName'.
                The cellName argument is optional. If not specified it is
                set to ''. In WAS 6.1 environment there is only one cell, so
                cellName is not really needed. It is there for possible future
                use (we may be moving to WebSphere XD, which allows multiple
                cells in an environment). Functions of wsadmin interface work
                correctly with '' value.
"""
def getId (admBeans, cellName=''):

  # Get a reference to the AdminConfig object from the first argument
  # which is a HashMap, and then use that to get cell id.

  AdminConfig = admBeans['AdminConfig']
  return AdminConfig.getid('/Cell:' + cellName + '/')

#end getId
#-------------------------------------------------------------------------------
"""
FUNCTION:       getName
ARGS:           admBeans, cellId
RETURNS:        Name of the cell
DESCRIPTION:    Returns the Name of the Cell identified by 'cellId'.
                The cellId argument is optional. 
"""
def getName (admBeans, cellId=''):
		
  # Get Cell Id if not provided
  if not cellId:
	  print "Cell ID Not Provided. Getting it"
	  cellId = getId(admBeans)

  # Get a reference to the AdminConfig object and use that.
  AdminConfig = admBeans['AdminConfig']
  return AdminConfig.showAttribute(cellId, 'name')

#end getName
#-------------------------------------------------------------------------------
"""
FUNCTION:       getNodeNames
ARGS:           admBeans
RETURNS:        A Hashmap object
DESCRIPTION:    This Hashmap contains names of WebSphere managed nodes as keys 
		and their respective IDs as values.
"""
def getNodeNames(admBeans):

  # Get a reference to the AdminTask object, and use that to get the node names
  AdminTask = admBeans['AdminTask']
  return AdminTask.listNodes().splitlines()

#end getNodeNames
#-------------------------------------------------------------------------------
"""
FUNCTION:       getWASNodeNames
ARGS:           admBeans
RETURNS:        A Hashmap object
DESCRIPTION:    This Hashmap contains names of WebSphere managed nodes as keys 
		and their respective IDs as values.
"""
def getWASNodeNames(admBeans):

  # Get a reference to the AdminTask object, and use that to get the node names
  AdminTask = admBeans['AdminTask']
  return AdminTask.listManagedNodes().splitlines()

#end getWASNodeNames
#-------------------------------------------------------------------------------
"""
FUNCTION:       getClusters
ARGS:           admBeans, cellName
RETURNS:        HashMap
DESCRIPTION:    Returns the HashMap with Cluster Names contained in the cell 
		(identified by cellName) as the keys, and the corresponding 
		IDs as the values.  The cellName argument is optional. 
"""
def getClusters (admBeans, cellName=''):
		
  clusterMap = {}
  AdminConfig = admBeans['AdminConfig']
  clstrIdList = AdminConfig.getid('/Cell:%s/ServerCluster:/' % cellName).splitlines()
  for id in clstrIdList:
	if not id:
		 continue
	clstrName = AdminConfig.showAttribute(id, 'name')
	clusterMap[clstrName] = id

  return clusterMap

#end getClusters
#-------------------------------------------------------------------------------
"""
FUNCTION:       getVariables
ARGS:           admBeans, cellName
RETURNS:        HashMap
DESCRIPTION:    Returns the HashMap with VariableNames contained at the Cell 
		scope as the keys, and their corresponding values as the values.  
		The cellName argument is optional. 
"""
def getVariables (admBeans, cellName=''):
		
  variableMap = {}
  AdminConfig = admBeans['AdminConfig']
  varmapId = AdminConfig.getid('/Cell:%s/VariableMap:/' % cellName)
  variableMap = {}
  if varmapId:
  	variableMap = Admin.getVarmapFromID(admBeans, varmapId)
  return variableMap

#end getVariables
#-------------------------------------------------------------------------------
"""
FUNCTION:       getJDBCProviders
ARGS:           admBeans, cellName
RETURNS:        HashMap
DESCRIPTION:    Returns the HashMap with JDBCProviderNames defined at the cell 
		scope as the keys, and the corresponding IDs as the values.  
		The cellName argument is optional. 
"""
def getJDBCProviders (admBeans, cellName=''):
		
  JDBCProviderMap = {}
  AdminConfig = admBeans['AdminConfig']
  jdbcIdList = AdminConfig.getid('/Cell:%s/JDBCProvider:/' % cellName).splitlines()
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
ARGS:           admBeans,  cellName
RETURNS:        HashMap
DESCRIPTION:    Returns the HashMap with DataSources defined at the cell 
		scope as the keys, and the corresponding IDs as the values.  
		The cellName argument is optional. 
"""
def getDataSources (admBeans, cellName=''):
		
  DataSourceMap = {}
  AdminConfig = admBeans['AdminConfig']
  dsIdList = AdminConfig.getid('/Cell:%s/JDBCProvider:/DataSource:/' % cellName).splitlines()
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
ARGS:           admBeans, cellName
RETURNS:        HashMap
DESCRIPTION:    Returns the HashMap with JMSProviders defined at the cell 
		scope as the keys, and the corresponding IDs as the values.  
		The cellName argument is optional. 
"""
def getJMSProviders (admBeans, cellName=''):
		
  JMSProviderMap = {}
  AdminConfig = admBeans['AdminConfig']
  jmsIdList = AdminConfig.getid('/Cell:%s/JMSProvider:/' % cellName).splitlines()
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
ARGS:           admBeans, cellName
RETURNS:        HashMap
DESCRIPTION:    Returns the HashMap with MQQueueConnectionFactories defined at the 
		cell scope as the keys, and the corresponding IDs as the values.  
		The cellName argument is optional. 
"""
def getMQQueueConnectionFactories (admBeans, cellName=''):
		
  MQQueueConnectionFactoryMap = {}
  AdminConfig = admBeans['AdminConfig']
  mqqcfIdList = AdminConfig.getid('/Cell:%s/JMSProvider:/MQQueueConnectionFactory:/' % cellName).splitlines()
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
ARGS:           admBeans, cellName
RETURNS:        HashMap
DESCRIPTION:    Returns the HashMap with MQQueues defined at the 
		cell scope as the keys, and the corresponding IDs as the values.  
		The cellName argument is optional. 
"""
def getMQQueues (admBeans, cellName=''):
		
  MQQueueMap = {}
  AdminConfig = admBeans['AdminConfig']
  mqqIdList = AdminConfig.getid('/Cell:%s/JMSProvider:/MQQueue:/' % cellName).splitlines()
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
ARGS:           admBeans, cellName
RETURNS:        HashMap
DESCRIPTION:    Returns the HashMap with MQTopicConnectionFactories defined at the 
		cell scope as the keys, and the corresponding IDs as the values.  
		The cellName argument is optional. 
"""
def getMQTopicConnectionFactories (admBeans, cellName=''):
		
  MQTopicConnectionFactoryMap = {}
  AdminConfig = admBeans['AdminConfig']
  mqtcfIdList = AdminConfig.getid('/Cell:%s/JMSProvider:/MQTopicConnectionFactory:/' % cellName).splitlines()
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
ARGS:           admBeans, cellName
RETURNS:        HashMap
DESCRIPTION:    Returns the HashMap with MQTopics defined at the 
		cell scope as the keys, and the corresponding IDs as the values.  
		The cellName argument is optional. 
"""
def getMQTopics (admBeans, cellName=''):
		
  MQTopicMap = {}
  AdminConfig = admBeans['AdminConfig']
  mqtIdList = AdminConfig.getid('/Cell:%s/JMSProvider:/MQTopic:/' % cellName).splitlines()
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
ARGS:           admBeans, cellName
RETURNS:        HashMap
DESCRIPTION:    Returns the HashMap with WorkManagers defined at the 
		cell scope as the keys, and the corresponding IDs as the values.  
		The cellName argument is optional. 
"""
def getWorkManagers (admBeans, cellName=''):
		
  WorkManagerMap = {}
  AdminConfig = admBeans['AdminConfig']
  wrkmgrIdList = AdminConfig.getid('/Cell:%s/WorkManagerProvider:/WorkManagerInfo:/' % cellName).splitlines()
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
ARGS:           admBeans, cellName
RETURNS:        HashMap
DESCRIPTION:    Returns the HashMap with Libraries defined at the 
		cell scope as the keys, and the corresponding IDs as the values.  
		The cellName argument is optional. 
"""
def getLibraries (admBeans, cellName=''):
		
  LibraryMap = {}
  AdminConfig = admBeans['AdminConfig']
  libIdList = AdminConfig.getid('/Cell:%s/Library:/' % cellName).splitlines()
  for id in libIdList:
	if not id:
		 continue
	libName = AdminConfig.showAttribute(id, 'name')
	LibraryMap[libName] = id

  return LibraryMap

#end getLibraries
#-------------------------------------------------------------------------------
"""
FUNCTION:       setVar
ARGS:           admBeans, name, vaue, cellName
RETURNS:        true/false string 
DESCRIPTION:    Used to set a WebSphere Managed Variable, defined via
                arguments name and value, at a Cell scope.
"""
def setVar(admBeans, varName, varValue, cellName=''):

  # Get a reference to AdminTask object
  AdminTask = admBeans['AdminTask']

  # set up scope srting
  scope = "Cell=%s" % cellName
  return AdminTask.setVariable(['-variableName', varName, '-variableValue', varValue, '-scope', scope])

#end setVar
#-------------------------------------------------------------------------------
"""
FUNCTION:       createCluster
ARGS:           admBeans, propMap, cellName
RETURNS:        ID of the newly created/existing Cluster.
DESCRIPTION:    Used to create a new ServerCluster in the Cell. 
		The cellName argument is optional. 
"""
def createCluster(admBeans,propMap,cellName=''):

  # Check required parameters.
  if not propMap.has_key('name') or not propMap['name']:
    raise CellError("In createCluster: Required attribute 'name' is missing.")
  name =  propMap['name']

  # Get reference to AdminConfig object.
  AdminConfig = admBeans['AdminConfig']

  # Get parentId
  parentId = AdminConfig.getid("/Cell:%s/" % cellName)
  print "Cell Name: ", cellName
  if not parentId:
    raise CellError("In createCluster: Null parentId for parent %s." % cellName)

  # Check if this Cluster already exists.
  id = AdminConfig.getid("/Cell:%s/ServerCluster:%s/" % (cellName,name))
  if id:
    print "Cluster %s already exists in the cell. Returing its id" % name
    return id

  # Create a new Cluster
  id = Admin.createCluster(admBeans,propMap,parentId)

  return id

#end createCluster
#-------------------------------------------------------------------------------
"""
FUNCTION:       createJAASAuthData
ARGS:           admBeans, alias, userId, password, cellName
RETURNS:        ID of the newly created/existing JAASAuthData.
DESCRIPTION:    Used to create a new JAASAuthData. 
		The cellName argument is optional. 
"""
def createJAASAuthData(admBeans, alias, userId, password, cellName=''):

  # Get a reference to AdminConfig object
  AdminConfig = admBeans['AdminConfig']

  # Get parentId
  parentId = AdminConfig.getid("/Cell:%s/Security:/" % cellName)
  if not parentId:
    raise CellError("In createJAASAuthData: Null SecurityId for cell %s." % cellName)
  attrList = [['alias', alias], ['userId', userId], ['password', password]]
  adLst = AdminConfig.list('JAASAuthData', parentId).splitlines()
  for id in adLst:
    if id and (AdminConfig.showAttribute(id, 'alias') == alias): 
      print "JAASAuthData %s already exists in this cell" % alias
      return id
  id = AdminConfig.create('JAASAuthData', parentId, attrList)
  return id
#end createJAASAuthData
#-------------------------------------------------------------------------------
"""
FUNCTION:       createJDBCProvider
ARGS:           admBeans, propMap, cellName
RETURNS:        ID of the newly created/existing JDBCProvider.
DESCRIPTION:    Used to create a new JDBCProvider at Cell scope. 
		The cellName argument is optional. 
"""
def createJDBCProvider(admBeans,propMap,cellName=''):

  # Check required parameters.
  if not propMap.has_key('name') or not propMap['name']:
    raise CellError("In createJDBCProvider: Required attribute 'name' is missing.")
  name =  propMap['name']

  # Get reference to AdminConfig object.
  AdminConfig = admBeans['AdminConfig']

  # Get parentId
  parentId = AdminConfig.getid("/Cell:%s/" % cellName)
  if not parentId:
    raise CellError("In createJDBCProvider: Null parentId for parent %s." % cellName)

  # Check if this JDBCProvider already exists.
  id = AdminConfig.getid("/Cell:%s/JDBCProvider:%s/" % (cellName,name))
  if id:
    print "JDBCProvider %s already exists in the cell. Returing its id" % name
    return id

  # Create a new JDBCProvider
  id = Admin.createJDBCProvider(admBeans,propMap,parentId)

  return id

#end createJDBCProvider
#-------------------------------------------------------------------------------
"""
FUNCTION:       createDataSource
ARGS:           admBeans, propMap, cellName
RETURNS:        ID of the newly created/existing DataSource.
DESCRIPTION:    Used to create a new DataSource at Cell scope. 
		The cellName argument is optional. 
"""
def createDataSource(admBeans,propMap,cellName=''):

  # Check required parameters.
  if not propMap.has_key('name') or not propMap['name']:
    raise CellError("In createDataSource: Required attribute 'name' is missing.")
  name =  propMap['name']
  if not propMap.has_key('jdbcProviderName') or not propMap['jdbcProviderName']:
    raise CellError("In createDataSource: Required attribute 'jdbcProviderName' is missing.")
  jdbcProviderName =  propMap['jdbcProviderName']

  # Get reference to AdminConfig object.
  AdminConfig = admBeans['AdminConfig']

  # Get parentId
  parentId = AdminConfig.getid("/Cell:%s/JDBCProvider:%s/" % (cellName,jdbcProviderName))
  if not parentId:
    raise CellError("In createDataSource: Null parentId for parent %s." % jdbcProviderName)

  # Check if this DataSource already exists.
  id = AdminConfig.getid("/Cell:%s/JDBCProvider:%s/DataSource:%s/" % (cellName,jdbcProviderName,name))
  if id:
    print "DataSource %s already exists in the cell. Returing its id" % name
    return id

  # Create a new DataSource
  id = Admin.createDataSource(admBeans,propMap,parentId)

  return id

#end createDataSource
#-------------------------------------------------------------------------------
"""
FUNCTION:       createLibrary
ARGS:           admBeans, propMap, cellName
RETURNS:        ID of the newly created/existing Library.
DESCRIPTION:    Used to create a new Library at Cell scope 
		The cellName argument is optional. 
"""
def createLibrary(admBeans,propMap,cellName=''):

  # Check required parameters.
  if not propMap.has_key('name') or not propMap['name']:
    raise CellError("In createLibrary: Required attribute 'name' is missing.")
  name =  propMap['name']

  # Get reference to AdminConfig object.
  AdminConfig = admBeans['AdminConfig']

  # Get parentId
  parentId = AdminConfig.getid("/Cell:%s/" % cellName)
  if not parentId:
    raise CellError("In createLibrary: Null Id returned for the parent cell."  )

  # Check if this Library already exists.
  id = AdminConfig.getid("/Cell:%s/Library:%s/" % (cellName,name))
  if id:
    print "Library %s already exists in the cell. Returing its id" % name
    return id

  # Create a new Library
  id = Admin.createLibrary(admBeans,propMap,parentId)

  return id

#end createLibrary
#-------------------------------------------------------------------------------
"""
FUNCTION:       createMQQueueConnectionFactory
ARGS:           admBeans, propMap, cellName
RETURNS:        ID of the newly created/existing MQQueueConnectionFactory.
DESCRIPTION:    Used to create a new MQQueueConnectionFactory at Cell scope.
		The cellName argument is optional. 
"""
def createMQQueueConnectionFactory(admBeans,propMap,cellName=''):

  # Check required parameters.
  if not propMap.has_key('jmsProviderName') or not propMap['jmsProviderName']:
    raise CellError("In createMQQueueConnectionFactory: Required attribute 'jmsProviderName' is missing.")
  jmsProviderName =  propMap['jmsProviderName']

  if not propMap.has_key('name') or not propMap['name']:
    raise CellError("In createMQQueueConnectionFactory: Required attribute 'name' is missing.")
  name =  propMap['name']

  # Get reference to AdminConfig object.
  AdminConfig = admBeans['AdminConfig']

  # Get parentId
  parentId = AdminConfig.getid("/Cell:%s/JMSProvider:%s/" % (cellName,jmsProviderName))
  if not parentId:
    raise CellError("In createMQQueueConnectionFactory: Null parentId for parent %s." % jmsProviderName)

  # Check if this MQQueueConnectionFactory already exists.
  id = AdminConfig.getid("/Cell:%s/JMSProvider:%s/MQQueueConnectionFactory:%s/" % (cellName,jmsProviderName,name))
  if id:
    print "MQQueueConnectionFactory %s already exists in the cell. Returing its id" % name
    return id

  # Create a new MQQueueConnectionFactory
  id = Admin.createMQQueueConnectionFactory(admBeans,propMap,parentId)

  return id

#end createMQQueueConnectionFactory
#-------------------------------------------------------------------------------
"""
FUNCTION:       createMQQueue
ARGS:           admBeans, propMap, cellName
RETURNS:        ID of the newly created/existing MQQueue.
DESCRIPTION:    Used to create a new MQQueue at Cell scope.
		The cellName argument is optional. 
"""
def createMQQueue(admBeans,propMap,cellName=''):

  # Check required parameters.
  if not propMap.has_key('jmsProviderName') or not propMap['jmsProviderName']:
    raise CellError("In createMQQueue: Required attribute 'jmsProviderName' is missing.")
  jmsProviderName =  propMap['jmsProviderName']

  if not propMap.has_key('name') or not propMap['name']:
    raise CellError("In createMQQueue: Required attribute 'name' is missing.")
  name =  propMap['name']

  # Get reference to AdminConfig object.
  AdminConfig = admBeans['AdminConfig']

  # Get parentId
  parentId = AdminConfig.getid("/Cell:%s/JMSProvider:%s/" % (cellName,jmsProviderName))
  if not parentId:
    raise CellError("In createMQQueue: Null parentId for parent %s." % jmsProviderName)

  # Check if this MQQueue already exists.
  id = AdminConfig.getid("/Cell:%s/JMSProvider:%s/MQQueue:%s/" % (cellName,jmsProviderName,name))
  if id:
    print "MQQueue %s already exists in the cell. Returing its id" % name
    return id

  # Create a new MQQueue
  id = Admin.createMQQueue(admBeans,propMap,parentId)

  return id

#end createMQQueue
#-------------------------------------------------------------------------------
"""
FUNCTION:       createMQTopicConnectionFactory
ARGS:           admBeans, propMap, cellName
RETURNS:        ID of the newly created/existing MQTopicConnectionFactory.
DESCRIPTION:    Used to create a new MQTopicConnectionFactory at Cell scope.
		The cellName argument is optional. 
"""
def createMQTopicConnectionFactory(admBeans,propMap,cellName=''):

  # Check required parameters.
  if not propMap.has_key('jmsProviderName') or not propMap['jmsProviderName']:
    raise CellError("In createMQTopicConnectionFactory: Required attribute 'jmsProviderName' is missing.")
  jmsProviderName =  propMap['jmsProviderName']

  if not propMap.has_key('name') or not propMap['name']:
    raise CellError("In createMQTopicConnectionFactory: Required attribute 'name' is missing.")
  name =  propMap['name']

  # Get reference to AdminConfig object.
  AdminConfig = admBeans['AdminConfig']

  # Get parentId
  parentId = AdminConfig.getid("/Cell:%s/JMSProvider:%s/" % (cellName,jmsProviderName))
  if not parentId:
    raise CellError("In createMQTopicConnectionFactory: Null parentId for parent %s." % jmsProviderName)

  # Check if this MQTopicConnectionFactory already exists.
  id = AdminConfig.getid("/Cell:%s/JMSProvider:%s/MQTopicConnectionFactory:%s/" % (cellName,jmsProviderName,name))
  if id:
    print "MQTopicConnectionFactory %s already exists in the cell. Returing its id" % name
    return id

  # Create a new MQTopicConnectionFactory
  id = Admin.createMQTopicConnectionFactory(admBeans,propMap,parentId)

  return id

#end createMQTopicConnectionFactory
#-------------------------------------------------------------------------------
"""
FUNCTION:       createMQTopic
ARGS:           admBeans, propMap, cellName
RETURNS:        ID of the newly created/existing MQTopic.
DESCRIPTION:    Used to create a new MQTopic at Cell scope.
		The cellName argument is optional. 
"""
def createMQTopic(admBeans,propMap,cellName=''):

  # Check required parameters.
  if not propMap.has_key('jmsProviderName') or not propMap['jmsProviderName']:
    raise CellError("In createMQTopic: Required attribute 'jmsProviderName' is missing.")
  jmsProviderName =  propMap['jmsProviderName']

  if not propMap.has_key('name') or not propMap['name']:
    raise CellError("In createMQTopic: Required attribute 'name' is missing.")
  name =  propMap['name']

  # Get reference to AdminConfig object.
  AdminConfig = admBeans['AdminConfig']

  # Get parentId
  parentId = AdminConfig.getid("/Cell:%s/JMSProvider:%s/" % (cellName,jmsProviderName))
  if not parentId:
    raise CellError("In createMQTopic: Null parentId for parent %s." % jmsProviderName)

  # Check if this MQTopic already exists.
  id = AdminConfig.getid("/Cell:%s/JMSProvider:%s/MQTopic:%s/" % (cellName,jmsProviderName,name))
  if id:
    print "MQTopic %s already exists in the cell. Returing its id" % name
    return id

  # Create a new MQTopic
  id = Admin.createMQTopic(admBeans,propMap,parentId)

  return id

#end createMQTopic
#-------------------------------------------------------------------------------
"""
FUNCTION:       createWorkManager
ARGS:           admBeans, propMap, cellName
RETURNS:        ID of the newly created/existing WorkManager.
DESCRIPTION:    Used to create a new WorkManager at Cell scope.
		The cellName argument is optional. 
"""
def createWorkManager(admBeans,propMap,cellName=''):

  # Check required parameters.
  if not propMap.has_key('name') or not propMap['name']:
    raise CellError("In createWorkManager: Required attribute 'name' is missing.")
  name =  propMap['name']

  # Get reference to AdminConfig object.
  AdminConfig = admBeans['AdminConfig']

  # Get parentId
  parentId = AdminConfig.getid("/Cell:%s/WorkManagerProvider:WorkManagerProvider/" % cellName)
  if not parentId:
    raise CellError("In createWorkManager: Null parentId for parent WorkManagerProvider.") 

  # Check if this WorkManager already exists.
  id = AdminConfig.getid("/Cell:%s/WorkManagerProvider:WorkManagerProvider/WorkManagerInfo:%s/" 
                                 % (cellName,name))
  if id:
    print "WorkManager %s already exists in the cell. Returing its id" % name
    return id

  # Create a new WorkManager
  id = Admin.createWorkManager(admBeans,propMap,parentId)

  return id

#end createWorkManager
#-------------------------------------------------------------------------------
"""
FUNCTION:       createVirtualHost
ARGS:           admBeans, propMap, cellName
RETURNS:        ID of the newly created/existing VirtualHost.
DESCRIPTION:    Used to create a new VirtualHost at Cell scope.
		The cellName argument is optional. 
"""
def createVirtualHost(admBeans,vhostName,cellName=''):

  # Get reference to AdminConfig object.
  AdminConfig = admBeans['AdminConfig']

  # Get parentId
  cellId = getId(admBeans, cellName)
  if not cellId:
    raise CellError("In createVirtualHost: Null cellId returned for cell %s." % cellName) 

  # Check if this VirtualHost already exists.
  id = AdminConfig.getid("/Cell:%s/VirtualHost:%s/" % (cellName,vhostName))
  if id:
    print "VirtualHost %s already exists in the cell. Returing its id" % vhostName
    return id

  # Create a new VirtualHost
  attrList = [['name', vhostName]]
  id = AdminConfig.create('VirtualHost', cellId, attrList)

  return id
#end createVirtualHost
#-------------------------------------------------------------------------------
"""
FUNCTION:       createVirtualHostAlias
ARGS:           admBeans, vhostName, host, port, cellName
RETURNS:        ID of the newly created/existing VirtualHostAlias.
DESCRIPTION:    Used to create a new VirtualHostAlias for a given
		Virtual Host. The cellName argument is optional. 
"""
def createVirtualHostAlias(admBeans, vhostName, hostname, port, cellName=''):

  # Get reference to AdminConfig object.
  AdminConfig = admBeans['AdminConfig']

  # Get parentId
  parentId = AdminConfig.getid("/Cell:%s/VirtualHost:%s/" % (cellName, vhostName))
  if not parentId:
    raise CellError("In createVirtualHostAlias: Null parentId for parent Virtual Host %s." % vhostName) 

  # Check if this VirtualHostAlias already exists.
  lst = AdminConfig.list('HostAlias', parentId).splitlines()
  for als in lst:
    if not als:
      continue    
    h = AdminConfig.showAttribute(als, 'hostname')
    p = AdminConfig.showAttribute(als, 'port')
    if (hostname==h and port==p):
      print "Alias %s:%s already exists for %s" % (hostname, port, vhostName)
      return als

  # Create a new VirtualHostAlias
  attrs = [['hostname', hostname], ['port', port]]
  id = AdminConfig.create('HostAlias', parentId, attrs)
  return id

#end createVirtualHostAlias
#-------------------------------------------------------------------------------
