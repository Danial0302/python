import pygame
import datetime
import os
import math

pygame.init()

WIDTH, HEIGHT = 900, 650
TOOLBAR_H = 80

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint TSIS2")

canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_H))
canvas.fill((255, 255, 255))

clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 18)

tool = "pencil"
color = (0, 0, 0)
brush_size = 5

drawing = False
start_pos = None
last_pos = None

typing = False
text_input = ""
text_pos = None


def canvas_pos(pos):
    return pos[0], pos[1] - TOOLBAR_H


def in_canvas(pos):
    return pos[1] >= TOOLBAR_H


def save_canvas():
    filename = datetime.datetime.now().strftime("paint_%Y%m%d_%H%M%S.png")
    base_path = os.path.dirname(__file__)
    full_path = os.path.join(base_path, filename)

    pygame.image.save(canvas, full_path)
    print("Saved to:", full_path)


def flood_fill(surface, x, y, new_color):
    if x < 0 or x >= surface.get_width() or y < 0 or y >= surface.get_height():
        return

    target_color = surface.get_at((x, y))

    if target_color == new_color:
        return

    stack = [(x, y)]

    while stack:
        x, y = stack.pop()

        if x < 0 or x >= surface.get_width() or y < 0 or y >= surface.get_height():
            continue

        if surface.get_at((x, y)) != target_color:
            continue

        surface.set_at((x, y), new_color)

        stack.append((x + 1, y))
        stack.append((x - 1, y))
        stack.append((x, y + 1))
        stack.append((x, y - 1))


