#!/usr/bin/env python
import git
import requests
import yaml
import json
import os
from urllib.parse import urlparse
import shutil


origin_headers = None
dist_headers = None
m_config = None

def config():
    with open('config.yaml', 'r') as f:
        data = yaml.safe_load(f)
        
    if data != None:
        return data
    
    return None
    
    
def main():
    global origin_headers, dist_headers, m_config
    m_config = config()
    origin_headers = { 'accept' : 'application/json', 'Authorization' : 'token ' + m_config['ORIGIN_TOKEN'], 'content-type' : 'application/json' }
    dist_headers = { 'accept' : 'application/json', 'Authorization' : 'token ' + m_config['DIST_TOKEN'], 'content-type' : 'application/json' }
    repos = origin_repositore_list();

    for repo in repos:
        data = {
            "auth_token": m_config['ORIGIN_TOKEN'],
            "clone_addr": repo['clone_url'],
            "issues": True,
            "labels": True,
            "lfs": True,
            "milestones": True,
            "mirror": False,
            "private": True,
            "pull_requests": True,
            "releases": True,
            "repo_name": repo['name'],
            "repo_owner": m_config['DIST_ORG_NAME'],
            "service": "git",
            "uid": 0,
            "wiki": True
        }
        response = requests.post(m_config['DIST_URL'] + 'api/v1/repos/migrate', headers = dist_headers, data = json.dumps(data))


def origin_repositore_list():
    repos_search_path = 'api/v1/orgs/' + m_config['ORIGIN_ORG_NAME'] + '/repos'
    req = requests.get(m_config['ORIGIN_URL'] + repos_search_path, headers=origin_headers)
    repos = json.loads(req.text)
    return repos


if __name__ == '__main__':
    main()