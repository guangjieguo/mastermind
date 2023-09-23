__author__ = "Lech Szymanski"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "lech.szymanski@otago.ac.nz"

import numpy as np

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

   def __init__(self, code_length,  colours, num_guesses):
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

      # Extract different parts of percepts.
      guess_counter, last_guess, in_place, in_colour = percepts

      # Make a random choice of colour character over a code_length numpy array
      action = np.random.choice(self.colours, size=(self.code_length))

      # Return a random guess
      return action
