import sys
import os
import re
#sys.path.append('C:\WID\WAS61ToolsLib')
#from was61core import *
import Admin
import Cell
import Node
import Server
import Cluster
import Utils

#
#----------------------------------------------------------
#
class DefaultActionsError(Utils.Error):
  
  def __init__(self,msg=''):
    msg = "DefaultActionsError: %s" % msg
    Utils.Error.__init__(self,msg)

#
#-------------------------------------------------------------------------
# Test Action 
#-------------------------------------------------------------------------
#
def testAction(admBeans, props, args = []):
  print "Action: testAction"
  print "Arguments: ", args
  print "Properties are:"
  props.print()

#
#-------------------------------------------------------------------------
# Action to configure JVM Attributes
#-------------------------------------------------------------------------
#
def setupJvmAttributes(admBeans, props, args = []):
  print "Setting up JVM Attributes"

  # extract required properties
  if props.isSet('cellName'):
    cellName = props.get('cellName')
  else:
    cellName = Cell.getName(admBeans)
  if not props.isSet('nodeName'):
    raise DefaultActionsError("In setupJvmAttributes: required parameter 'nodeName' is missing")           
  nodeName=props.get('nodeName')
  if not props.isSet('serverName'):
    raise DefaultActionsError("In setupJvmAttributes: required parameter 'serverName' is missing")           
  serverName=props.get('serverName')

  # Now Extract property subMap for JVM attributes and set them.
  patt = r'^jvm\.'
  subMap = props.getSubMap(patt)
  if len(subMap) > 0:
    print "Setting JVM Attributes of Application Server"
    Server.setJvmAttributes(admBeans, subMap, serverName, nodeName, cellName)
  else:
    print "There are no JVM Attributes to set."
  
#
#-------------------------------------------------------------------------
# Action to configure JVM Custom Properties
#-------------------------------------------------------------------------
#
def setupJvmCustomProperties(admBeans, props, args = []):
  print "Setting up JVM Custom Properties"

  # extract required properties
  if props.isSet('cellName'):
    cellName = props.get('cellName')
  else:
    cellName = Cell.getName(admBeans)
  if not props.isSet('nodeName'):
    raise DefaultActionsError("In setupJvmCustomProperties: required parameter 'nodeName' is missing")           
  nodeName=props.get('nodeName')
  if not props.isSet('serverName'):
    raise DefaultActionsError("In setupJvmCustomProperties: required parameter 'serverName' is missing")           
  serverName=props.get('serverName')

  # Now Extract property subMap for JVM Custom Properties and set them.
  patt = r'^jvmCustomProperty\.'
  subMap = props.getSubMap(patt)
  if len(subMap) > 0:
    print "Setting JVM Custom Properties for the Application Server"
    for k in subMap.keys():
      print "Setting property \'%s\' to value \'%s\'" % (k, subMap[k])
      Server.setJvmCustomProperty(admBeans, k, subMap[k], serverName, nodeName, cellName)
  else:
    print "There are no JVM Custom Properties to set."
  
#
#-------------------------------------------------------------------------
# Action to configure Server Stdout attributes
#-------------------------------------------------------------------------
#
def setupServerStdout(admBeans, props, args = []):
  print "Setting up Server Stdout Attributes"

  # extract required properties
  if props.isSet('cellName'):
    cellName = props.get('cellName')
  else:
    cellName = Cell.getName(admBeans)
  if not props.isSet('nodeName'):
    raise DefaultActionsError("In setupServerStdout: required parameter 'nodeName' is missing")           
  nodeName=props.get('nodeName')
  if not props.isSet('serverName'):
    raise DefaultActionsError("In setupServerStdout: required parameter 'serverName' is missing")           
  serverName=props.get('serverName')

  # Now Extract property subMap for Stdout attributes and update them.
  patt = r'^stdout\.'
  subMap = props.getSubMap(patt)
  if len(subMap) > 0:
    print "Setting Attributes of SystemOut log for the Application Server"
    Server.modifyStdout(admBeans, subMap, serverName, nodeName, cellName)
  else:
    print "There are no Server Stdout attributes to be set."
  
#
#-------------------------------------------------------------------------
# Action to configure Server Stderr attributes
#-------------------------------------------------------------------------
#
def setupServerStderr(admBeans, props, args = []):
  print "Setting up Server Stderr Attributes"

  # extract required properties
  if props.isSet('cellName'):
    cellName = props.get('cellName')
  else:
    cellName = Cell.getName(admBeans)
  if not props.isSet('nodeName'):
    raise DefaultActionsError("In setupServerStderr: required parameter 'nodeName' is missing")           
  nodeName=props.get('nodeName')
  if not props.isSet('serverName'):
    raise DefaultActionsError("In setupServerStderr: required parameter 'serverName' is missing")           
  serverName=props.get('serverName')

  # Now Extract property subMap for Stderr attributes and update them.
  patt = r'^stderr\.'
  subMap = props.getSubMap(patt)
  if len(subMap) > 0:
    print "Setting Attributes of SystemErr log for the Application Server"
    Server.modifyStderr(admBeans, subMap, serverName, nodeName, cellName)
  else:
    print "There are no Server Stderr attributes to be set."
  
#
#-------------------------------------------------------------------------
# Action to configure WebContainer Threadpool attributes
#-------------------------------------------------------------------------
#
def setupWCThreadpool(admBeans, props, args = []):
  print "Setting up WebContainer Threadpool Attributes"

  # extract required properties
  if props.isSet('cellName'):
    cellName = props.get('cellName')
  else:
    cellName = Cell.getName(admBeans)
  if not props.isSet('nodeName'):
    raise DefaultActionsError("In setupWCThreadpool: required parameter 'nodeName' is missing")           
  nodeName=props.get('nodeName')
  if not props.isSet('serverName'):
    raise DefaultActionsError("In setupWCThreadpool: required parameter 'serverName' is missing")           
  serverName=props.get('serverName')

  # Now Extract property subMap for WC Threadpool attributes and update them.
  patt = r'^WCThreadpool\.'
  subMap = props.getSubMap(patt)
  if len(subMap) > 0:
    print "Setting Attributes of WebContainer Threadpool for the Application Server"
    Server.modifyWCThreadpool(admBeans, subMap, serverName, nodeName, cellName)
  else:
    print "There are no WebContainer Threadpool attributes to be set."
  
