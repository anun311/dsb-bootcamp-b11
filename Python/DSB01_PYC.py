#!/usr/bin/env python
# coding: utf-8

# In[135]:


import random 

win, loss, tie = 0, 0, 0
choices = [1, 2, 3, 9]
session_ = True

while session_ == True:
    player_move = input("Your move: [1] Rock, [2] Paper, [3] Scissors, [9] Exit:")
    player_move = int(player_move)
    
    if player_move not in choices:
        print("Please select aviliable option")
    else:
        if player_move == 9:
            # บอก บ๊าย บาย พร้อมบอกคะแนน และจำนวนรอบการเล่น
            print("Bye bye 👋")
            print("You play:", (win+loss+tie), "Rounds")
            print(f"Win: {win} Loss: {loss} Tie: {tie} ")
            session_ = False
        else:
        
            data_move = {1: "Rock", 2: "Paper", 3: "Scissors", 9:"Quit"}
            player_choice = data_move[player_move] 
        
            my_list = ["Rock", "Paper", "Scissors"]
            random_choice = random.choice(my_list)
        
            # if loop เฉพาะ tie กับ loss นอกนั้น win
            if (player_choice == "" and random_choice == ""):
                None
            elif (player_choice == random_choice):
                txt = "- Tie 😁 -"
                tie += 1
            elif (player_choice == 'Rock' and random_choice == 'Paper'):
                txt = "- You Loss 😭 -"
                loss += 1
            elif (player_choice == 'Paper' and random_choice == 'Scissors'):
                txt = "- You Loss 😭 -"
                loss += 1
            elif (player_choice == 'Scissors' and random_choice == 'Rock'):
                txt = "- You Loss 😭 -"
                loss += 1
            else:
                txt = "- You Win 😎 -"
                win += 1
                
            print(f"Rounds: {win+loss+tie}")
            print(f"Computer Move: {random_choice} :: Player Move: {player_choice}")
            print(f"Result: {txt}")
            print(f"Win: {win}  Loss: {loss}  Tie: {tie} ")
            print("")


# In[ ]:




