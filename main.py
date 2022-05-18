import random
import pygame
import sys

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 1000,600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
BLACK = (000,000,000)
WHITE = (255,255,255)
FONT = pygame.font.SysFont("Verdana",20)
FPS = 60

PADDLE_IMAGE = pygame.image.load("paddle.png")
BALL_IMAGE = pygame.image.load("ball.png")

#Display instructions in text format.
def drawMenu(singlePlayerText,singlePlayerRect, multiPlayerText, multiPlayerRect):
    SCREEN.fill(BLACK)
    text = FONT.render("Welcome to pong! Use W, S and the up and down arrows to move your paddle.",False, WHITE)
    textBlock = text.get_rect(center=(WIDTH/2,HEIGHT/2 - 20))
    SCREEN.blit(text,textBlock)
    text = FONT.render("First to 10 points wins. Click to get started.", False, WHITE)
    textBlock = text.get_rect(center=(WIDTH/2,HEIGHT/2))
    SCREEN.blit(text,textBlock)
    SCREEN.blit(singlePlayerText,singlePlayerRect)
    SCREEN.blit(multiPlayerText,multiPlayerRect)
    pygame.display.update()

#Draw location of all objects on screen
def drawScreen(player1, player2, ball, player1Score, player2Score):
    SCREEN.fill(BLACK)
    SCREEN.blit(PADDLE_IMAGE, (player1.x, player1.y))
    SCREEN.blit(PADDLE_IMAGE, (player2.x, player2.y))
    SCREEN.blit(BALL_IMAGE, (ball.x, ball.y))
    text = FONT.render("Player 1: "+str(player1Score),False, WHITE)
    textBlock = text.get_rect(center=(WIDTH/4,HEIGHT/4))
    SCREEN.blit(text,textBlock)
    text = FONT.render("Player 2: "+str(player2Score),False, WHITE)
    textBlock = text.get_rect(center=((WIDTH/4) * 3,HEIGHT/4))
    SCREEN.blit(text,textBlock)
    pygame.display.update()

def drawWinner(player1Score, player2Score):
    SCREEN.fill(BLACK)
    if player1Score > player2Score:
        text = FONT.render("Player 1 Wins!", False, WHITE)
    else:
        text = FONT.render("Player 2 Wins!", False, WHITE)
    textBlock = text.get_rect(center=(WIDTH/2,HEIGHT/2))
    SCREEN.blit(text,textBlock)
    pygame.display.update()

def main():

    #Game Menu w/Instructions
    runMenu = True
    clock = pygame.time.Clock()
    singlePlayer = False
    multiPlayer = False
    singlePlayerText = FONT.render("Single Player",False, WHITE)
    singlePlayerRect = singlePlayerText.get_rect(center=(WIDTH/4,HEIGHT/4*3))
    multiPlayerText = FONT.render("Multi Player",False, WHITE)
    multiPlayerRect = singlePlayerText.get_rect(center=(WIDTH/4 *3,HEIGHT/4*3))

    while runMenu:

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and singlePlayerRect.collidepoint(pygame.mouse.get_pos()):
                runMenu = False
                singlePlayer=True
            elif event.type == pygame.MOUSEBUTTONDOWN and multiPlayerRect.collidepoint(pygame.mouse.get_pos()):
                runMenu = False
                multiPlayer=True

        drawMenu(singlePlayerText, singlePlayerRect, multiPlayerText, multiPlayerRect)

    #Game initialisation
    player1 = pygame.Rect(0,HEIGHT/2 -50, 15,100)
    player2 = pygame.Rect(WIDTH-15, HEIGHT/2 -50, 15,100)
    ball = pygame.Rect(WIDTH/2 - 20, HEIGHT/2 - 20, 40, 40)
    ballVelocity = [-10,0]
    player1Score = 0
    player2Score = 0

    hitUpperBoundary = False
    hitLowerBoundary = True

    while player1Score < 10 and player2Score < 10:

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        #Player1 Paddle Movement
        keyInput = pygame.key.get_pressed()
        if keyInput[pygame.K_UP]:
            if player2.y > 0:
                        player2.y -= 10
        if keyInput[pygame.K_DOWN]:
            if player2.y < HEIGHT-100:
                        player2.y += 10

        #Player2 Paddle Movement
        if singlePlayer:
            if not hitUpperBoundary:
                player1.y -= 10
                if player1.y <= 0:
                    hitUpperBoundary = True
                    hitLowerBoundary = False
            elif not hitLowerBoundary:
                player1.y += 10
                if player1.y >= HEIGHT-100:
                    hitUpperBoundary = False
                    hitLowerBoundary = True
        if multiPlayer:
            if keyInput[pygame.K_w]:
                if player1.y > 0:
                    player1.y -= 10
            if keyInput[pygame.K_s]:
                if player1.y < HEIGHT-100:
                    player1.y += 10

        #Ball Movement
        ball.x += ballVelocity[0]
        ball.y += ballVelocity[1]
        if ball.colliderect(player1):
            ballVelocity[0] = 10
            ballVelocity[1] = random.randint(-5,5)
        if ball.colliderect(player2):
            ballVelocity[0] = -10
            ballVelocity[1] = random.randint(-5,5)
        if ball.y >= HEIGHT-40:
            ballVelocity[1] = -ballVelocity[1]
        if ball.y <=0:
            ballVelocity[1] = -ballVelocity[1]
        if ball.x <=0:
            ball.x = WIDTH/2 - 20
            ball.y = HEIGHT/2 - 20
            ballVelocity = [10,0]
            player2Score += 1
        if ball.x >= WIDTH-40:
            ball.x = WIDTH/2 - 20
            ball.y = HEIGHT/2 - 20
            ballVelocity = [-10,0]
            player1Score += 1
        
        drawScreen(player1, player2, ball, player1Score, player2Score)
    
    while True:

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        drawWinner(player1Score,player2Score)


if __name__ == "__main__":
    main()