#
#-------------------------------------------------------------------------
# Action to configure Environment Entries
#-------------------------------------------------------------------------
#
def setupEnvEntries(admBeans, props, args = []):
  print "Setting up Environment Entries"

  # extract required properties
  if props.isSet('cellName'):
    cellName = props.get('cellName')
  else:
    cellName = Cell.getName(admBeans)
  if not props.isSet('nodeName'):
    raise DefaultActionsError("In setupServerStderr: required parameter 'nodeName' is missing")           
  nodeName=props.get('nodeName')
  if not props.isSet('serverName'):
    raise DefaultActionsError("In setupServerStderr: required parameter 'serverName' is missing")           
  serverName=props.get('serverName')

  # Now Extract property subMap for Environment Entries and set them.
  patt = r'^envEntry\.'
  subMap = props.getSubMap(patt)
  if len(subMap) > 0:
    print "Setting Environment Entries for the Application Server"
    for k in subMap.keys():
      print "Setting Environment Entry \'%s\' to value \'%s\'" % (k, subMap[k])
      Server.setEnvEntry(admBeans, k, subMap[k], serverName, nodeName, cellName)
  else:
    print "There are no Environment Entries to be set."
  
#
#-------------------------------------------------------------------------
# Action to configure Application Server Ports
#-------------------------------------------------------------------------
#
def setupServerPorts(admBeans, props, args = []):
  print "Setting up Application Server Ports"

  # extract required properties
  if props.isSet('cellName'):
    cellName = props.get('cellName')
  else:
    cellName = Cell.getName(admBeans)
  if not props.isSet('nodeName'):
    raise DefaultActionsError("In setupServerPorts: required parameter 'nodeName' is missing")           
  nodeName=props.get('nodeName')
  if not props.isSet('serverName'):
    raise DefaultActionsError("In setupServerPorts: required parameter 'serverName' is missing")           
  serverName=props.get('serverName')

  # Now Extract property subMap for Server Ports and set them.
  patt = r'^serverPort\.'
  subMap = props.getSubMap(patt)
  if len(subMap) > 0:
    print "Setting Ports for Application Server"
    for portName in subMap.keys():
      port = subMap[portName]
      Server.setPort(admBeans, portName, port, serverName, nodeName, cellName)
  else:
    print "There are no Application Server Ports to be set."

#
#-------------------------------------------------------------------------
# Action to configure Listener Ports for Messaging Beans
#-------------------------------------------------------------------------
#
def setupListenerPorts(admBeans, props, args = []):
  print "Setting up Listener Ports"

  # extract required properties
  if props.isSet('cellName'):
    cellName = props.get('cellName')
  else:
    cellName = Cell.getName(admBeans)
  if not props.isSet('nodeName'):
    raise DefaultActionsError("In setupServerPorts: required parameter 'nodeName' is missing")           
  nodeName=props.get('nodeName')
  if not props.isSet('serverName'):
    raise DefaultActionsError("In setupServerPorts: required parameter 'serverName' is missing")           
  serverName=props.get('serverName')

  # Now Extract property subMap for Listener Ports and create them.
  patt = re.compile(r'^(listenerPort\d{,}\.)name')
  ks = props.getKeys()
  for k in ks:
    match = patt.search(k)
    if match:
      subMap = props.getSubMap(match.group(1))
      name = subMap['name']
      print "Creating Listener Port %s on %s/%s" % (name, nodeName, serverName)
      id = Server.createListenerPort(admBeans, subMap, serverName, nodeName, cellName)
      if not id:
        print "Failed to Create Listener Port %s on %s/%s" % (name, nodeName, serverName)
      else:
        #print Admin.showObject(admBeans, id)
        print id

#
#-------------------------------------------------------------------------
# Action to configure a Standard Cluster.
#-------------------------------------------------------------------------
#
def setupStandardCluster(admBeans, props, args = []):
  print "Setting up Cluster"

  AdminConfig = admBeans['AdminConfig']

  # extract required properties
  if not props.isSet('jvmShortName'):
    raise DefaultActionsError("In setupStandardCluster: required parameter 'jvmShortName' is missing")           
  jvmShortName=props.get('jvmShortName')
  if not props.isSet('env'):
    raise DefaultActionsError("In setupStandardCluster: required parameter 'env' is missing")           
  env=props.get('env')
  if not props.isSet('cellShortName'):
    raise DefaultActionsError("In setupStandardCluster: required parameter 'cellShortName' is missing")          
  cellShortName=props.get('cellShortName')
  if props.isSet('cellName'):
    cellName = props.get('cellName')
  else:
    cellName = Cell.getName(admBeans)

  # If clusterName is defined, set a standard default name
  if props.isSet('clusterName'):
    clusterName = props.get('clusterName')
  else:
    clusterName = "%s%sCluster" % (jvmShortName, env)

  # Create empty cluster
  propMap = props.getSubMap(r'^cluster\.')
  #clusterName = propMap['name']
  propMap['name'] = clusterName
  id = Cell.createCluster(admBeans, propMap,cellName)
  #print AdminConfig.show(id)

  # Extract node list from props and create member(s) on each node
  patt1 = re.compile(r'^(node\d{,}\.)host')
  ks = props.getKeys()
  for k1 in ks:
    match1 = patt1.search(k1)
    if match1:
      nodeSubMap = props.getSubMap(match1.group(1))
      nodeHost = nodeSubMap['host']

      # if node name is defined in prop file use that else
      # create a default name
      if nodeSubMap.has_key('name'):
        nodeName = nodeSubMap['name']
      else:
        #nodeName = "%s%s%sNode0" % (cellShortName,env,nodeHost) 
        nodeName = "%s%sNode0" % (cellShortName,nodeHost) 
      print nodeName

      # if member names are defined in prop file use those 
      # else create default names using noClones property
      memberList = []
      patt2 = re.compile('^(' + match1.group(1) + 'member\d{,}\.)name')
      for k2 in ks:
        match2 = patt2.search(k2)
        if match2:
	  memberList.append(props.get(k2))
      if len(memberList) == 0:
        if nodeSubMap.has_key('noClones'):
	  noClones = nodeSubMap['noClones']
        else:
	  noClones = 1
        for i in range(0, int(noClones)):
          memberList.append("%s%s%sClone%d" % (jvmShortName,env,nodeHost,i))

      # Now create each member and configure it
      for m in memberList:

        # Create member
        mPropMap = {}
        mPropMap['memberName'] = m
        print "  Creating a ClusterMember %s for %s on Node %s" % (m,clusterName,nodeName)
        mId = Cluster.createClusterMember(admBeans,mPropMap,clusterName,nodeName)
        print AdminConfig.show(mId)

        # add props that uniquely identify this member
	mProps = props.clone()
	mProps.set('serverName', m)
	mProps.set('nodeName', nodeName)
	mProps.set('cellName', cellName)

        # Set up JVM Attributes
	setupJvmAttributes(admBeans,mProps)

        # Set up JVM Custom Properties
	setupJvmCustomProperties(admBeans,mProps)

        # Set up JVM Stdout attributes
	setupServerStdout(admBeans,mProps)

        # Set up JVM Stderr attributes
	setupServerStderr(admBeans,mProps)

        # Set up WC Threadpool attributes
	setupWCThreadpool(admBeans,mProps)

        # Set up Application Server Ports
        setupServerPorts(admBeans,mProps)

        # Set up Environ Entries
	setupEnvEntries(admBeans,mProps)

        # Set up Listener Ports 
        setupListenerPorts(admBeans,mProps)

