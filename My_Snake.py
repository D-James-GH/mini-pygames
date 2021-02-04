import pygame
import time
import random

pygame.init()

#section below is the basic display window set up
display_width = 600 
display_height = 400
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Snake')

        # Defining colours
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,155,0)
blue = (0,0,155)

        # Importing the pygame clock so that FPS can be established
clock = pygame.time.Clock()
FPS =10


        # Size (width and diameter in pixels) of the snakes segments
block_size = 20
movement_size = 2
prize_size = 40

        # Importing a font from pygame fonts, none = default font, 25 is the size.
smallfont = pygame.font.SysFont("comicsansms", 10)
medfont = pygame.font.SysFont("comicsansms", 25)
largefont = pygame.font.SysFont("comicsansms", 50)




   

def pause():
    paused = True

    message_to_screen("Paused", black, -100, "large")
    message_to_screen("Press C to continue or Q to quit", black)
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        #gameDisplay.fill(white)
        clock.tick(10)


def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                    
        gameDisplay.fill(white)
        message_to_screen("Welcome to Snake", green, -80,"large")
        message_to_screen("press C to play and Q to quit", black, 0, "medium")
        pygame.display.update()
        clock.tick(15)
        

def snake(block_size, snakelist):
    for XnY in snakelist:
        pygame.draw.rect(gameDisplay, green, [XnY[0],XnY[1],block_size,block_size]) # Draw snake

def text_objects(text,colour,size):
    if size == "small":
        textSurface = smallfont.render(text,True,colour)
    elif size == "medium":
        textSurface = medfont.render(text,True,colour)
    elif size == "large":
        textSurface = largefont.render(text,True,colour)
    return textSurface, textSurface.get_rect()
    

        # Function for any message to the screen. Can be called with (Message to display, Colour of the message)
def message_to_screen(msg,colour, y_displace = 0, size = "small"):
    textSurf, textRect = text_objects(msg,colour,size)   
    textRect.center = (display_width / 2),(display_height /2)+y_displace
    gameDisplay.blit(textSurf, textRect)

def scoreText(num,num2):
    
    Stext = smallfont.render("Score: " + str(num)+"  "+ "Highscore: "+str(num2), True, black)
    gameDisplay.blit(Stext, [0, 0])

        # Actual  game function. Everything that not hard coded.
def gameLoop():

    gameExit = False # Set to False until the user quits.
    gameOver = False # Set to False until the user loses.

    try:
        with open("highscore.txt","r") as f:
            highscore = int(f.read())
            print (highscore)
    except:
        with open("highscore.txt","w+") as f:
            highscore = 0
            f.write(str(highscore))
            print (highscore)

            # Starting position of the snake's head.
    lead_x = display_width/2 
    lead_y = display_height/2
            # Starting direction of the snakes head 
    lead_x_change = block_size
    lead_y_change = 0

    snakeList = [(lead_x-block_size,lead_y),(lead_x,lead_y)] #(lead_x-20,lead_y),(lead_x-10,lead_y)
    snakeLength = 3
    direction = "right"
    

    score = 0
    
    randPrize_x = random.randrange(0, display_width-prize_size,block_size )
    randPrize_y = random.randrange(0, display_height-prize_size,block_size)
    
    randApple_x = random.randrange(0, display_width-block_size, block_size)
    randApple_y = random.randrange(0,display_height-block_size, block_size)

            # The main game while loop. This runs when the user is playing.
    while not gameExit:
        
                # While loop to define what happens when the user loses
        while gameOver:
            gameDisplay.fill(white)
            message_to_screen("Game over,", red, -50, "large")
            message_to_screen("Press C to play again or Q to quit.", black, 100)
            scoreText(score, highscore)
            
            if score > highscore:
                print('highscore reached')
                highscore = score
                with open("highscore.txt","w+") as f:
                    f.write(str(highscore))
             
            text1 = medfont.render("Highscore: " + str(highscore), True, black)
            text_rect1 = text1.get_rect(center=(display_width/2, display_height/2))
            gameDisplay.blit(text1, text_rect1)   
            
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True # In order to exit the game this
                        gameOver = False # gameOver while loop must be exited first
                    if event.key == pygame.K_c:
                        gameLoop() # If the user continues the 'if' fustatement will call the gameLoop function and reset the game.

                    
        # This is all of the event handling (user interaction)
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN: # event type is a key press
                if event.key == pygame.K_LEFT and direction != "right" : # The key press is found here
                    lead_x_change = -block_size 
                    lead_y_change = 0
                    direction = "left"
                    break
                elif event.key == pygame.K_RIGHT and direction != "left" :
                    lead_x_change = block_size
                    lead_y_change = 0
                    direction = "right"
                    break
                elif event.key == pygame.K_UP and direction != "down" :
                    lead_y_change = -block_size
                    lead_x_change = 0
                    direction = "up"
                    break
                elif event.key == pygame.K_DOWN and direction != "up":
                    lead_y_change = block_size
                    lead_x_change = 0
                    direction = "down"
                    break
                elif event.key == pygame.K_p:
                    pause()



   
            
        lead_y += lead_y_change # How the snake moves
        lead_x += lead_x_change

        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)
                
        # Every time something changes the display must be updated
        gameDisplay.fill(white)

        if score // 10 > 0 and score%10 == 0:
            pygame.draw.rect(gameDisplay, blue,[randPrize_x,randPrize_y, prize_size, prize_size])
            
            if lead_x + block_size > randPrize_x and lead_x < randPrize_x + prize_size:
                if lead_y + block_size > randPrize_y and lead_y <randPrize_y + prize_size:
                    score += 4
                      
        pygame.draw.rect(gameDisplay, red, [randApple_x, randApple_y, block_size, block_size])


                     # Setting the boundarys
        if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
            if lead_x >= display_width:
                lead_x =0 
            elif lead_x <0:
                lead_x = display_width - block_size
            elif lead_y >= display_height:
                lead_y = 0# - block_size
            elif lead_y<0:
                lead_y = display_height - block_size
        
        if len(snakeList) > snakeLength:
            del snakeList[0]

        for eachSegment in snakeList[:-1]: #snakeList[:-1] = everything up to the last one ie. the head
                if eachSegment == snakeHead:
                    gameOver = True
                    
        snake(block_size, snakeList) # Draw snake
        scoreText(score,highscore)
        pygame.display.update()

        if lead_x == randApple_x and lead_y == randApple_y:
            randApple_x = random.randrange(0, display_width-block_size, block_size)
            randApple_y = random.randrange(0,display_height-block_size, block_size)
            snakeLength += 1
            score += 1
        
        clock.tick(FPS) # Forces the game to run at the desired FPS, which in this the while loop will run 15 times a second
        
    pygame.quit()
    quit()

game_intro()
gameLoop()
