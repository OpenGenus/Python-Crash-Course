from enum import IntEnum
from random import randint

class Action(IntEnum):
    Rock=1 
    Paper=2 
    Scissors=3 

def get_action(number):
    
    action=Action(number)
    return action.name
    
replayflag=True
while replayflag==True:
    
    user_no=int(input('Pick an action(number)\n 1.Rock \n 2.Paper \n 3.Scissors\n'))
    try:
        numcheck=False
        while numcheck==False:
            if(user_no<1 or user_no>3):
                print('pick again')
            else:
                numcheck=True
    except:
        print('pick again')

    
    computer_no=randint(1,3)
    
    print(computer_no)
    
    user_pick=get_action(user_no)
    computer_pick=get_action(computer_no)


    print(f"The user picked {user_pick} and the computer picked {computer_pick}")
    
    if ( user_pick==computer_pick):
        print(" IT'S A DRAW ")
            
    elif ((user_pick==1 and computer_pick==3) or (user_pick==2 and computer_pick==1) or (user_pick==3 and computer_pick==2)):
        print(" USER WINS ")
    else:
        print(" COMPUTER WINS ")
        
    rep=input('Want to play again? Y/N')
    replayflag= True if rep=='Y' else False


