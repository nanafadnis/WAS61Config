##############################################################################
# Project:	WebSphere 6.1 Automation - Core Library
# Package: 	was61core
# Module: 	Server
# Authors: 	Nana Fadnis & Leao Fernandes
# Start Date: 	01/01/2008
###############################################################################
import re
import sys
import Cell
import Node
import Admin
import Utils
###############################################################################
class ServerError(Utils.Error):
  
  def __init__(self,msg=''):
    msg = "ServerError: %s" % msg
    Utils.Error.__init__(self,msg)

###############################################################################
#  get Functions
###############################################################################
"""
FUNCTION:       getId
ARGS:           admBeans, serverName, nodeName, [cellName]
RETURNS:        ID of the Server
DESCRIPTION:    Returns the ID of the AppServer named 'serverName'
		on Node 'nodeName'. The cellName argument is optional. 
"""
def getId(admBeans, serverName, nodeName, cellName=''):

  # Get a reference to the AdminConfig object from the first argument
  # which is a HashMap, and then use that to get Server id.

  AdminConfig = admBeans['AdminConfig']
  return AdminConfig.getid('/Cell:%s/Node:%s/Server:%s/' % (cellName, nodeName, serverName))

#end getId
#-------------------------------------------------------------------------------
"""
FUNCTION:       getProcessDefId
ARGS:           admBeans, serverName, nodeName, [cellName]
RETURNS:        ID of the ProcessDef object
DESCRIPTION:    Returns the ID of the ProcessDef object inside the 
		AppServer named 'serverName' on Node 'nodeName'. 
		The cellName argument is optional. 
"""
def getProcessDefId(admBeans, serverName, nodeName, cellName=''):

  # Get a reference to the AdminConfig object from the first argument
  # which is a HashMap, and then use that to get ids.

  AdminConfig = admBeans['AdminConfig']

  serverId =  AdminConfig.getid('/Cell:%s/Node:%s/Server:%s/' % (cellName, nodeName, serverName))
  if not serverId:
    raise ServerError("In getProcessDefId: Null ID was returned for %s" %  serverName)

  return AdminConfig.list('JavaProcessDef', serverId)
#end getProcessDefId
#-------------------------------------------------------------------------------
"""
FUNCTION:       getVariables
ARGS:           admBeans, serverName, nodeName, cellName
RETURNS:        HashMap
DESCRIPTION:    Returns the HashMap containing Variable names defined at server scope,
		for the server 'serverName' defined on node 'nodeName'. The var names 
		are used as the keys, and the corresponding the values as the values.  
		The cellName argument is optional. 
"""
def getVariables(admBeans, serverName, nodeName, cellName=''):
		
  variableMap = {}

  # Get a reference to the AdminConfig object from the first argument
  AdminConfig = admBeans['AdminConfig']

  # Get an ID of VariableMap object defined on this Server and extract the 
  # variable name-value pairs from it to populate the HashMap object to be returned. 
  # For the latter step code calls a reusable function defined in Admin module.
  varmapId = AdminConfig.getid('/Cell:%s/Node:%s/Server:%s/VariableMap:/' % (cellName, nodeName,serverName))
  variableMap = {}
  if varmapId:
  	variableMap = Admin.getVarmapFromID(admBeans, varmapId)
  return variableMap

#end getVariables
#-------------------------------------------------------------------------------
"""
FUNCTION:       getJDBCProviders
ARGS:           admBeans, serverName, nodeName, cellName
RETURNS:        HashMap
DESCRIPTION:    Returns the HashMap with JDBCProvider names at the server scope 
		(for server 'serverName' on node 'nodeName') as the keys, and the 
		corresponding IDs as the values.  The cellName argument is optional. 
"""
def getJDBCProviders (admBeans, serverName, nodeName, cellName=''):
		
  JDBCProviderMap = {}

  # Get a reference to the AdminConfig object from the first argument
  AdminConfig = admBeans['AdminConfig']

  # Get a list of all the JDBCProviders defined on this Server, and get their names and IDs
  # to populate the HashMap object.
  jdbcIdList = AdminConfig.getid('/Cell:%s/Node:%s/Server:%s/JDBCProvider:/' 
                  % (cellName, nodeName, serverName)).splitlines()
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
ARGS:           admBeans, serverName, nodeName, cellName
RETURNS:        HashMap
DESCRIPTION:    Returns the HashMap with DataSource names at the server scope 
		(for server 'serverName' on node 'nodeName') as the keys, and the 
		corresponding IDs as the values.  The cellName argument is optional. 
