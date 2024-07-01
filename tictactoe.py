from collections import deque
import random
import numpy as np
import copy

playboard = np.array([['-','-','-'],['-','-','-'],['-','-','-']])
filled = 0
result = ''
level = 0

best = deque()

def print_board(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            print(board[i][j],end=' ')
        print()

def checkWin(person):
    if(playboard[0][0]==playboard[1][1]==playboard[2][2] and playboard[0][0]!='-'):
        return 'win' if playboard[0][0] == person else 'loss'
    
    if(playboard[0][2]==playboard[1][1]==playboard[2][0] and playboard[0][2]!='-'):
        return 'win' if playboard[0][2] == person else 'loss'

    for i in range(len(playboard)):
        if(all(x==playboard[i][0] and x!='-' for x in playboard[i])):
            return 'win' if playboard[i][0]==person else 'loss'
    
    for i in range(len(playboard)):
        column = playboard[:,i]
        if(all(x==column[0] and x!='-' for x in column)):
            return 'win' if column[0]==person else 'loss'
        
    return 'proceed'

def find_score(person):
    global playboard
    count = 0
    pc = 'O' if person=='X' else 'X'

    left_diag = [playboard[0][0], playboard[1][1], playboard[2][2]]
    right_diag = [playboard[0][2], playboard[1][1], playboard[2][0]]

    for i in playboard:
        if pc not in i and person in i:
            count+=1

    for i in range(len(playboard)):
        column = playboard[:,i]

        if pc not in column and person in column:
            count+=1
    
    if person in left_diag and pc not in left_diag:
        count+=1
    
    if person in right_diag and pc not in right_diag:
        count+=1
    
    return count

def user_score(person):
    pc = 'O' if person=='X' else 'X'
    return find_score(person) - find_score(pc)


def check_space(arr):
    if (arr[0] == arr[1] and arr[0]!='-') and arr[2]=='-':
        return 2
    elif (arr[0] == arr[2] and arr[0]!='-') and arr[1]=='-':
        return 1
    elif (arr[1] == arr[2] and arr[1]!='-') and arr[0]=='-':
        return 0
    else:
        return None

def check_empty():
    left_diag = [playboard[0][0], playboard[1][1], playboard[2][2]]
    right_diag = [playboard[0][2], playboard[1][1], playboard[2][0]]

    for i in range(len(playboard)):
        if check_space(playboard[i]) is not None:
            return (i,check_space(playboard[i]))
        
    for i in range(len(playboard)):
        col = playboard[:,i]
        if check_space(col) is not None:
            return (check_space(col),i)
        
    if check_space(left_diag) is not None:
        return (check_space(left_diag),check_space(left_diag))
    
    if check_space(right_diag) is not None:
        return (check_space(right_diag),2-check_space(right_diag))
    
    return None

def tictactoe_game(n, start, person):
    global level, result, playboard, filled, best
    pc = 'O' if person=='X' else 'X'
    if start=='N':
        filled+=1
        row = random.randint(0,2)
        col = random.randint(0,2)
        playboard[row][col] = 'X' if person=='O' else 'O'
        print("PC's turn:")
        print_board(playboard)
        print()

    while level<n and result not in ('win','loss') and filled < 9: 
        max_score = float('-inf')
        print("Player's turn:")
        pos = check_empty()
        if pos is not None:
            row, col = pos
            playboard[row][col] = person
            print_board(playboard)
            print()
        else:
            for i in range(len(playboard)):
                for j in range(len(playboard)):
                    if playboard[i][j] not in ('X','O'):
                        playboard[i][j] = person
                        score = user_score(person)
                        if score > max_score:
                            max_score = score
                            best.clear()
                            best.append(copy.deepcopy(playboard))
                        elif score == max_score:
                            best.append(copy.deepcopy(playboard))
                        playboard[i][j] = '-'
            
            if best:
                playboard = random.choice(best)
                filled += 1
            
            best.clear()
            print_board(playboard)
            print()

        if checkWin(person)=='win':
            print('You win!')
            print_board(playboard)
            print()
            return
        elif checkWin(person) == 'loss':
            print('You lose!')
            print_board(playboard)
            print()
            return

        if filled < 9:
            print("PC's turn:")
            row, col = random.choice([(i, j) for i in range(3) for j in range(3) if playboard[i][j] == '-'])
            playboard[row][col] = pc
            filled += 1
            result = checkWin(person)
            if result == 'loss':
                print('You lose!')
                print_board(playboard)
                return
            elif result=='win':
                print('You win!')
                print_board(playboard)
                return

        print_board(playboard)
        print()
        level+=1
    
    if level==n:
        print('Level = ',n,':')
        print_board(playboard)
        print()

    if filled==9 and result not in ('win','loss'):
        print('Draw!')
        print_board(playboard)
        return

person = input('Which would you like to choose? X or O: ')
pc = 'O'
if person=='X':
    pc = 'O'
else:
    pc = 'X'

person_start = input('Would you like to start the game? (Y/N) ')
n = int(input('Enter the depth upto which the tree must be constructed: '))
tictactoe_game(n,person_start,person)