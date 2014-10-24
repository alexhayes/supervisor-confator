from unittest.case import TestCase
from collections import OrderedDict
from supervisor_confator import SupervisorConfator

class SupervisorConfCreatorTestCase(TestCase):
    
    def get_programs(self):
        programs = OrderedDict()
        programs['web'] = OrderedDict(
            command='/usr/local/bin/uwsgi --ini /path/to/uwsgi.ini',
            user='deploy',
            stopsignal='INT'
        )
        programs['flower'] = OrderedDict(
            command='/data/python/virtualenvs/myapp/bin/python /data/python/virtualenvs/myapp/bin/celery flower -A myapp --logging=warning',
            process_name='%(program_name)s',
            numprocs=1,
            numprocs_start=0,
            startsecs=1,
            startretries=3,
            exitcodes=[0,2],
            stopsignal='TERM',
            stopwaitsecs=10,
            user='deploy',
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
            directory='/data/vhosts/hosts/myapp.com',
            serverurl='AUTO',
            autostart=False,
            autorestart=False
        )
        
        return programs

    def get_groups(self):
        groups = OrderedDict()
        groups['myappgroup'] = dict(programs=['web', 'flower'], priority=999)
        return groups

    def test_programs(self):
        programs = self.get_programs()
        
        expected = """[program:web]
command=/usr/local/bin/uwsgi --ini /path/to/uwsgi.ini
user=deploy
stopsignal=INT

[program:flower]
command=/data/python/virtualenvs/myapp/bin/python /data/python/virtualenvs/myapp/bin/celery flower -A myapp --logging=warning
user=deploy
process_name=%(program_name)s
autorestart=false
autostart=false
directory=/data/vhosts/hosts/myapp.com
exitcodes=0,2
numprocs=1
numprocs_start=0
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
"""
        actual = SupervisorConfator(programs).generate()
        self.assertEqual(expected, actual)

    def test_groups(self):
        groups = self.get_groups()
        
        expected = """[group:myappgroup]
programs=web,flower
priority=999
        """        