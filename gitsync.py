#!/usr/bin/python

import sys
import os

def run_cmd(command):
    print command

def run_git_action(action, path):
    command = "git {0} {1}".format(action, path)
    run_cmd(command)

def run_git_commit(commit_msg):
    command = 'git commit -m "{0}"'.format(commit_msg)
    run_cmd(command)
    command = "git push"
    run_cmd(command)

def run_git_pull():
    command = "git pull"
    run_cmd(command)

if len(sys.argv) < 2:
    print "Please suply directory"

directory = sys.argv[1]
old_directory = os.getcwd()
os.chdir(directory)

try:
    fh = os.popen('inotifywait -e modify -e create -e delete -m -r {0}'.format(directory))
except IOError:
    print 'Could no open inotifywait, exiting'
    sys.exit(1)
    
while True:
    buf = fh.readline()
    if buf == "":
        break
    buf = buf.replace('\n', '').replace('\r', '')
    (folder, action, filename) = buf.split(' ')
    
    if action == 'MODIFY' or action == 'CREATE':
        run_git_pull()
        run_git_action('add', os.path.join(folder, filename))
        run_git_commit("Commit done by git sync")
    elif action == 'DELETE':
        run_git_pull()
        run_git_action('rm', os.path.join(folder, filename))
        run_git_commit("Commit done by git sync")
