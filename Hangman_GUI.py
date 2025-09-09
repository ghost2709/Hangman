
import pygame
import string
import random
import asyncio
import platform

# Expanded wordlist with categories
wordlist = {
    'Actor': ['al pacino', 'tom hanks', 'meryl streep', 'leonardo dicaprio', 'angelina jolie'],
    'Fruit': ['apple', 'banana', 'cherry', 'orange', 'strawberry'],
    'Country': ['france', 'brazil', 'japan', 'australia', 'canada'],
    'Animal': ['elephant', 'tiger', 'dolphin', 'penguin', 'giraffe']
}

def choose_word(wordlist):
    category = random.choice(list(wordlist.keys()))
    return random.choice(wordlist[category]), category

def is_word_guessed(secret_word, letters_guessed):
    return all(letter in letters_guessed for letter in secret_word.replace(' ', ''))

def get_guessed_word(secret_word, letters_guessed):
    return ' '.join(letter.upper() if letter in letters_guessed else '_' for letter in secret_word)

def get_available_letters(letters_guessed):
    return ''.join(letter for letter in string.ascii_lowercase if letter not in letters_guessed)

# Pygame setup
def setup():
    global screen, font, large_font, small_font, secret_word, category, letters_guessed, warnings_left, guesses_left, game_over, message, restart_button, letter_buttons, hint_button
    pygame.init()
    screen = pygame.display.set_mode((1000, 700))
    pygame.display.set_caption("Hangman Game")
    
    # Multiple font sizes for better typography
    large_font = pygame.font.SysFont('arial', 48, bold=True)
    font = pygame.font.SysFont('arial', 32)
    small_font = pygame.font.SysFont('arial', 24)
    
    secret_word, category = choose_word(wordlist)
    letters_guessed = []
    warnings_left = 3
    guesses_left = 6
    game_over = False
    message = ""
    
    # Better positioned buttons
    restart_button = pygame.Rect(750, 600, 120, 50)
    hint_button = pygame.Rect(600, 600, 120, 50)
    
    # Improved letter button layout (2 rows)
    letter_buttons = {}
    letters = string.ascii_uppercase
    # First row: A-M
    x_start, y_start = 50, 450
    for i, letter in enumerate(letters[:13]):
        x = x_start + (i * 65)
        letter_buttons[letter] = pygame.Rect(x, y_start, 60, 60)
    
    # Second row: N-Z
    for i, letter in enumerate(letters[13:]):
        x = x_start + (i * 65)
        letter_buttons[letter] = pygame.Rect(x, y_start + 70, 60, 60)

def draw_hangman(guesses_left):
    # Enhanced hangman with better proportions and colors
    base_x, base_y = 150, 350
    
    # Gallows base
    pygame.draw.rect(screen, (101, 67, 33), (base_x - 20, base_y, 80, 10))
    
    # Vertical pole
    pygame.draw.rect(screen, (139, 69, 19), (base_x, base_y - 200, 8, 200))
    
    # Horizontal beam
    pygame.draw.rect(screen, (139, 69, 19), (base_x, base_y - 200, 120, 8))
    
    # Rope
    pygame.draw.rect(screen, (160, 82, 45), (base_x + 115, base_y - 192, 4, 30))
    
    # Draw hangman parts based on wrong guesses
    hang_x, hang_y = base_x + 117, base_y - 160
    
    if guesses_left < 6:  # Head
        pygame.draw.circle(screen, (255, 220, 177), (hang_x, hang_y), 25)
        pygame.draw.circle(screen, (0, 0, 0), (hang_x, hang_y), 25, 3)
        # Eyes
        pygame.draw.circle(screen, (0, 0, 0), (hang_x - 8, hang_y - 5), 3)
        pygame.draw.circle(screen, (0, 0, 0), (hang_x + 8, hang_y - 5), 3)
        # Mouth
        if guesses_left <= 2:  # Sad face when close to losing
            pygame.draw.arc(screen, (0, 0, 0), (hang_x - 8, hang_y + 2, 16, 10), 0, 3.14, 2)
        else:
            pygame.draw.line(screen, (0, 0, 0), (hang_x - 6, hang_y + 8), (hang_x + 6, hang_y + 8), 2)
    
    if guesses_left < 5:  # Body
        pygame.draw.line(screen, (0, 0, 0), (hang_x, hang_y + 25), (hang_x, hang_y + 100), 5)
    
    if guesses_left < 4:  # Left arm
        pygame.draw.line(screen, (0, 0, 0), (hang_x, hang_y + 45), (hang_x - 30, hang_y + 70), 4)
    
    if guesses_left < 3:  # Right arm
        pygame.draw.line(screen, (0, 0, 0), (hang_x, hang_y + 45), (hang_x + 30, hang_y + 70), 4)
    
    if guesses_left < 2:  # Left leg
        pygame.draw.line(screen, (0, 0, 0), (hang_x, hang_y + 100), (hang_x - 25, hang_y + 140), 4)
    
    if guesses_left < 1:  # Right leg
        pygame.draw.line(screen, (0, 0, 0), (hang_x, hang_y + 100), (hang_x + 25, hang_y + 140), 4)