#
#-------------------------------------------------------------------------
# Action to configure Application Server.
#-------------------------------------------------------------------------
#
def setupAppServer(admBeans, props, args = []):
  print "Setting up Application Server"

  # get the property map to be sent to Server creation function.
  patt = r'^server\.'
  subMap = props.getSubMap(patt)

  # Check required parameters
  if props.isSet('cellName'):
    cellName = props.get('cellName')
  else:
    cellName = Cell.getName(admBeans)
  if not props.isSet('nodeName'):
    raise DefaultActionsError("In setupAppServer: required parameter 'nodeName' is missing")           
  nodeName = props.get('nodeName')
  if not props.isSet('serverName'):
    raise DefaultActionsError("In setupAppServer: required parameter 'serverName' is missing")           
  serverName = props.get('serverName')
  subMap['name'] = serverName

  # Create the App Server
  print "Creating Application Server"
  id = Node.createServer(admBeans, subMap, nodeName, cellName)
  if not id:
    raise DefaultActionsError("In setupAppServer: Failed to create Application Server")           
  #print Admin.showObject(admBeans, id)
  #print  "Server ID: ", id

  # Set up JVM Attributes
  setupJvmAttributes(admBeans,props)

  # Set up JVM Custom Properties
  setupJvmCustomProperties(admBeans,props)

  # Set up JVM Stdout attributes
  setupServerStdout(admBeans,props)

  # Set up JVM Stderr attributes
  setupServerStderr(admBeans,props)

  # Set up WC Threadpool attributes
  setupWCThreadpool(admBeans,props)

  # Set up Environ Entries
  setupEnvEntries(admBeans,props)

  # Set up Application Server Ports
  setupServerPorts(admBeans,props)

  # Set up Any Listener Ports needed
  setupListenerPorts(admBeans,props)

#
#-------------------------------------------------------------------------
# Action to configure up all the WebSphere Variables at various scopes.
#-------------------------------------------------------------------------
#
def setupWebSphereVariables(admBeans, props, args = []):
  print "Setting up WebSphere Variables"
  patt = re.compile(r'^(var\d{,}\.)name')
  ks = props.getKeys()
  for k in ks:
    match = patt.search(k)
    if match:
      subMap = props.getSubMap(match.group(1))
      name = subMap['name']
      if not subMap.has_key('value'):
        raise DefaultActionsError("In setupWebSphereVariables: required parameter 'value' is missing for Var %s" % name)           
      value = subMap['value']
      if not subMap.has_key('scope'):
        raise DefaultActionsError("In setupWebSphereVariables: required parameter 'scope' is missing for Var %s" % name)           
      scope = subMap['scope']

      # Get Cell Name
      if props.isSet('cellName'):
        cellName = props.get('cellName')
      else:
        cellName = Cell.getName(admBeans)

      # Check scope and invoke appropriate function
      if scope.lower() == 'cell':
        print "Setting variable %s to %s on %s" % (name, value, cellName)
	print "Status: ", Cell.setVar(admBeans, name, value, cellName)

      elif scope.lower() == 'node':
        if subMap.has_key('nodeName'):
          nodeName = subMap['nodeName']
        elif props.isSet('nodeName'):
          nodeName = props.get('nodeName')
        else:
          raise DefaultActionsError("In setupWebSphereVariables: required parameter 'nodeName' is missing")           
        print "Setting variable %s to %s on %s/%s" % (name, value, cellName, nodeName)
	print "Status: ", Node.setVar(admBeans, name, value, nodeName, cellName)

      elif scope.lower() == 'cluster':
        if subMap.has_key('clusterName'):
          clusterName = subMap['clusterName']
        elif props.isSet('clusterName'):
          clusterName = props.get('clusterName')
        else:
          raise DefaultActionsError("In setupWebSphereVariables: required parameter 'clusterName' is missing")           
        print "Setting variable %s to %s on %s/%s" % (name, value, cellName, clusterName)
	print "Status: ", Cluster.setVar(admBeans, name, value, clusterName, cellName)

      elif scope.lower() == 'server':
        if subMap.has_key('serverName'):
          serverName = subMap['serverName']
        elif props.isSet('serverName'):
            serverName = props.get('serverName')
        else:
          raise DefaultActionsError("In setupWebSphereVariables: required parameter 'serverName' is missing")           
        if subMap.has_key('nodeName'):
          nodeName = subMap['nodeName']
        elif props.isSet('nodeName'):
          nodeName = props.get('nodeName')
        else:
          raise DefaultActionsError("In setupWebSphereVariables: required parameter 'nodeName' is missing")           
        print "Setting variable %s to %s on %s/%s/%s" % (name, value, cellName, nodeName, serverName)
	print "Status: ", Server.setVar(admBeans, name, value, serverName, nodeName, cellName)

      elif scope.lower() == 'clustermember':
        if subMap.has_key('clusterName'):
          clusterName = subMap['clusterName']
        elif props.isSet('clusterName'):
          clusterName = props.get('clusterName')
        else:
          raise DefaultActionsError("In setupWebSphereVariables: required parameter 'clusterName' is missing")           
        print "Setting variable %s to %s on clusterMembers of cluster %s" % (name, value, clusterName)
	memberMap =  Cluster.getMembers(admBeans,clusterName,cellName)
	for mName in (memberMap.keys()):
          mId = memberMap[mName]
          admCfg = admBeans['AdminConfig']  
	  ndName = admCfg.showAttribute(mId, 'nodeName')
          print "Setting variable %s to %s on %s/%s/%s" % (name, value, cellName, ndName, mName)
	  print "Status: ", Server.setVar(admBeans, name, value, mName, ndName, cellName)

      else:
        print "Unknown scope: %s" % scope
#
#-------------------------------------------------------------------------
# Action to configure all the J2CAuthAliases.
#-------------------------------------------------------------------------
#
def setupJ2CAuthAliases(admBeans, props, args = []):
  print "Setting up J2CAuthAliases"

  if props.isSet('cellName'):
    cellName = props.get('cellName')
  else:
    cellName = Cell.getName(admBeans)

  patt = re.compile(r'^(j2cAuthAlias\d{,}\.)alias')
  ks = props.getKeys()
  for k in ks:
    match = patt.search(k)
    if match:
      subMap = props.getSubMap(match.group(1))
      alias = subMap['alias']
      if subMap.has_key('userId'):
        userId = subMap['userId']
      else:
        raise DefaultActionsError("In setupJ2CAuthAliases : required parameter 'userId' is missing")           
      if subMap.has_key('password'):
        password = subMap['password']
      else:
        raise DefaultActionsError("In setupJ2CAuthAliases : required parameter 'password' is missing")           
      id = Cell.createJAASAuthData(admBeans, alias, userId, password, cellName)
      if not id:
        print "Failed to create Authentication Alias"
      else:
        #print Admin.showObject(admBeans, id)
        print id

