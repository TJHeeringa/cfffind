# cfffind

This is a Python library to automatically retrieve .cff files from packages you have installed.

**NB: This is a very early stage package.**

## How to use
So far, you can find all the Github urls belonging to the packages installed through conda using
```
./conda_env_to_package_list.sh | sed "s/ /\n/g" | xargs -I {} python get_github_url.py {}
```
The command `conda_env_to_package_list.sh` takes you installed packages and gives you a space separated list of packages you have installed explicitly. `sed` with `xargs` feeds the packages one by one into the `get_github_url` command. This will go through the metadata and see if it can find a Github url.   

## How it will work
You can run the command
```
python cfffind
```
to go over all your installed Python packages, detect whether they are hosted on Github and, if so, check for a citation file. The citation files will be parsed into the `references` format specified by the `.cff` standard. By running
```
python cfffind >> references.bib
```
you can store the results in the file `references.bib`.

