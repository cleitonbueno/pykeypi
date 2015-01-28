#-*- coding: utf-8 -*-

import sys
import time
import os



try:
    import RPi.GPIO as GPIO
except ImportError as ie:
    print("Problema ao importar modulo {0}").format(ie)
    sys.exit()


__author__ = "Cleiton Bueno (cleitonrbueno@gmail.com)"
__copyright__ = "Copyright 2014, Cleiton Bueno"
__credits__ = ["Cleiton Bueno"]
__license__ = "MIT"
__version__ = 1.0




def print_msg(msg):
    tam = len(msg)+4
    
    print "\n" 
    print "#"*tam
    print "# %s #" % (msg)
    print "#"*tam
    print


def exit():
    GPIO.cleanup()


def info():
    print "Revisão Raspberry PI %d" % (GPIO.RPI_REVISION)
    print "Versão RPi.GPIO %s" % (GPIO.VERSION)
    print "Versão %s" % (__version__)


class keypad():


    # Matriz KeyPad 4x4
    __KEYPAD = [
    [1,2,3,"A"],
    [4,5,6,"B"],
    [7,8,9,"C"],
    ["*",0,"#","D"]
    ]

    __row = [7,11,13,15]
    __column = [12,16,18,22]

    __last_key = None



    def __init__(self):

        # Garantindo que sera executado com permissao de super-usuario
        self.check_user()

        # Iniciando o modo como BOARD e desabilitando os Warnings do Rpi.GPIO
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        
        # Configuro todos os pinos da coluna como OUT e nivel LOW(0V)
        for j in range(len(self.__column)):
            GPIO.setup(self.__column[j], GPIO.OUT)
            GPIO.output(self.__column[j], GPIO.LOW)

        # Configuro todos os pinos da linha como INPUT e Pull-Up
        for i in range(len(self.__row)):
            GPIO.setup(self.__row[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)


        # Configurando as interrupcoes que iram ocorrer em algum dos pinos de linha
        GPIO.add_event_detect(7, GPIO.FALLING, callback=self.trataPino, bouncetime=300)    
        GPIO.add_event_detect(11, GPIO.FALLING, callback=self.trataPino, bouncetime=300)    
        GPIO.add_event_detect(13, GPIO.FALLING, callback=self.trataPino, bouncetime=300)    
        GPIO.add_event_detect(15, GPIO.FALLING, callback=self.trataPino, bouncetime=300)    

        self.valor_linha = -1
        self.valor_coluna = -1


    def check_user(self):
        if os.geteuid() != 0:
            print("Vocêeve executar o programa como super-usuario!")
            print("Exemplo:\nsudo python {0}").format(__file__)
            sys.exit()


    def get_key(self):
        
        self.valor_linha = -1
        self.valor_coluna = -1

        while self.valor_coluna == -1 and self.valor_linha == -1:
            pass

        self.__last_key = self.__KEYPAD[self.valor_linha][self.valor_coluna]
        
        # Retorna o valor da tecla pressionada baseada na linhaxcoluna
        return self.__KEYPAD[self.valor_linha][self.valor_coluna]


    def last_key(self): 
        return self.__last_key


    def trataPino(self,pino):

        self.valor_linha = self.__row.index(pino)

        for i in range(len(self.__column)):

            GPIO.setup(self.__column[i], GPIO.IN)
            
            if GPIO.input(pino) == GPIO.HIGH:
                self.valor_coluna = i
                break
        
        self.restaura_gpio()


    def restaura_gpio(self):
        for i in range(len(self.__column)):
            GPIO.setup(self.__column[i], GPIO.OUT)
            GPIO.output(self.__column[i], GPIO.LOW)
