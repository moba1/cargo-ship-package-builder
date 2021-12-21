#!/usr/bin/env bash

ansible-playbook \
  -c local \
  --extra-vars dist_dir="$DIST_DIR" \
  --extra-vars tool_dir="$WORK_ROOT/tools" \
  --extra-vars target="$TARGET" \
  --extra-vars root="$WORK_ROOT" \
  ansible/site.yml
