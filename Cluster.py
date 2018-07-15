##############################################################################
# Project:	WebSphere 6.1 Automation - Core Library
# Package: 	was61core
# Module: 	Cluster
# Authors: 	Nana Fadnis & Leao Fernandes
# Start Date: 	01/01/2008
###############################################################################
import re
import Admin
import Utils
###############################################################################
# Classes
###############################################################################
class ClusterError(Utils.Error):
  
  def __init__(self,msg=''):
    msg = "ClusterError: %s" % msg
    Utils.Error.__init__(self,msg)

###############################################################################
#-------------------------------------------------------------------------------
# 'get' functions
#-------------------------------------------------------------------------------
"""
FUNCTION:       getId
ARGS:           admBeans, clusterName, cellName
RETURNS:        ID of the ServerCluster
DESCRIPTION:    Returns the ID of the ServerCluster identified by 'clusterName'.
                The cellName argument is optional. If not specified it is
                set to ''. 
"""
def getId (admBeans, clusterName, cellName=''):

  # Get a reference to the AdminConfig object from the first argument
  # which is a HashMap, and then use that to get cluster id.

  AdminConfig = admBeans['AdminConfig']
  return AdminConfig.getid('/Cell:%s/ServerCluster:%s/' % (cellName, clusterName))

#end getId
#-------------------------------------------------------------------------------
"""
FUNCTION:       getMembers
ARGS:           admBeans, clusterName, cellName
RETURNS:        HashMap
DESCRIPTION:    Returns the HashMap with memberNames contained in the cluster 
		(identified by clusterName) as the keys, and the corresponding 
		IDs as the values.  The cellName argument is optional. 
"""
def getMembers (admBeans, clusterName, cellName=''):
		
  memberMap = {}
  AdminConfig = admBeans['AdminConfig']
  memberIdList = AdminConfig.getid('/Cell:%s/ServerCluster:%s/ClusterMember:/' % (cellName, clusterName)).splitlines()
  for id in memberIdList:
	if not id:
		 continue
	memberName = AdminConfig.showAttribute(id, 'memberName')
	memberMap[memberName] = id

  return memberMap

#end getMembers
#-------------------------------------------------------------------------------
"""
FUNCTION:       getVariables
ARGS:           admBeans, clusterName, cellName
RETURNS:        HashMap
DESCRIPTION:    Returns the HashMap with VariableNames contained in the cluster 
		(identified by clusterName) as the keys, and the corresponding 
		the values as the values.  The cellName argument is optional. 
"""
def getVariables (admBeans, clusterName, cellName=''):
		
  variableMap = {}
  AdminConfig = admBeans['AdminConfig']
  varmapId = AdminConfig.getid('/Cell:%s/ServerCluster:%s/VariableMap:/' % (cellName, clusterName))
  if varmapId:
  	variableMap = Admin.getVarmapFromID(admBeans, varmapId)
  return variableMap

#end getVariables
#-------------------------------------------------------------------------------
"""
FUNCTION:       getJDBCProviders
ARGS:           admBeans, clusterName, cellName
RETURNS:        HashMap
DESCRIPTION:    Returns the HashMap with JDBCProviderNames contained in the cluster 
		(identified by clusterName) as the keys, and the corresponding 
		IDs as the values.  The cellName argument is optional. 
"""
def getJDBCProviders (admBeans, clusterName, cellName=''):
		
  JDBCProviderMap = {}
  AdminConfig = admBeans['AdminConfig']
  jdbcIdList = AdminConfig.getid('/Cell:%s/ServerCluster:%s/JDBCProvider:/' % (cellName, clusterName)).splitlines()
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
ARGS:           admBeans, clusterName, cellName
RETURNS:        HashMap
DESCRIPTION:    Returns the HashMap with DataSourceNames contained in the cluster 
		(identified by clusterName) as the keys, and the corresponding 
		IDs as the values.  The cellName argument is optional. 