"""
def getDataSources (admBeans, serverName, nodeName, cellName=''):
		
  DataSourceMap = {}

  # Get a reference to the AdminConfig object from the first argument
  AdminConfig = admBeans['AdminConfig']

  # Get a list of all the DataSources defined on this Server, and get their names and IDs
  # to populate the HashMap object to be returned.
  dsIdList = AdminConfig.getid('/Cell:%s/Node:%s/Server:%s/JDBCProvider:/DataSource:/' 
                        % (cellName, nodeName, serverName)).splitlines()
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
ARGS:           admBeans, serverName, nodeName, cellName
RETURNS:        HashMap
DESCRIPTION:    Returns the HashMap with JMSProvider names at the Server scope 
		(for server 'serverName' on node 'nodeName') as the keys, and the 
		corresponding IDs as the values.  The cellName argument is optional. 
"""
def getJMSProviders (admBeans, serverName, nodeName, cellName=''):
		
  JMSProviderMap = {}

  # Get a reference to the AdminConfig object from the first argument
  AdminConfig = admBeans['AdminConfig']

  # Get a list of all the JMSProviders defined in this Server, and get their names and IDs
  # to populate the HashMap object to be returned.
  jmsIdList = AdminConfig.getid('/Cell:%s/Node:%s/Server:%s/JMSProvider:/' 
                                % (cellName, nodeName, serverName)).splitlines()
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
ARGS:           admBeans, serverName, nodeName, cellName
RETURNS:        HashMap
DESCRIPTION:    Returns the HashMap with MQQueueConnectionFactory names at the Server scope 
		(for server 'serverName' on node 'nodeName') as the keys, and the 
		corresponding IDs as the values.  The cellName argument is optional. 
"""
def getMQQueueConnectionFactories (admBeans, serverName, nodeName, cellName=''):
		
  MQQueueConnectionFactoryMap = {}

  # Get a reference to the AdminConfig object from the first argument
  AdminConfig = admBeans['AdminConfig']

  # Get a list of all the MQQueueConnectionFactories defined in this Server, and get their names and IDs
  # to populate the HashMap object to be returned.
  mqqcfIdList = AdminConfig.getid('/Cell:%s/Node:%s/Server:%s/JMSProvider:/MQQueueConnectionFactory:/' 
                                % (cellName, nodeName, serverName)).splitlines()
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
ARGS:           admBeans, serverName, nodeName, cellName
RETURNS:        HashMap
DESCRIPTION:    Returns the HashMap with MQQueue names at the Server scope 
		(for server 'serverName' on node 'nodeName') as the keys, and the 
		corresponding IDs as the values.  The cellName argument is optional. 
"""
def getMQQueues (admBeans, serverName, nodeName, cellName=''):
		
  MQQueueMap = {}

  # Get a reference to the AdminConfig object from the first argument
  AdminConfig = admBeans['AdminConfig']

  # Get a list of all the MQQueues defined on this Server, and get their names and IDs
  # to populate the HashMap object to be returned.
  mqqIdList = AdminConfig.getid('/Cell:%s/Node:%s/Server:%s/JMSProvider:/MQQueue:/' 
                                % (cellName, nodeName, serverName)).splitlines()
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
ARGS:           admBeans, serverName, nodeName, cellName
RETURNS:        HashMap
DESCRIPTION:    Returns the HashMap with MQTopicConnectionFactory names at the Server scope 
		(for server 'serverName' on node 'nodeName') as the keys, and the 
		corresponding IDs as the values.  The cellName argument is optional. 
"""
def getMQTopicConnectionFactories (admBeans, serverName, nodeName, cellName=''):
		
  MQTopicConnectionFactoryMap = {}

  # Get a reference to the AdminConfig object from the first argument
  AdminConfig = admBeans['AdminConfig']

  # Get a list of all the MQTopicConnectionFactories defined on this Server, and get their names and IDs
  # to populate the HashMap object to be returned.
  mqtcfIdList = AdminConfig.getid('/Cell:%s/Node:%s/Server:%s/JMSProvider:/MQTopicConnectionFactory:/' 
                                % (cellName, nodeName, serverName)).splitlines()
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
ARGS:           admBeans, serverName, nodeName, cellName
RETURNS:        HashMap
DESCRIPTION:    Returns the HashMap with MQTopic names at the Server scope 
		(for server 'serverName' on node 'nodeName') as the keys, and the 
		corresponding IDs as the values.  The cellName argument is optional. 
"""
def getMQTopics (admBeans, serverName, nodeName, cellName=''):
		
  MQTopicMap = {}

  # Get a reference to the AdminConfig object from the first argument
  AdminConfig = admBeans['AdminConfig']

  # Get a list of all the MQTopics defined on this Server, and get their names and IDs
  # to populate the HashMap object to be returned.
  mqtIdList = AdminConfig.getid('/Cell:%s/Node:%s/Server:%s/JMSProvider:/MQTopic:/' 
                                % (cellName, nodeName, serverName)).splitlines()
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
ARGS:           admBeans, serverName, nodeName, cellName
RETURNS:        HashMap
DESCRIPTION:    Returns the HashMap with WorkManager names at the Server scope 
		(for server 'serverName' on node 'nodeName') as the keys, and the 
		corresponding IDs as the values.  The cellName argument is optional. 
