from collections import OrderedDict
from contextlib import contextmanager

class ProgramExistsError(Exception): pass

class SupervisorConfator(object):
    
    def __init__(self, program_options={}, command_formats={}):
        self.programs = OrderedDict()
        self.groups = OrderedDict()
        self.program_options = program_options
        self.command_formats = command_formats
        self.context_options = dict()
        self.context_group_programs = []
    
    @contextmanager
    def options(self, **kwargs):
        self.context_options = kwargs
        yield
        self.context_options = {}
    
    @contextmanager
    def group(self, group_name, **kwargs):
        self.context_group_programs = []
        yield
        self.groups[group_name] = dict(programs=self.context_group_programs, **kwargs)
    
    def program(self, program_name, command, extra_command_formats={}, **kwargs):
        
        if program_name in self.programs:
            raise ProgramExistsError("Program '%s' already exists." % program_name)

        # Create the program options
        options = dict(**self.program_options)
        options.update(**self.context_options)
        options.update(**kwargs)
        
        # Format the command
        command_formats = dict(**self.command_formats)
        command_formats.update(**extra_command_formats)
        options.update(command=command.format(**command_formats))

        # Add the program        
        self.programs[program_name] = dict(**options)
        
        # Append it to the current group
        self.context_group_programs.append(program_name)
    
    def write(self):
        """
        Generate the output.
        """
        conf = []
        
        # First off write the programs
        initial_option_keys = ['command', 'user', 'process_name']
        
        for program,options in self.programs.items():
            conf.append('[program:%s]' % program)
            
            for key in initial_option_keys:
                try:
                    conf.append('%s=%s' % (key, self.to_supervisor(options.pop(key))))
                except KeyError: pass
            
            # Put the rest of the options in alpha order            
            for option,value in self.sort_options(options).items():
                conf.append('%s=%s' % (option, self.to_supervisor(value)))
        
            conf.append('')
        
        # Now write the groups
        for group,options in self.groups.items():
            conf.append('[group:%s]' % group)
            conf.append('programs=%s' % self.to_supervisor(options.pop('programs')))
            
            # Put the rest of the options in alpha order            
            for option,value in self.sort_options(options).items():
                conf.append('%s=%s' % (option, self.to_supervisor(value)))
        
            conf.append('')
            
        return "\n".join(conf)

    def sort_options(self, options):
        return OrderedDict(sorted(options.items(), key=lambda t: t[0]))

    def to_supervisor(self, value):
        if value is False:
            return 'false'
        elif value is True:
            return 'true'
        elif isinstance(value, (list, tuple)) and not isinstance(value, basestring):
            return ",".join([u'%s' % v for v in value])
        else:
            return '%s' % value