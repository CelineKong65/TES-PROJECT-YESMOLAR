Most important thing:
**Install the clipspy to ensure that the code (from clips import Environment) can be used**
1) Open VS Code
2) In the Terminal -> New Terminal
3) Run:
   pip install clipspy
4) After run, you can run the example.py to test your clipspy is download successful or not. If yes, print("You're Smart!!!). If no, try to solve it hahahaahahaah.

First Version 
1) Page 1
- Main page for the user interface:
- Display "WELCOME!" and then below have button with word "Start Testing".
- After click the "Start Testing" button , it will jump to Page 2.
2) Page 2
- This page is for TEST 1 (MCQ memory test). 
- In this page, user need to answer 3 question by provide a short article (this article will be shown only 10 seconds). 
- Once user view the article and answer the mcq question, below have a "Done" button. 
- After click the "Done" button, the system will save the result for this user and it will go to Page 3.
3) Page 3
- This is page for TEST 2 (user need to memorize image on a set of cards then fold the card for them to find match cards). 
4) Page 4
- After done this two test, it will have a overall result (TEST 1 and  TEST 2) and display the result and recommendations to the user.

**TEST 1 & TEST 2 （还要改的）**
MCQ - 对完3题是good, 对2题是moderate, else是poor
Card Matching - 总共6个水果，少过等于6次是good, 少过等于9次是good, else是poor
Final result
- poor + poor = high risk
- good + good = low risk
- any moderate = moderate
- 假如有poor + good = inconclusive result