"""
def getWorkManagers (admBeans, serverName, nodeName, cellName=''):
		
  WorkManagerMap = {}

  # Get a reference to the AdminConfig object from the first argument
  AdminConfig = admBeans['AdminConfig']

  # Get a list of all the WorkManagers defined on this Server, and get their names and IDs
  # to populate the HashMap object to be returned.
  wrkmgrIdList = AdminConfig.getid('/Cell:%s/Node:%s/Server:%s/WorkManagerProvider:/WorkManagerInfo:/' 
                                % (cellName, nodeName, serverName)).splitlines()
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
ARGS:           admBeans, serverName, nodeName, cellName
RETURNS:        HashMap
DESCRIPTION:    Returns the HashMap with Library names at the Server scope 
		(for server 'serverName' on node 'nodeName') as the keys, and the 
		corresponding IDs as the values.  The cellName argument is optional. 
"""
def getLibraries (admBeans, serverName, nodeName, cellName=''):
		
  LibraryMap = {}

  # Get a reference to the AdminConfig object from the first argument
  AdminConfig = admBeans['AdminConfig']

  # Get a list of all the Libraries defined on this Server, and get their names and IDs
  # to populate the HashMap object to be returned.
  libIdList = AdminConfig.getid('/Cell:%s/Node:%s/Server:%s/Library:/' 
                                    % (cellName, nodeName,serverName)).splitlines()
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
ARGS:           admBeans, name, vaue, serverName, nodeName, cellName
RETURNS:        true/false string 
DESCRIPTION:    Used to set a WebSphere Managed Variable, defined via
                arguments name and value, at a Server scope.
"""
def setVar(admBeans, varName, varValue, serverName, nodeName, cellName=''):

  # Get a reference to AdminTask object
  AdminTask = admBeans['AdminTask']

  # set up scope srting
  scope = "Cell=%s,Node=%s,Server=%s" % (cellName, nodeName, serverName)
  return AdminTask.setVariable(['-variableName', varName, '-variableValue', varValue, '-scope', scope])

#end setVar
#-------------------------------------------------------------------------------
"""
FUNCTION:       setPort
ARGS:           admBeans, portName, port, serverName, nodeName, cellName
RETURNS:        nothing
DESCRIPTION:    Used to set a port on a given NamedEndPoint
"""
def setPort(admBeans, portName, port, serverName, nodeName, cellName=''):

  # Get a reference to AdminConfig object
  AdminConfig = admBeans['AdminConfig']

  nodeId = Node.getId(admBeans, nodeName, cellName)
  if not nodeId:
    raise ServerError("In setPort: Null node ID was returned for %s" %  nodeName)

  seId = ''
  seList = AdminConfig.list('ServerEntry', nodeId).splitlines()
  for se in seList:
    if AdminConfig.showAttribute(se, 'serverName') == serverName:
      seId = se
      break
  if not seId:
    raise ServerError("In setPort: Could not obtain ServerEntry ID for %s/%s" %  nodeName, serverName)

  epList = AdminConfig.list('NamedEndPoint', seId).splitlines()
  portFound = 'false'
  for ep in epList:
    if (AdminConfig.showAttribute(ep, 'endPointName') == portName):
      epId = AdminConfig.showAttribute(ep, 'endPoint')
      print "Updating %s/%s. Setting %s to %s" % (nodeName,serverName,portName,port)
      AdminConfig.modify(epId, [['port',port]])
      #print AdminConfig.show(epId)
      portFound = 'true'
      break

  if portFound == 'false':
    print "Port %s is not a defined NamedEndPoint on %s/%s" % (portName, nodeName, serverName)

#end setPort
#-------------------------------------------------------------------------------
"""
FUNCTION:       setJvmAttributes
ARGS:           admBeans, propMap, serverName, nodeName, cellName
RETURNS:        ID of the modified JVM object
DESCRIPTION:    Used to set various  JVM Attributes defined via
                propMap (HashMap)
"""
def setJvmAttributes(admBeans, propMap, serverName, nodeName, cellName=''):

  # Get a reference to AdminConfig object
  AdminConfig = admBeans['AdminConfig']

  # Get Server ID and JVM Id from that.
  serverId = getId(admBeans, serverName, nodeName, cellName)
  if not serverId:
    raise ServerError("In setJvmAttributes: Null Server ID was returned for %s/%s" % (serverName, nodeName))
  jvmId = AdminConfig.list('JavaVirtualMachine', serverId)
  if not jvmId:
    raise ServerError("In setJvmAttributes: Null JVM ID was returned for %s/%s" % (serverName, nodeName))

  # set up Attributes List
  attrsList = []
  if propMap.has_key('initialHeapSize'):
    attrsList.append(['initialHeapSize', propMap['initialHeapSize']])
  if propMap.has_key('maximumHeapSize'):
    attrsList.append(['maximumHeapSize', propMap['maximumHeapSize']])
  if propMap.has_key('classpath'):
    attrsList.append(['classpath', propMap['classpath']])
  if propMap.has_key('bootClasspath'):
    attrsList.append(['bootClasspath', propMap['bootClasspath']])
  if propMap.has_key('verboseModeGarbageCollection'):
    attrsList.append(['verboseModeGarbageCollection', propMap['verboseModeGarbageCollection']])
  if propMap.has_key('genericJvmArguments'):
    attrsList.append(['genericJvmArguments', propMap['genericJvmArguments']])

  # Now update the attributes.
  if len(attrsList) > 0:
    print "Modifying the JVM attributes of %s on %s/%s" % (serverName, cellName, nodeName)
    print "Attributes list is: ", attrsList
    AdminConfig.modify(jvmId, attrsList)  
    return jvmId
#end setJvmAttributes
#-------------------------------------------------------------------------------
"""
FUNCTION:       setJvmCustomProperty
ARGS:           admBeans, name, vaue, serverName, nodeName, cellName
RETURNS:        true/false string 
DESCRIPTION:    Used to set a  JVM Custom Property defined via
                arguments name and value
