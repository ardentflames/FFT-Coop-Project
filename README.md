This is just a small project I worked on during my third Co-op Work Term. 
It uses numpy and matplotlib to simulate an FFT, without using any prebuilt external FFT modules. 
Please drag the wav. file you wish to analyze into the SAME FOLDER as this program

MAKE SURE YOU HAVE NUMPY, MATPLOTLIB, AND SCIPY INSTALLED IN YOUR PYTHON ENVIRONMENT, or wherever you run this program from.

*Note* For smaller intervals (less than 16k), and/or larger wav. files, you might have dozens of plots/graphs that occur.
Close each graph to get the program to calculate the next interval.

Uses a matrix representation of the cooley tukey algorithm to perform the FFT.

DO NOT USE INTERVALS LARGER THAN 32K - WILL CRASH YOUR COMPUTER.

(I know it's reinventing the wheel but it's a project I could have done in the time I had)
