#!/bin/bash

ansible-playbook --ask-become-pass -i hosts -u ubuntu couchdb.yaml
