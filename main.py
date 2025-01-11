import random
import pygame

def open_file(file_name):
    file = open(file_name)
    words = file.readlines()
    file.close()
    return [word.upper().strip() for word in words]

d = open_file("wordl.txt")
answer = random.choice(d)
print(answer)

WIDTH = 500
HEIGHT = 600
MARGIN = 10
TD_MARGIN = 100
LR_MARGIN = 100

GREY = (70, 70, 80)
GREEN = (6, 214, 160)
YELLOW = (255, 209, 102)

INPUT = ""
GUESSES = []
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
UNGUESSED = ALPHABET
GAME_OVER = False
MESSAGE = ""

pygame.init()
pygame.font.init()
pygame.display.set_caption("WORDL")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

S_SIZE = (WIDTH - 4 * MARGIN - 2 * LR_MARGIN) // 5
FONT = pygame.font.SysFont("free sans bold", S_SIZE)
FONT_SMALL = pygame.font.SysFont("free sans bold", S_SIZE // 2)

animating = True
while animating:
    screen.fill("White")

    y = TD_MARGIN
    for i in range(6):
        x = LR_MARGIN
        for j in range(5):
            square = pygame.Rect(x, y, S_SIZE, S_SIZE)
            pygame.draw.rect(screen, GREY, square, width=2, border_radius=5)

            if i < len(GUESSES):
                color = GREY
                if GUESSES[i][j] == answer[j]:
                    color = GREEN
                elif GUESSES[i][j] in answer:
                    color = YELLOW
                pygame.draw.rect(screen, color, square, border_radius=5)
                letter = FONT.render(GUESSES[i][j], False, (255, 255, 255))
                surface = letter.get_rect(center=(x + S_SIZE // 2, y + S_SIZE // 2))
                screen.blit(letter, surface)

            x += S_SIZE + MARGIN
        y += S_SIZE + MARGIN

    # Display win/loss message
    if GAME_OVER:
        message_text = FONT.render(MESSAGE, False, (0, 0, 0))
        message_surface = message_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        screen.blit(message_text, message_surface)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            animating = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                animating = False
            elif event.key == pygame.K_RETURN:
                if len(INPUT) == 5 and not GAME_OVER:
                    GUESSES.append(INPUT)
                    if INPUT == answer:
                        GAME_OVER = True
                        MESSAGE = "WON!"
                    elif len(GUESSES) == 6:
                        GAME_OVER = True
                        MESSAGE = "TRY AGAIN! ANSWER: " + answer
                    INPUT = ""
            elif event.key == pygame.K_BACKSPACE and len(INPUT) > 0:
                INPUT = INPUT[:-1]
            elif len(INPUT) < 5 and not GAME_OVER and event.unicode.upper() in ALPHABET:
                INPUT = INPUT + event.unicode.upper()
                print(INPUT)

pygame.quit()