"""
def getDataSources (admBeans, clusterName, cellName=''):
		
  DataSourceMap = {}
  AdminConfig = admBeans['AdminConfig']
  dsIdList = AdminConfig.getid('/Cell:%s/ServerCluster:%s/JDBCProvider:/DataSource:/' % (cellName, clusterName)).splitlines()
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
ARGS:           admBeans, clusterName, cellName
RETURNS:        HashMap
DESCRIPTION:    Returns the HashMap with JMSProviderNames contained in the cluster 
		(identified by clusterName) as the keys, and the corresponding 
		IDs as the values.  The cellName argument is optional. 
"""
def getJMSProviders (admBeans, clusterName, cellName=''):
		
  JMSProviderMap = {}
  AdminConfig = admBeans['AdminConfig']
  jmsIdList = AdminConfig.getid('/Cell:%s/ServerCluster:%s/JMSProvider:/' % (cellName, clusterName)).splitlines()
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
ARGS:           admBeans, clusterName, cellName
RETURNS:        HashMap
DESCRIPTION:    Returns the HashMap with MQQueueConnectionFactoryNames contained in the cluster 
		(identified by clusterName) as the keys, and the corresponding 
		IDs as the values.  The cellName argument is optional. 
"""
def getMQQueueConnectionFactories (admBeans, clusterName, cellName=''):
		
  MQQueueConnectionFactoryMap = {}
  AdminConfig = admBeans['AdminConfig']
  mqqcfIdList = AdminConfig.getid('/Cell:%s/ServerCluster:%s/JMSProvider:/MQQueueConnectionFactory:/' % (cellName, clusterName)).splitlines()
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
ARGS:           admBeans, clusterName, cellName
RETURNS:        HashMap
DESCRIPTION:    Returns the HashMap with MQQueueNames contained in the cluster 
		(identified by clusterName) as the keys, and the corresponding 
		IDs as the values.  The cellName argument is optional. 
"""
def getMQQueues (admBeans, clusterName, cellName=''):
		
  MQQueueMap = {}
  AdminConfig = admBeans['AdminConfig']
  mqqIdList = AdminConfig.getid('/Cell:%s/ServerCluster:%s/JMSProvider:/MQQueue:/' % (cellName, clusterName)).splitlines()
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
ARGS:           admBeans, clusterName, cellName
RETURNS:        HashMap
DESCRIPTION:    Returns the HashMap with MQTopicConnectionFactoryNames contained in the cluster 
		(identified by clusterName) as the keys, and the corresponding 
		IDs as the values.  The cellName argument is optional. 
"""
def getMQTopicConnectionFactories (admBeans, clusterName, cellName=''):
		
  MQTopicConnectionFactoryMap = {}
  AdminConfig = admBeans['AdminConfig']
  mqtcfIdList = AdminConfig.getid('/Cell:%s/ServerCluster:%s/JMSProvider:/MQTopicConnectionFactory:/' % (cellName, clusterName)).splitlines()
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
ARGS:           admBeans, clusterName, cellName
RETURNS:        HashMap
DESCRIPTION:    Returns the HashMap with MQTopicNames contained in the cluster 
		(identified by clusterName) as the keys, and the corresponding 
		IDs as the values.  The cellName argument is optional. 
"""
def getMQTopics (admBeans, clusterName, cellName=''):
		
  MQTopicMap = {}
  AdminConfig = admBeans['AdminConfig']
  mqtIdList = AdminConfig.getid('/Cell:%s/ServerCluster:%s/JMSProvider:/MQTopic:/' % (cellName, clusterName)).splitlines()
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
ARGS:           admBeans, clusterName, cellName
RETURNS:        HashMap
DESCRIPTION:    Returns the HashMap with WorkManagerNames contained in the cluster 
		(identified by clusterName) as the keys, and the corresponding 
		IDs as the values.  The cellName argument is optional. 