"""
def setJvmCustomProperty(admBeans, varName, varValue, serverName, nodeName, cellName=''):

  # Get a reference to AdminConfig object
  AdminConfig = admBeans['AdminConfig']

  # Get Server ID and JVM Id from that.
  serverId = getId(admBeans, serverName, nodeName, cellName)
  if not serverId:
    raise ServerError("In setJvmCustomProperty: Null Server ID was returned for %s/%s" % (serverName, nodeName))
  jvmId = AdminConfig.list('JavaVirtualMachine', serverId)
  attrList = [['systemProperties', [[['name', varName], ['value', varValue]]]]]
  return AdminConfig.modify(jvmId, attrList)

#end setJvmCustomProperty
#-------------------------------------------------------------------------------
"""
FUNCTION:       setEnvEntry
ARGS:           admBeans, name, vaue, serverName, nodeName, cellName
RETURNS:        true/false string 
DESCRIPTION:    Used to set a  Environment Entry for ProcessDef defined via
                arguments name and value
"""
def setEnvEntry(admBeans, varName, varValue, serverName, nodeName, cellName=''):

  # Get a reference to AdminConfig object
  AdminConfig = admBeans['AdminConfig']

  # Get ProcessDef Id 
  procDefId = getProcessDefId(admBeans, serverName, nodeName, cellName)
  if not procDefId:
    raise ServerError("In setEnvEntry: Null ProcessDef ID was returned for %s/%s" % (serverName, nodeName))

  attrList = [['environment', [[['name', varName], ['value', varValue]]]]]
  return AdminConfig.modify(procDefId, attrList)

#end setEnvEntry
#-------------------------------------------------------------------------------
"""
FUNCTION:       modifyWCThreadpool
ARGS:           admBeans, propMap, serverName, nodeName, cellName
RETURNS:        true/false string 
DESCRIPTION:    Used to modify the WebContainer Threadpool settings of 
		a Server scope identified by the serverName/nodeName. 
		The cellName argument is optional. 
"""
def modifyWCThreadpool(admBeans,propMap,serverName,nodeName,cellName=''):


  # Get a reference to AdminConfig object
  AdminConfig = admBeans['AdminConfig']

  # Get serverId
  serverId = AdminConfig.getid("/Cell:%s/Node:%s/Server:%s/" % (cellName,nodeName,serverName))
  if not serverId:
    raise ServerError("In modifyWCThreadPool: Null ID returned for node/server %s/%s." % (nodeName,serverName))

  #print "SERVER ID: ", serverId

  # Get list of Threadpools and select the one named 'WebContainer'
  tpl = AdminConfig.list('ThreadPool', serverId).splitlines()
  wcTp = ''

  #print "THREADPOOL LIST: ", tpl

  for tp in tpl:
    tpName = AdminConfig.showAttribute(tp, 'name')
    if tpName == 'WebContainer':
      wcTp = tp
      break

  #print "WC TP ID: ", wcTp

  # Build attributes list
  tpAttrList = []  
  if propMap.has_key('minimumSize'):
    tpAttrList.append(['minimumSize',  propMap['minimumSize']])
  if propMap.has_key('maximumSize'):
    tpAttrList.append(['maximumSize',  propMap['maximumSize']])
  if propMap.has_key('inactivityTimeout'):
    tpAttrList.append(['inactivityTimeout',  propMap['inactivityTimeout']])

  # Update WC Threadpool
  if len(tpAttrList) > 0 : 
		print "Modifying WebContainer Threadpool in %s/%s." % (nodeName, serverName)
		print "Attributes to be modified: ", tpAttrList
		AdminConfig.modify(wcTp, tpAttrList)

#end modifyWCThreadpool
#-------------------------------------------------------------------------------
"""
FUNCTION:       createJDBCProvider
ARGS:           admBeans, propMap, serverName, nodeName, cellName
RETURNS:        ID of the newly created/existing JDBCProvider.
DESCRIPTION:    Used to create a new JDBCProvider at Server scope identified
		by the serverName/nodeName. The cellName argument is optional. 
