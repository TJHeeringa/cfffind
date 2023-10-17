# cfffind

This is a Python library to automatically retrieve .cff files from packages you have installed.

**NB: This is a very early stage package.**

## How to use
So far, you can find all the Github urls belonging to the packages installed through conda using
```
./conda_env_to_package_list.sh | sed "s/ /\n/g" | xargs -I {} python get_github_url.py {}
```
The command `conda_env_to_package_list.sh` takes you installed packages and gives you a space separated list of packages you have installed explicitly. `sed` with `xargs` feeds the packages one by one into the `get_github_url` command. This will go through the metadata and see if it can find a Github url.   

