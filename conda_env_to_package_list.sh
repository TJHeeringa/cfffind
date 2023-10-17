#!/bin/bash

conda_env_file=$(conda env export --from-history)
dep_line=$(echo "$conda_env_file" | grep -n 'dependencies:' | cut -d: -f1)
conda_deps=$(echo "$conda_env_file" | tail -n +$dep_line | grep '  - .*' | cut -c 4-)
echo $conda_deps
