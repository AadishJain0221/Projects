board=[' 'for i in range(16)]

def grid3():
    print("   | 1 | 2 | 3 |")
    print("---|---|---|---|")
    for i in range(3):
        print(f" {i+1} | {board[i]} | {board[i+1]} | {board[i+2]} |")
        if i<2:
            print("---|---|---|---|")
            
def grid4():
    print("   | 1 | 2 | 3 | 4 |")
    print("---|---|---|---|---|")
    for i in range(4):
        print(f" {i+1} | {board[i]} | {board[i+1]} | {board[i+2]} | {board[i+3]} |")
        # if i<3:
        print("---|---|---|---|---|")
    
def chance3(players):
    while True:
        choice=int(input("Enter the position (1-9)"))-1
        if(choice>=0 and choce<9 and board[choice]==' '):
            board [choice]=players
    
def chance4(current_player):
    while True:
        choice=int (input("Enter the position (1-16):"))-1
        if(choice>=0 and choice<16 and board[choice]==' '):
            board[choice]=current_player
            break
        else:
            if(choice<0 or choice>15):
                print("Invalid Input!!!")
            else:
                print("Position Is Already Taken!!!")
        print("Please Enter Again ")
        
def winner4(player):
    win=[[0,1,2],[1,2,3],[4,5,6],[5,6,7],[8,9,10],[9,10,11],[12,13,14],[13,14,15],#rows
         [1,5,9],[4,8,12],[2,9,13],[2,6,10],[6,10,14],[3,7,11],[7,11,15],#columns
         [0,5,10],[1,6,11],[2,5,8],[3,6,9],[4,9,14],[5,10,15],[6,9,12],[7,10,13]]#diagonals

    for condition in win:
        if all(board[i]==player for i in condition):
            return True
    return False