"""
def getWorkManagers (admBeans, clusterName, cellName=''):
		
  WorkManagerMap = {}
  AdminConfig = admBeans['AdminConfig']
  wrkmgrIdList = AdminConfig.getid('/Cell:%s/ServerCluster:%s/WorkManagerProvider:/WorkManagerInfo:/' 
                                       % (cellName, clusterName)).splitlines()
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
ARGS:           admBeans, clusterName, cellName
RETURNS:        HashMap
DESCRIPTION:    Returns the HashMap with LibraryNames contained in the cluster 
		(identified by clusterName) as the keys, and the corresponding 
		IDs as the values.  The cellName argument is optional. 
"""
def getLibraries (admBeans, clusterName, cellName=''):
		
  LibraryMap = {}
  AdminConfig = admBeans['AdminConfig']
  libIdList = AdminConfig.getid('/Cell:%s/ServerCluster:%s/Library:/' % (cellName, clusterName)).splitlines()
  for id in libIdList:
	if not id:
		 continue
	libName = AdminConfig.showAttribute(id, 'name')
	LibraryMap[libName] = id

  return LibraryMap

#end getLibraries
#-------------------------------------------------------------------------------
# Create Functions
#-------------------------------------------------------------------------------
"""
FUNCTION:       setVar
ARGS:           admBeans, name, vaue, clusterName, [cellName]
RETURNS:        true/false string 
DESCRIPTION:    Used to set a WebSphere Managed Variable, defined via
                arguments name and value, at a Cluster scope.
"""
def setVar(admBeans, varName, varValue, clusterName, cellName=''):

  # Get a reference to AdminTask object
  AdminTask = admBeans['AdminTask']

  # set up scope srting
  scope = "Cell=%s,ServerCluster=%s" % (cellName, clusterName)
  return AdminTask.setVariable(['-variableName', varName, '-variableValue', varValue, '-scope', scope])

#end setVar
#-------------------------------------------------------------------------------
"""
FUNCTION:       createClusterMember
ARGS:           admBeans, propMap, clusterName, nodeName, [cellName]
RETURNS:        ID of the newly created/existing ClusterMember.
DESCRIPTION:    Used to create a new ClusterMember for the Cluster identified
		by the clusterName on a node identified by nodeName. 
		The cellName argument is optional. 
"""
def createClusterMember(admBeans,propMap,clusterName,nodeName,cellName=''):

  # Check required parameters.
  if not propMap.has_key('memberName') or not propMap['memberName']:
    raise ClusterError("In createClusterMember: Required attribute 'memberName' is missing.")
  memberName =  propMap['memberName']

  # Get reference to AdminConfig object.
  AdminConfig = admBeans['AdminConfig']

  # Get clusterId
  clusterId = AdminConfig.getid("/Cell:%s/ServerCluster:%s/" % (cellName,clusterName))
  if not clusterId:
    raise ClusterError("In createClusterMember: Null parentId for Cluster %s." % clusterName)

  # Get nodeId
  print "NODE NAME: %s" % nodeName
  nodeId = AdminConfig.getid("/Cell:%s/Node:%s/" % (cellName,nodeName))
  if not nodeId:
    raise ClusterError("In createClusterMember: Null nodeId for Node %s." % nodeName)

  # Check if Server with this name already exists.
  id = AdminConfig.getid("/Cell:%s/Node:%s/Server:%s/" % (cellName,nodeName,memberName))
  if id:
    print "Server %s already exists on node %s. Returing its id" % (memberName,nodeName)
    return id

  # Create a new ClusterMember
  id = Admin.createClusterMember(admBeans,propMap,clusterId,nodeId)

  return id
#end createClusterMember
#-------------------------------------------------------------------------------
"""
FUNCTION:       createJDBCProvider
ARGS:           admBeans, propMap, clusterName, [cellName]
RETURNS:        ID of the newly created/existing JDBCProvider.
DESCRIPTION:    Used to create a new JDBCProvider at Cluster scope identified
		by the clusterName. The cellName argument is optional. 
"""
def createJDBCProvider(admBeans,propMap,clusterName,cellName=''):

  # Check required parameters.
  if not propMap.has_key('name') or not propMap['name']:
    raise ClusterError("In createJDBCProvider: Required attribute 'name' is missing.")
  name =  propMap['name']

  # Get reference to AdminConfig object.
  AdminConfig = admBeans['AdminConfig']

  # Get parentId
  parentId = AdminConfig.getid("/Cell:%s/ServerCluster:%s/" % (cellName,clusterName))
  if not parentId:
    raise ClusterError("In createJDBCProvider: Null parentId for parent %s." % clusterName)

  # Check if this JDBCProvider already exists.
  id = AdminConfig.getid("/Cell:%s/ServerCluster:%s/JDBCProvider:%s/" % (cellName,clusterName,name))
  if id:
    print "JDBCProvider %s already exists in cluster %s. Returing its id" % (name,clusterName)
    return id

  # Create a new JDBCProvider
  id = Admin.createJDBCProvider(admBeans,propMap,parentId)

  return id

