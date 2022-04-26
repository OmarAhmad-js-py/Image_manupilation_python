import pygame
import main as m

height = 600
width = 800
fps = 20

pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption("Image Manipulation Tool")

original = None
last_image = None
flag = False
default_arg = 2

choices = {
    "Image to Grayscale": m.img_to_grayscale,
    "Switch Color Channels": m.switch_color_channels,
    "Invert Image": m.invert_img,
}

choices_with_args = {
    "Brighten Image": m.brighten_img,
    "Darken Image": m.darken_img,
    "Add Noise": m.img_noise,
    "Pixelate Image": m.img_pixelate,
    "Blur Image (SLOW)": m.gaussian_blur_img
}


def button(x, y, w, h, _text, color, text_color):
    pygame.draw.rect(screen, color, (x, y, w, h))
    font = pygame.font.SysFont('Arial', 20)
    _text = font.render(_text, True, text_color)
    text_rect = _text.get_rect()
    # noinspection SpellCheckingInspection
    text_rect.topleft = (x + w / 2, y + h / 2)
    screen.blit(_text, text_rect)
    return text_rect


def default_value(_events):
    global default_arg
    box = pygame.draw.rect(screen, (230, 230, 230), (0, height - 55, 200, 70))
    font = pygame.font.SysFont('Arial', 15)
    _text = font.render("Value used as argument: " + str(default_arg), True, (0, 0, 0))
    text_rect = _text.get_rect()
    text_rect.center = (95, height - 35)
    screen.blit(_text, text_rect)
    desc = font.render("Click to change", True, (0, 0, 0))
    desc_rect = desc.get_rect()
    desc_rect.center = (95, height - 15)
    screen.blit(desc, desc_rect)
    if box.collidepoint(pygame.mouse.get_pos()):
        for _event in _events:
            if _event.type == pygame.MOUSEBUTTONDOWN:
                default_arg += 1
                if default_arg > 10:
                    default_arg = 1


while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    screen.fill((255, 255, 255))

    if m.path and original is None:
        img = pygame.image.load(m.path)
        original = img
    elif original is not None:
        width = original.get_width()
        screen = pygame.display.set_mode(((width * 2) + 200, height))
        screen.blit(original, (width + 230, 0))
        default_value(events)
    else:
        text = pygame.font.SysFont("Arial", 50).render("No image selected", True, (0, 0, 0))
        rect = text.get_rect()
        rect.center = (width / 2, height / 2)
        screen.blit(text, rect)
        if rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                m.select_file()

    if original:
        last_i = 0
        for i, choice in enumerate(choices):
            rect = button(10, i * 50, 0, 50, choice, (0, 0, 0), (255, 255, 255))
            last_i = i
            if rect.collidepoint(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[0]:
                    img = m.path_to_image(m.path)
                    choices[choice](img)
                    flag = True

        text = pygame.font.SysFont("Arial", 20).render("Image with arguments", True, (200, 200, 200))
        rect = text.get_rect()
        # noinspection SpellCheckingInspection
        rect.topleft = (10, (last_i + 1.2) * 50 + 25)
        screen.blit(text, rect)
        for i, choice in enumerate(choices_with_args):
            rect = button(10, (i + last_i + 2) * 50, 0, 50, choice, (0, 0, 0), (255, 255, 255))
            if rect.collidepoint(pygame.mouse.get_pos()):
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        text = pygame.font.SysFont("Arial", 50).render("Enter value on the keyboard (1-10)", True,
                                                                       (0, 0, 0))
                        rect = text.get_rect()
                        rect.center = (width / 2, height / 2)
                        screen.blit(text, rect)
                        img = m.path_to_image(m.path)
                        choices_with_args[choice](img, int(default_arg))
                        flag = True

    if flag and m.latest_path is not None:
        flag = False
        last_image = pygame.image.load(m.latest_path)
    elif not flag and last_image is not None:
        screen.blit(last_image, (width - last_image.get_width() + 230, 0))

    pygame.display.update()
    clock.tick(fps)