"""
def createJDBCProvider(admBeans,propMap,serverName,nodeName,cellName=''):

  # Check required parameters.
  if not propMap.has_key('name') or not propMap['name']:
    raise ServerError("In createJDBCProvider: Required attribute 'name' is missing.")
  name =  propMap['name']

  # Get reference to AdminConfig object.
  AdminConfig = admBeans['AdminConfig']

  # Get parentId
  parentId = AdminConfig.getid("/Cell:%s/Node:%s/Server:%s/" % (cellName,nodeName,serverName))
  if not parentId:
    raise ServerError("In createJDBCProvider: Null parentId for node/server %s/%s." % (nodeName,serverName))

  # Check if this JDBCProvider already exists.
  id = AdminConfig.getid("/Cell:%s/Node:%s/Server:%s/JDBCProvider:%s/" % (cellName,nodeName,serverName,name))
  if id:
    print "JDBCProvider %s already exists on server/node %s/%s. Returing its id" % (name,serverName,nodeName)
    return id

  # Create a new JDBCProvider
  id = Admin.createJDBCProvider(admBeans,propMap,parentId)

  return id

#end createJDBCProvider
#-------------------------------------------------------------------------------
"""
FUNCTION:       createDataSource
ARGS:           admBeans, propMap, serverName, nodeName, cellName
RETURNS:        ID of the newly created/existing DataSource.
DESCRIPTION:    Used to create a new DataSource at Server scope identified
		by serverName/nodeName. The cellName argument is optional. 
"""
def createDataSource(admBeans,propMap,serverName,nodeName,cellName=''):

  # Check required parameters.
  if not propMap.has_key('name') or not propMap['name']:
    raise ServerError("In createDataSource: Required attribute 'name' is missing.")
  name =  propMap['name']
  if not propMap.has_key('jdbcProviderName') or not propMap['jdbcProviderName']:
    raise ServerError("In createDataSource: Required attribute 'jdbcProviderName' is missing.")
  jdbcProviderName =  propMap['jdbcProviderName']

  # Get reference to AdminConfig object.
  AdminConfig = admBeans['AdminConfig']

  # Get parentId
  parentId = AdminConfig.getid("/Cell:%s/Node:%s/Server:%s/JDBCProvider:%s/" 
                                         % (cellName,nodeName,serverName,jdbcProviderName))
  if not parentId:
    raise ServerError("In createDataSource: Null parentId returned for %s." % jdbcProviderName)

  # Check if this DataSource already exists.
  id = AdminConfig.getid("/Cell:%s/Node:%s/Server:%s/JDBCProvider:%s/DataSource:%s/" 
                               % (cellName,nodeName,serverName,jdbcProviderName,name))
  if id:
    print "DataSource %s already exists on server/node %s/%s. Returing its id" % (name,serverName,nodeName)
    return id

  # Create a new DataSource
  id = Admin.createDataSource(admBeans,propMap,parentId)

  return id

#end createDataSource
#-------------------------------------------------------------------------------
"""
FUNCTION:       createLibrary
ARGS:           admBeans, propMap, serverName, nodeName, cellName
RETURNS:        ID of the newly created/existing Library.
DESCRIPTION:    Used to create a new Library at Server scope identified
		by the serverName/nodeName. The cellName argument is optional. 
"""
def createLibrary(admBeans,propMap,serverName,nodeName,cellName=''):

  # Check required parameters.
  if not propMap.has_key('name') or not propMap['name']:
    raise ServerError("In createLibrary: Required attribute 'name' is missing.")
  name =  propMap['name']

  # Get reference to AdminConfig object.
  AdminConfig = admBeans['AdminConfig']

  # Get parentId
  parentId = AdminConfig.getid("/Cell:%s/Node:%s/Server:%s/" % (cellName,nodeName,serverName))
  if not parentId:
    raise ServerError("In createLibrary: Null parentId for parent %s." % nodeName)

  # Check if this Library already exists.
  id = AdminConfig.getid("/Cell:%s/Node:%s/Server:%s/Library:%s/" % (cellName,nodeName,serverName,name))
  if id:
    print "Library %s already exists on server/node %s/%s. Returing its id" % (name,serverName,nodeName)
    return id

  # Create a new Library
  id = Admin.createLibrary(admBeans,propMap,parentId)

  return id

#end createLibrary
#-------------------------------------------------------------------------------
"""
FUNCTION:       createMQQueueConnectionFactory
ARGS:           admBeans, propMap, serverName, nodeName, cellName
RETURNS:        ID of the newly created/existing MQQueueConnectionFactory.
DESCRIPTION:    Used to create a new MQQueueConnectionFactory at Server scope identified
		by serverName/nodeName. The cellName argument is optional. 
