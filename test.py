#!/usr/bin/env python

import subprocess
from git import Repo
import os
import sys
from subprocess import check_output
import json
import pymongo
from pymongo import MongoClient
client = MongoClient()
client = MongoClient('mongodb://localhost:27017/')
db = client.test_database

jsonObj = {}
jsonObj['repoName'] = sys.argv[1]
jsonBranchesArr = []
repo_url = '' + sys.argv[1] + '.git'
repo_path = '/Users/prajaktachavan/Documents/testrepo/'
Repo.clone_from(repo_url, repo_path)

versionCommand = '''
cd /Users/prajaktachavan/Documents/testrepo
mvn org.apache.maven.plugins:maven-help-plugin:2.1.1:evaluate -Dexpression=project.version | grep -v '\['
'''

class Command(object):
    """Run a command and capture it's output string, error string and exit status"""
    def __init__(self, command):
        self.command = command 
    def run(self, shell=True):
        import subprocess as sp
        process = sp.Popen(self.command, shell = shell, stdout = sp.PIPE, stderr = sp.PIPE)
        self.pid = process.pid
        self.output, self.error = process.communicate()
        self.failed = process.returncode
        return self
    @property
    def returncode(self):
        return self.failed

os.chdir(repo_path)
raw_results = check_output("git ls-remote --heads origin  | sed 's?.*refs/heads/??'", shell=True)
for branch in raw_results.split('\n'):
	if branch:
		check_output('git checkout %s' % branch.strip() , shell=True).strip()
		com = Command(versionCommand).run()
		print com.output
		version = com.output
		jsonBranchesArr.append({"branchname":branch,"version":version,"status":"active"})

jsonObj['branches'] = jsonBranchesArr
print jsonObj
db.sourcecontrol.insert(jsonObj)
