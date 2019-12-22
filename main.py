import func_1
import func_2
import func_3
import func_4
'''
Our main function, it will ask you to tell us which function you want to use and the input
'''
def main():
    c=input("Welcome to the Homework 5 done by group 27\nPlease choose the funcion that you want to call\nPut the number of the fuction that you want to call (1 to 4)\n")
    elif c=="1":
        l=inputting()
        print(func_1.start(func_1.get_neighbours(l[0],l[1:len(l)])))
    elif c=="2":
        l=inputting()
        print(func_2.start(func_2.get_smatest_neighbours(l[0],l[1:len(l)])))
    elif c=="3":
        l=inputting()
        print(func_3.start(func_3.creategraph(),l[0],l[1:len(l)]))
    elif c=="4":
        l=inputting()
        print(func_4.start(func_4.creategraph(),l[0],l[1:len(l)]))
    else:
        print("Please follow the rules!")
        return main()
        
def inputting():
    h=int(input("Starting point? " )) #Starting point input
    p=list(map(int,input("List of points? " ).split())) #the whole points that you want to check
    return [h]+p

main()