#
#-------------------------------------------------------------------------
# Action to configure all the JDBCProviders at various scopes.
#-------------------------------------------------------------------------
#
def setupJDBCProviders(admBeans, props, args = []):
  print "Setting up JDBCProviders"

  if props.isSet('cellName'):
    cellName = props.get('cellName')
  else:
    cellName = Cell.getName(admBeans)

  patt = re.compile(r'^(jdbcProvider\d{,}\.)name')
  ks = props.getKeys()
  for k in ks:
    match = patt.search(k)
    if match:
      subMap = props.getSubMap(match.group(1))
      name = subMap['name']

      # Identify the JDBCProviderTemplate to be used from supplied properties
      # and add that property to subMap
      templateName = Admin.getJdbcTemplateName(subMap)
      if not templateName:
        if not subMap.has_key('implementationClassName'):
          raise DefaultActionsError("In setupJDBCProviders: either templateName or implementationClassName is required.")           
        print "implementationClassName: ", subMap['implementationClassName']
      print "templateName: ", templateName
      subMap['templateName'] = templateName

      if not subMap.has_key('scope'):
        raise DefaultActionsError("In setupJDBCProviders: required parameter 'scope' is missing for JDBCProvider %s" % name)           
      scope = subMap['scope']

      # Check scope and invoke appropriate function
      if scope.lower() == 'cell':
        print "Creating JDBCProvider %s on %s" % (name, cellName)
	id = Cell.createJDBCProvider(admBeans, subMap, cellName)
	if not id:
	  print "Failed to create JDBCProvider"
        else:
	  #print Admin.showObject(admBeans, id)
	  print id

      elif scope.lower() == 'node':
        if subMap.has_key('nodeName'):
          nodeName = subMap['nodeName']
        elif props.isSet('nodeName'):
          nodeName = props.get('nodeName')
        else:
          raise DefaultActionsError("In setupJDBCProviders: required parameter 'nodeName' is missing")           
        print "Creating JDBCProvider %s on %s/%s" % (name, cellName, nodeName)
	id = Node.createJDBCProvider(admBeans, subMap, nodeName, cellName)
	if not id:
	  print "Failed to create JDBCProvider"
        else:
	  #print Admin.showObject(admBeans, id)
	  print id

      elif scope.lower() == 'cluster':
        if subMap.has_key('clusterName'):
          clusterName = subMap['clusterName']
        elif props.isSet('clusterName'):
          clusterName = props.get('clusterName')
        else:
          raise DefaultActionsError("In setupJDBCProviders: required parameter 'clusterName' is missing")           
        print "Creating JDBCProvider %s on %s/%s" % (name, cellName, clusterName)
	id = Cluster.createJDBCProvider(admBeans, subMap, clusterName, cellName)
	if not id:
	  print "Failed to create JDBCProvider"
        else:
	  #print Admin.showObject(admBeans, id)
	  print id

      elif scope.lower() == 'server':
        if subMap.has_key('serverName'):
          serverName = subMap['serverName']
        elif props.isSet('serverName'):
            serverName = props.get('serverName')
        else:
          raise DefaultActionsError("In setupJDBCProviders: required parameter 'serverName' is missing")           
        if subMap.has_key('nodeName'):
          nodeName = subMap['nodeName']
        elif props.isSet('nodeName'):
          nodeName = props.get('nodeName')
        else:
          raise DefaultActionsError("In setupJDBCProviders: required parameter 'nodeName' is missing")           
        print "Creating JDBCProvider %s on %s/%s/%s" % (name, cellName, nodeName, serverName)
	id = Server.createJDBCProvider(admBeans, subMap, serverName, nodeName, cellName)
	if not id:
	  print "Failed to create JDBCProvider"
        else:
	  #print Admin.showObject(admBeans, id)
	  print id

      elif scope.lower() == 'clustermember':
        if subMap.has_key('clusterName'):
          clusterName = subMap['clusterName']
        elif props.isSet('clusterName'):
          clusterName = props.get('clusterName')
        else:
          raise DefaultActionsError("In setupJDBCProviders: required parameter 'clusterName' is missing")           
        print "Creating JDBCProvider %s on clusterMembers of cluster %s" % (name, clusterName)
	memberMap =  Cluster.getMembers(admBeans,clusterName,cellName)
	for mName in (memberMap.keys()):
          mId = memberMap[mName]
          admCfg = admBeans['AdminConfig']  
	  ndName = admCfg.showAttribute(mId, 'nodeName')
          print "Creating JDBCProvider %s on clusterMember %s of cluster %s" % (name, mName, clusterName)
	  id = Server.createJDBCProvider(admBeans, subMap, mName, ndName, cellName)
	  if not id:
	    print "Failed to create JDBCProvider %s" % name
          else:
	    #print Admin.showObject(admBeans, id)
	    print id

      else:
        print "Unknown scope: %s" % scope
