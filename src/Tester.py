import unittest
import os
import subprocess
from Constants import *
from JFlapToCode import JFlapParser
JFF = ".jff"


class Test_Sequence(unittest.TestCase):
    def setUp(self):
        self.parser = JFlapParser(config_file=config_file)
        self.parser.quiet_mode()
        self.extention = ".foo"
        self.compile_flags = []

class CSharpTest(Test_Sequence):
   def setUp(self):
       Test_Sequence.setUp( self )
       self.extention = ".cs"
       self.parser.set_mode( 'CSharp' )
       self.compile_flags = [ 'mcs', '--parse' ]

class CTest(Test_Sequence):
   def setUp(self):
       Test_Sequence.setUp( self )
       self.extention = ".c"
       self.parser.set_mode( 'C' )
       self.compile_flags = [ 'gcc', '-fsyntax-only' ]


class UnityTest(CSharpTest):
    def setUp(self):
       CSharpTest.setUp(self)
       self.parser.set_mode( 'Unity' )


generic_modes = [ 'Arduino', 'Arduino_c', 'Python' ]
custom_modes = [ CSharpTest, UnityTest, CTest ]

def make_test_case( mode ):
    class Anon_Test_Sequence(Test_Sequence):
        def setUp(self):
            Test_Sequence.setUp( self )
            self.parser.set_mode( mode )
    return Anon_Test_Sequence

def is_jff( file_name ):
    return len(file_name) > len(JFF) and file_name[-len(JFF):] == JFF

def strip_jff(filename):
    return filename[:-len(JFF)]

"""
This function creates functions to be assign to test classes
"""
def test_generator( name, full_path ):
    def runTest(self):
       out_name = name + self.extention
       try:
            self.parser.parse(full_path)
            self.assertTrue( True )
            self.parser.dump_to_file( out_name )
            if self.compile_flags:
                exit_code = subprocess.check_call( self.compile_flags + [ out_name ])
                self.assertEquals( exit_code, 0 )
       except:
            self.assertFalse( True )
       finally:
            os.remove( out_name )
    return runTest

def create_test_suite():
    rv = unittest.TestSuite()
    tests_loc = os.path.join('..',  'samples' )
    test_files = os.listdir( tests_loc )
    test_files = [ (strip_jff(file), os.path.join( tests_loc, file)) for file in test_files if  is_jff(file) ]
    for test,path in test_files:
        test_case = test_generator( test, path )
        fmt_string = "%s_translate_%s"
        for mode in generic_modes:
            _class = make_test_case( mode )
            test_name = fmt_string % (mode, test) 
            setattr(_class, test_name, test_case)
            rv.addTest( _class( test_name ) )
        for mode in custom_modes:
            _mode_name = mode.__name__
            test_name = fmt_string % (_mode_name, test) 
            setattr(mode, test_name, test_case)
            rv.addTest( mode( test_name ) )
    return rv


if __name__ == '__main__':
    tests = create_test_suite()
    unittest.TextTestRunner().run(tests)