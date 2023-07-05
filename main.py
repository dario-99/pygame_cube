import pygame
import numpy as np

from matrix import *

# Constants
WIN_HEIGHT = 980
WIN_WIDTH = 1820
SCALE = 100
ROTATE_SPEED = 0.001
FOC_INC = 0.1
SHIFT_INC = 1

# Clock
clock = pygame.time.Clock()

# Windows build
window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
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
u0 = WIN_WIDTH//2
v0 = WIN_HEIGHT//2
skew = 0
pu = 1/(WIN_WIDTH//2)
pv = 1/(WIN_HEIGHT//2)
proj = intrinsic_matrix(focal_lenght, u0, v0, skew, pu, pv)

# camera position in world coordinate
camera_pos = np.array(
    [
        [0],
        [0],
        [-2],
    ]
)


def draw_cube(cube):
    
    for i in range(8):
        x = cube[0][i]/cube[2][i]
        y = cube[1][i]/cube[2][i]
        pygame.draw.circle(window, (255, 0, 0), (x, y), 5)

    #base
    pygame.draw.line(window, (255, 255, 255), (cube[0][0]/cube[2][0], cube[1][0]/cube[2][0]) , (cube[0][1]/cube[2][1], cube[1][1]/cube[2][1]))
    pygame.draw.line(window, (255, 255, 255), (cube[0][0]/cube[2][0], cube[1][0]/cube[2][0]) , (cube[0][4]/cube[2][4], cube[1][4]/cube[2][4]))
    pygame.draw.line(window, (255, 255, 255), (cube[0][5]/cube[2][5], cube[1][5]/cube[2][5]) , (cube[0][1]/cube[2][1], cube[1][1]/cube[2][1]))
    pygame.draw.line(window, (255, 255, 255), (cube[0][5]/cube[2][5], cube[1][5]/cube[2][5]) , (cube[0][4]/cube[2][4], cube[1][4]/cube[2][4]))

    #top
    pygame.draw.line(window, (255, 255, 255), (cube[0][3]/cube[2][3], cube[1][3]/cube[2][3]) , (cube[0][7]/cube[2][7], cube[1][7]/cube[2][7]))
    pygame.draw.line(window, (255, 255, 255), (cube[0][3]/cube[2][3], cube[1][3]/cube[2][3]) , (cube[0][2]/cube[2][2], cube[1][2]/cube[2][2]))
    pygame.draw.line(window, (255, 255, 255), (cube[0][6]/cube[2][6], cube[1][6]/cube[2][6]) , (cube[0][7]/cube[2][7], cube[1][7]/cube[2][7]))
    pygame.draw.line(window, (255, 255, 255), (cube[0][6]/cube[2][6], cube[1][6]/cube[2][6]) , (cube[0][2]/cube[2][2], cube[1][2]/cube[2][2]))

    #lateral
    pygame.draw.line(window, (255, 255, 255), (cube[0][0]/cube[2][0], cube[1][0]/cube[2][0]) , (cube[0][3]/cube[2][3], cube[1][3]/cube[2][3]))
    pygame.draw.line(window, (255, 255, 255), (cube[0][4]/cube[2][4], cube[1][4]/cube[2][4]) , (cube[0][7]/cube[2][7], cube[1][7]/cube[2][7]))
    pygame.draw.line(window, (255, 255, 255), (cube[0][1]/cube[2][1], cube[1][1]/cube[2][1]) , (cube[0][2]/cube[2][2], cube[1][2]/cube[2][2]))
    pygame.draw.line(window, (255, 255, 255), (cube[0][5]/cube[2][5], cube[1][5]/cube[2][5]) , (cube[0][6]/cube[2][6], cube[1][6]/cube[2][6]))
    
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

    pygame.draw.line(window, (255,0,0), (origin[0][0]/ origin[2][0], origin[1][0]/origin[2][0]), (x_axis[0][0]/ x_axis[2][0], x_axis[1][0]/ x_axis[2][0]))
    pygame.draw.line(window, (0,255,0), (origin[0][0]/ origin[2][0], origin[1][0]/origin[2][0]), (y_axis[0][0]/ y_axis[2][0], y_axis[1][0]/ y_axis[2][0]))
    pygame.draw.line(window, (0,0,255), (origin[0][0]/ origin[2][0], origin[1][0]/origin[2][0]), (z_axis[0][0]/ z_axis[2][0], z_axis[1][0]/ z_axis[2][0]))

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
    intrinsic = intrinsic_matrix(focal_lenght, u0, v0, skew)

    extrinsic = extrinsic_matrix(R, camera_pos)

    proj = intrinsic@extrinsic

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
            rot_speed_y = rot_speed_x = rot_speed_z = skew = 0
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