"""
def createMQQueueConnectionFactory(admBeans,propMap,serverName,nodeName,cellName=''):

  # Check required parameters.
  if not propMap.has_key('jmsProviderName') or not propMap['jmsProviderName']:
    raise ServerError("In createMQQueueConnectionFactory: Required attribute 'jmsProviderName' is missing.")
  jmsProviderName =  propMap['jmsProviderName']

  if not propMap.has_key('name') or not propMap['name']:
    raise ServerError("In createMQQueueConnectionFactory: Required attribute 'name' is missing.")
  name =  propMap['name']

  # Get reference to AdminConfig object.
  AdminConfig = admBeans['AdminConfig']

  print "***************************"
  print "/Cell:%s/Node:%s/Server:%s/JMSProvider:%s/" %  (cellName,nodeName,serverName,jmsProviderName)
  print "***************************"

  # Get parentId
  parentId = AdminConfig.getid("/Cell:%s/Node:%s/Server:%s/JMSProvider:%s/" 
                              % (cellName,nodeName,serverName,jmsProviderName))
  if not parentId:
    raise ServerError("In createMQQueueConnectionFactory: Null parentId for parent %s." % jmsProviderName)

  # Check if this MQQueueConnectionFactory already exists.
  id = AdminConfig.getid("/Cell:%s/Node:%s/Server:%s/JMSProvider:%s/MQQueueConnectionFactory:%s/" 
                        % (cellName,nodeName,serverName,jmsProviderName,name))
  if id:
    print "MQQueueConnectionFactory %s already exists in server/node %s/%s. Returing its id" % (name,serverName,nodeName)
    return id

  # Create a new MQQueueConnectionFactory
  id = Admin.createMQQueueConnectionFactory(admBeans,propMap,parentId)

  return id

#end createMQQueueConnectionFactory
#-------------------------------------------------------------------------------
"""
FUNCTION:       createMQQueue
ARGS:           admBeans, propMap, serverName, nodeName, cellName
RETURNS:        ID of the newly created/existing MQQueue.
DESCRIPTION:    Used to create a new MQQueue at Server scope identified
		by serverName/nodeName. The cellName argument is optional. 
"""
def createMQQueue(admBeans,propMap,serverName,nodeName,cellName=''):

  # Check required parameters.
  if not propMap.has_key('jmsProviderName') or not propMap['jmsProviderName']:
    raise ServerError("In createMQQueue: Required attribute 'jmsProviderName' is missing.")
  jmsProviderName =  propMap['jmsProviderName']

  if not propMap.has_key('name') or not propMap['name']:
    raise ServerError("In createMQQueue: Required attribute 'name' is missing.")
  name =  propMap['name']

  # Get reference to AdminConfig object.
  AdminConfig = admBeans['AdminConfig']

  # Get parentId
  parentId = AdminConfig.getid("/Cell:%s/Node:%s/Server:%s/JMSProvider:%s/" 
                                 % (cellName,nodeName,serverName,jmsProviderName))
  if not parentId:
    raise ServerError("In createMQQueue: Null parentId for parent %s." % jmsProviderName)

  # Check if this MQQueue already exists.
  id = AdminConfig.getid("/Cell:%s/Node:%s/Server:%s/JMSProvider:%s/MQQueue:%s/" % (cellName,nodeName,serverName,jmsProviderName,name))
  if id:
    print "MQQueue %s already exists in server/node %s/%s. Returing its id" % (name,serverName,nodeName)
    return id

  # Create a new MQQueue
  id = Admin.createMQQueue(admBeans,propMap,parentId)

  return id

#end createMQQueue
#-------------------------------------------------------------------------------
"""
FUNCTION:       createMQTopicConnectionFactory
ARGS:           admBeans, propMap, serverName, nodeName, cellName
RETURNS:        ID of the newly created/existing MQTopicConnectionFactory.
DESCRIPTION:    Used to create a new MQTopicConnectionFactory at Server scope identified
		by serverName/nodeName. The cellName argument is optional. 
"""
def createMQTopicConnectionFactory(admBeans,propMap,serverName,nodeName,cellName=''):

  # Check required parameters.
  if not propMap.has_key('jmsProviderName') or not propMap['jmsProviderName']:
    raise ServerError("In createMQTopicConnectionFactory: Required attribute 'jmsProviderName' is missing.")
  jmsProviderName =  propMap['jmsProviderName']

  if not propMap.has_key('name') or not propMap['name']:
    raise ServerError("In createMQTopicConnectionFactory: Required attribute 'name' is missing.")
  name =  propMap['name']

  # Get reference to AdminConfig object.
  AdminConfig = admBeans['AdminConfig']

  # Get parentId
  parentId = AdminConfig.getid("/Cell:%s/Node:%s/Server:%s/JMSProvider:%s/" 
                                  % (cellName,nodeName,serverName,jmsProviderName))
  if not parentId:
    raise ServerError("In createMQTopicConnectionFactory: Null parentId for parent %s." % jmsProviderName)

  # Check if this MQTopicConnectionFactory already exists.
  id = AdminConfig.getid("/Cell:%s/Node:%s/Server:%s/JMSProvider:%s/MQTopicConnectionFactory:%s/" 
                            % (cellName,nodeName,serverName,jmsProviderName,name))
  if id:
    print "MQTopicConnectionFactory %s already exists on server/node %s/%s. Returing its id" % (name,serverName,nodeName)
    return id

  # Create a new MQTopicConnectionFactory
  id = Admin.createMQTopicConnectionFactory(admBeans,propMap,parentId)

  return id

#end createMQTopicConnectionFactory
#-------------------------------------------------------------------------------
"""
FUNCTION:       createMQTopic
ARGS:           admBeans, propMap, serverName, nodeName, cellName
RETURNS:        ID of the newly created/existing MQTopic.
DESCRIPTION:    Used to create a new MQTopic at Server scope identified
		by serverName/nodeName. The cellName argument is optional. 
