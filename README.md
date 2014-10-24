# Supervisor Confator

Supervisor Confator (Config Creator) is a Python interface to generate supervisor configuration files.

Using Python dicts as input it creates a configuration file suitable for supervisor (and probably other applications also...).

## Why

At http://roi.com.au we have a lot of supervisor program sections and I was sick and tired of managing without variables for things like directories, executables (ie.. python, celery etc..).

## Limitations

Currently Supervisor Confator only supports program and group sections.

## Example

```#!python
sc = SupervisorConfator(program_options=dict(user='myuser'),
                        command_formats=dict(bin='/usr/bin/',
                                             log_dir='/var/log/'))

sc.program('eggs', '{bin}eggs')

with sc.options(autorestart=False):
    sc.program('sausage', '{bin}sausage --log-dir={log_dir}sausage.log')

with sc.group('mygroup', priority=999):
    with sc.options(priority=998):
        sc.program('silly', '{bin}silly')
        sc.program('walks', '{bin}walks', 
                   user='myotheruser', 
                   process_name='%(program_name)s',
                   numprocs=1,
                   numprocs_start=0,
                   startsecs=1,
                   startretries=3,
                   exitcodes=[0,2],
                   stopsignal='TERM',
                   stopwaitsecs=10,
                   redirect_stderr=False,
                   stdout_logfile='AUTO',
                   stdout_logfile_maxbytes='50MB',
                   stdout_logfile_backups=10,
                   stdout_capture_maxbytes=0,
                   stdout_events_enabled=False,
                   stderr_logfile='AUTO',
                   stderr_logfile_maxbytes='50MB',
                   stderr_logfile_backups=10,
                   stderr_capture_maxbytes=0,
                   stderr_events_enabled=False,
                   directory='/path/to/myapp.com',
                   serverurl='AUTO',
                   autostart=False,
                   autorestart=False)
    
print sc.write()
```

Outputs the following;

```#!ini
[program:eggs]
command=/usr/bin/eggs
user=myuser

[program:sausage]
command=/usr/bin/sausage --log-dir=/var/log/sausage.log
user=myuser
autorestart=false

[program:silly]
command=/usr/bin/silly
user=myuser
priority=998

[program:walks]
command=/usr/bin/walks
user=myotheruser
process_name=%(program_name)s
autorestart=false
autostart=false
directory=/path/to/myapp.com
exitcodes=0,2
numprocs=1
numprocs_start=0
priority=998
redirect_stderr=false
serverurl=AUTO
startretries=3
startsecs=1
stderr_capture_maxbytes=0
stderr_events_enabled=false
stderr_logfile=AUTO
stderr_logfile_backups=10
stderr_logfile_maxbytes=50MB
stdout_capture_maxbytes=0
stdout_events_enabled=false
stdout_logfile=AUTO
stdout_logfile_backups=10
stdout_logfile_maxbytes=50MB
stopsignal=TERM
stopwaitsecs=10

[group:mygroup]
programs=silly,walks
priority=999
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
