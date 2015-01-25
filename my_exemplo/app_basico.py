#! /usr/bin/python
#-*- coding: utf-8 -*-

import pykeypi as teclado
import sys

if __name__ == '__main__':

    try:

        tecla_pressionada = teclado.keypad()

        teclado.print_msg("Pressione alguma tecla...") 


        while True:
            if str(tecla_pressionada.getKey()):
                tecla = tecla_pressionada.getKey()
                sys.stdout.flush()
                break

        teclado.print_msg("Tecla: %s" % (tecla))

    except KeyboardInterrupt:
        teclado.exit()
    
    teclado.exit()
