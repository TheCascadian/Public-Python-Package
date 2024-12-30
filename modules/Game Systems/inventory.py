import pygame
import pygame_gui
import sys

pygame.init()

#region Inventory Init
WIDTH, HEIGHT = 1720, 980
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE | pygame.DOUBLEBUF)

manager = pygame_gui.UIManager((WIDTH, HEIGHT))
spacing = 20
GRID_SIZE = 60
HOTBAR_SIZE = 60
MIN_PADDING = 50
MAX_PADDING = 250
item_categories = ["Weapons", "Armor", "Consumables", "Materials"]
current_tab = "Weapons"

inventory_tabs = {
    "Weapons": [[None for _ in range(8)] for _ in range(5)],
    "Armor": [[None for _ in range(8)] for _ in range(5)],
    "Consumables": [[None for _ in range(8)] for _ in range(5)],
    "Materials": [[None for _ in range(8)] for _ in range(5)],
}



hotbar = [None for _ in range(10)]

items = [
    {"shape": "circle", "color": (255, 0, 0), "tooltip": "Red Circle", "quantity": 1},
    {"shape": "rect", "color": (0, 255, 0), "tooltip": "Green Rectangle", "quantity": 5},
    {"shape": "triangle", "color": (0, 0, 255), "tooltip": "Blue Triangle", "quantity": 10},
    {"shape": "circle", "color": (255, 255, 0), "tooltip": "Yellow Circle", "quantity": 3},
    {"shape": "rect", "color": (255, 165, 0), "tooltip": "Orange Rectangle", "quantity": 7}
]

inventory_tabs["Weapons"][0][0] = items[0]
inventory_tabs["Armor"][1][2] = items[1]
hotbar[0] = items[2]
hotbar[1] = items[3]

custom_font = pygame.font.SysFont("Cascadia Code", 16)  # Adjust the size as needed
show_inventory = False
debug_mode = False
dragging_item = None
dragging_from = None
#endregion

def calculate_padding(ui_size):
    return max(MIN_PADDING, min(MAX_PADDING, ui_size // 10))

def draw_inventory(ui_size):
    if show_inventory:
        padding = 10  # Set the padding around elements inside the background rectangles

        third_width = WIDTH // 3
        half_height = HEIGHT // 2

        main_inv_x = third_width + (third_width - 8 * GRID_SIZE) // 2
        main_inv_y = half_height - 2.5 * GRID_SIZE  # Align with the vertical center of armor and crafting grids

        hotbar_x = third_width + (third_width - 10 * HOTBAR_SIZE) // 2  # Updated to fit 10 slots
        hotbar_y = HEIGHT - padding * 2 - HOTBAR_SIZE

        draw_background_rect(main_inv_x - padding, main_inv_y - padding, 8 * GRID_SIZE + padding * 2, 5 * GRID_SIZE + padding * 2)
        draw_background_rect(hotbar_x - padding, hotbar_y - padding, 10 * HOTBAR_SIZE + padding * 2, HOTBAR_SIZE + padding * 2)  # Updated for 10 slots

        draw_grid(inventory_tabs[current_tab], main_inv_x, main_inv_y, 5, 8, GRID_SIZE)
        draw_hotbar(hotbar_x, hotbar_y)
        draw_tabs(main_inv_x, main_inv_y - GRID_SIZE - 10, 8 * GRID_SIZE, GRID_SIZE)

        if dragging_item:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            draw_item(dragging_item, mouse_x - GRID_SIZE // 2, mouse_y - GRID_SIZE // 2, GRID_SIZE)

def draw_background_rect(x, y, width, height):
    rect_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    rect_surface.set_alpha(128)  # Semi-transparent background (128/255)

    pygame.draw.rect(rect_surface, (50, 50, 50), (0, 0, width, height), 0, border_radius=10)
    pygame.draw.rect(rect_surface, (100, 100, 100), (0, 0, width, height), 2, border_radius=10)

    screen.blit(rect_surface, (x, y))

def draw_tabs(x, y, width, height):
    global current_tab  # Declare global here
    tab_width = width // len(item_categories)
    for i, category in enumerate(item_categories):
        tab_x = x + i * tab_width
        tab_color = (200, 200, 200) if category == current_tab else (100, 100, 100)

        tab_surface = pygame.Surface((tab_width, height), pygame.SRCALPHA)
        tab_surface.set_alpha(128)  # Semi-transparent background

        pygame.draw.rect(tab_surface, tab_color, (0, 0, tab_width, height), 0, border_radius=10)
        pygame.draw.rect(tab_surface, (150, 150, 150), (0, 0, tab_width, height), 2, border_radius=10)

        screen.blit(tab_surface, (tab_x, y))

        label_position = (tab_x + (tab_width - custom_font.size(category)[0]) // 2, y + (height - custom_font.size(category)[1]) // 2)
        draw_text_with_outline_and_shadow(category, custom_font, (255, 255, 255), (0, 0, 0), (50, 50, 50), label_position)

        if pygame.mouse.get_pressed()[0]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if tab_x <= mouse_x <= tab_x + tab_width and y <= mouse_y <= y + height:
                current_tab = category

def draw_grid(grid, start_x, start_y, rows, cols, size):
    for row in range(rows):
        for col in range(cols):
            x = start_x + col * size
            y = start_y + row * size
            
            draw_background_rect(x, y, size, size)
            
            item = grid[row][col]
            if item:
                draw_item(item, x, y, size)

def draw_hotbar(start_x, start_y):
    for col in range(10):
        x = start_x + col * HOTBAR_SIZE

        draw_background_rect(x, start_y, HOTBAR_SIZE, HOTBAR_SIZE)
        
        item = hotbar[col]
        if item:
            draw_item(item, x, start_y, HOTBAR_SIZE)


def draw_text_with_outline(text, font, color, outline_color, position, outline_width=2):
    # Render the text multiple times for the outline
    x, y = position
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx != 0 or dy != 0:
                outline_surface = font.render(text, True, outline_color)
                screen.blit(outline_surface, (x + dx, y + dy))

    # Render the main text on top
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

def draw_text_with_shadow(text, font, color, shadow_color, position, shadow_offset=(2, 2)):
    # Render the shadow
    shadow_surface = font.render(text, True, shadow_color)
    shadow_x, shadow_y = position[0] + shadow_offset[0], position[1] + shadow_offset[1]
    screen.blit(shadow_surface, (shadow_x, shadow_y))

    # Render the main text on top
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

def draw_text_with_outline_and_shadow(text, font, color, outline_color, shadow_color, position, outline_width=2, shadow_offset=(2, 2)):
    # First, draw the shadow
    shadow_surface = font.render(text, True, shadow_color)
    shadow_x, shadow_y = position[0] + shadow_offset[0], position[1] + shadow_offset[1]
    screen.blit(shadow_surface, (shadow_x, shadow_y))

    # Then, draw the outline
    draw_text_with_outline(text, font, color, outline_color, position, outline_width)

def draw_item(item, x, y, size):
    # Draw the item shape
    if item["shape"] == "circle":
        pygame.draw.circle(screen, item["color"], (x + size//2, y + size//2), size//3)
    elif item["shape"] == "rect":
        pygame.draw.rect(screen, item["color"], (x + 10, y + 10, size - 20, size - 20))
    elif item["shape"] == "triangle":
        pygame.draw.polygon(screen, item["color"], [(x + size//2, y + 10), 
                                                    (x + 10, y + size - 10), 
                                                    (x + size - 10, y + size - 10)])
    
    # Draw the quantity if the item has more than one, with shadow and outline
    if item["quantity"] > 1:
        quantity_text = str(item["quantity"])
        text_position = (x + size - 5, y + size - 5)
        draw_text_with_outline_and_shadow(quantity_text, custom_font, (255, 255, 255), (0, 0, 0), (50, 50, 50), 
                                          (text_position[0] - custom_font.size(quantity_text)[0], text_position[1] - custom_font.size(quantity_text)[1]))

def draw_debug_outlines(main_inv_x, main_inv_y, hotbar_x, hotbar_y, padding):
    pygame.draw.rect(screen, (255, 0, 0), (main_inv_x - padding, main_inv_y - padding, 8 * GRID_SIZE + padding * 2, 5 * GRID_SIZE + padding * 2), 2)
    pygame.draw.rect(screen, (255, 0, 0), (hotbar_x - padding, hotbar_y - padding, 10 * HOTBAR_SIZE + padding * 2, HOTBAR_SIZE + padding * 2), 2)

def handle_drag_drop():
    global dragging_item, dragging_from

    mouse_pos = pygame.mouse.get_pos()

    if pygame.mouse.get_pressed()[0]:  # Left mouse button held down
        if dragging_item is None:  # No item is being dragged
            # Check all grids (armor, cosmetic armor, main inventory, crafting, hotbar, trinkets)
            check_grids_for_drag(mouse_pos)

    elif dragging_item:  # Mouse button released and an item is being dragged
        # Check all grids to place the item
        if not place_item_in_grids(mouse_pos):
            # If not placed in a valid slot, return item to original slot
            restore_dragged_item()

        dragging_item = None
        dragging_from = None

def check_grids_for_drag(mouse_pos):
    global dragging_item, dragging_from

    # Check main inventory
    for row in range(5):
        for col in range(8):
            x = (WIDTH - 8 * GRID_SIZE) // 2 + col * GRID_SIZE
            y = (HEIGHT - 5 * GRID_SIZE) // 2 + row * GRID_SIZE
            rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
            if rect.collidepoint(mouse_pos):
                if inventory_tabs[current_tab][row][col]:
                    dragging_item = inventory_tabs[current_tab][row][col]
                    dragging_from = ('inventory', row, col)
                    inventory_tabs[current_tab][row][col] = None
                return

    # Check hotbar
    hotbar_x = (WIDTH - 10 * HOTBAR_SIZE) // 2  # Updated for 10 slots
    hotbar_y = HEIGHT - MIN_PADDING - HOTBAR_SIZE
    for col in range(10):  # Updated for 10 slots
        x = hotbar_x + col * HOTBAR_SIZE
        rect = pygame.Rect(x, hotbar_y, HOTBAR_SIZE, HOTBAR_SIZE)
        if rect.collidepoint(mouse_pos):
            if hotbar[col]:
                dragging_item = hotbar[col]
                dragging_from = ('hotbar', col)
                hotbar[col] = None
            return

def place_item_in_grids(mouse_pos):
    global dragging_item

    # Check main inventory
    for row in range(5):
        for col in range(8):
            x = (WIDTH - 8 * GRID_SIZE) // 2 + col * GRID_SIZE
            y = (HEIGHT - 5 * GRID_SIZE) // 2 + row * GRID_SIZE
            rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
            if rect.collidepoint(mouse_pos):
                if inventory_tabs[current_tab][row][col] is None:
                    inventory_tabs[current_tab][row][col] = dragging_item
                    return True

    # Check hotbar
    hotbar_x = (WIDTH - 10 * HOTBAR_SIZE) // 2  # Updated for 10 slots
    hotbar_y = HEIGHT - MIN_PADDING - HOTBAR_SIZE
    for col in range(10):  # Updated for 10 slots
        x = hotbar_x + col * HOTBAR_SIZE
        rect = pygame.Rect(x, hotbar_y, HOTBAR_SIZE, HOTBAR_SIZE)
        if rect.collidepoint(mouse_pos):
            if hotbar[col] is None:
                hotbar[col] = dragging_item
                return True


    return False

def restore_dragged_item():
    global dragging_item, dragging_from

    if dragging_from[0] == 'inventory':
        inventory_tabs[current_tab][dragging_from[1]][dragging_from[2]] = dragging_item
    elif dragging_from[0] == 'hotbar':
        hotbar[dragging_from[1]] = dragging_item

def game_loop():
    global show_inventory, WIDTH, HEIGHT, screen, current_tab, debug_mode
    clock = pygame.time.Clock()

    while True:
        time_delta = clock.tick(120) / 1000.0 # adjust the FPS as needed, using 120 FPS as an example

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                manager.set_window_resolution((WIDTH, HEIGHT))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    show_inventory = not show_inventory
                if event.key == pygame.K_d:  # Toggle debug mode with 'd' key
                    debug_mode = not debug_mode
                if event.key == pygame.K_1:
                    current_tab = item_categories[0]
                if event.key == pygame.K_2:
                    current_tab = item_categories[1]
                if event.key == pygame.K_3:
                    current_tab = item_categories[2]
                if event.key == pygame.K_4:
                    current_tab = item_categories[3]

            manager.process_events(event)

        handle_drag_drop()

        screen.fill((0, 0, 0))
        draw_inventory(min(WIDTH, HEIGHT))

        manager.update(time_delta)
        manager.draw_ui(screen)

        pygame.display.flip()
        fps = clock.get_fps()

        # Update window caption with FPS
        pygame.display.set_caption(f"Pygame FPS Example - FPS: {fps:.2f}")

# Run the game
game_loop()
