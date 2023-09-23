__author__ = "Guangjie Guo"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "guo_guangjie@163.com"

import numpy as np
import random
from mastermind import evaluate_guess


def gen_best_guess_partially(candidates, n=50):

   #randomly generate n guesses
   random_elements = random.sample(candidates, n)

   # generate best guess
   scores = []
   for i in range(n):
      counts = {}
      for j in range(len(candidates)):
         my_tuple = tuple(evaluate_guess(random_elements[i],candidates[j]))
         if my_tuple in counts.keys():
            counts[my_tuple] += 1
         else:
            counts[my_tuple] = 1
      np_counts = np.array(list(counts.values()))
      score = np.sum(np_counts * np_counts) / len(candidates)
      scores.append(score)
   min_score = min(scores)
   index = scores.index(min_score)
   best_guess = random_elements[index]

   return best_guess

def gen_best_guess_miniavrg(candidates):

   n = len(candidates)
   code_length = len(candidates[0])
   my_array = np.full((n, n, 2), 0)
   for i in range(n):
      for j in range(n):
         if i == j:
            my_array[i,j] = [code_length, 0]
         if i < j:
            my_array[i, j] = evaluate_guess(candidates[i],candidates[j])
         if i > j:
            my_array[i, j] = my_array[j, i]

   scores = []
   for i in range(n):
      counts = {}
      for j in range(n):
         my_tuple = tuple(my_array[i, j])
         if my_tuple in counts.keys():
            counts[my_tuple] += 1
         else:
            counts[my_tuple] = 1
      np_counts = np.array(list(counts.values()))
      score = np.sum(np_counts * np_counts) / n
      scores.append(score)

   min_score = min(scores)
   index = scores.index(min_score)
   best_guess = candidates[index]

   return best_guess

def gen_corpus(colours, code_length):
   corpus = []
   numcolours = len(colours)
   for i in range(numcolours ** code_length):
      ele = [0] * code_length
      decimal_num = i
      k = 1
      while decimal_num > 0:
         remainder = decimal_num % numcolours
         ele[code_length - k] = remainder
         decimal_num //= numcolours
         k += 1
      ele_chars = []
      for j in range(code_length):
         ele_chars.append(colours[ele[j]])
      corpus.append(ele_chars)
   return corpus

def gen_first_guess(colours, code_length, n = 10):

   # generate corpus of all candidates
   corpus = gen_corpus(colours, code_length)

   # randomly choose 10 candidates
   candidates = []
   for i in range(n):
      candidates.append(np.random.choice(colours, size=(code_length)))

   # generate best guess
   scores = []
   for i in range(n):
      counts = {}
      for j in range(len(corpus)):
         my_tuple = tuple(evaluate_guess(candidates[i],corpus[j]))
         if my_tuple in counts.keys():
            counts[my_tuple] += 1
         else:
            counts[my_tuple] = 1
      np_counts = np.array(list(counts.values()))
      score = np.sum(np_counts * np_counts) / len(corpus)
      scores.append(score)
   min_score = min(scores)
   index = scores.index(min_score)
   best_guess = candidates[index]

   return best_guess

def find_candidates(last_guess, in_place, in_colour, pre_candidates):
   candidates = []
   for i in range(len(pre_candidates)):
      in_place1, in_colour1 = evaluate_guess(last_guess, pre_candidates[i])
      if in_place1 == in_place and in_colour1 == in_colour:
         candidates.append(pre_candidates[i])
   return candidates


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

      # save last candidates
      self.pre_candidates = []

      # initiate corpus
      self.corpus = gen_corpus(colours, code_length)

      # initiate first guess
      self.first_guess = gen_first_guess(colours, code_length, n = 20)

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

      # selecting from the candidates by using miniavrg method
      if guess_counter == 0:
         action = self.first_guess

      elif guess_counter == 1:
         candidates = find_candidates(last_guess, in_place, in_colour, self.corpus)
         if len(candidates) > 1000:
            action = gen_best_guess_partially(candidates, n=100)
         else:
            action = gen_best_guess_miniavrg(candidates)
         self.pre_candidates = candidates

      else:
         candidates = find_candidates(last_guess, in_place, in_colour, self.pre_candidates)
         if len(candidates) > 1000:
            action = gen_best_guess_partially(candidates, n=100)
         else:
            action = gen_best_guess_miniavrg(candidates)
         self.pre_candidates = candidates

      # Return a guess
      return action
