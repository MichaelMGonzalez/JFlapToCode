import os

rm = "rm -f "
if os.name == "nt":
    rm = "del "
def delete(ext):
    os.system( rm + ext)
delete( "*.cs" )
delete( "*.hpp" )
delete( "*.cpp" )
delete( "*.java" )
delete( "*.pyc" )