def draw_shape(surface, shape, start, end, col, size):
    x1, y1 = start
    x2, y2 = end

    rect = pygame.Rect(
        min(x1, x2),
        min(y1, y2),
        abs(x2 - x1),
        abs(y2 - y1)
    )

    if shape == "rect":
        pygame.draw.rect(surface, col, rect, size)

    elif shape == "circle":
        radius = int(math.hypot(x2 - x1, y2 - y1))
        pygame.draw.circle(surface, col, start, radius, size)

    elif shape == "square":
        side = min(abs(x2 - x1), abs(y2 - y1))
        rect = pygame.Rect(
            x1,
            y1,
            side if x2 >= x1 else -side,
            side if y2 >= y1 else -side
        )
        rect.normalize()
        pygame.draw.rect(surface, col, rect, size)

    elif shape == "right_triangle":
        points = [(x1, y1), (x1, y2), (x2, y2)]
        pygame.draw.polygon(surface, col, points, size)

    elif shape == "equilateral_triangle":
        points = [
            ((x1 + x2) // 2, y1),
            (x1, y2),
            (x2, y2)
        ]
        pygame.draw.polygon(surface, col, points, size)

    elif shape == "rhombus":
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        points = [
            (cx, y1),
            (x2, cy),
            (cx, y2),
            (x1, cy)
        ]

        pygame.draw.polygon(surface, col, points, size)


def draw_toolbar():
    pygame.draw.rect(screen, (220, 220, 220), (0, 0, WIDTH, TOOLBAR_H))

    info = f"Tool: {tool} | Size: {brush_size} | Color: {color}"
    screen.blit(font.render(info, True, (0, 0, 0)), (10, 10))

    controls1 = "Tools: P Pencil | L Line | R Rect | C Circle | S Square | A RightTri | E EqTri | H Rhombus | F Fill | T Text"
    controls2 = "Size: 1 Small  2 Medium  3 Large | Colors: K Black D Red G Green B Blue Y Yellow W White | Cmd/Ctrl+S Save"

    screen.blit(font.render(controls1, True, (0, 0, 0)), (10, 35))
    screen.blit(font.render(controls2, True, (0, 0, 0)), (10, 58))

    pygame.draw.rect(screen, color, (820, 15, 40, 40))


running = True

while running:
    screen.fill((180, 180, 180))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # ---------- KEYBOARD ----------
        if event.type == pygame.KEYDOWN:

            # text typing mode
            if typing:
                if event.key == pygame.K_RETURN:
                    txt = font.render(text_input, True, color)
                    canvas.blit(txt, text_pos)
                    typing = False
                    text_input = ""
                    text_pos = None

                elif event.key == pygame.K_ESCAPE:
                    typing = False
                    text_input = ""
                    text_pos = None

                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]

                else:
                    text_input += event.unicode

            # normal shortcuts
            else:
                # save: works with Ctrl+S and Command+S
                if event.key == pygame.K_s and pygame.key.get_mods() & (pygame.KMOD_CTRL | pygame.KMOD_META):
                    save_canvas()

                # brush sizes
                elif event.key == pygame.K_1:
                    brush_size = 2
                elif event.key == pygame.K_2:
                    brush_size = 5
                elif event.key == pygame.K_3:
                    brush_size = 10

                # tools
                elif event.key == pygame.K_p:
                    tool = "pencil"
                elif event.key == pygame.K_l:
                    tool = "line"
                elif event.key == pygame.K_r:
                    tool = "rect"
                elif event.key == pygame.K_c:
                    tool = "circle"
                elif event.key == pygame.K_s:
                    tool = "square"
                elif event.key == pygame.K_a:
                    tool = "right_triangle"
                elif event.key == pygame.K_e:
                    tool = "equilateral_triangle"
                elif event.key == pygame.K_h:
                    tool = "rhombus"
                elif event.key == pygame.K_f:
                    tool = "fill"
                elif event.key == pygame.K_t:
                    tool = "text"

                # colors
                elif event.key == pygame.K_k:
                    color = (0, 0, 0)
                elif event.key == pygame.K_d:
                    color = (255, 0, 0)
                elif event.key == pygame.K_g:
                    color = (0, 180, 0)
                elif event.key == pygame.K_b:
                    color = (0, 0, 255)
                elif event.key == pygame.K_y:
                    color = (255, 255, 0)
                elif event.key == pygame.K_w:
                    color = (255, 255, 255)

        # ---------- MOUSE DOWN ----------
        if event.type == pygame.MOUSEBUTTONDOWN and in_canvas(event.pos):
            pos = canvas_pos(event.pos)

            if tool == "fill":
                flood_fill(canvas, pos[0], pos[1], color)

            elif tool == "text":
                typing = True
                text_pos = pos
                text_input = ""

            else:
                drawing = True
                start_pos = pos
                last_pos = pos

        # ---------- MOUSE MOTION ----------
        if event.type == pygame.MOUSEMOTION and drawing:
            pos = canvas_pos(event.pos)

            if tool == "pencil":
                pygame.draw.line(canvas, color, last_pos, pos, brush_size)
                last_pos = pos

        # ---------- MOUSE UP ----------
        if event.type == pygame.MOUSEBUTTONUP and drawing:
            pos = canvas_pos(event.pos)
            drawing = False

            if tool == "line":
                pygame.draw.line(canvas, color, start_pos, pos, brush_size)

            elif tool in [
                "rect",
                "circle",
                "square",
                "right_triangle",
                "equilateral_triangle",
                "rhombus"
            ]:
                draw_shape(canvas, tool, start_pos, pos, color, brush_size)

    # draw canvas
    screen.blit(canvas, (0, TOOLBAR_H))

    # live preview
    if drawing and tool in [
        "line",
        "rect",
        "circle",
        "square",
        "right_triangle",
        "equilateral_triangle",
        "rhombus"
    ]:
        temp = canvas.copy()
        mouse = pygame.mouse.get_pos()

        if in_canvas(mouse):
            end = canvas_pos(mouse)

            if tool == "line":
                pygame.draw.line(temp, color, start_pos, end, brush_size)
            else:
                draw_shape(temp, tool, start_pos, end, color, brush_size)

        screen.blit(temp, (0, TOOLBAR_H))

    # text preview
    if typing and text_pos:
        txt = font.render(text_input, True, color)
        screen.blit(txt, (text_pos[0], text_pos[1] + TOOLBAR_H))

    draw_toolbar()

    pygame.display.update()
    clock.tick(60)

pygame.quit()