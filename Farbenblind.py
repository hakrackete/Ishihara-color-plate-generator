import math
import pygame
import pygame.gfxdraw
import random
import datetime
import time
start_time = time.time()

white = (255, 255, 255, 255)
black = (0, 0, 0, 255)
dark_grey = (50, 50, 50, 255)



background_colour = white
display_size = 900
outer_radius = display_size/2
(width, height) = (display_size, display_size)
middle = (width/2, height/2)

screen = pygame.display.set_mode((width, height))
progressbar = pygame.display.set_mode((width, height))
pygame.display.set_caption('Base')
screen.fill(background_colour)
running = True
schablone = pygame.image.load("hahalol.jpg")
schablone_size = schablone.get_size()

scaling_factor_x = schablone_size[0]/width
scaling_factor_y = schablone_size[1]/height


min_radius = 4
max_radius = 15

shifting_range = 30
modify_range = 1.5
gradient_range = 0.3

do_colorschwift = False
do_lightschwift = False
do_gradientshift = False

use_bw = False

use_redgreen = False


iterations = 50000

if use_redgreen:  # standard values that I can't see (am red-green colorblind)
    color1 = (148, 173, 81)
    color2 = (217, 111, 71)
else:  # values that I can see :)
    color1 = (202, 252, 3)
    color2 = (6, 138, 214)


def colorschwift(color, intervall):
    color = list(color)
    for i in range(3):
        shifted_color = random.randint(color[i] - intervall, color[i] + intervall)
        color[i] = int(max(min(255, shifted_color), 0))
    return tuple(color)


def lightschwift(color, modifier):
    color = list(color)
    if modifier < 1:
        modifier = 1/modifier
    modifier = random.uniform(1/modifier, modifier)
    for i in range(3):
        color[i] = int(min(255, color[i] * modifier))
    return tuple(color)


def gradientshift(first_color, second_color, gradient_range):  # how much one color changes into the other, only works with b/w
    first_color = list(first_color)
    second_color = list(second_color)
    gradient_change = random.uniform(0, gradient_range)

    for i in range(3):
        difference = first_color[i] - second_color[i]
        first_color[i] = int(first_color[i] - (difference * gradient_change))

    return tuple(first_color)


class Circle(object):
    def __init__(self, x, y, radius, state):
        self.x = x
        self.y = y
        self.radius = radius
        self.state = state # only useful for b/w drawing

# idk, weird draw function so that every possible combination of modifiers can be possible
    def draw(self, surface):
        if use_bw:
            if self.state:
                farbe = color1
                farbe2 = color2
            else:
                farbe = color2
                farbe2 = color1
            if do_gradientshift:
                farbe = gradientshift(farbe, farbe2, gradient_range)
        else:
            farbe = schablonenfarbe
        if do_colorschwift:
            farbe = colorschwift(farbe, shifting_range)
        if do_lightschwift:
            farbe = lightschwift(farbe, modify_range)
        pygame.gfxdraw.aacircle(surface, self.x, self.y, self.radius, farbe)
        pygame.gfxdraw.filled_circle(surface, self.x, self.y, self.radius, farbe)


circles = []

screen.fill(background_colour)
# pygame.draw.rect(progressbar,black,(10,10,100,30),1)

for i in range(iterations):
    # random valueon the original picture to pick the color of the to be drawn circle
    random_x = random.randint(0, schablone_size[0]-1)
    random_y = random.randint(0, schablone_size[1]-1)

    #get the accoriding coordinates for the endimage
    resize_x = int(random_x / scaling_factor_x)
    resize_y = int(random_y / scaling_factor_y)
    schablonenfarbe = schablone.get_at((random_x, random_y))
    if schablonenfarbe == black:
        state = True
    else:
        state = False

    # checks, if theres already been drawn on this pixel
    if not((screen.get_at((resize_x, resize_y))) == background_colour):
        continue

    # checks, if the circle can be drawn inside the bounds of the outer circle
    # also begins to calculate the biggest possible radius for the circle
    # this variable will be reduced throughout the process
    distance_to_origin = math.dist((resize_x, resize_y), middle)
    biggest_possible_radius = outer_radius - distance_to_origin
    if not(biggest_possible_radius > min_radius):
        continue

    # checks for collision with other circles so they don't overlap
    for circle in circles:
        current_radius = math.dist((resize_x, resize_y), (circle.x, circle.y)) - circle.radius

        # makes sure, that the biggest possible radius is always the smallest, so no circle can overlap
        if current_radius < biggest_possible_radius:
            biggest_possible_radius = current_radius
            if biggest_possible_radius < min_radius:
                break

    # reduces to minimum and maximum radius, then draws
    if biggest_possible_radius >= min_radius:
        biggest_possible_radius = int(biggest_possible_radius)
        biggest_possible_radius = min(biggest_possible_radius, max_radius)
        myCircle = Circle(resize_x, resize_y, biggest_possible_radius, state)
        circles.append(myCircle)
        myCircle.draw(screen)

    #pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] or not running:
        break
    if keys[pygame.K_ESCAPE]:
        break

print(str(i + 1) + "/" + str(iterations))
print("fertig mit malen :)")
print(len(circles))
print("--- %s seconds ---" % (time.time() - start_time))
while running:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for circle in circles:
                if math.dist(mouse_pos,(circle.x,circle.y)) < circle.radius:
                    # only works with the b/w version, as the it wouldnt change the color
                    circle.state = not circle.state
                    circle.draw(screen)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False

# unique filenames
fileoutput = "testcircle from: " + str(datetime.datetime.now()) + ".jpg"
pygame.image.save(screen, fileoutput.replace(":", "."))
pygame.quit()
