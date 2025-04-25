board3=[' ' for i in range(9)]

board4=[' 'for i in range(16)]
playing=["X","O","\u0394"]

def grid3():
    for i in range(9):
        print(f" {i+1 if board3[i]==' ' else board3[i]} ", end='|')
        if(i+1)%3==0 :
            print()
            print("---|---|---|")  
            
def grid4():
    for i in range(16):
        if(i<9):
            print(f" {i+1 if board4[i]==' ' else board4[i]}  ", end='|')
        else:
            if(board4[i]==' '):
                print(f" {i+1} ", end='|')
            else:
                print(f" {board4[i]}  ", end='|')
        if(i+1)%4==0:
            print()
            print("----|----|----|----|") 
            

    
def chance3(player):
    while True:
        try:
            choice=int(input(f"Player {player} enter your move (1-9)"))-1
            if board3[choice]==' ':
                board3[choice]=player
                break
            else:
                print("Position Is Already Taken!!!")
                
        except (ValueError, IndexError):
            print("Invalid Input , Enter Again")   
        
                
    
def chance4(player):
    while True:
        try:
            choice=int(input(f"Player {player} enter your move (1-16)"))-1
            if board4[choice]==' ':
                board4[choice]=player
                break
            else:
                print("Position Is Already Taken!!!")
                
        except (ValueError, IndexError):
            print("Invalid Input , Enter Again") 
        
def winner3(player):
    win=[[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]       
    
    for condition in win:
        if all(board3[i]==player for i in condition):
            return True
    return False
    

def winner4(player):
    win=[[0,1,2],[1,2,3],[4,5,6],[5,6,7],[8,9,10],[9,10,11],[12,13,14],[13,14,15],#rows
         [1,5,9],[4,8,12],[2,9,13],[2,6,10],[6,10,14],[3,7,11],[7,11,15],#columns
         [0,5,10],[1,6,11],[2,5,8],[3,6,9],[4,9,14],[5,10,15],[6,9,12],[7,10,13]]#diagonals

    for condition in win:
        if all(board4[i]==player for i in condition):
            return True
    return False

def draw3():
    return ' ' not in board3
def draw4():
    return ' ' not in board4

def play2():
    
    current='X'
    while True:
            grid3()
            chance3(current)
            if winner3(current):
                grid3()
                print(f"Congractulations!!!{current} is the winner ")
                break
            elif draw3():
                grid3()
                break
            current='O' if current=='X' else 'X'
            

                
def play3():
    
    current=playing[0]
    while True:
            grid4()
            chance4(current)
            if winner4(current):
                grid4()
                print(f"Congractulations!!!{current} is the winner ")
                break
            elif draw4():
                grid4()
                break
            # current='O' if current=='X' else 'X'
            if current==playing[0]:
                current=playing[1]
            elif current==playing[1]:
                current=playing[2]
            elif current==playing[2]:
                current=playing[0]
            else:
                print("Error Occured!!!")


num=int(input("Enter the number of players (2 or 3): "))               
if(num==2):
    play2()
elif(num==3):
    play3()
else:
    print("Invalid Input!!!")
    exit(0)   
            
