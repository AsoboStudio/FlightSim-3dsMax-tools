import os
import subprocess

def P4delete(filePath, changelistName="default"):
    if os.path.exists(filePath):
        cmd = "p4 delete -c {0} -v {1}".format(changelistName,filePath )
        process = subprocess.Popen(cmd, shell=True)
        process.wait()  # wait for process end
        # os.system('cmd /c "{0}"'.format(cmd))
        # print cmd


def P4edit(filePath, changelistName="default"):
    if os.path.exists(filePath):
        cmd = "p4 add -c {0} -v {1}| p4 edit -c {0} -v {1} ".format(changelistName,filePath)
        process = subprocess.Popen(cmd, shell=True)
        process.wait() #wait for process end
        # os.system('cmd /c "{0}"'.format(cmd))
        # print cmd


def P4add(filePath, changelistName="default"):
    if os.path.exists(filePath):
        cmd = "p4 add -c {0} -v {1}".format(changelistName,filePath)
        process = subprocess.Popen(cmd, shell=True)
        process.wait()  # wait for process end
        # os.system('cmd /c "{0}"'.format(cmd))
        # print cmd

def P4revert(filePath, changelistName="default"):
    if os.path.exists(filePath):
        cmd = "p4 revert -c {0} -w {1}".format(changelistName, filePath)
        process = subprocess.Popen(cmd, shell=True)
        process.wait()
        os.system('cmd /c "{0}"'.format(cmd))
        print(cmd)

def P4createChangelist(changelistName):
    #empthy changelist
    if changelistName:
        cmd = 'p4 --field "Description={0}" --field "Files=" change -o | p4 change -i'.format(changelistName )
        process = subprocess.Popen(cmd, shell=True)
        process.wait()  # wait for process end
        # os.system('cmd /c "{0}"'.format(cmd))
        # print cmd