def draw_word_blanks(word, letters_guessed):
    # More attractive word display
    x_start = 400
    y_pos = 250
    letter_spacing = 50
    
    display_word = get_guessed_word(word, letters_guessed)
    word_surface = large_font.render(display_word, True, (25, 25, 112))
    word_rect = word_surface.get_rect(center=(500, y_pos))
    screen.blit(word_surface, word_rect)
    
    # Draw decorative underlines for unguessed letters
    for i, char in enumerate(word):
        if char != ' ' and char not in letters_guessed:
            x = word_rect.left + (i * 35)  # Approximate character width
            pygame.draw.line(screen, (25, 25, 112), (x, y_pos + 30), (x + 25, y_pos + 30), 3)

def update_loop():
    global warnings_left, guesses_left, game_over, message, letters_guessed, secret_word, category
    
    # Gradient background
    for y in range(700):
        color = (173 + y//10, 216 + y//20, 230)
        color = tuple(min(255, c) for c in color)
        pygame.draw.line(screen, color, (0, y), (1000, y))
    
    # Header section with improved styling
    header_rect = pygame.Rect(0, 0, 1000, 80)
    pygame.draw.rect(screen, (70, 130, 180), header_rect)
    pygame.draw.rect(screen, (25, 25, 112), header_rect, 3)
    
    title_text = large_font.render("🎯 HANGMAN CHALLENGE", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(500, 40))
    screen.blit(title_text, title_rect)
    
    # Category display with styling
    category_bg = pygame.Rect(350, 100, 300, 50)
    pygame.draw.rect(screen, (255, 255, 255), category_bg)
    pygame.draw.rect(screen, (70, 130, 180), category_bg, 2)
    
    category_text = font.render(f"Category: {category.upper()}", True, (25, 25, 112))
    category_rect = category_text.get_rect(center=category_bg.center)
    screen.blit(category_text, category_rect)
    
    # Game stats panel
    stats_bg = pygame.Rect(700, 150, 250, 150)
    pygame.draw.rect(screen, (255, 255, 255), stats_bg)
    pygame.draw.rect(screen, (70, 130, 180), stats_bg, 2)
    
    # Stats text
    guesses_text = font.render(f"Guesses: {guesses_left}", True, (220, 20, 60) if guesses_left <= 2 else (25, 25, 112))
    warnings_text = font.render(f"Warnings: {warnings_left}", True, (25, 25, 112))
    
    screen.blit(guesses_text, (stats_bg.x + 10, stats_bg.y + 20))
    screen.blit(warnings_text, (stats_bg.x + 10, stats_bg.y + 60))
    
    # Progress bar for guesses
    progress_bg = pygame.Rect(stats_bg.x + 10, stats_bg.y + 100, 200, 20)
    pygame.draw.rect(screen, (200, 200, 200), progress_bg)
    progress_width = int((guesses_left / 6) * 200)
    progress_color = (34, 139, 34) if guesses_left > 3 else (255, 165, 0) if guesses_left > 1 else (220, 20, 60)
    pygame.draw.rect(screen, progress_color, (progress_bg.x, progress_bg.y, progress_width, 20))
    pygame.draw.rect(screen, (0, 0, 0), progress_bg, 2)
    
    # Draw hangman
    draw_hangman(guesses_left)
    
    # Draw word
    draw_word_blanks(secret_word, letters_guessed)
    
    # Letter buttons with improved styling
    for letter, rect in letter_buttons.items():
        if letter.lower() in letters_guessed:
            if letter.lower() in secret_word.replace(' ', ''):
                color = (144, 238, 144)  # Light green for correct
                text_color = (0, 100, 0)
            else:
                color = (255, 182, 193)  # Light red for incorrect
                text_color = (139, 0, 0)
        else:
            color = (240, 248, 255)  # Alice blue for available
            text_color = (25, 25, 112)
        
        # Button with border
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (70, 130, 180), rect, 2)
        
        # Letter text
        letter_text = font.render(letter, True, text_color)
        text_rect = letter_text.get_rect(center=rect.center)
        screen.blit(letter_text, text_rect)
    
    # Control buttons with better styling
    # Restart button
    pygame.draw.rect(screen, (34, 139, 34), restart_button)
    pygame.draw.rect(screen, (0, 100, 0), restart_button, 2)
    restart_text = font.render("Restart", True, (255, 255, 255))
    restart_rect = restart_text.get_rect(center=restart_button.center)
    screen.blit(restart_text, restart_rect)
    
    # Hint button
    pygame.draw.rect(screen, (255, 165, 0), hint_button)
    pygame.draw.rect(screen, (255, 140, 0), hint_button, 2)
    hint_text = font.render("Hint", True, (255, 255, 255))
    hint_rect = hint_text.get_rect(center=hint_button.center)
    screen.blit(hint_text, hint_rect)
    
    # Message display
    if message:
        message_bg = pygame.Rect(50, 380, 900, 40)
        if "Congratulations" in message:
            pygame.draw.rect(screen, (144, 238, 144), message_bg)
        elif "Game over" in message:
            pygame.draw.rect(screen, (255, 182, 193), message_bg)
        else:
            pygame.draw.rect(screen, (255, 255, 255), message_bg)
        
        pygame.draw.rect(screen, (70, 130, 180), message_bg, 2)
        message_text = font.render(message, True, (25, 25, 112))
        message_rect = message_text.get_rect(center=message_bg.center)
        screen.blit(message_text, message_rect)
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return False
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Restart button
            if restart_button.collidepoint(event.pos):
                secret_word, category = choose_word(wordlist)
                letters_guessed = []
                warnings_left = 3
                guesses_left = 6
                game_over = False
                message = ""
            
            # Hint button
            if hint_button.collidepoint(event.pos) and not game_over:
                available = [c for c in secret_word.replace(' ', '') if c not in letters_guessed]
                if available and warnings_left > 0:
                    hint_letter = random.choice(available)
                    letters_guessed.append(hint_letter)
                    warnings_left -= 1
                    message = f"Hint used! Letter '{hint_letter.upper()}' revealed"
                    if is_word_guessed(secret_word, letters_guessed):
                        score = len(set(secret_word.replace(' ', ''))) * guesses_left
                        message = f"Congratulations! You won with a hint! Score: {score}"
                        game_over = True
                elif warnings_left <= 0:
                    message = "No hints remaining!"
            
            # Letter buttons
            for letter, rect in letter_buttons.items():
                if rect.collidepoint(event.pos) and letter.lower() not in letters_guessed and not game_over:
                    letters_guessed.append(letter.lower())
                    
                    if letter.lower() in secret_word.replace(' ', ''):
                        message = f"Great guess! '{letter}' is in the word"
                        if is_word_guessed(secret_word, letters_guessed):
                            score = len(set(secret_word.replace(' ', ''))) * guesses_left
                            message = f"🎉 Congratulations! You won! Score: {score} 🎉"
                            game_over = True
                    else:
                        penalty = 2 if letter.lower() in 'aeiou' else 1
                        guesses_left -= penalty
                        message = f"'{letter}' is not in the word. -{penalty} guess{'es' if penalty > 1 else ''}"
                    
                    if guesses_left <= 0:
                        message = f"💀 Game Over! The word was: {secret_word.upper()}"
                        game_over = True
    
    pygame.display.flip()
    return True

async def main():
    setup()
    clock = pygame.time.Clock()
    running = True
    
    while running:
        running = update_loop()
        clock.tick(60)  # 60 FPS
        await asyncio.sleep(0)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())