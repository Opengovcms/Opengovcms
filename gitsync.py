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
        self.REPO_CHANGED = False
        self.REPO_CHANGED_LOCK = Lock()

    def take_lock(self):
        self.REPO_CHANGED_LOCK.acquire()

    def release_lock(self):
        self.REPO_CHANGED_LOCK.release()

    def changed(self):
        self.REPO_CHANGED = True

    def reset(self):
        self.REPO_CHANGED = False

    def is_changed(self):
        is_changed = self.REPO_CHANGED
        return is_changed


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

    def run(self):
        while True:
            self.git_updated.take_lock()
            if self.git_updated.is_changed():
                self.run_git_pull()
                self.run_git_commit("Commit done by gitsync.")
                self.run_git_push()
                self.git_updated.reset()
            self.git_updated.release_lock()
            time.sleep(10)
            print "Commit thread ran"

class GitActionWorker(Thread):

    def __init__(self, git_updated):
        Thread.__init__(self)
        self.git_updated = git_updated
        self.directory = sys.argv[1]
        self.old_directory = os.getcwd()
        os.chdir(self.directory)

    def run_git_action(self, action, path):
        command = "git {0} {1}".format(action, path)
        run_cmd(command)
        print "Running", action, path
        self.git_updated.take_lock()
        self.git_updated.changed()
        self.git_updated.release_lock()

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
                self.run_git_action('add', os.path.join(folder, filename))
            elif action == 'DELETE':
                self.run_git_action('rm', os.path.join(folder, filename))
            print "Action thread ran"

git_updated = GitUpdated()

action_worker = GitActionWorker(git_updated)
action_worker.start()

commit_worker = GitCommitWorker(git_updated)
commit_worker.start()

