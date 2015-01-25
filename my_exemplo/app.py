#! /usr/bin/python
#-*- coding: utf-8 -*-

import pykeypi as teclado
import sys

if __name__ == '__main__':

    teclado.info()

    try:

        tecla_pressionada = teclado.keypad()

        senha_acesso = str()
        tam_senha = 0

        teclado.print_msg("Digite a senha de controle de acesso") 

        while tam_senha < 5:
            senha_acesso += str(tecla_pressionada.getKey())
            tam_senha += 1
            
            print "\rFaltam %d caracteres" % (5-tam_senha),
            sys.stdout.flush()

        teclado.print_msg("Senha: %s" % (senha_acesso))

    except KeyboardInterrupt:
        teclado.exit()
    
    teclado.exit()
