__author__ = "Lech Szymanski"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "lech.szymanski@otago.ac.nz"


import numpy as np
import sys
import readchar
from mastermind import print_colour_char

class MastermindAgent():
   """
             A class that encapsulates the code dictating the
             behaviour of the agent playing the game of Mastermind.

             ...

             Attributes
             ----------
             code_length: int
                 the length of the code to guess
             colours : list of char
                 a list of colours represented as characters
             num_guesses : int
                 the max. number of guesses per game

             Methods
             -------
             AgentFunction(percepts)
                 Returns the next guess of the colours on the board
             """

   def __init__(self, code_length, colours, num_guesses):
      """
      :param code_length: the length of the code to guess
      :param colours: list of letter representing colours used to play
      :param num_guesses: the max. number of guesses per game
      """

      self.code_length = code_length
      self.colours = colours
      self.num_guesses = num_guesses


   def AgentFunction(self, percepts):

      """Returns the next board guess given state of the game in percepts

            :param percepts: a tuple of four items: guess_counter, last_guess, in_place, in_colour

                     , where

                     guess_counter - is an integer indicating how many guesses have been made, starting with 0 for
                                     initial guess;

                     last_guess - is a num_rows x num_cols structure with the copy of the previous guess

                     in_place - is the number of character in the last guess of correct colour and position

                     in_colour - is the number of characters in the last guess of correct colour but not in the
                                 correct position

            :return: list of chars - a list of code_length chars constituting the next guess
            """

      # Unpack the percepts tuple
      guess_counter, last_guess, in_place, in_colour = percepts


      # Print out the available colours
      sys.stdout.write("Valid colours: [")
      for c in self.colours:
         print_colour_char(c)
      sys.stdout.write("]\n\r")


      # Create a list of code_length size
      action = [0]*self.code_length


      # ...prompt the user for a guess
      sys.stdout.write("   ")
      # Show the blanks for where guesses are supposed to go
      for i in range(self.code_length):
         sys.stdout.write("_")
      # Back the cursor to the start of the row (blanks will stay on the screen)
      for i in range(self.code_length):
         sys.stdout.write("\b")
      sys.stdout.flush()

      # Get the input for each colour...
      i = 0
      while i < self.code_length+1:
         while True:
            c = readchar.readchar()
            if c=='\x03':
               # Ctrl-C exits the entire program
               sys.exit(-1)
            if c=='\x04':
               # Ctrl-D gives up on the current game
               sys.stdout.write("\n\r")
               sys.stdout.write("\r")
               return None
            elif c=='\x7f':
               # Backspace removes last character written
               if i>0:
                  sys.stdout.write("\b_\b")
                  sys.stdout.flush()
                  i -= 1
               i -= 1
               break

            elif (c=='\r' or c=='\n') and i==self.code_length:
               break

            c = str(c)
            c = c.upper()
            print

            try:
               if c in self.colours:
                  action[i] = c
                  print_colour_char(c)
                  break
            except:
               pass

         i += 1

      sys.stdout.write("\r\n")
      sys.stdout.flush()

      # Return the board guess as action
      return action