#end createJDBCProvider
#-------------------------------------------------------------------------------
"""
FUNCTION:       createDataSource
ARGS:           admBeans, propMap, clusterName, [cellName]
RETURNS:        ID of the newly created/existing DataSource.
DESCRIPTION:    Used to create a new DataSource at Cluster scope identified
		by the clusterName. The cellName argument is optional. 
"""
def createDataSource(admBeans,propMap,clusterName,cellName=''):

  # Check required parameters.
  if not propMap.has_key('name') or not propMap['name']:
    raise ClusterError("In createDataSource: Required attribute 'name' is missing.")
  name =  propMap['name']
  if not propMap.has_key('jdbcProviderName') or not propMap['jdbcProviderName']:
    raise ClusterError("In createDataSource: Required attribute 'jdbcProviderName' is missing.")
  jdbcProviderName =  propMap['jdbcProviderName']

  # Get reference to AdminConfig object.
  AdminConfig = admBeans['AdminConfig']

  # Get parentId
  parentId = AdminConfig.getid("/Cell:%s/ServerCluster:%s/JDBCProvider:%s/" % (cellName,clusterName,jdbcProviderName))
  if not parentId:
    raise ClusterError("In createDataSource: Null parentId for parent %s." % jdbcProviderName)

  # Check if this DataSource already exists.
  id = AdminConfig.getid("/Cell:%s/ServerCluster:%s/JDBCProvider:%s/DataSource:%s/" % (cellName,clusterName,jdbcProviderName,name))
  if id:
    print "DataSource %s already exists in cluster %s. Returing its id" % (name,clusterName)
    return id

  # Create a new DataSource
  id = Admin.createDataSource(admBeans,propMap,parentId)

  return id

#end createDataSource
#-------------------------------------------------------------------------------
"""
FUNCTION:       createLibrary
ARGS:           admBeans, propMap, clusterName, [cellName]
RETURNS:        ID of the newly created/existing Library.
DESCRIPTION:    Used to create a new Library at Cluster scope identified
		by the clusterName. The cellName argument is optional. 
"""
def createLibrary(admBeans,propMap,clusterName,cellName=''):

  # Check required parameters.
  if not propMap.has_key('name') or not propMap['name']:
    raise ClusterError("In createLibrary: Required attribute 'name' is missing.")
  name =  propMap['name']

  # Get reference to AdminConfig object.
  AdminConfig = admBeans['AdminConfig']

  # Get parentId
  parentId = AdminConfig.getid("/Cell:%s/ServerCluster:%s/" % (cellName,clusterName))
  if not parentId:
    raise ClusterError("In createLibrary: Null parentId for parent %s." % clusterName)

  # Check if this Library already exists.
  id = AdminConfig.getid("/Cell:%s/ServerCluster:%s/Library:%s/" % (cellName,clusterName,name))
  if id:
    print "Library %s already exists in cluster %s. Returing its id" % (name,clusterName)
    return id

  # Create a new Library
  id = Admin.createLibrary(admBeans,propMap,parentId)

  return id

