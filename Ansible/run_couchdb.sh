#!/bin/bash

. ./openrc.sh; ansible-playbook -i hosts --ask-become-pass run_couchdb.yaml