"""
def createMQTopic(admBeans,propMap,serverName,nodeName,cellName=''):

  # Check required parameters.
  if not propMap.has_key('jmsProviderName') or not propMap['jmsProviderName']:
    raise ServerError("In createMQTopic: Required attribute 'jmsProviderName' is missing.")
  jmsProviderName =  propMap['jmsProviderName']

  if not propMap.has_key('name') or not propMap['name']:
    raise ServerError("In createMQTopic: Required attribute 'name' is missing.")
  name =  propMap['name']

  # Get reference to AdminConfig object.
  AdminConfig = admBeans['AdminConfig']

  # Get parentId
  parentId = AdminConfig.getid("/Cell:%s/Node:%s/Server:%s/JMSProvider:%s/" 
                            % (cellName,nodeName,serverName,jmsProviderName))
  if not parentId:
    raise ServerError("In createMQTopic: Null parentId for parent %s." % jmsProviderName)

  # Check if this MQTopic already exists.
  id = AdminConfig.getid("/Cell:%s/Node:%s/Server:%s/JMSProvider:%s/MQTopic:%s/" 
                         % (cellName,nodeName,serverName,jmsProviderName,name))
  if id:
    print "MQTopic %s already exists on server/node %s/%s. Returing its id" % (name,serverName,nodeName)
    return id

  # Create a new MQTopic
  id = Admin.createMQTopic(admBeans,propMap,parentId)

  return id

#end createMQTopic
#-------------------------------------------------------------------------------
"""
FUNCTION:       createListenerPort
ARGS:           admBeans, propMap, serverName, nodeName, cellName
RETURNS:        ID of the newly created/existing ListenerPort.
DESCRIPTION:    Used to create a new Listener Port on the AppServer identified
		by serverName/nodeName. The cellName argument is optional. 
"""
def createListenerPort(admBeans,propMap,serverName,nodeName,cellName=''):

  # Check required parameters.
  if not propMap.has_key('name') or not propMap['name']:
    raise ServerError("In createListenerPort: Required attribute 'name' is missing.")
  name =  propMap['name']
  attrList = [['name', name]]

  if not propMap.has_key('connectionFactoryJNDIName'):
    raise ServerError("In createListenerPort: Required attribute 'connectionFactoryJNDIName' is missing.")
  connectionFactoryJNDIName = propMap['connectionFactoryJNDIName']
  attrList.append(['connectionFactoryJNDIName', connectionFactoryJNDIName])

  if not propMap.has_key('destinationJNDIName'):
    raise ServerError("In createListenerPort: Required attribute 'destinationJNDIName' is missing.")
  destinationJNDIName = propMap['destinationJNDIName']
  attrList.append(['destinationJNDIName', destinationJNDIName])

  # Other attributes
  if propMap.has_key('maxMessages'):
    attrList.append(['maxMessages', propMap['maxMessages']])
  if propMap.has_key('maxRetries'):
    attrList.append(['maxRetries', propMap['maxRetries']])
  if propMap.has_key('maxSessions'):
    attrList.append(['maxSessions', propMap['maxSessions']])

  # Get reference to AdminConfig object.
  AdminConfig = admBeans['AdminConfig']

  # Get the Server Id and grab Id of MessageListenerService object from it
  srvrId = AdminConfig.getid("/Cell:%s/Node:%s/Server:%s/" % (cellName,nodeName,serverName))
  if not srvrId:
    raise ServerError("In createListenerPort: Null Server Id was returned.")
  ml = AdminConfig.list('MessageListenerService', srvrId)

  # Check if the MListenerPort with this name already exists
  lps = AdminConfig.list('ListenerPort', srvrId).splitlines()
  lpId = ""

  for lp in lps:
    if not lp:
      continue
    if AdminConfig.showAttribute(lp, 'name') == name:
      lpId  = lp
      break

  if lpId:
    print "ListenerPort %s already exists on %s/%s." % (name, nodeName, serverName)
    return lpId

  # Create a new ListenerPort
  print "Creating a new ListenerPort %s on %s/%s" % (name, nodeName, serverName)
  lpId = AdminConfig.create('ListenerPort', ml, attrList)

  return lpId

#end createListenerPort
#-------------------------------------------------------------------------------
"""
FUNCTION:       createWorkManager
ARGS:           admBeans, propMap, serverName, nodeName, cellName
RETURNS:        ID of the newly created/existing WorkManager.
DESCRIPTION:    Used to create a new WorkManager at Server scope identified
		by serverName/nodeName. The cellName argument is optional. 
