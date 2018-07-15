##############################################################################
# Project:	WebSphere 6.1 Automation - Core Library
# Package: 	was61core
# Module: 	Utils
# Authors: 	Nana Fadnis & Leao Fernandes
# Start Date: 	01/01/2008
###############################################################################
import sys
import re

###############################################################################
"""
CLASS:          Props
PURPOSE:        A simple class for handling properties defined in a property
		file with each line of the format <prop name>=<prop value>. In 
		the current implementation it stores the properties internally
		as a HashMap object. It also keeps a list of all keys in the 
		same order as they appear in the property file. Furthermore, it
		allows one property to be defined in terms of another through
		syntax p2 = ...${p1}...
		
INST. VARS:     MAP         	HashMap to store the property key-value pairs.
                KEYS        	A List object storing all the keys in the order they
				appear in the file.
METHODS:        __init__()    	Initializer. Gets called when you say p = Props()
                load(fn)    	Reads the property file specified by name 'fn' and
				loads the key-value pairs defined there in the
				HashMap. The lines beginning with '#' are considered
				as the comment lines, and are ignored. You can also
				have spae around '=' character, it will be removed
				during loading.
"""
class Props:

  #----------------------------------------------------------------------
  def __init__(self):
    self.MAP = {}
    self.KEYS = []
  #----------------------------------------------------------------------
  def load(self, fn):
    pf = open(fn, "r")
    while 1:
      ln = pf.readline()
      if not ln:
        break
      
      # Remove newline character at the end of the string.
      ln = ln[:len(ln)-1]

      # Next if comment line.
      if (re.search(r'^\#', ln)):
        continue

      # Break the line into key-value pairs and build a map
      #match = re.search(r'(\w+)\s*=\s*(.+)$', ln)
      match = re.search(r'([^=]+)\s*=\s*(.*)$', ln)
      if match:
        k = match.group(1)
        v =  match.group(2)
        self.MAP[k] = v
        self.KEYS.append(k)
  #----------------------------------------------------------------------
  def getKeys(self):
    return self.KEYS  
  #----------------------------------------------------------------------
  def getMap(self):
    return self.MAP  
  #----------------------------------------------------------------------
  def get(self, k):
    return self.MAP[k]  
  #----------------------------------------------------------------------
  def isSet(self, k):
    return self.MAP.has_key(k)  
  #----------------------------------------------------------------------
  def set(self, k, v):
    
    # Check to see if the key is already defined
    # If not push it into KEYS array 
    if not self.MAP.has_key(k):
      self.KEYS.append(k)

    # Now set the value
    self.MAP[k] = v  
  #----------------------------------------------------------------------
  def clone(self):
    tmp = Props()
    tmp.MAP = self.getMap()
    tmp.KEYS = self.getKeys()
    return tmp
  #----------------------------------------------------------------------
CLASS:          Error
PURPOSE:        This is a simple implementation of an Error class that is inherited
                from the python 'Exception' object.
                Error object will be propagated to the caller function/script using
                the 'raise Error([msg])' statement. While initializing the Error object
                the function raising the error can optionally pass a message (string),
                which, along with any Exception information (if there was an Exception)
                is encapsulated by the Error object. This informaton can be extraced
                by the caller function/script through one of the methods of Error object
                e.g. getErrorInfo()
INST. VARS:     message         (stores the message string passed during initialization),
                                excinfo (stores a list of 3 objects returned by sys.exc_info().
                                If there is no exception all three will have value 'None')
                errorStr        (stores information about the latest error)
CLASS VAR:      errorHist       (list of errors raised at different levels all the way down to
                                where the error actually originated)
METHODS:        getMessage()    returns 'message' passed by the function that raised
                                the Error.
                getExcinfo()    returns a the list of 3 objects that were passed by
                                sys.exc_info() when exception occured.
                getErrorInfo()  returns a formatted string containing error information about
                                the last error raised.
                getErrorHist()  returns the error history list
"""
class Error(Exception):

  errorHist = []
  errorString = ''

  #----------------------------------------------------------------------
  def __init__(self, message=''):
    self.message = message
    self.excinfo = sys.exc_info()
    self.setErrorStr()
    self.setErrorHist()
  #----------------------------------------------------------------------
  def getMessage(self):
    return self.message
  #----------------------------------------------------------------------
  def getExcinfo(self):::q!
:
    return self.excinfo
  #----------------------------------------------------------------------
  def setErrorStr(self):
    msg = self.message
    excinfo = self.excinfo
    tp,dtl,tb = ('', '', '')
    if (len(excinfo)>0 and excinfo[0]!=None):
      tp = str(excinfo[0])
    if (len(excinfo)>1 and excinfo[1]!=None):
      dtl =  string.replace(str(excinfo[1]), '\n', '')
    if (len(excinfo)>2 and excinfo[2]!=None):
      tb = str(traceback.extract_tb(excinfo[2]))
    self.errorStr = "(MESSAGE: %s|TYPE: %s|DETAILS: %s|TRACEBACK: %s)" % (msg,tp,dtl,tb)
  #----------------------------------------------------------------------
  def setErrorHist(self):
    self.__class__.errorHist.insert(0, self.errorStr)
  #----------------------------------------------------------------------
  def getErrorInfo(self):
    return self.errorStr
  #----------------------------------------------------------------------
  def getErrorHist(self):
    return self.errorHist

#end class Error 
###############################################################################
"""
CLASS:          ActionProcessor
PURPOSE:        A simple class for executing actions mapped to functions 
		which may be defined in a pluggable external module. These
		functions must be of the form f(props, argList), where
		props is of type 'Props' (class defined in this module)
		and argList is a list containing any command-line arguments
		that may have been passed to the action. The 'props'
		object will contain all the properties that the action may
		need for its execution (so it could be empty as well if
		actions do not need any properties)
"""

class ActionProcessor:
  
  #----------------------------------------------------------------------
  #def __init__(self, actionMap, props=Props()):
  def __init__(self, actionMap, admBeans, propsFile=''):
    self.ACTIONS = actionMap.keys()
    self.ACTION_MAP = actionMap
    self.ADMIN_BEANS_MAP = admBeans
    if propsFile:
      props = Props()
      props.load(propsFile)
      props.eval()
      self.PROPS = props
    else:
      self.PROPS = Props()
  #----------------------------------------------------------------------
  #def execute(self, action, args=[]):
  def execute(self, action, args=[]):
    if not self.ACTION_MAP.has_key(action):
      raise Error("In ActionProcessor: Action %s not supported" % action)
    self.ACTION_MAP[action](self.ADMIN_BEANS_MAP, self.PROPS, args)
  #----------------------------------------------------------------------
  def getActions(self):
    return self.ACTIONS
  #----------------------------------------------------------------------
  def setProps(self, props):
    self.PROPS = props
  #----------------------------------------------------------------------

#end class ActionProcessor 
###############################################################################
