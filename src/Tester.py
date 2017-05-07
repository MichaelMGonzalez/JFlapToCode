import unittest
import os
from glob import glob
import sys
import logging
import traceback
from subprocess import PIPE, Popen
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

class DotTest(Test_Sequence):
   out_file = "out.png"
   def setUp(self):
       Test_Sequence.setUp( self )
       self.extention = ".dot"
       self.parser.set_mode( 'Dot' )
       self.compile_flags = [ 'dot', '-Tpng', '-o', DotTest.out_file]
   def tearDown(self):
        if os.path.exists( DotTest.out_file ):
            os.remove( DotTest.out_file )

class CppTest(Test_Sequence):
   def setUp(self):
       Test_Sequence.setUp( self )
       self.extention = ".cpp"
       self.parser.set_mode( 'Cpp' )
       self.compile_flags = [ 'g++', '-fsyntax-only', '-std=c++11' ]

class JavaTest(Test_Sequence):
   def setUp(self):
       Test_Sequence.setUp( self )
       self.extention = "AbstractFSM.java"
       self.parser.set_mode( 'Java' )
       self.compile_flags = [ 'javac' ]

class PyTest(Test_Sequence):
   def setUp(self):
       Test_Sequence.setUp( self )
       self.extention = ".py"
       self.parser.set_mode( 'Python' )
       self.compile_flags = [ 'python', '-m', 'py_compile' ]

class UnityTest(CSharpTest):
    def setUp(self):
       CSharpTest.setUp(self)
       self.parser.set_mode( 'Unity' )
class UnitySimpleTest(CSharpTest):
    def setUp(self):
       CSharpTest.setUp(self)
       self.parser.set_mode( 'UnitySimple' )
class UnityCompactTest(CSharpTest):
    def setUp(self):
       CSharpTest.setUp(self)
       self.parser.set_mode( 'UnityCompact' )


generic_modes = [ 'Arduino', 'Arduino_c' ]
custom_modes = [ CSharpTest, UnityTest, UnitySimpleTest, UnityCompactTest, CTest, CppTest, PyTest, DotTest, JavaTest ]
#generic_modes = [  ]
#custom_modes = [ CppTest ]

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
       test_log = logging.getLogger( self.parser.mode )
       output = "" 
       err = ""
       try:
            self.parser.parse(full_path)
            self.assertTrue( True )
            self.parser.write_to_file( out_name )
            if self.compile_flags:
                proc = Popen( self.compile_flags + [ out_name ], stdin=PIPE, stdout=PIPE, stderr=PIPE)
                output, err = proc.communicate( )
                output = output.decode('ascii')
                err    = err.decode('utf-8')
                exit_code = proc.returncode
                self.assertEquals( exit_code, 0 )
       except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            test_log.error( " %s failed to translate" % name )
            test_log.debug( "%s\nstdout:\n%s\nstderr:\n%s" %( name, output, err )) 
            test_log.debug( e )
            tb_list = traceback.extract_tb(exc_traceback)
            test_log.debug( str(exc_type))
            test_log.debug( "\n".join(traceback.format_list(tb_list) ) )
            self.assertFalse( True )
            
       finally:
            os.remove( out_name )
            pass
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
    error_log = open( "test_error_log.txt", 'w+' )
    logging.basicConfig( stream=error_log, level=logging.DEBUG)
    tests = create_test_suite()
    unittest.TextTestRunner().run(tests)
    error_log.close()
    for f in glob( './*.class'):
        os.remove(f)