"""
def createWorkManager(admBeans,propMap,serverName,nodeName,cellName=''):

  # Check required parameters.
  if not propMap.has_key('name') or not propMap['name']:
    raise ServerError("In createWorkManager: Required attribute 'name' is missing.")
  name =  propMap['name']

  # Get reference to AdminConfig object.
  AdminConfig = admBeans['AdminConfig']

  # Get parentId
  parentId = AdminConfig.getid("/Cell:%s/Node:%s/Server:%s/WorkManagerProvider:WorkManagerProvider/"  
                                              % (cellName,nodeName,serverName))
  if not parentId:
    raise ServerError("In createWorkManager: Null parentId for parent WorkManagerProvider in node %s." % nodeName)

  # Check if this WorkManager already exists.
  id = AdminConfig.getid("/Cell:%s/Node:%s/Server:%s/WorkManagerProvider:WorkManagerProvider/WorkManagerInfo:%s/" 
                                 % (cellName,nodeName,serverName,name))
  if id:
    print "WorkManager %s already exists on server/node %s. Returing its id" % (name,serverName,nodeName)
    return id

  # Create a new WorkManager
  id = Admin.createWorkManager(admBeans,propMap,parentId)

  return id

#end createWorkManager
#-------------------------------------------------------------------------------
"""
FUNCTION:       modifyStdout
ARGS:           admBeans, propMap, serverName, nodeName, cellName
RETURNS:        nothing
DESCRIPTION:    Used to set attributes of SystemOut log of the App Server.
		The cellName argument is optional. 
"""
def modifyStdout(admBeans,propMap,serverName,nodeName,cellName=''):

  # Get reference to AdminConfig object.
  AdminConfig = admBeans['AdminConfig']

  # Get Server ID 
  serverId = getId(admBeans, serverName, nodeName, cellName)
  if not serverId:
    raise ServerError("In modifyStdout: Null Server ID was returned for %s/%s" % (serverName, nodeName))

  # Set attributes list
  attrList = []
  if propMap.has_key('fileName'):
    attrList.append(['fileName', propMap['fileName']])
  if propMap.has_key('rolloverType'):
    attrList.append(['rolloverType', propMap['rolloverType']])
  if propMap.has_key('rolloverPeriod'):
    attrList.append(['rolloverPeriod', propMap['rolloverPeriod']])
  if propMap.has_key('rolloverSize'):
    attrList.append(['rolloverSize', propMap['rolloverSize']])
  if propMap.has_key('baseHour'):
    attrList.append(['baseHour', propMap['baseHour']])
  if propMap.has_key('maxNumberOfBackupFiles'):
    attrList.append(['maxNumberOfBackupFiles', propMap['maxNumberOfBackupFiles']])
  
  if len(attrList) > 0:
    print "Modifying Stdout attributes for %s/%s" % (nodeName, serverName)
    print "Attributes are: " , attrList
  AdminConfig.modify(serverId, [['outputStreamRedirect', attrList]])

#end modifyStdout
#-------------------------------------------------------------------------------
"""
FUNCTION:       modifyStderr
ARGS:           admBeans, propMap, serverName, nodeName, cellName
RETURNS:        nothing
DESCRIPTION:    Used to set attributes of SystemOut log of the App Server.
		The cellName argument is optional. 
"""
def modifyStderr(admBeans,propMap,serverName,nodeName,cellName=''):

  # Get reference to AdminConfig object.
  AdminConfig = admBeans['AdminConfig']

  # Get Server ID
  serverId = getId(admBeans, serverName, nodeName, cellName)
  if not serverId:
    raise ServerError("In modifyStderr: Null Server ID was returned for %s/%s" % (serverName, nodeName))

  # Set attributes list
  attrList = []
  if propMap.has_key('fileName'):
    attrList.append(['fileName', propMap['fileName']])
  if propMap.has_key('rolloverType'):
    attrList.append(['rolloverType', propMap['rolloverType']])
  if propMap.has_key('rolloverPeriod'):
    attrList.append(['rolloverPeriod', propMap['rolloverPeriod']])
  if propMap.has_key('rolloverSize'):
    attrList.append(['rolloverSize', propMap['rolloverSize']])
  if propMap.has_key('baseHour'):
    attrList.append(['baseHour', propMap['baseHour']])
  if propMap.has_key('maxNumberOfBackupFiles'):
    attrList.append(['maxNumberOfBackupFiles', propMap['maxNumberOfBackupFiles']])
  
  if len(attrList) > 0:
    print "Modifying Stderr attributes for %s/%s" % (nodeName, serverName)
    print "Attributes are: " , attrList
  AdminConfig.modify(serverId, [['errorStreamRedirect', attrList]])

#end modifyStderr
#-------------------------------------------------------------------------------
