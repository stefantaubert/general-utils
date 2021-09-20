# general-utils

pipenv install -e git+https://github.com/stefantaubert/general-utils.git@master#egg=general_utils


## Pipfile

### Local

```Pipfile
general-utils = {editable = true, path = "./../general-utils"}
```

### Remote

```Pipfile
general-utils = {editable = true, ref = "master", git = "https://github.com/stefantaubert/general-utils.git"}
```

## setup.cfg

```cfg
general_utils@git+https://github.com/stefantaubert/general-utils@master
```
