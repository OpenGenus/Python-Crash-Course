from random import randint

print('Welcome to the ROCK, PAPER, SCISSORS game \n Choose a number from the below')

replayflag=True

while replayflag==True:
    numbercheckflag=False
    
    while numbercheckflag==False:
        
        try:
            user_no=int(input(" 0. rock \n 1. paper \n 2. scissors \n"))
            if(user_no<0 or user_no>2):
                print(' Pick again')
            else:
                numbercheckflag=True
        except:
            print('pick again')
           
                
            
    options=['Rock', 'Paper', 'Scissors']
    
    
    user_choice=options[user_no]
    
    
    computer_no=randint(0,3)
        
        
    if ( user_no==computer_no):
        print(" IT'S A DRAW ")
            
    elif ((user_no==1 and computer_no==3) or (user_no==2 and computer_no==1) or (user_no==3 and computer_no==2)):
        print(" USER WINS ")
    else:
        print(" COMPUTER WINS ")
    
    
    rep_choice=input(' DO you wanna play again?\n Press Y or N\n')
    replayflag= True if(rep_choice=='Y') else False
    
    
