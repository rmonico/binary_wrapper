import unittest
from unittest import TestCase

from binary_wrapper import BinaryWrapper


class TestsBinaryWrapper(TestCase):

    def setUp(self):
        class PythonWrapper(BinaryWrapper):
            def regular_method(self):
                return 'regular method called'

            def __init__(self):
                super().__init__('python3')

            def _wrap(self, *args, **kwargs):
                return super()._wrap('-c', 'import sys; print(";".join(sys.argv[1:]))', *args, **kwargs)

        self._python_wrapper = PythonWrapper()


    def test_when_non_existing_method_called_then_pass_method_name_to_binary_as_first_arg(self):
        process = self._python_wrapper.parameter_passed_to_script()
        self.assertEqual(process.returncode, 0)

        stdout = process.stdout.decode()[:-1]
        self.assertEqual(stdout, 'parameter_passed_to_script')

    def test_when_regular_method_called_then_just_call_it(self):
        result = self._python_wrapper.regular_method()

        self.assertEqual(result, 'regular method called')

    def test_when_non_existing_method_called_with_unnamed_args_then_must_pass_as_its_parameters(self):
        result = self._python_wrapper.non_existing_method('first arg', 'second arg')

        stdout = result.stdout.decode()[:-1]
        self.assertEqual(stdout, 'non_existing_method;first arg;second arg')

    def test_when_non_existing_method_called_with_kwargs_then_must_pass_then_as_switches(self):
        result = self._python_wrapper.non_existing_method(first='value 1', second='second value')

        stdout = result.stdout.decode()[:-1]
        self.assertEqual(stdout, 'non_existing_method;--first;value 1;--second;second value')

    def test_when_non_existing_method_called_with_one_letter_kwarg_then_must_pass_as_single_letter_switch(self):
        result = self._python_wrapper.non_existing_method(c='value of -c')

        stdout = result.stdout.decode()[:-1]
        self.assertEqual(stdout, 'non_existing_method;-c;value of -c')


if __name__ == '__main__':
    unittest.main()
