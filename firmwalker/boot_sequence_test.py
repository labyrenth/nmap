import subprocess
import os
import sys
import argparse
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

# Specify arguments required for stand-alone execution
def Argparsing():
    parser = argparse.ArgumentParser(description='USAGE = boot_sequence_check.py [rootfs_Path]')
    parser.add_argument('rootfs_path', type=str, help="Path where the root file system is located")
    return parser.parse_args().rootfs_path

# Check the boot process on the root file system. if success, it returns 0
def Check_boot_sequence(rootfs_path):
    if type(rootfs_path) != str :
        print("command type is not str")
        exit(1)
    command = os.path.dirname(__file__)+"/firmwalker_mod.sh " + rootfs_path
    return subprocess.check_call(command, shell=True)

#read files
def Get_result_file_path():
    for path,dirs,files in os.walk("./result"):
	    for filename in files:
		return os.path.join(path,filename)

# stand-alone execution code
if __name__ == "__main__" :
    if Check_boot_sequence(Argparsing()) == 0:
	#temp        
	print(success!)
    else :
	print("error!")
	exit(1)

