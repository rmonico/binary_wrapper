import os
import subprocess


"""
Example:
    from binary_wrapper import BinaryWrapper

    git = Binary('git') # Find git in PATH

    git.init() # Run 'git init'
    git.add('README') # Run 'git add README'
    git.commit(m='First commit') # Run 'git commit -m "First commit"
    git.config(get='core.pager') # Run 'git config --get core.pager  # << notice the -- instead -
"""
class BinaryWrapper(object):

    def __init__(self, binary):
        super().__init__()
        import distutils.spawn

        self._binary_path = distutils.spawn.find_executable(binary)

        if not self._binary_path:
            raise BinaryWrapperException('{} not found in PATH'.format(binary))

    def _wrap(self, method, *args, **kwargs):
        switchs = []
        for key, value in kwargs.items():
            prefix = '--' if len(key) > 1 else '-'
            # TODO Convert _ in key to - in parameter
            # TODO Handle parameters which requires = between key and value
            # TODO Handle flag parameters (when value == True)
            switchs.append('{}{}'.format(prefix, key))
            switchs.append(str(value))

        binary_with_args = [self._binary_path, method] + list(args) + switchs

        process = subprocess.run(args=binary_with_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return process

    def __getattr__(self, attribute_name):
        def __call_wrapper__(*args, **kwargs):
            return self._wrap(attribute_name, *args, **kwargs)

        return __call_wrapper__

class BinaryWrapperException(Exception):
    pass
