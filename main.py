import random
import pygame

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
def drawMenu():
    SCREEN.fill(BLACK)
    text = FONT.render("Welcome to pong! Use the up and down arrows to move your paddle.",False, WHITE)
    textBlock = text.get_rect(center=(WIDTH/2,HEIGHT/2 - 20))
    SCREEN.blit(text,textBlock)
    text = FONT.render("First to 10 points wins. Click anywhere to get started.", False, WHITE)
    textBlock = text.get_rect(center=(WIDTH/2,HEIGHT/2))
    SCREEN.blit(text,textBlock)
    pygame.display.update()

#Draw location of all objects on screen
def drawScreen(player1, player2, ball, player1Score, player2Score):
    SCREEN.fill(BLACK)
    SCREEN.blit(PADDLE_IMAGE, (player1.x, player1.y))
    SCREEN.blit(PADDLE_IMAGE, (player2.x, player2.y))
    SCREEN.blit(BALL_IMAGE, (ball.x, ball.y))
    text = FONT.render(str(player1Score),False, WHITE)
    textBlock = text.get_rect(center=(WIDTH/4,HEIGHT/4))
    SCREEN.blit(text,textBlock)
    text = FONT.render(str(player2Score),False, WHITE)
    textBlock = text.get_rect(center=((WIDTH/4) * 3,HEIGHT/4))
    SCREEN.blit(text,textBlock)
    pygame.display.update()

def main():

    #Game Menu w/Instructions
    runMenu = True
    clock = pygame.time.Clock()

    while runMenu:

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                runMenu = False

        drawMenu()

    #Game initialisation
    runGame = True
    player1 = pygame.Rect(0,HEIGHT/2 -50, 15,100)
    player2 = pygame.Rect(WIDTH-15, HEIGHT/2 -50, 15,100)
    ball = pygame.Rect(WIDTH/2 - 20, HEIGHT/2 - 20, 40, 40)
    ballVelocity = [-10,0]
    player1Score = 0
    player2Score = 0

    hitUpperBoundary = False
    hitLowerBoundary = True

    while runGame and player1Score < 10 and player2Score < 10:

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runGame = False
        
        #Player1 Paddle Movement
        keyInput = pygame.key.get_pressed()
        if keyInput[pygame.K_UP]:
            if player1.y > 0:
                        player1.y -= 10
        if keyInput[pygame.K_DOWN]:
            if player1.y < HEIGHT-100:
                        player1.y += 10

        #Player2 Paddle Movement
        if not hitUpperBoundary:
            player2.y -= 10
            if player2.y <= 0:
                hitUpperBoundary = True
                hitLowerBoundary = False
        elif not hitLowerBoundary:
            player2.y += 10
            if player2.y >= HEIGHT-100:
                hitUpperBoundary = False
                hitLowerBoundary = True

        #Ball Movement
        ball.x += ballVelocity[0]
        ball.y += ballVelocity[1]
        if ball.colliderect(player1):
            ballVelocity[0] = 10
            ballVelocity[1] = random.randint(-5,5)
        elif ball.colliderect(player2):
            ballVelocity[0] = -10
            ballVelocity[1] = random.randint(-5,5)
        elif ball.y >= HEIGHT-40:
            ballVelocity[1] = -ballVelocity[1]
        elif ball.y <=0:
            ballVelocity[1] = -ballVelocity[1]
        elif ball.x <=0:
            ball.x = WIDTH/2 - 20
            ball.y = HEIGHT/2 - 20
            ballVelocity = [10,0]
            player2Score += 1
        elif ball.x >= WIDTH-40:
            ball.x = WIDTH/2 - 20
            ball.y = HEIGHT/2 - 20
            ballVelocity = [-10,0]
            player1Score += 1
        
        drawScreen(player1, player2, ball, player1Score, player2Score)
        

    pygame.quit()


if __name__ == "__main__":
    main()