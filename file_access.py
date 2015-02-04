
import platform
import os
import subprocess
import sys
import logging
import argparse
import re
import string
from subprocess import call


#-------------------------------------------
## file_operations    
class file_operations(object):
    def __init__(self, name, **kwargs):
        self.name = name
        self.current_os = platform.system( )
        self.curr_os_lower = self.current_os.lower( )
        self.argList = [ ]
        #print("\n%s Init over" %self.name)
        
    def parse_args(self, args):
        """Parse the command-line arguments."""
        parser = argparse.ArgumentParser(description='Parse input directories/files.')
        parser.add_argument('inp_files', nargs='*',
                           help='Provie file1\'s path to check')
        args = parser.parse_args( )
        self.argList = args.inp_files

    def find_file_access_times(self):
         access_times_dict = { }
         if(self.curr_os_lower == "darwin"):
            print("%s Found OS as %s calling mac_obj\n" % (self.name, self.curr_os_lower))
            mac_obj = mac_file_operations("macFileOps")
            mac_obj.parse_args(self.argList)
            access_times_dict = mac_obj.find_file_access_times( )
         elif(self.curr_os_lower == "windows"):
            print("%s Found OS as %s calling win_obj" %(self.name, self.curr_os_lower))
            win_obj = win_file_operations("winFileOps")
            win_obj.parse_args(self.argList)
            win_obj.find_last_accessed_file( )
         elif(self.curr_os_lower == "linux"):
            print("%s Found OS as %s calling linux_obj" %(self.name, self.curr_os_lower))
            linux_obj = win_file_operations("linuxFileOps")
            linux_obj.parse_args(self.argList)
            linux_obj.find_last_accessed_file( )
         else:
            print("%s does not support this OS: %s"  %(self.name, self.curr_os_lower))
         #Sort File access times
         access_times_dict_rev = [ (val, key) for key, val in access_times_dict.iteritems( ) ]
         access_times_dict_rev.sort(reverse=True)
         result = 0
         for keys, values in access_times_dict_rev:
             if(result == 0):
                 print "ANSWER", values, keys
             else:
                 print "REST", values, keys
             result = result + 1
            
         print ("\nEnd of Prog")
        

#-------------------------------------------
## mac_file_operations           
class mac_file_operations(file_operations):  ##extends from file_operations
    def __init__(self, name):
        file_operations.__init__(self, name)
        
    def find_file_access_times(self):
                #Run MAC commands
        print("%s argList = %s\n"  %(self.name, self.argList))
        access_times_dict =  { }
        for file in self.argList:
            one_file_list = []
            one_file_list.append(file)
            print("MAC one_file_list is %s" %one_file_list)
            p = subprocess.Popen(['stat', '-x'] + one_file_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
            print("MAC %s for file:%s \n printing \n\n %s" % (self.name, file, out))
            access_times_dict[file] = self.parse_access_time(out)

        return access_times_dict

    def parse_access_time(self, out):
            line_list = out.split('\n')
            access_pattern = re.compile(r'^Access:', re.VERBOSE)
            for line in line_list:
                if access_pattern.search(line):
                    time_list = line.split(': ')
                    time = time_list[1]
                    print "ACCESS TIME IS " , time_list[1], "\n"
            return time_list[1]
            #print("MAC output", line_list[2])


#-------------------------------------------
## win_file_operations           
class win_file_operations(file_operations):  ##extends from file_operations
    def __init__(self, name):
        file_operations.__init__(self, name)
        
    def find_last_accessed_file(self):
                    #Run WINDOWS commands
        print("WINDOWS %s last_file %s" %(self.name, self.argList))
        access_times_list = []
        for file in self.argList:
            one_file_list = []
            one_file_list.append(file)
            print("WINDOWS one_file_list is %s" %one_file_list)
            p = subprocess.Popen(['dir', '/T:A', '|', 'findstr'] + self.argList, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            out, err = p.communicate()
            print("WINDOWS %s printing \n\n %s" % (self.name, out))
       

#-------------------------------------------
## linux_file_operations    
class linux_file_operations(file_operations):  ##extends from file_operations
    def __init__(self, name):
        file_operations.__init__(self, name)
        
    def find_last_accessed_file(self):
        #Run LINUX commands
        print("LINUX %s last_file %s"  %(self.name, self.argList))
        access_times_list = []
        for file in self.argList:
            one_file_list = []
            one_file_list.append(file)
            print("LINUX one_file_list is %s" %one_file_list)
            p = subprocess.Popen(['stat'] + self.argList, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, shell=False)
            out, err = p.communicate()
            print("LINUX %s printing \n\n %s" % (self.name, out))
       

#########################################################################################    
##---MAIN----##
if __name__ == '__main__':
#For Normal completion
    exitCode = 0
    print("\n\n    Main Program Starts ....   \n");
    file_ops = file_operations("fileOps")
    file_ops.parse_args(sys.argv[1:] )
    file_ops.find_file_access_times( )
    sys.exit(exitCode)

