import sys
import getopt
import re
sys.path.append('D:/WID/WAS61ToolsLib')
import Utils
import Cell
import Admin
import Cluster
import Server
import DefaultActions


#------------------------------------------------------------------------------

def usage():
  print """

USAGE: 

    To execute actions listed in a action batch file use:

      <path to wsadmin.sh> -f WASConfig.py -b <batch file> <property file>

      Or: 

      <path to wsadmin.sh> -f WASConfig.py --batch <batch file> <property file>

    To execute single action use:

      <path to wsadmin.sh> -f WASConfig.py <property file>  <action> [<arg1> ...]
  """

#------------------------------------------------------------------------------
# main
#------------------------------------------------------------------------------

# Read in command-line options and arguments
try:
  #opts, args = getopt.getopt(sys.argv[1:], "hb:", ["help", "batch="])
  opts, args = getopt.getopt(sys.argv, "hb:", ["help", "batch=", "test"])
except getopt.GetoptError, err:
  usage()
  sys.exit()

# Check options
actionFile = ''
for o, a in opts:
  if o in ("-h", "--help"):
    usage()
    sys.exit()
  elif o in ("-b", "--batch"):
    actionFile = a
  else:
    usage()
    sys.exit()

# Get the property file name
if len(args)==0:
  usage()
  sys.exit()
propsFile = args.pop(0)

# Set the Admin MBeans Map
admBeans = Admin.setAdminBeans(AdminConfig, AdminControl, AdminApp, AdminTask, Help)

# Initialize ActionProcessor
actionMap = DefaultActions.getActionMap()
ap = Utils.ActionProcessor(actionMap, admBeans, propsFile)

# Execute action(s)
if actionFile:
  print "Processing actions in the actionFile %s" % actionFile
  print "------------------------------------------------------------------------";
  fp = open(actionFile, "r")
  while 1:
    ln = fp.readline()
    # check for EOF
    if not ln:
      break
    # Remove newline character at the end of the string.
    if ln[len(ln)-1] == "\n":
      ln = ln[:len(ln)-1]
    # Ignore blank lines and comment lines.
    if ln == "" or re.search(r'^\#', ln):
      continue
    # Parse the lines read to extract action name and any arguments supplied.
    fields = re.split('\s+', ln)
    actionName = fields.pop(0)
    print "Executing action %s with arguments" % actionName, fields
    try:
      ap.execute(actionName, fields)
    except Utils.Error, e:
      #print e.getErrorInfo()
      print e.getErrorHist()
    print "------------------------------------------------------------------------";
    AdminConfig.save()
else:  
  print "------------------------------------------------------------------------";
  if len(args)==0:
    usage()
    sys.exit()
  actionName = args.pop(0)
  print "Executing action %s with arguments" % actionName, args
  try:
    ap.execute(actionName, args)
  except Utils.Error, e:
    #print e.getErrorInfo()
    print e.getErrorHist()
  print "------------------------------------------------------------------------";
  AdminConfig.save()
