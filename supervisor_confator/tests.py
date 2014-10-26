from unittest.case import TestCase
from collections import OrderedDict
from supervisor_confator import SupervisorConfator, ProgramExistsError

class SupervisorConfCreatorTestCase(TestCase):
    
    def test_one_program(self):
        sc = SupervisorConfator()
        sc.program('eggs', '/usr/bin/eggs')
        actual = sc.write()
        expected = """[program:eggs]
command=/usr/bin/eggs
"""
        self.assertEqual(expected, actual)
    
    def test_program_exists(self):
        sc = SupervisorConfator()
        sc.program('eggs', '/usr/bin/eggs')
        self.assertRaises(ProgramExistsError, sc.program, 'eggs', '/usr/bin/eggs')
    
    def test_complex(self):
        
        sc = SupervisorConfator(program_options=dict(user='myuser'),
                                command_formats=dict(bin='/usr/bin/',
                                                     log_dir='/var/log/'))
        
        sc.program('eggs', '{bin}eggs')
        
        with sc.options(autorestart=False):
            sc.program('sausage', '{bin}sausage --log-dir={log_dir}sausage.log')
        
        with sc.group('mygroup', priority=999):
            with sc.options(priority=998):
                sc.program('silly', '{bin}silly')
                sc.program('walks', '{bin}walks {extra}',
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
                           autorestart=False,
                           extra_command_formats=dict(extra=1))
            
        actual = sc.write()
        
        expected = """[program:eggs]
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
command=/usr/bin/walks 1
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
"""
        self.assertEqual(expected, actual)