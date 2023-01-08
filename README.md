# MineSweeperAI

## MineSweeper AI made in python
Author : Loïc Pottier  
<br/>
# Notes about the different parts:



1. > ## Simples checks
   
    Loop on the whole board and see if a square match one of thoses situations: 
    * the number of unknown squares around is equal to the bomb amount --> we can flag all of them  
    * the number of flagged squares around is equal to the bomb amount --> we can click on all of them  
    <br>
    Thoses are the simple squares, they can't cause a loose as they are 100% sure  
    The ONLY way of loosing due to a basic action from this part is to have a incorrect pattern  
    If the game flag a non-bomb square, the next basic action will probably fail, but no due to an error from this part  
    <br>
    ## TODO : 

<br>
<br>

1. > ## Pattern recognition  
    Search in the whole board for pattern that are located in patter.py  
    if it find a pattern, return either the bomb or safe position  
    <br>
    ## TODO :  
    * Some pattern are much more common than others, need to run a lot of games with differents bombs density and re-arrange the pattern list so the patterRecognition algorithm can find them faster  
    * Need to add another character to pattern, this one would mean "anything but a flag or border" so patterns could be more efficient,   
    need to check if there is unknown case on the pattern because new char would not need an unknown case to work, it would just find patterns on already discovered parts  
<br>
<br>

1. > ## Pattern reduction  
    Do almost the same as the previous part with a little difference  
    It will reduce numbers with a flag around by the number of flags, when all numbers are reduced, every flag is deleted  
    Then it just put the reduced board in the pattern reducer and see if it can find matching patterns  
    <br>
    ## TODO :  

<br>
<br>

4. > ## Probability clicks  
    This part makes probabilities for every square with unknown square around  
    It will just create a new empty board filled with 0, and for every square found do :  
    * get the number of unknown square around  
    * divide it by the number on the square - number of flags around  
    Once all probas are done, we just do the average for each square, and we have the best chance to not loose on the next click  
    <br>
    ## TODO :  

<br>
<br>

5. > ## Random click  
    In a very uncommon case, the last unknown squares are hidden behind a wall of flags  
    In this case, we have to gamble because we can't do probabilities on thoses as they have no numbers around them  
    <br>
    ## TODO :  

<br>
<br>

# TODO GLOBAL  

* remove from the board the parts that are already fully discovered --> efficacity boost  

<br>
<br>

# NOTES  

AI can be disabled by setting the variable AI_ON at the start of the AI PART to False (to play without help :))