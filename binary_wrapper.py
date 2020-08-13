import os
import subprocess


class BinaryWrapper(object):

    def __init__(self, binary):
        import distutils

        self._binary_path = distutils.spawn.find_executable(binary)

        if not self._binary_path:
            raise BinaryWrapperException('{} not found in PATH'.format(binary))

    def _binary(self, *args):
        process = subprocess.run(
            [self._git_path] + list(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return process

    def __getattribute__(self, attribute_name):
        if GitWrapper._should_not_wrap(attribute_name):
            return object.__getattribute__(self, attribute_name)

        def __call_wrapper__(*args, **kwargs):
            command = attribute_name

            args = args[1:]

            return self._binary(command, *args, **kwargs)

        return __call_wrapper__

    @staticmethod
    def _should_not_wrap(attribute_name):
        return attribute_name.startswith('_')


class BinaryWrapperException(Exception):
    pass
