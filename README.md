# MineSweeperAI

## MineSweeper AI made in python

Author : Loïc Pottier  

<br>

# How to play  

* Install Pillow and TKinter
* Launch main.py from the minesweeper directory
* Play / watch the AI  


AI can be turned of by setting the AI_ON variable to False (at the start of the AI part)

<br>

# Notes about the different parts:

1. > ## Simples checks  

    Loop on the whole board and see if a square match one of thoses situations: 
    * the number of unknown squares around is equal to the bomb amount --> flag all of them  
    * the number of flagged squares around is equal to the bomb amount --> click on all of them  
    
    <br>

    Thoses are the simple cases, they can't cause a loose as they are 100% sure  
    The ONLY way of loosing due to a basic action from this part is to have a incorrect pattern  
    If the game flag a non-bomb square, the next basic action will probably fail, but no due to an error from this part  

    ## TODO : 

<br>
<br>

2. > ## Pattern recognition  

    Search in the whole board for pattern that are located in patter.py  
    if it find a pattern, return either the bomb or safe position  

    ## TODO :  

    * Some pattern are much more common than others, need to run a lot of games with differents bombs density and re-arrange the pattern list so the patter recognition algorithm can find them faster  
    * Need to add another character to pattern, this one would mean "anything but a flag or border" so patterns could be more efficient,   
    need to check if there is AT LEAST one unknown case on the pattern because new char would not need an unknown case to work, it would just find patterns on already discovered parts  

<br>
<br>

3. > ## Pattern reduction 

    It reduces numbers with a flag around by the number of flags, when all numbers are reduced, every flags are deleted  
    Then it just put the reduced board in the pattern finder and search for matching patterns  

    ## TODO :  

<br>
<br>

4. > ## Probability clicks  

    This part makes probabilities for every square with unknown square around  
    It will just create a new empty board filled with 0, and for every square with an unknown sqare around :  
    * get the number of unknown square around  
    * divide it by the number on the square - number of flags around 
    * append the number to all quares around in the new board

    Once all probabilities lists are done, we just do the average of each list and we can search the new board for the best probability  

    ## TODO :  

<br>
<br>

5. > ## Random click  

    In a very uncommon case, the last unknown squares are hidden behind a wall of flags  
    In this case, we have to gamble because we can't do probabilities on thoses as they have no numbers around them  

    ## TODO :  

<br>
<br>

# TODO GLOBAL  

* the ai struggle a lot on big boards as it have to browse all of the sqares for each action,  
  removing from the board the parts that are already fully discovered/unknown could improve a lot its efficacity  

<br>
<br>

# NOTES  

AI can be disabled by setting the variable AI_ON at the start of the AI PART to False (to play without help :))  

There are a lot of other parts to add :  
*  DONE function to remove useless lines from the board, and add them back when they are needed.
* function that count remaining mines and look for a 100% safe place, can be used on the end of a game
* high complexity pattern
* ...
