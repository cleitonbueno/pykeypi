# #####################################################
# Python Library for 3x4 matrix keypad using
# 7 of the avialable GPIO pins on the Raspberry Pi.
#
# This could easily be expanded to handle a 4x4 but I
# don't have one for testing. The KEYPAD constant
# would need to be updated. Also the setting/checking
# of the colVal part would need to be expanded to
# handle the extra column.
#
# Written by Chris Crumpacker
# May 2013
#
# main structure is adapted from Bandono's
# matrixQPI which is wiringPi based.
# https://github.com/bandono/matrixQPi?source=cc
# #####################################################

import RPi.GPIO as GPIO

"""
def trataPino(pino):
    print "Ocorreu interrupcao no pino %d" % pino
"""




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
        GPIO.setmode(GPIO.BOARD)
        
        # Set all columns as output low
        for j in range(len(self.COLUMN)):
            GPIO.setup(self.COLUMN[j], GPIO.OUT)
            GPIO.output(self.COLUMN[j], GPIO.LOW)

        # Set all rows as input
        for i in range(len(self.ROW)):
            GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)


        # Configurando as interrupcoes
        GPIO.add_event_detect(7, GPIO.FALLING, callback=self.trataPino, bouncetime=300)    
        GPIO.add_event_detect(11, GPIO.FALLING, callback=self.trataPino, bouncetime=300)    
        GPIO.add_event_detect(13, GPIO.FALLING, callback=self.trataPino, bouncetime=300)    
        GPIO.add_event_detect(15, GPIO.FALLING, callback=self.trataPino, bouncetime=300)    





    def getKey(self):

        
        # Set all columns as output low
        for j in range(len(self.COLUMN)):
            GPIO.setup(self.COLUMN[j], GPIO.OUT)
            #GPIO.output(self.COLUMN[j], GPIO.LOW)


        # Set all rows as input
        for i in range(len(self.ROW)):
            GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Scan rows for pushed key/button
        # A valid key press should set "rowVal"  between 0 and 3.
        #rowVal = -1
        for i in range(len(self.ROW)):
            tmpRead = GPIO.input(self.ROW[i])
            if tmpRead == 0:
                #rowVal = i
                self.valor_linha = i

        # if rowVal is not 0 thru 3 then no button was pressed and we can exit
        if self.valor_linha < 0 or self.valor_linha > 3:
            self.exit()
            return

        """ 
        # Convert columns to input
        for j in range(len(self.COLUMN)):
            GPIO.setup(self.COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # Switch the i-th row found from scan to output
        GPIO.setup(self.ROW[rowVal], GPIO.OUT)
        GPIO.output(self.ROW[rowVal], GPIO.HIGH)

        # Scan columns for still-pushed key/button
        # A valid key press should set "colVal"  between 0 and 2.
        colVal = -1
        for j in range(len(self.COLUMN)):
            tmpRead = GPIO.input(self.COLUMN[j])
            if tmpRead == 1:
                colVal=j

        # if colVal is not 0 thru 2 then no button was pressed and we can exit
        if colVal < 0 or colVal > 3:
            self.exit()
            return
        
        """
        # Return the value of the key pressed
        self.exit()
        print "A tecla %s foi pressionada LINHA[%d] COLUNA[%d]" % (self.KEYPAD[self.valor_linha][self.valor_coluna],self.valor_linha, self.valor_coluna)
        return self.KEYPAD[self.valor_linha][self.valor_coluna]

    def trataPino(self,pino):
        print "Ocorreu interrupcao no pino %d" % pino       
        for i in range(len(self.COLUMN)):
            
            GPIO.setup(self.COLUMN[i], GPIO.IN)

            if GPIO.input(pino) == GPIO.HIGH:
                self.valor_coluna = i
                break

        self.restaura_gpio_row


    def restaura_gpio_row(self):
        for i in range(len(self.COLUMN)):
            GPIO.setup(self.COLUMN[i], GPIO.OUT)
            GPIO.output(self.COLUMN[i], GPIO.LOW)

    def exit(self):
        # Reinitialize all rows and columns as input at exit
        for i in range(len(self.ROW)):
            GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        for j in range(len(self.COLUMN)):
            GPIO.setup(self.COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_UP)


if __name__ == '__main__':
    # Initialize the keypad class
    kp = keypad()

    # Loop while waiting for a keypress
    digit = None
    while digit == None:
        digit = kp.getKey()

    # Print the result
    print digit
