from __future__ import print_function
import sys

class FmcPrint( object ):
    def __init__( self ):
        pass

    def printError( self, text ):
        print("\033[1;31;0m [-] {0} \033[0;0;0m\n".format(text))
    
    def printSuccess( self, text  ):
        print("\033[1;32;0m [*] {0} \033[0;0;0m \n".format(text))

    def printSuccessNum( self, text, idx, price  ):
        print("\033[1;32;0m [{0}] {1} {2} \033[0;0;0m \n".format(idx, text, price))

    def printWarning( self, text ):
        print("\033[1;33;0m [-] {0} \033[0;0;0m \n".format(text))

    def printDiag( self, text ):
        print("\033[1;34;0m [+] {0} \033[0;0;0m \n".format(text))
