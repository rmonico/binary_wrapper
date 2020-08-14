import os
import subprocess


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
