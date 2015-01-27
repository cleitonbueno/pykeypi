#! /usr/bin/env python
#-*- coding: utf-8 -*-

import pykeypi as teclado
import sys

if __name__ == '__main__':

    try:

        tecla_pressionada = teclado.keypad()

        teclado.print_msg("Pressione alguma tecla...") 


        while True:
            if str(tecla_pressionada.get_key()):
                sys.stdout.flush()
                break
        
        print "Tecla: %s" % (tecla_pressionada.last_key())

    except KeyboardInterrupt:
        teclado.exit()
    
    teclado.exit()