#
#
#-------------------------------------------------------------------------
# Action to configure all the DataSources at various scopes.
#-------------------------------------------------------------------------
#
def setupDataSources(admBeans, props, args = []):
  print "Setting up DataSources"

  if props.isSet('cellName'):
    cellName = props.get('cellName')
  else:
    cellName = Cell.getName(admBeans)

  patt = re.compile(r'^(dataSource\d{,}\.)name')
  ks = props.getKeys()
  for k in ks:
    match = patt.search(k)
    if match:
      subMap = props.getSubMap(match.group(1))
      name = subMap['name']

      if not subMap.has_key('scope'):
        raise DefaultActionsError("In setupDataSources: required parameter 'scope' is missing for DataSource %s" % name)           
      scope = subMap['scope']

      # Check scope and invoke appropriate function
      if scope.lower() == 'cell':
        print "Creating DataSource %s on %s" % (name, cellName)
	id = Cell.createDataSource(admBeans, subMap, cellName)
	if not id:
	  print "Failed to create DataSource"
        else:
	  #print Admin.showObject(admBeans, id)
	  print id

      elif scope.lower() == 'node':
        if subMap.has_key('nodeName'):
          nodeName = subMap['nodeName']
        elif props.isSet('nodeName'):
          nodeName = props.get('nodeName')
        else:
          raise DefaultActionsError("In setupDataSources: required parameter 'nodeName' is missing")           
        print "Creating DataSource %s on %s/%s" % (name, cellName, nodeName)
	id = Node.createDataSource(admBeans, subMap, nodeName, cellName)
	if not id:
	  print "Failed to create DataSource"
        else:
	  #print Admin.showObject(admBeans, id)
	  print id

      elif scope.lower() == 'cluster':
        if subMap.has_key('clusterName'):
          clusterName = subMap['clusterName']
        elif props.isSet('clusterName'):
          clusterName = props.get('clusterName')
        else:
          raise DefaultActionsError("In setupDataSources: required parameter 'clusterName' is missing")           
        print "Creating DataSource %s on %s/%s" % (name, cellName, clusterName)
	id = Cluster.createDataSource(admBeans, subMap, clusterName, cellName)
	if not id:
	  print "Failed to create DataSource"
        else:
	  #print Admin.showObject(admBeans, id)
	  print id

      elif scope.lower() == 'server':
        if subMap.has_key('serverName'):
          serverName = subMap['serverName']
        elif props.isSet('serverName'):
            serverName = props.get('serverName')
        else:
          raise DefaultActionsError("In setupDataSources: required parameter 'serverName' is missing")           
        if subMap.has_key('nodeName'):
          nodeName = subMap['nodeName']
        elif props.isSet('nodeName'):
          nodeName = props.get('nodeName')
        else:
          raise DefaultActionsError("In setupDataSources: required parameter 'nodeName' is missing")           
        print "Creating DataSource %s on %s/%s/%s" % (name, cellName, nodeName, serverName)
	id = Server.createDataSource(admBeans, subMap, serverName, nodeName, cellName)
	if not id:
	  print "Failed to create DataSource"
        else:
	  #print Admin.showObject(admBeans, id)
	  print id

      elif scope.lower() == 'clustermember':
        if subMap.has_key('clusterName'):
          clusterName = subMap['clusterName']
        elif props.isSet('clusterName'):
          clusterName = props.get('clusterName')
        else:
          raise DefaultActionsError("In setupDataSources: required parameter 'clusterName' is missing")           
        print "Creating DataSource %s on clusterMembers of cluster %s" % (name, clusterName)
	memberMap =  Cluster.getMembers(admBeans,clusterName,cellName)
	for mName in (memberMap.keys()):
          mId = memberMap[mName]
          admCfg = admBeans['AdminConfig']  
	  ndName = admCfg.showAttribute(mId, 'nodeName')
          print "Creating DataSource %s on clusterMember %s of cluster %s" % (name, mName, clusterName)
	  id = Server.createDataSource(admBeans, subMap, mName, ndName, cellName)
	  if not id:
	    print "Failed to create DataSource %s" % name
          else:
	    #print Admin.showObject(admBeans, id)
	    print id

      else:
        print "Unknown scope: %s" % scope

#
#-------------------------------------------------------------------------
# Action to configure all the Libraries at various scopes.
#-------------------------------------------------------------------------
#
def setupLibraries(admBeans, props, args = []):
  print "Setting up Libraries"

  if props.isSet('cellName'):
    cellName = props.get('cellName')
  else:
    cellName = Cell.getName(admBeans)

  patt = re.compile(r'^(library\d{,}\.)name')
  ks = props.getKeys()
  for k in ks:
    match = patt.search(k)
    if match:
      subMap = props.getSubMap(match.group(1))
      name = subMap['name']

      if not subMap.has_key('scope'):
        raise DefaultActionsError("In setupLibrarys: required parameter 'scope' is missing for Library %s" % name)           
      scope = subMap['scope']

      # Check scope and invoke appropriate function
      if scope.lower() == 'cell':
        print "Creating Library %s on %s" % (name, cellName)
	id = Cell.createLibrary(admBeans, subMap, cellName)
	if not id:
	  print "Failed to create Library"
        else:
	  #print Admin.showObject(admBeans, id)
	  print id

      elif scope.lower() == 'node':
        if subMap.has_key('nodeName'):
          nodeName = subMap['nodeName']
        elif props.isSet('nodeName'):
          nodeName = props.get('nodeName')
        else:
          raise DefaultActionsError("In setupLibrarys: required parameter 'nodeName' is missing")           
        print "Creating Library %s on %s/%s" % (name, cellName, nodeName)
	id = Node.createLibrary(admBeans, subMap, nodeName, cellName)
	if not id:
	  print "Failed to create Library"
        else:
	  #print Admin.showObject(admBeans, id)
	  print id

      elif scope.lower() == 'cluster':
        if subMap.has_key('clusterName'):
          clusterName = subMap['clusterName']
        elif props.isSet('clusterName'):
          clusterName = props.get('clusterName')
        else:
          raise DefaultActionsError("In setupLibrarys: required parameter 'clusterName' is missing")           
        print "Creating Library %s on %s/%s" % (name, cellName, clusterName)
	id = Cluster.createLibrary(admBeans, subMap, clusterName, cellName)
	if not id:
	  print "Failed to create Library"
        else:
	  #print Admin.showObject(admBeans, id)
	  print id

      elif scope.lower() == 'server':
        if subMap.has_key('serverName'):
          serverName = subMap['serverName']
        elif props.isSet('serverName'):
            serverName = props.get('serverName')
        else:
          raise DefaultActionsError("In setupLibrarys: required parameter 'serverName' is missing")           
        if subMap.has_key('nodeName'):
          nodeName = subMap['nodeName']
        elif props.isSet('nodeName'):
          nodeName = props.get('nodeName')
        else:
          raise DefaultActionsError("In setupLibrarys: required parameter 'nodeName' is missing")           
        print "Creating Library %s on %s/%s/%s" % (name, cellName, nodeName, serverName)
	id = Server.createLibrary(admBeans, subMap, serverName, nodeName, cellName)
	if not id:
	  print "Failed to create Library %s" % name
        else:
	  #print Admin.showObject(admBeans, id)
	  print id

      else:
        print "Unknown scope: %s" % scope
