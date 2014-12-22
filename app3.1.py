#-*- coding: utf-8 -*-

import sys

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
    
    print 
    print "#"*tam
    print "# %s #" % (msg)
    print "#"*tam
    print


class keypad():


    # CONSTANTS
    KEYPAD = [
    [1,2,3,"A"],
    [4,5,6,"B"],
    [7,8,9,"C"],
    ["*",0,"#","D"]
    ]

    ROW = [7,11,13,15]
    COLUMN = [12,16,18,22]

    #    ROW = [18,23,24,25]
    #    COLUMN = [4,17,22]


    valor_linha = -1
    valor_coluna = -1


    def __init__(self):

        # Iniciando o modo como BOARD e desabilitando os Warnings do Rpi.GPIO
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        
        # Configuro todos os pinos da coluna como OUT e nivel LOW(0V)
        for j in range(len(self.COLUMN)):
            GPIO.setup(self.COLUMN[j], GPIO.OUT)
            GPIO.output(self.COLUMN[j], GPIO.LOW)

        # Configuro todos os pinos da linha como INPUT e Pull-Up
        for i in range(len(self.ROW)):
            GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)


        # Configurando as interrupcoes que iram ocorrer em algum dos pinos de linha
        GPIO.add_event_detect(7, GPIO.FALLING, callback=self.trataPino, bouncetime=300)    
        GPIO.add_event_detect(11, GPIO.FALLING, callback=self.trataPino, bouncetime=300)    
        GPIO.add_event_detect(13, GPIO.FALLING, callback=self.trataPino, bouncetime=300)    
        GPIO.add_event_detect(15, GPIO.FALLING, callback=self.trataPino, bouncetime=300)    


    def getKey(self):

        while self.valor_coluna == -1 and self.valor_linha == -1:
            pass

        #self.exit()
        
        # Retorna o valor da tecla pressionada baseada na linhaxcoluna
        return self.KEYPAD[self.valor_linha][self.valor_coluna]


    def trataPino(self,pino):

        self.valor_linha = self.ROW.index(pino)

        for i in range(len(self.COLUMN)):

            GPIO.setup(self.COLUMN[i], GPIO.IN)
            
            if GPIO.input(pino) == GPIO.HIGH:
                self.valor_coluna = i
                break
        
        self.restaura_gpio_row()


    def restaura_gpio_row(self):
        for i in range(len(self.COLUMN)):
            GPIO.setup(self.COLUMN[i], GPIO.OUT)
            GPIO.output(self.COLUMN[i], GPIO.LOW)



if __name__ == '__main__':

    print "Revisão Raspberry PI %d" % (GPIO.RPI_REVISION)
    print "Versão RPi.GPIO %s" % (GPIO.VERSION)


    try:

        """
        # Initialize the keypad class
        kp = keypad()

        # Loop while waiting for a keypress
        digit = str()
        
        digit = kp.getKey()
        
        # Print the result
        print digit
        """
        
        tecla_pressionada = keypad()

        senha_acesso = str()
        tam_senha = 0

        print_msg("Digite a senha de controle de acesso") 

        while tam_senha < 5:
            """
            senha_acesso += str(tecla_pressionada.getKey())
            tam_senha += 1
            """
        print_msg("Senha digitada")
        print senha_acesso


    except KeyboardInterrupt:
        GPIO.cleanup()

    GPIO.cleanup()