#end createLibrary
#-------------------------------------------------------------------------------
"""
FUNCTION:       createMQQueueConnectionFactory
ARGS:           admBeans, propMap, clusterName, [cellName]
RETURNS:        ID of the newly created/existing MQQueueConnectionFactory.
DESCRIPTION:    Used to create a new MQQueueConnectionFactory at Cluster scope identified
		by the clusterName. The cellName argument is optional. 
"""
def createMQQueueConnectionFactory(admBeans,propMap,clusterName,cellName=''):

  # Check required parameters.
  if not propMap.has_key('jmsProviderName') or not propMap['jmsProviderName']:
    raise ClusterError("In createMQQueueConnectionFactory: Required attribute 'jmsProviderName' is missing.")
  jmsProviderName =  propMap['jmsProviderName']

  if not propMap.has_key('name') or not propMap['name']:
    raise ClusterError("In createMQQueueConnectionFactory: Required attribute 'name' is missing.")
  name =  propMap['name']

  # Get reference to AdminConfig object.
  AdminConfig = admBeans['AdminConfig']

  # Get parentId
  parentId = AdminConfig.getid("/Cell:%s/ServerCluster:%s/JMSProvider:%s/" % (cellName,clusterName,jmsProviderName))
  if not parentId:
    raise ClusterError("In createMQQueueConnectionFactory: Null parentId for parent %s." % jmsProviderName)

  # Check if this MQQueueConnectionFactory already exists.
  id = AdminConfig.getid("/Cell:%s/ServerCluster:%s/JMSProvider:%s/MQQueueConnectionFactory:%s/" % (cellName,clusterName,jmsProviderName,name))
  if id:
    print "MQQueueConnectionFactory %s already exists in cluster %s. Returing its id" % (name,clusterName)
    return id

  # Create a new MQQueueConnectionFactory
  id = Admin.createMQQueueConnectionFactory(admBeans,propMap,parentId)

  return id

#end createMQQueueConnectionFactory
#-------------------------------------------------------------------------------
"""
FUNCTION:       createMQQueue
ARGS:           admBeans, propMap, clusterName, [cellName]
RETURNS:        ID of the newly created/existing MQQueue.
DESCRIPTION:    Used to create a new MQQueue at Cluster scope identified
		by the clusterName. The cellName argument is optional. 
"""
def createMQQueue(admBeans,propMap,clusterName,cellName=''):

  # Check required parameters.
  if not propMap.has_key('jmsProviderName') or not propMap['jmsProviderName']:
    raise ClusterError("In createMQQueue: Required attribute 'jmsProviderName' is missing.")
  jmsProviderName =  propMap['jmsProviderName']

  if not propMap.has_key('name') or not propMap['name']:
    raise ClusterError("In createMQQueue: Required attribute 'name' is missing.")
  name =  propMap['name']

  # Get reference to AdminConfig object.
  AdminConfig = admBeans['AdminConfig']

  # Get parentId
  parentId = AdminConfig.getid("/Cell:%s/ServerCluster:%s/JMSProvider:%s/" % (cellName,clusterName,jmsProviderName))
  if not parentId:
    raise ClusterError("In createMQQueue: Null parentId for parent %s." % jmsProviderName)

  # Check if this MQQueue already exists.
  id = AdminConfig.getid("/Cell:%s/ServerCluster:%s/JMSProvider:%s/MQQueue:%s/" % (cellName,clusterName,jmsProviderName,name))
  if id:
    print "MQQueue %s already exists in cluster %s. Returing its id" % (name,clusterName)
    return id

  # Create a new MQQueue
  id = Admin.createMQQueue(admBeans,propMap,parentId)

  return id

#end createMQQueue
#-------------------------------------------------------------------------------
"""
FUNCTION:       createMQTopicConnectionFactory
ARGS:           admBeans, propMap, clusterName, [cellName]
RETURNS:        ID of the newly created/existing MQTopicConnectionFactory.
DESCRIPTION:    Used to create a new MQTopicConnectionFactory at Cluster scope identified
		by the clusterName. The cellName argument is optional. 
"""
def createMQTopicConnectionFactory(admBeans,propMap,clusterName,cellName=''):

  # Check required parameters.
  if not propMap.has_key('jmsProviderName') or not propMap['jmsProviderName']:
    raise ClusterError("In createMQTopicConnectionFactory: Required attribute 'jmsProviderName' is missing.")
  jmsProviderName =  propMap['jmsProviderName']

  if not propMap.has_key('name') or not propMap['name']:
    raise ClusterError("In createMQTopicConnectionFactory: Required attribute 'name' is missing.")
  name =  propMap['name']

  # Get reference to AdminConfig object.
  AdminConfig = admBeans['AdminConfig']

  # Get parentId
  parentId = AdminConfig.getid("/Cell:%s/ServerCluster:%s/JMSProvider:%s/" % (cellName,clusterName,jmsProviderName))
  if not parentId:
    raise ClusterError("In createMQTopicConnectionFactory: Null parentId for parent %s." % jmsProviderName)

  # Check if this MQTopicConnectionFactory already exists.
  id = AdminConfig.getid("/Cell:%s/ServerCluster:%s/JMSProvider:%s/MQTopicConnectionFactory:%s/" % (cellName,clusterName,jmsProviderName,name))
  if id:
    print "MQTopicConnectionFactory %s already exists in cluster %s. Returing its id" % (name,clusterName)
    return id

  # Create a new MQTopicConnectionFactory
  id = Admin.createMQTopicConnectionFactory(admBeans,propMap,parentId)

  return id

