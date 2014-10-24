# Supervisor Confator

Supervisor Confator (Config Creator) is a Python interface to generate supervisor configuration files.

Using Python dicts as input it creates a configuration file suitable for supervisor (and probably other applications also...).

## Why

At http://roi.com.au we have a lot of supervisor program sections and I was sick and tired of managing without variables for things like directories, executables (ie.. python, celery etc..).

## Limitations

Currently Supervisor Confator only supports program and group sections.

## Example

```#!python
import sys
from collections import OrderedDict

formats = dict(python=sys.executable)

programs = OrderedDict()
programs['myapp'] = OrderedDict(
    command='{python} /path/to/my/app.py'.format(**formats),
    user='app',
    stopsignal='INT'
)
print SupervisorConfCreator(programs).generate()
```

Outputs the following;

```#!ini
[program:myapp]
command=/usr/bin/python /path/to/my/app.py
user=app
stopsignal=INT
```

## Contributing

Contributions welcome - note that I plan to significantly change the API, see branch feature/context-api

### Setup

```#!bash
git clone https://github.com/alexhayes/supervisor-confator.git
cd supervisor-confator
git submodule init
git submodule update
mkvirtualenv supervisor-confator
pip install -r requirements
```

### Running Tests

```#!python
nosetests
```

## Thanks

Special thanks to http://roi.com.au for supporting this project.

## Author

Alex Hayes <alex@alution.com>
