import pygame
import numpy as np

from matrix import *

# Constants
WIN_HEIGHT = 800
WIN_WIDTH = 800
SCALE = 100
ROTATE_SPEED = 0.001
FOC_INC = 0.1
SHIFT_INC = 1

# Clock
clock = pygame.time.Clock()

# Windows build
window = pygame.display.set_mode((WIN_HEIGHT, WIN_WIDTH))
pygame.font.init()

# Starting Angle
angle_x = 0
angle_y = 0
angle_z = 0

rot_speed_x = 0
rot_speed_y = 0
rot_speed_z = 0

# Cube points
cube = np.array(
    [
        [-1,  1,  1, -1, -1,  1,  1, -1],
        [-1, -1,  1,  1, -1, -1,  1,  1],
        [ 1,  1,  1,  1, -1, -1, -1, -1],
        [ 1,  1,  1,  1,  1,  1,  1,  1]
    ]
)


# Projection matrix
focal_lenght = 1
u0 = 0
v0 = 0
skew = 0
proj = intrinsic_matrix(focal_lenght, u0, v0, skew)

# camera position in world coordinate
camera_pos = np.array(
    [
        [0],
        [0],
        [0],
    ]
)

def draw_cube(cube):
    
    for i in range(8):
        x = cube[0][i] * SCALE + WIN_HEIGHT//2
        y = cube[1][i] * SCALE + WIN_WIDTH//2
        pygame.draw.circle(window, (255, 0, 0), (x, y), 5)

    #base
    pygame.draw.line(window, (255, 255, 255), (cube[0][0]* SCALE + WIN_HEIGHT//2, cube[1][0]* SCALE + WIN_WIDTH//2) , (cube[0][1]* SCALE + WIN_HEIGHT//2, cube[1][1]* SCALE + WIN_WIDTH//2))
    pygame.draw.line(window, (255, 255, 255), (cube[0][0]* SCALE + WIN_HEIGHT//2, cube[1][0]* SCALE + WIN_WIDTH//2) , (cube[0][4]* SCALE + WIN_HEIGHT//2, cube[1][4]* SCALE + WIN_WIDTH//2))
    pygame.draw.line(window, (255, 255, 255), (cube[0][5]* SCALE + WIN_HEIGHT//2, cube[1][5]* SCALE + WIN_WIDTH//2) , (cube[0][1]* SCALE + WIN_HEIGHT//2, cube[1][1]* SCALE + WIN_WIDTH//2))
    pygame.draw.line(window, (255, 255, 255), (cube[0][5]* SCALE + WIN_HEIGHT//2, cube[1][5]* SCALE + WIN_WIDTH//2) , (cube[0][4]* SCALE + WIN_HEIGHT//2, cube[1][4]* SCALE + WIN_WIDTH//2))

    #top
    pygame.draw.line(window, (255, 255, 255), (cube[0][3]* SCALE + WIN_HEIGHT//2, cube[1][3]* SCALE + WIN_WIDTH//2) , (cube[0][7]* SCALE + WIN_HEIGHT//2, cube[1][7]* SCALE + WIN_WIDTH//2))
    pygame.draw.line(window, (255, 255, 255), (cube[0][3]* SCALE + WIN_HEIGHT//2, cube[1][3]* SCALE + WIN_WIDTH//2) , (cube[0][2]* SCALE + WIN_HEIGHT//2, cube[1][2]* SCALE + WIN_WIDTH//2))
    pygame.draw.line(window, (255, 255, 255), (cube[0][6]* SCALE + WIN_HEIGHT//2, cube[1][6]* SCALE + WIN_WIDTH//2) , (cube[0][7]* SCALE + WIN_HEIGHT//2, cube[1][7]* SCALE + WIN_WIDTH//2))
    pygame.draw.line(window, (255, 255, 255), (cube[0][6]* SCALE + WIN_HEIGHT//2, cube[1][6]* SCALE + WIN_WIDTH//2) , (cube[0][2]* SCALE + WIN_HEIGHT//2, cube[1][2]* SCALE + WIN_WIDTH//2))

    #lateral
    pygame.draw.line(window, (255, 255, 255), (cube[0][0]* SCALE + WIN_HEIGHT//2, cube[1][0]* SCALE + WIN_WIDTH//2) , (cube[0][3]* SCALE + WIN_HEIGHT//2, cube[1][3]* SCALE + WIN_WIDTH//2))
    pygame.draw.line(window, (255, 255, 255), (cube[0][4]* SCALE + WIN_HEIGHT//2, cube[1][4]* SCALE + WIN_WIDTH//2) , (cube[0][7]* SCALE + WIN_HEIGHT//2, cube[1][7]* SCALE + WIN_WIDTH//2))
    pygame.draw.line(window, (255, 255, 255), (cube[0][1]* SCALE + WIN_HEIGHT//2, cube[1][1]* SCALE + WIN_WIDTH//2) , (cube[0][2]* SCALE + WIN_HEIGHT//2, cube[1][2]* SCALE + WIN_WIDTH//2))
    pygame.draw.line(window, (255, 255, 255), (cube[0][5]* SCALE + WIN_HEIGHT//2, cube[1][5]* SCALE + WIN_WIDTH//2) , (cube[0][6]* SCALE + WIN_HEIGHT//2, cube[1][6]* SCALE + WIN_WIDTH//2))
    
def draw_coordinate_frame(proj):
    origin = np.array([
        [0],
        [0],
        [0],
        [1]
    ])

    x_axis = np.array([
        [1],
        [0],
        [0],
        [1]
    ])
    y_axis = np.array([
        [0],
        [1],
        [0],
        [1]
    ])
    z_axis = np.array([
        [0],
        [0],
        [1],
        [1]
    ])
    
    origin = proj@origin
    x_axis = proj@x_axis
    y_axis = proj@y_axis
    z_axis = proj@z_axis

    pygame.draw.line(window, (255,0,0), (origin[0][0]* SCALE + WIN_HEIGHT//2, origin[1][0]* SCALE + WIN_WIDTH//2), (x_axis[0][0]* SCALE + WIN_HEIGHT//2, x_axis[1][0]* SCALE + WIN_WIDTH//2))
    pygame.draw.line(window, (0,255,0), (origin[0][0]* SCALE + WIN_HEIGHT//2, origin[1][0]* SCALE + WIN_WIDTH//2), (y_axis[0][0]* SCALE + WIN_HEIGHT//2, y_axis[1][0]* SCALE + WIN_WIDTH//2))
    pygame.draw.line(window, (0,0,255), (origin[0][0]* SCALE + WIN_HEIGHT//2, origin[1][0]* SCALE + WIN_WIDTH//2), (z_axis[0][0]* SCALE + WIN_HEIGHT//2, z_axis[1][0]* SCALE + WIN_WIDTH//2))

def print_values():
    myfont = pygame.font.SysFont("monospace", 15)

    label = myfont.render(f"angle_x = {angle_x:.2f}", 1, (255,255,255))
    window.blit(label, (0, 10))
    label = myfont.render(f"angle_y = {angle_y:.2f}", 1, (255,255,255))
    window.blit(label, (0, 30))
    label = myfont.render(f"angle_z = {angle_z:.2f}", 1, (255,255,255))
    window.blit(label, (0, 50))

    label = myfont.render(f"camera_x = {camera_pos[0,0]:.2f}", 1, (255,255,255))
    window.blit(label, (0, 70))
    label = myfont.render(f"camera_y = {camera_pos[1,0]:.2f}", 1, (255,255,255))
    window.blit(label, (0, 90))
    label = myfont.render(f"camera_z = {camera_pos[2,0]:.2f}", 1, (255,255,255))
    window.blit(label, (0, 110))

while True:
    clock.tick(60)
    window.fill((0,0,0))

    angle_x += rot_speed_x
    angle_y += rot_speed_y
    angle_z += rot_speed_z


    R = rotation_matrix(angle_x, angle_y, angle_z)
    K = intrinsic_matrix(focal_lenght, u0, v0, skew)

    extrinsic = extrinsic_matrix(R, camera_pos)
    # base = np.array([0,0,0,1])
    # top = np.hstack([R.T, -R.T@camera_pos])
    # extrinsic = np.vstack([top,base])

    proj = K@extrinsic

    proj_cube = proj@cube

    # Draw calls
    draw_cube(proj_cube)
    draw_coordinate_frame(proj)
    print_values()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            rot_speed_y = rot_speed_x = rot_speed_z = u0 = v0 = skew = 0
            focal_lenght = 1
        if keys[pygame.K_a]:
            rot_speed_y -= ROTATE_SPEED
        if keys[pygame.K_d]:
            rot_speed_y += ROTATE_SPEED      
        if keys[pygame.K_w]:
            rot_speed_z += ROTATE_SPEED
        if keys[pygame.K_s]:
            rot_speed_z -= ROTATE_SPEED
        if keys[pygame.K_q]:
            rot_speed_x -= ROTATE_SPEED
        if keys[pygame.K_e]:
            rot_speed_x += ROTATE_SPEED
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
        if keys[pygame.K_LEFT]:
            # x_shift + INC
            camera_pos[0,0] -= SHIFT_INC
        if keys[pygame.K_RIGHT]:
            # x_shift - INC
            camera_pos[0,0] += SHIFT_INC
        if keys[pygame.K_UP]:
            # z_shift + INC
            camera_pos[2,0] += SHIFT_INC
        if keys[pygame.K_DOWN]:
            # z_shift - INC
            camera_pos[2,0] -= SHIFT_INC
        if keys[pygame.K_SPACE]:
            # y_shift - INC
            camera_pos[1,0] -= SHIFT_INC
        if keys[pygame.K_LSHIFT]:
            # y_shift - INC
            camera_pos[1,0] += SHIFT_INC
    pygame.display.update()