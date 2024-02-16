import Hall_Effect, LCD_timer


def main():
    x = input("Hall Effect Communication = 1, LCD = 2, Motors = 3, Game = 4")
    x = int(x)
    if x == 1:
        print(read_halleffects_once())
    if x == 2:
        start_count = 0
    
        y = input("Input Play Time 1:9: ")
    
        LCD_timer.initialize(y)
        
        
if __name__ == "__main__":
    main()
        
    