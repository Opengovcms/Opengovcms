#!/usr/bin/python
import sys
import os
import time
import subprocess

from threading import Thread, Lock

def run_cmd(command):
    print "Running, ", command
    subprocess.call(command, shell=True)

if len(sys.argv) < 2:
    print "Please suply directory"


class GitUpdated(object):
    def __init__(self):
        self.REPO_QUEUE = {}
        self.REPO_LOCK = Lock()

    def take_lock(self):
        self.REPO_LOCK.acquire()

    def release_lock(self):
        self.REPO_LOCK.release()

    def add(self, path, action):
        self.REPO_QUEUE[path] = action

    def get(self):
        result = []
        for elem in self.REPO_QUEUE.items():
            result.append(elem)
        self.REPO_QUEUE = {}
        return result

class GitCommitWorker(Thread):

    def __init__(self, git_updated):
        Thread.__init__(self)
        self.git_updated = git_updated

    def run_git_pull(self):
        command = "git pull"
        run_cmd(command)

    def run_git_push(self):
        command = "git push"
        run_cmd(command)

    def run_git_commit(self, commit_msg):
        command = 'git commit -m "{0}"'.format(commit_msg)
        run_cmd(command)

    def run_git_action(self, action, path):
        command = "git {0} {1}".format(action, path)
        run_cmd(command)
        print "Running", action, path

    def run(self):
        while True:
            self.git_updated.take_lock()

            elements = self.git_updated.get()

            for (path, action) in elements:
                self.run_git_action(action, path)

            if len(elements) > 0:
                self.run_git_pull()
                self.run_git_commit("Commit done by gitsync.")
                self.run_git_push()

            self.git_updated.release_lock()
            time.sleep(60)
            print "Commit thread ran"

class GitActionWorker(Thread):

    def __init__(self, git_updated):
        Thread.__init__(self)
        self.git_updated = git_updated
        self.directory = sys.argv[1]
        self.old_directory = os.getcwd()
        os.chdir(self.directory)

    def run(self):
        try:
            fh = os.popen('inotifywait -e modify -e create -e delete -m -r {0}'.format(self.directory))
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
                self.git_updated.take_lock()
                self.git_updated.add(os.path.join(folder, filename), 'add')
                self.git_updated.release_lock()
            elif action == 'DELETE':
                self.git_updated.take_lock()
                self.git_updated.add(os.path.join(folder, filename), 'rm')
                self.git_updated.release_lock()

            print "Action thread ran"

git_updated = GitUpdated()

action_worker = GitActionWorker(git_updated)
action_worker.start()

commit_worker = GitCommitWorker(git_updated)
commit_worker.start()

