#!/bin/bash

. ./openrc.sh; ansible-playbook --ask-become-pass -vv mrc.yaml