#
#-------------------------------------------------------------------------
# Action to configure all the Virtual Hosts and VirtualHost Aliases
#-------------------------------------------------------------------------
#
def setupVirtualHosts(admBeans, props, args = []):
  print "Setting up VirtualHosts"

  if props.isSet('cellName'):
    cellName = props.get('cellName')
  else:
    cellName = Cell.getName(admBeans)

  # Create Virtual Host
  patt1 = re.compile(r'^(vhost\d{,}\.)name')
  ks1 = props.getKeys()
  for k1 in ks1:
    match1 = patt1.search(k1)
    if match1:
      subMap = props.getSubMap(match1.group(1))
      vhostName = subMap['name']
      print "Creating VirtualHost %s in cell %s" % (vhostName, cellName)
      id = Cell.createVirtualHost(admBeans, vhostName, cellName)
      if not id:
        print "Failed to create Virtual Host %s" % vhostName
      else:
        #print Admin.showObject(admBeans, id)
        print id
     
      # Now create host aliases for this Virtual Host
      patt2 = re.compile(r'^(alias\d{,}\.)hostname')
      ks2 = subMap.keys()
      for k2 in ks2:
        match2 = patt2.search(k2)
	if match2:
          hostname = subMap[k2]
	  portKey = match2.group(1) + 'port'
	  if not subMap.has_key(portKey):
            port = '*'
          else:  
	    port = subMap[portKey]
	  print "Creating Virtual Host Alias %s:%s for %s" % (hostname, port, vhostName)
	  alsId = Cell.createVirtualHostAlias(admBeans, vhostName, hostname, port, cellName)
          if not alsId:
	    print "Failed to create Virtual Host Alias %s:%s for %s" % (hostname, port, vhostName)
          else:
            #print Admin.showObject(admBeans, alsId)
            print alsId
#
#-------------------------------------------------------------------------
# Action to configure all the MQQueueConnectionFactories at various scopes.
#-------------------------------------------------------------------------
#
def setupMQQueueConnectionFactories(admBeans, props, args = []):
  print "Setting up MQQueueConnectionFactories"

  if props.isSet('cellName'):
    cellName = props.get('cellName')
  else:
    cellName = Cell.getName(admBeans)

  patt = re.compile(r'^(mqQueueConnectionFactory\d{,}\.)name')
  ks = props.getKeys()
  for k in ks:
    match = patt.search(k)
    if match:
      subMap = props.getSubMap(match.group(1))
      name = subMap['name']

      if not subMap.has_key('scope'):
        raise DefaultActionsError("In mqQueueConnectionFactory: required parameter 'scope' is missing for MQQueueConnectionFactory %s" % name)           
      scope = subMap['scope']

      # Check scope and invoke appropriate function
      if scope.lower() == 'cell':
        print "Creating MQQueueConnectionFactory %s on %s" % (name, cellName)
	id = Cell.createMQQueueConnectionFactory(admBeans, subMap, cellName)
	if not id:
	  print "Failed to create MQQueueConnectionFactory"
        else:
	  #print Admin.showObject(admBeans, id)
	  print id

      elif scope.lower() == 'node':
        if subMap.has_key('nodeName'):
          nodeName = subMap['nodeName']
        elif props.isSet('nodeName'):
          nodeName = props.get('nodeName')
        else:
          raise DefaultActionsError("In setupMQQueueConnectionFactories: required parameter 'nodeName' is missing")           
        print "Creating MQQueueConnectionFactory %s on %s/%s" % (name, cellName, nodeName)
	id = Node.createMQQueueConnectionFactory(admBeans, subMap, nodeName, cellName)
	if not id:
	  print "Failed to create MQQueueConnectionFactory"
        else:
	  #print Admin.showObject(admBeans, id)
	  print id

      elif scope.lower() == 'cluster':
        if subMap.has_key('clusterName'):
          clusterName = subMap['clusterName']
        elif props.isSet('clusterName'):
          clusterName = props.get('clusterName')
        else:
          raise DefaultActionsError("In setupMQQueueConnectionFactories: required parameter 'clusterName' is missing")           
        print "Creating MQQueueConnectionFactory %s on %s/%s" % (name, cellName, clusterName)
	id = Cluster.createMQQueueConnectionFactory(admBeans, subMap, clusterName, cellName)
	if not id:
	  print "Failed to create MQQueueConnectionFactory"
        else:
	  #print Admin.showObject(admBeans, id)
	  print id

      elif scope.lower() == 'server':
        if subMap.has_key('serverName'):
          serverName = subMap['serverName']
        elif props.isSet('serverName'):
            serverName = props.get('serverName')
        else:
          raise DefaultActionsError("In setupMQQueueConnectionFactories: required parameter 'serverName' is missing")           
        if subMap.has_key('nodeName'):
          nodeName = subMap['nodeName']
        elif props.isSet('nodeName'):
          nodeName = props.get('nodeName')
        else:
          raise DefaultActionsError("In setupMQQueueConnectionFactories: required parameter 'nodeName' is missing")           
        print "Creating MQQueueConnectionFactory %s on %s/%s/%s" % (name, cellName, nodeName, serverName)
	id = Server.createMQQueueConnectionFactory(admBeans, subMap, serverName, nodeName, cellName)
	if not id:
	  print "Failed to create MQQueueConnectionFactory %s" % name
        else:
	  #print Admin.showObject(admBeans, id)
	  print id

      elif scope.lower() == 'clustermember':
        if subMap.has_key('clusterName'):
          clusterName = subMap['clusterName']
        elif props.isSet('clusterName'):
          clusterName = props.get('clusterName')
        else:
          raise DefaultActionsError("In setupMQQueueConnectionFactories: required parameter 'clusterName' is missing")           
        print "Creating MQQueueConnectionFactory %s on clusterMembers of cluster %s" % (name, clusterName)
	memberMap =  Cluster.getMembers(admBeans,clusterName,cellName)
	for mName in (memberMap.keys()):
          mId = memberMap[mName]
          admCfg = admBeans['AdminConfig']  
	  ndName = admCfg.showAttribute(mId, 'nodeName')
          print "Creating MQQueueConnectionFactory %s on clusterMember %s of cluster %s" % (name, mName, clusterName)
	  id = Server.createMQQueueConnectionFactory(admBeans, subMap, mName, ndName, cellName)
	  if not id:
	    print "Failed to create MQQueueConnectionFactory %s" % name
          else:
	    #print Admin.showObject(admBeans, id)
	    print id


      else:
        print "Unknown scope: %s" % scope
