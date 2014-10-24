# Supervisor Confator

Supervisor Confator (Config Creator) is a Python interface to generate supervisor configuration files.

Using Python dicts as input it creates a configuration file suitable for supervisor (and probably other applications also...).

## Why

At http://roi.com.au we have a lot of supervisor program sections and I was sick and tired of managing without variables for things like directories, executables (ie.. python, celery etc..).

## Limitations

Currently Supervisor Confator only supports program and group sections.

## Example

```#!python
sc = SupervisorConfator(default_program_options=dict(user='myuser'),
                        command_formats=dict(bin='/usr/bin/',
                                             log_dir='/var/log/'))

sc.program('eggs', '{bin}eggs')

with sc.options(autorestart=False):
	sc.program('sausage', '{bin}sausage --log-dir={log_dir}sausage.log')

with sc.group('mygroup', priority=999):
	with sc.options(priority=998):
		sc.program('silly', '{bin}silly')
		sc.program('walks', '{bin}walks', user='myotheruser', stopsignal='INT')
    
sc.write()
```

Outputs the following;

```#!ini
[program:eggs]
command=/usr/bin/eggs
user=myuser

[program:sausage]
command=/usr/bin/sausage
user=myuser
autorestart=false

[program:silly]
command=/usr/bin/walks
priority=998

[program:walks]
command=/usr/bin/walks
user=myotheruser
stopsignal=INT
priority=998

[group:mygroup]
programs=silly,walks
priority=999
```

## Thanks

Special thanks to http://roi.com.au for supporting this project.

## Author

Alex Hayes <alex@alution.com>
