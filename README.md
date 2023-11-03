# cfffind

This is a Python library to automatically retrieve .cff files from packages you have installed.

**NB: This only works for packages installed through Anaconda.**

## How to use
You can run the command
```
python cfffind
```
to go over all your installed Python packages, detect whether they are hosted on Github and, if so, check for a citation file. The citation files will be parsed into the `references` format specified by the `.cff` standard, and written to `references.cff`.