#
#-------------------------------------------------------------------------
# Action to configure all the MQTopicConnectionFactories at various scopes.
#-------------------------------------------------------------------------
#
def setupMQTopicConnectionFactories(admBeans, props, args = []):
  print "Setting up MQTopicConnectionFactories"

  if props.isSet('cellName'):
    cellName = props.get('cellName')
  else:
    cellName = Cell.getName(admBeans)

  patt = re.compile(r'^(mqTopicConnectionFactory\d{,}\.)name')
  ks = props.getKeys()
  for k in ks:
    match = patt.search(k)
    if match:
      subMap = props.getSubMap(match.group(1))
      name = subMap['name']

      if not subMap.has_key('scope'):
        raise DefaultActionsError("In mqTopicConnectionFactory: required parameter 'scope' is missing for MQTopicConnectionFactory %s" % name)           
      scope = subMap['scope']

      # Check scope and invoke appropriate function
      if scope.lower() == 'cell':
        print "Creating MQTopicConnectionFactory %s on %s" % (name, cellName)
	id = Cell.createMQTopicConnectionFactory(admBeans, subMap, cellName)
	if not id:
	  print "Failed to create MQTopicConnectionFactory"
        else:
	  #print Admin.showObject(admBeans, id)
	  print id

      elif scope.lower() == 'node':
        if subMap.has_key('nodeName'):
          nodeName = subMap['nodeName']
        elif props.isSet('nodeName'):
          nodeName = props.get('nodeName')
        else:
          raise DefaultActionsError("In setupMQTopicConnectionFactories: required parameter 'nodeName' is missing")           
        print "Creating MQTopicConnectionFactory %s on %s/%s" % (name, cellName, nodeName)
	id = Node.createMQTopicConnectionFactory(admBeans, subMap, nodeName, cellName)
	if not id:
	  print "Failed to create MQTopicConnectionFactory"
        else:
	  #print Admin.showObject(admBeans, id)
	  print id

      elif scope.lower() == 'cluster':
        if subMap.has_key('clusterName'):
          clusterName = subMap['clusterName']
        elif props.isSet('clusterName'):
          clusterName = props.get('clusterName')
        else:
          raise DefaultActionsError("In setupMQTopicConnectionFactories: required parameter 'clusterName' is missing")           
        print "Creating MQTopicConnectionFactory %s on %s/%s" % (name, cellName, clusterName)
	id = Cluster.createMQTopicConnectionFactory(admBeans, subMap, clusterName, cellName)
	if not id:
	  print "Failed to create MQTopicConnectionFactory"
        else:
	  #print Admin.showObject(admBeans, id)
	  print id

      elif scope.lower() == 'server':
        if subMap.has_key('serverName'):
          serverName = subMap['serverName']
        elif props.isSet('serverName'):
            serverName = props.get('serverName')
        else:
          raise DefaultActionsError("In setupMQTopicConnectionFactories: required parameter 'serverName' is missing")           
        if subMap.has_key('nodeName'):
          nodeName = subMap['nodeName']
        elif props.isSet('nodeName'):
          nodeName = props.get('nodeName')
        else:
          raise DefaultActionsError("In setupMQTopicConnectionFactories: required parameter 'nodeName' is missing")           
        print "Creating MQTopicConnectionFactory %s on %s/%s/%s" % (name, cellName, nodeName, serverName)
	id = Server.createMQTopicConnectionFactory(admBeans, subMap, serverName, nodeName, cellName)
	if not id:
	  print "Failed to create MQTopicConnectionFactory %s" % name
        else:
	  #print Admin.showObject(admBeans, id)
	  print id

      elif scope.lower() == 'clustermember':
        if subMap.has_key('clusterName'):
          clusterName = subMap['clusterName']
        elif props.isSet('clusterName'):
          clusterName = props.get('clusterName')
        else:
          raise DefaultActionsError("In setupMQTopicConnectionFactories: required parameter 'clusterName' is missing")           
        print "Creating MQTopicConnectionFactory %s on clusterMembers of cluster %s" % (name, clusterName)
	memberMap =  Cluster.getMembers(admBeans,clusterName,cellName)
	for mName in (memberMap.keys()):
          mId = memberMap[mName]
          admCfg = admBeans['AdminConfig']  
	  ndName = admCfg.showAttribute(mId, 'nodeName')
          print "Creating MQTopicConnectionFactory %s on clusterMember %s of cluster %s" % (name, mName, clusterName)
	  id = Server.createMQTopicConnectionFactory(admBeans, subMap, mName, ndName, cellName)
	  if not id:
	    print "Failed to create MQTopicConnectionFactory %s" % name
          else:
	    #print Admin.showObject(admBeans, id)
	    print id


      else:
        print "Unknown scope: %s" % scope
#
#-------------------------------------------------------------------------
# Action to configure all the MQQueues at various scopes.
#-------------------------------------------------------------------------
#
def setupMQQueues(admBeans, props, args = []):
  print "Setting up MQQueues"

  if props.isSet('cellName'):
    cellName = props.get('cellName')
  else:
    cellName = Cell.getName(admBeans)

  patt = re.compile(r'^(mqQueue\d{,}\.)name')
  ks = props.getKeys()
  for k in ks:
    match = patt.search(k)
    if match:
      subMap = props.getSubMap(match.group(1))
      name = subMap['name']

      if not subMap.has_key('scope'):
        raise DefaultActionsError("In setupMQQueues: required parameter 'scope' is missing for MQQueue %s" % name)           
      scope = subMap['scope']

      # Check scope and invoke appropriate function
      if scope.lower() == 'cell':
        print "Creating MQQueue %s on %s" % (name, cellName)
	id = Cell.createMQQueue(admBeans, subMap, cellName)
	if not id:
	  print "Failed to create MQQueue"
        else:
	  #print Admin.showObject(admBeans, id)
	  print id

      elif scope.lower() == 'node':
        if subMap.has_key('nodeName'):
          nodeName = subMap['nodeName']
        elif props.isSet('nodeName'):
          nodeName = props.get('nodeName')
        else:
          raise DefaultActionsError("In setupMQQueues: required parameter 'nodeName' is missing")           
        print "Creating MQQueue %s on %s/%s" % (name, cellName, nodeName)
	id = Node.createMQQueue(admBeans, subMap, nodeName, cellName)
	if not id:
	  print "Failed to create MQQueue"
        else:
	  #print Admin.showObject(admBeans, id)
	  print id

      elif scope.lower() == 'cluster':
        if subMap.has_key('clusterName'):
          clusterName = subMap['clusterName']
        elif props.isSet('clusterName'):
          clusterName = props.get('clusterName')
        else:
          raise DefaultActionsError("In setupMQQueues: required parameter 'clusterName' is missing")           
        print "Creating MQQueue %s on %s/%s" % (name, cellName, clusterName)
	id = Cluster.createMQQueue(admBeans, subMap, clusterName, cellName)
	if not id:
	  print "Failed to create MQQueue"
        else:
	  #print Admin.showObject(admBeans, id)
	  print id

      elif scope.lower() == 'server':
        if subMap.has_key('serverName'):
          serverName = subMap['serverName']
        elif props.isSet('serverName'):
            serverName = props.get('serverName')
        else:
          raise DefaultActionsError("In setupMQQueues: required parameter 'serverName' is missing")           
        if subMap.has_key('nodeName'):
          nodeName = subMap['nodeName']
        elif props.isSet('nodeName'):
          nodeName = props.get('nodeName')
        else:
          raise DefaultActionsError("In setupMQQueues: required parameter 'nodeName' is missing")           
        print "Creating MQQueue %s on %s/%s/%s" % (name, cellName, nodeName, serverName)
	id = Server.createMQQueue(admBeans, subMap, serverName, nodeName, cellName)
	if not id:
	  print "Failed to create MQQueue %s" % name
        else:
	  #print Admin.showObject(admBeans, id)
	  print id

      elif scope.lower() == 'clustermember':
        if subMap.has_key('clusterName'):
          clusterName = subMap['clusterName']
        elif props.isSet('clusterName'):
          clusterName = props.get('clusterName')
        else:
          raise DefaultActionsError("In setupMQQueues: required parameter 'clusterName' is missing")           
        print "Creating MQQueue %s on clusterMembers of cluster %s" % (name, clusterName)
	memberMap =  Cluster.getMembers(admBeans,clusterName,cellName)
	for mName in (memberMap.keys()):
          mId = memberMap[mName]
          admCfg = admBeans['AdminConfig']  
	  ndName = admCfg.showAttribute(mId, 'nodeName')
          print "Creating MQQueue %s on clusterMember %s of cluster %s" % (name, mName, clusterName)
	  id = Server.createMQQueue(admBeans, subMap, mName, ndName, cellName)
	  if not id:
	    print "Failed to create MQQueue %s" % name
          else:
	    #print Admin.showObject(admBeans, id)
	    print id


      else:
        print "Unknown scope: %s" % scope

