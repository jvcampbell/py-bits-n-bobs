# Encode/Decode text to caesar cipher. Includes a brute force method when the key is not known

import os

class CaesarCipherSimple(object):

    alphabet = 'abcdefghijklmnopqrstuvwxyz '

    def __init__(self):
        pass

    def encode(self,input_text,cipher_key = 1):
        '''Encodes text by receiving an integer and shifting the letter position that number of letters to the right '''
        
        try:
            return self.__shift_letter(input_text,cipher_key)
        except:
            print('Error encoding')

    def decode(self,input_text,cipher_key = 1):
        '''Encodes text by receiving an integer and shifting the letter position that number of letters to the right '''
        
        try:
            return self.__shift_letter(input_text,cipher_key*-1)
        except:
            print('Error decoding')  

    def brute_decode(self,input_text):
        '''Encodes text by receiving an integer and shifting the letter position that number of letters to the right '''
        
        try:
            decode_list = []

            for cipher_key in range(1,27):
                decode_list.append(str(cipher_key) + ': ' + self.__shift_letter(input_text,cipher_key*-1))
            return decode_list
        except:
            print('Error decoding')  

    def __shift_letter(self,input_text,shift_nb):
        
        new_text = ''

        for text_letter in input_text:
            
            letter_position = CaesarCipherSimple.alphabet.find(text_letter)

            letter_position += shift_nb

            # Handle letters that shift off the 0-26 position spectrum of the alphabet
            if shift_nb > 0:
                if letter_position > 27:
                    letter_position -= 27
                else:
                    pass
            else:
                if letter_position < 0:
                    letter_position += 27

            new_text += self.alphabet[letter_position]
        
        return new_text
            
#-----------------------------------------------#

os.system('cls')

print('-------------------------Caesar Cypher--------------------------')

action = input('Are you encoding a message or decoding a cypher? (e/d):').lower()
input_text = input('Enter the text you want to work on:').lower()

try:
    input_key = int(input('Enter an integer cypher key (press Enter if you don''t know):'))
except:
    input_key = None

if action == 'd' and (input_key == 0 or input_key is None):
    print('\n!!! Time to brute force this thing !!!')
    action = 'bd'

cypherMachine = CaesarCipherSimple()

print('\n----------OUTPUT----------------')

if action == 'e':
    print(cypherMachine.encode(input_text,input_key))
elif action == 'd':
    print(cypherMachine.decode(input_text,input_key))
elif action =='bd':
    for attempt in cypherMachine.brute_decode(input_text):
        print(attempt)


