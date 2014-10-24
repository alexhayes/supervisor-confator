from collections import OrderedDict

class SupervisorConfator(object):
    
    def __init__(self, programs, groups=None):
        self.programs = programs
        self.groups = groups
    
    def generate(self):
        """
        Generate the output.
        """
        conf = []
        initial_option_keys = ['command', 'user', 'process_name']
        
        for program,options in self.programs.items():
            conf.append('[program:%s]' % program)
            
            for key in initial_option_keys:
                try:
                    conf.append('%s=%s' % (key, options.pop(key)))
                except KeyError: pass
            
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