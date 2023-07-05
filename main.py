import pygame
import numpy as np

from matrix import *

# Constants
WIN_HEIGHT = 800
WIN_WIDTH = 800
SCALE = 100
ROTATE_SPEED = 0.001

FOC_INC = 0.1
SHIFT_INC = 0.01

# Clock
clock = pygame.time.Clock()

# Windows build
window = pygame.display.set_mode((WIN_HEIGHT, WIN_WIDTH))

# Starting Angle
angle_x = 0
angle_y = 0
angle_z = 0

# Cube points
cube = np.array(
    [
        [-1,  1,  1, -1, -1,  1,  1, -1],
        [-1, -1,  1,  1, -1, -1,  1,  1],
        [ 1,  1,  1,  1, -1, -1, -1, -1]
    ]
)


# Projection matrix
focal_lenght = 1
u0 = 0
v0 = 0
skew = 0
proj = projection_matrix(focal_lenght,u0,v0)


def draw_cube(cube, projection_matrix):

    proj_cube = projection_matrix @ cube
    
    for i in range(8):
        x = proj_cube[0][i] * SCALE + WIN_HEIGHT//2
        y = proj_cube[1][i] * SCALE + WIN_WIDTH//2
        pygame.draw.circle(window, (255, 0, 0), (x, y), 5)

    #base
    pygame.draw.line(window, (255, 255, 255), (proj_cube[0][0]* SCALE + WIN_HEIGHT//2, proj_cube[1][0]* SCALE + WIN_WIDTH//2) , (proj_cube[0][1]* SCALE + WIN_HEIGHT//2, proj_cube[1][1]* SCALE + WIN_WIDTH//2))
    pygame.draw.line(window, (255, 255, 255), (proj_cube[0][0]* SCALE + WIN_HEIGHT//2, proj_cube[1][0]* SCALE + WIN_WIDTH//2) , (proj_cube[0][4]* SCALE + WIN_HEIGHT//2, proj_cube[1][4]* SCALE + WIN_WIDTH//2))
    pygame.draw.line(window, (255, 255, 255), (proj_cube[0][5]* SCALE + WIN_HEIGHT//2, proj_cube[1][5]* SCALE + WIN_WIDTH//2) , (proj_cube[0][1]* SCALE + WIN_HEIGHT//2, proj_cube[1][1]* SCALE + WIN_WIDTH//2))
    pygame.draw.line(window, (255, 255, 255), (proj_cube[0][5]* SCALE + WIN_HEIGHT//2, proj_cube[1][5]* SCALE + WIN_WIDTH//2) , (proj_cube[0][4]* SCALE + WIN_HEIGHT//2, proj_cube[1][4]* SCALE + WIN_WIDTH//2))

    #top
    pygame.draw.line(window, (255, 255, 255), (proj_cube[0][3]* SCALE + WIN_HEIGHT//2, proj_cube[1][3]* SCALE + WIN_WIDTH//2) , (proj_cube[0][7]* SCALE + WIN_HEIGHT//2, proj_cube[1][7]* SCALE + WIN_WIDTH//2))
    pygame.draw.line(window, (255, 255, 255), (proj_cube[0][3]* SCALE + WIN_HEIGHT//2, proj_cube[1][3]* SCALE + WIN_WIDTH//2) , (proj_cube[0][2]* SCALE + WIN_HEIGHT//2, proj_cube[1][2]* SCALE + WIN_WIDTH//2))
    pygame.draw.line(window, (255, 255, 255), (proj_cube[0][6]* SCALE + WIN_HEIGHT//2, proj_cube[1][6]* SCALE + WIN_WIDTH//2) , (proj_cube[0][7]* SCALE + WIN_HEIGHT//2, proj_cube[1][7]* SCALE + WIN_WIDTH//2))
    pygame.draw.line(window, (255, 255, 255), (proj_cube[0][6]* SCALE + WIN_HEIGHT//2, proj_cube[1][6]* SCALE + WIN_WIDTH//2) , (proj_cube[0][2]* SCALE + WIN_HEIGHT//2, proj_cube[1][2]* SCALE + WIN_WIDTH//2))

    #lateral
    pygame.draw.line(window, (255, 255, 255), (proj_cube[0][0]* SCALE + WIN_HEIGHT//2, proj_cube[1][0]* SCALE + WIN_WIDTH//2) , (proj_cube[0][3]* SCALE + WIN_HEIGHT//2, proj_cube[1][3]* SCALE + WIN_WIDTH//2))
    pygame.draw.line(window, (255, 255, 255), (proj_cube[0][4]* SCALE + WIN_HEIGHT//2, proj_cube[1][4]* SCALE + WIN_WIDTH//2) , (proj_cube[0][7]* SCALE + WIN_HEIGHT//2, proj_cube[1][7]* SCALE + WIN_WIDTH//2))
    pygame.draw.line(window, (255, 255, 255), (proj_cube[0][1]* SCALE + WIN_HEIGHT//2, proj_cube[1][1]* SCALE + WIN_WIDTH//2) , (proj_cube[0][2]* SCALE + WIN_HEIGHT//2, proj_cube[1][2]* SCALE + WIN_WIDTH//2))
    pygame.draw.line(window, (255, 255, 255), (proj_cube[0][5]* SCALE + WIN_HEIGHT//2, proj_cube[1][5]* SCALE + WIN_WIDTH//2) , (proj_cube[0][6]* SCALE + WIN_HEIGHT//2, proj_cube[1][6]* SCALE + WIN_WIDTH//2))
    

while True:
    clock.tick(60)
    window.fill((0,0,0))
    # angle_x += 0.1

    R = rotation_matrix(angle_x, angle_y, angle_z)
    proj = projection_matrix(focal_lenght, u0, v0, skew)
    cube = R @ cube

    draw_cube(cube, proj)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            angle_y = angle_x = angle_z = u0 = v0 = skew = 0
            focal_lenght = 1
        if keys[pygame.K_a]:
            angle_y -= ROTATE_SPEED
        if keys[pygame.K_d]:
            angle_y += ROTATE_SPEED      
        if keys[pygame.K_w]:
            angle_z += ROTATE_SPEED
        if keys[pygame.K_s]:
            angle_z -= ROTATE_SPEED
        if keys[pygame.K_q]:
            angle_x -= ROTATE_SPEED
        if keys[pygame.K_e]:
            angle_x += ROTATE_SPEED
        if keys[pygame.K_1]:
            focal_lenght += FOC_INC
        if keys[pygame.K_2]:
            focal_lenght -= FOC_INC
            if focal_lenght < 0:
                focal_lenght = 0
        if keys[pygame.K_3]:
            skew += FOC_INC
        if keys[pygame.K_4]:
            skew -= FOC_INC
        if keys[pygame.K_5]:
            u0 += SHIFT_INC
        if keys[pygame.K_6]:
            u0 -= SHIFT_INC
    pygame.display.update()