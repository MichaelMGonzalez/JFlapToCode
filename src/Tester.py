import unittest
import os
from Constants import *
from JFlapToCode import JFlapParser
JFF = ".jff"

modes = [ 'Unity', 'CSharp', 'Arduino', 'Arduino_c', 'Python' ]

class Test_Sequence(unittest.TestCase):
    def setUp(self):
        self.parser = JFlapParser(config_file=config_file)
        self.parser.quiet_mode()


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
def test_generator( name, full_path ):
    def runTest(self):
       try:
            self.parser.parse(full_path)
            self.assertTrue( True )
            self.parser.dump_to_file( name )
            os.remove( name )
       except:
            self.assertFalse( True )
    return runTest

def suite():
    rv = unittest.TestSuite()
    tests_loc = os.path.join('..',  'samples' )
    test_files = os.listdir( tests_loc )
    test_files = [ (strip_jff(file), os.path.join( tests_loc, file)) for file in test_files if  is_jff(file) ]
    for test,path in test_files:
        for mode in modes:
            _class = make_test_case( mode )
            test_name = "%s_translate_%s" % (mode, test) 
            test_case = test_generator( test, path )
            setattr(_class, test_name, test_case)
            rv.addTest( _class( test_name ) )
    return rv


if __name__ == '__main__':
    tests = suite()
    unittest.TextTestRunner().run(tests)