import pygame
import sys
import argparse

# ==========================================
# CONFIGURATION SETTINGS (Visuals)
# ==========================================
PAUSE_DURATION = 0.8   # Seconds to pause on a period
FONT_SIZE = 60
FONT_COLOR = (255, 255, 255) 
BG_COLOR = (0, 0, 0)         
FOCUS_LINE_COLOR = (255, 0, 0) 
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
MARGIN = 100

# ==========================================
# LOGIC
# ==========================================

def load_text(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)

def wrap_text(text, font, max_width):
    """
    Splits text by the file's original newlines first, 
    then wraps lines that exceed the screen width.
    """
    # Split the raw text into logical paragraphs based on file newlines
    paragraphs = text.splitlines()
    
    final_lines = []
    
    for paragraph in paragraphs:
        # If it's an empty line in the file, keep it as an empty line on screen
        if not paragraph:
            final_lines.append("")
            continue

        words = paragraph.split(' ')
        current_line = []
        
        for word in words:
            # Check width of adding this word
            test_line = ' '.join(current_line + [word])
            w, h = font.size(test_line)
            
            if w < max_width:
                current_line.append(word)
            else:
                # Line is full, push it to final list
                final_lines.append(' '.join(current_line))
                current_line = [word]
        
        # Append whatever is left of this paragraph
        if current_line:
            final_lines.append(' '.join(current_line))
            
    return final_lines

def main():
    # --- CLI ARGUMENT PARSING ---
    parser = argparse.ArgumentParser(description="Python Teleprompter")
    parser.add_argument("filename", type=str, help="The text file to read")
    parser.add_argument("duration", type=float, help="Total time in seconds")
    parser.add_argument("--mirror", action="store_true", help="Enable mirror mode for teleprompter glass")
    
    args = parser.parse_args()

    filename = args.filename
    target_duration = args.duration
    is_mirrored = args.mirror

    pygame.init()
    
    # Setup Screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(f"Teleprompter - {filename}")
    font = pygame.font.SysFont("Arial", FONT_SIZE)
    
    # Load and Process Text
    raw_text = load_text(filename)
    wrapped_lines = wrap_text(raw_text, font, SCREEN_WIDTH - (MARGIN * 2))
    
    line_height = font.get_height() + 10
    total_text_height = len(wrapped_lines) * line_height
    
    # Pre-render text
    text_surface = pygame.Surface((SCREEN_WIDTH, max(total_text_height, SCREEN_HEIGHT)))
    text_surface.fill(BG_COLOR)
    
    period_y_locations = []
    
    for i, line in enumerate(wrapped_lines):
        y = i * line_height
        
        # Render text (if empty string, it renders nothing but takes up space)
        if line:
            render = font.render(line, True, FONT_COLOR)
            text_surface.blit(render, (MARGIN, y))
        
            # Check for period on this specific visual line
            if line.strip().endswith('.'):
                period_y_locations.append(y)

    # Calculate Speed
    total_pauses = len(period_y_locations)
    total_pause_time = total_pauses * PAUSE_DURATION
    effective_scroll_time = target_duration - total_pause_time
    
    if effective_scroll_time <= 0:
        print("Warning: Duration is very short relative to pauses. Speed adjusted.")
        effective_scroll_time = 1 
    
    # We calculate distance based on total text height so the end of the text eventually reaches the top
    pixels_per_second = total_text_height / effective_scroll_time
    
    # Runtime Variables
    clock = pygame.time.Clock()
    scroll_y = -SCREEN_HEIGHT / 3 
    running = True
    paused = False
    pause_timer = 0
    focus_y = SCREEN_HEIGHT * 0.3
    triggered_pauses = set()
    
    manual_pause = True 

    print(f"Loaded: {filename}")
    print(f"Duration: {target_duration}s")
    print(f"Mirror Mode: {is_mirrored}")
    print("Press SPACE to Start/Pause. ESC to quit.")

    while running:
        dt = clock.tick(60) / 1000.0 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    manual_pause = not manual_pause

        if not manual_pause:
            if paused:
                pause_timer -= dt
                if pause_timer <= 0:
                    paused = False
            else:
                scroll_y += pixels_per_second * dt
                
                # Check for period pauses
                for p_y in period_y_locations:
                    distance_to_focus = p_y - scroll_y
                    # Trigger if line hits the focus area
                    if distance_to_focus <= focus_y and p_y not in triggered_pauses:
                        paused = True
                        pause_timer = PAUSE_DURATION
                        triggered_pauses.add(p_y)
                        break

        # Drawing
        screen.fill(BG_COLOR)
        screen.blit(text_surface, (0, -scroll_y + focus_y))
        
        # Focus Line
        pygame.draw.line(screen, FOCUS_LINE_COLOR, (0, focus_y + line_height), (20, focus_y + line_height), 3)
        pygame.draw.line(screen, FOCUS_LINE_COLOR, (SCREEN_WIDTH-20, focus_y + line_height), (SCREEN_WIDTH, focus_y + line_height), 3)

        # Mirroring
        if is_mirrored:
            final_surface = pygame.transform.flip(screen, True, False)
            screen.blit(final_surface, (0, 0))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()