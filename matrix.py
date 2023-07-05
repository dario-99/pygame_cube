import numpy as np

# Rotation matrix Function
def rotation_matrix(yaw, pitch, roll):
    R_z = np.array(
        [
            [np.cos(yaw), -np.sin(yaw), 0],
            [np.sin(yaw),  np.cos(yaw), 0],
            [          0,            0, 1]
        ]
    )
    R_y = np.array(
        [
            [ np.cos(pitch), 0, np.sin(pitch)],
            [             0, 1,             0],
            [-np.sin(pitch), 0, np.cos(pitch)]
        ]
    )
    R_x = np.array(
        [
            [1,            0,             0],
            [0, np.cos(roll), -np.sin(roll)],
            [0, np.sin(roll),  np.cos(roll)]
        ]
    )
    R = R_z @ R_y @ R_x

    return R

def extrinsic_matrix(R, C):
    '''
        IN:
            R: translation matrix (3x3)
            C: Camera position in world coordinate frame (3x1)
    '''
    return R @ np.concatenate([np.eye(3), -C], axis=1)

def intrinsic_matrix(focal_lenght, u0=0, v0=0, skew=0):
    return np.array(
        [
            [focal_lenght,         skew, u0],
            [           0, focal_lenght, v0],
            [           0,            0,  1]
        ]
    )