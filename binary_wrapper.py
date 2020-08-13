import os
import subprocess


class BinaryWrapper(object):

    def __init__(self, binary):
        super().__init__()
        import distutils.spawn

        self._binary_path = distutils.spawn.find_executable(binary)

        if not self._binary_path:
            raise BinaryWrapperException('{} not found in PATH'.format(binary))

    def _call(self, *args):
        process = subprocess.run(
            [self._binary_path] + list(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return process

    def __getattr__(self, attribute_name):
        def __call_wrapper__(*args, **kwargs):
            command = attribute_name

            return self._call(command, *args, **kwargs)

        return __call_wrapper__

class BinaryWrapperException(Exception):
    pass