#end createMQTopicConnectionFactory
#-------------------------------------------------------------------------------
"""
FUNCTION:       createMQTopic
ARGS:           admBeans, propMap, clusterName, [cellName]
RETURNS:        ID of the newly created/existing MQTopic.
DESCRIPTION:    Used to create a new MQTopic at Cluster scope identified
		by the clusterName. The cellName argument is optional. 
"""
def createMQTopic(admBeans,propMap,clusterName,cellName=''):

  # Check required parameters.
  if not propMap.has_key('jmsProviderName') or not propMap['jmsProviderName']:
    raise ClusterError("In createMQTopic: Required attribute 'jmsProviderName' is missing.")
  jmsProviderName =  propMap['jmsProviderName']

  if not propMap.has_key('name') or not propMap['name']:
    raise ClusterError("In createMQTopic: Required attribute 'name' is missing.")
  name =  propMap['name']

  # Get reference to AdminConfig object.
  AdminConfig = admBeans['AdminConfig']

  # Get parentId
  parentId = AdminConfig.getid("/Cell:%s/ServerCluster:%s/JMSProvider:%s/" % (cellName,clusterName,jmsProviderName))
  if not parentId:
    raise ClusterError("In createMQTopic: Null parentId for parent %s." % jmsProviderName)

  # Check if this MQTopic already exists.
  id = AdminConfig.getid("/Cell:%s/ServerCluster:%s/JMSProvider:%s/MQTopic:%s/" % (cellName,clusterName,jmsProviderName,name))
  if id:
    print "MQTopic %s already exists in cluster %s. Returing its id" % (name,clusterName)
    return id

  # Create a new MQTopic
  id = Admin.createMQTopic(admBeans,propMap,parentId)

  return id

#end createMQTopic
#-------------------------------------------------------------------------------
"""
FUNCTION:       createWorkManager
ARGS:           admBeans, propMap, clusterName, [cellName]
RETURNS:        ID of the newly created/existing WorkManager.
DESCRIPTION:    Used to create a new WorkManager at Cluster scope identified
		by the clusterName. The cellName argument is optional. 
"""
def createWorkManager(admBeans,propMap,clusterName,cellName=''):

  # Check required parameters.
  if not propMap.has_key('name') or not propMap['name']:
    raise ClusterError("In createWorkManager: Required attribute 'name' is missing.")
  name =  propMap['name']

  # Get reference to AdminConfig object.
  AdminConfig = admBeans['AdminConfig']

  # Get parentId
  parentId = AdminConfig.getid("/Cell:%s/ServerCluster:%s/WorkManagerProvider:WorkManagerProvider/"  
                                              % (cellName,clusterName))
  if not parentId:
    raise ClusterError("In createWorkManager: Null parentId for parent WorkManagerProvider in cluster %s." % clusterName)

  # Check if this WorkManager already exists.
  id = AdminConfig.getid("/Cell:%s/ServerCluster:%s/WorkManagerProvider:WorkManagerProvider/WorkManagerInfo:%s/" 
                                 % (cellName,clusterName,name))
  if id:
    print "WorkManager %s already exists in cluster %s. Returing its id" % (name,clusterName)
    return id

  # Create a new WorkManager
  id = Admin.createWorkManager(admBeans,propMap,parentId)

  return id

#end createWorkManager
#-------------------------------------------------------------------------------
