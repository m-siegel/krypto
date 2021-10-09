# Krypto Puzzle Game

Krypto is an arithmetic puzzle game where players use five distinct random
numbers between 1 and 25, inclusive, to form arithmetic expressions that
evaluate to a sixth distinct random number between 1 and 25.

This program provides pseudorandom numbers and evaluates the expressions that
the user inputs. When the user enters 'quit', the program prints each correct
solution that the user entered.

## Running

Download krypto.py and run it from an IDE or shell using Python3.

## Pseudorandom number generator

I wrote this program for a class with restrictions on what Python tools
could be used. As a result, this program does not import other libraries,
including the random library and the time library.

This program uses its own pseudorandom number function instead of
random.randint(). It also uses a hard-coded int as the default seed instead 
of a more random seed like time.time().