#
#-------------------------------------------------------------------------
# Action to configure all the MQTopics at various scopes.
#-------------------------------------------------------------------------
#
def setupMQTopics(admBeans, props, args = []):
  print "Setting up MQTopics"

  if props.isSet('cellName'):
    cellName = props.get('cellName')
  else:
    cellName = Cell.getName(admBeans)

  patt = re.compile(r'^(mqTopic\d{,}\.)name')
  ks = props.getKeys()
  for k in ks:
    match = patt.search(k)
    if match:
      subMap = props.getSubMap(match.group(1))
      name = subMap['name']

      if not subMap.has_key('scope'):
        raise DefaultActionsError("In setupMQTopics: required parameter 'scope' is missing for MQTopic %s" % name)           
      scope = subMap['scope']

      # Check scope and invoke appropriate function
      if scope.lower() == 'cell':
        print "Creating MQTopic %s on %s" % (name, cellName)
	id = Cell.createMQTopic(admBeans, subMap, cellName)
	if not id:
	  print "Failed to create MQTopic"
        else:
	  #print Admin.showObject(admBeans, id)
	  print id

      elif scope.lower() == 'node':
        if subMap.has_key('nodeName'):
          nodeName = subMap['nodeName']
        elif props.isSet('nodeName'):
          nodeName = props.get('nodeName')
        else:
          raise DefaultActionsError("In setupMQTopics: required parameter 'nodeName' is missing")           
        print "Creating MQTopic %s on %s/%s" % (name, cellName, nodeName)
	id = Node.createMQTopic(admBeans, subMap, nodeName, cellName)
	if not id:
	  print "Failed to create MQTopic"
        else:
	  #print Admin.showObject(admBeans, id)
	  print id

      elif scope.lower() == 'cluster':
        if subMap.has_key('clusterName'):
          clusterName = subMap['clusterName']
        elif props.isSet('clusterName'):
          clusterName = props.get('clusterName')
        else:
          raise DefaultActionsError("In setupMQTopics: required parameter 'clusterName' is missing")           
        print "Creating MQTopic %s on %s/%s" % (name, cellName, clusterName)
	id = Cluster.createMQTopic(admBeans, subMap, clusterName, cellName)
	if not id:
	  print "Failed to create MQTopic"
        else:
	  #print Admin.showObject(admBeans, id)
	  print id

      elif scope.lower() == 'server':
        if subMap.has_key('serverName'):
          serverName = subMap['serverName']
        elif props.isSet('serverName'):
            serverName = props.get('serverName')
        else:
          raise DefaultActionsError("In setupMQTopics: required parameter 'serverName' is missing")           
        if subMap.has_key('nodeName'):
          nodeName = subMap['nodeName']
        elif props.isSet('nodeName'):
          nodeName = props.get('nodeName')
        else:
          raise DefaultActionsError("In setupMQTopics: required parameter 'nodeName' is missing")           
        print "Creating MQTopic %s on %s/%s/%s" % (name, cellName, nodeName, serverName)
	id = Server.createMQTopic(admBeans, subMap, serverName, nodeName, cellName)
	if not id:
	  print "Failed to create MQTopic %s" % name
        else:
	  #print Admin.showObject(admBeans, id)
	  print id

      elif scope.lower() == 'clustermember':
        if subMap.has_key('clusterName'):
          clusterName = subMap['clusterName']
        elif props.isSet('clusterName'):
          clusterName = props.get('clusterName')
        else:
          raise DefaultActionsError("In setupMQTopics: required parameter 'clusterName' is missing")           
        print "Creating MQTopic %s on clusterMembers of cluster %s" % (name, clusterName)
	memberMap =  Cluster.getMembers(admBeans,clusterName,cellName)
	for mName in (memberMap.keys()):
          mId = memberMap[mName]
          admCfg = admBeans['AdminConfig']  
	  ndName = admCfg.showAttribute(mId, 'nodeName')
          print "Creating MQTopic %s on clusterMember %s of cluster %s" % (name, mName, clusterName)
	  id = Server.createMQTopic(admBeans, subMap, mName, ndName, cellName)
	  if not id:
	    print "Failed to create MQTopic %s" % name
          else:
	    #print Admin.showObject(admBeans, id)
	    print id


      else:
        print "Unknown scope: %s" % scope

#
#-------------------------------------------------------------------------
# Create and return function map of all the actions defined
#-------------------------------------------------------------------------
#
def getActionMap():
  print "Creating action-map"
  return {
	    'testAction': testAction,
	    'setupJvmAttributes': setupJvmAttributes,
	    'setupJvmCustomProperties': setupJvmCustomProperties,
	    'setupServerStdout': setupServerStdout,
	    'setupServerStderr': setupServerStderr,
	    'setupWCThreadpool': setupWCThreadpool,
	    'setupEnvEntries': setupEnvEntries,
	    'setupServerPorts': setupServerPorts,
	    'setupStandardCluster': setupStandardCluster,
	    'setupAppServer': setupAppServer,
	    'setupWebSphereVariables': setupWebSphereVariables,
	    'setupJ2CAuthAliases': setupJ2CAuthAliases,
	    'setupJDBCProviders': setupJDBCProviders,
	    'setupDataSources': setupDataSources,
	    'setupLibraries': setupLibraries,
	    'setupMQQueueConnectionFactories': setupMQQueueConnectionFactories,
	    'setupMQQueues': setupMQQueues,
	    'setupMQTopicConnectionFactories': setupMQTopicConnectionFactories,
	    'setupMQTopics': setupMQTopics,
	    'setupListenerPorts': setupListenerPorts,
	    'setupVirtualHosts': setupVirtualHosts
         }
#
#-------------------------------------------------------------------------
