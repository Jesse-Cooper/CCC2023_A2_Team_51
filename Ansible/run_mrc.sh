#!/bin/bash

. ./openrc.sh; ansible-playbook --ask-become-pass mrc.yaml
