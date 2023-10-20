"""
moved up from ../../tools
visualized point and camera positions

>>> from pycolmapwrap.tools import scene_draw
>>> scene_draw.raw(colmap_path, image_path)

colmap_path     contains cameras.bin  images.bin  points3D.bin
    colmap default stores in sparse/0/

image_path      contains images, not required for plotly viz

"""
import sys
import os.path as osp
import json
import numpy as np
import plotly.graph_objs as go
from .. import SceneManager



def raw(scene_path, image_path, min_track_length=10):
    """ Draws pycolmap raw scene
    """
    scene_manager = SceneManager(scene_path, image_path)
    scene_manager.load()
    scene_manager.filter_points3D(min_track_len=min_track_length)
    scene_manager.camera_positions = get_camera_positions(scene_manager.images)

    fig = go.Figure()
    fig.add_trace(go.Scatter3d(
        x=scene_manager.points3D[:, 0],
        y=scene_manager.points3D[:, 1],
        z=scene_manager.points3D[:, 2],
        mode='markers',
        marker=dict(size=2),
    ))
    fig.add_trace(go.Scatter3d(
        x=scene_manager.camera_positions[:, 0],
        y=scene_manager.camera_positions[:, 1],
        z=scene_manager.camera_positions[:, 2],
        mode='markers',
        marker=dict(size=2),
    ))

    fig.update_layout(scene_dragmode='orbit')
    fig.show()
    return scene_manager

def get_camera_positions(colmap_images, rotate=True):
    out = []
    for i in colmap_images:
        position = -(colmap_images[i].t @ colmap_images[i].R())
        if not rotate:
            position = colmap_images[i].t
        out.append(position)

    return np.stack(out)


def load_scene_manager(scene_path, image_path, min_track_length=10):
    scene_manager = SceneManager(scene_path, image_path)
    scene_manager.load()
    scene_manager.filter_points3D(min_track_len=min_track_length)
    scene_manager.camera_positions = get_camera_positions(scene_manager.images)
    return scene_manager

class Scene(SceneManager):
    def __init__(self,scene_path, image_path, min_track_length=10):
        super(Scene, self).__init__(scene_path, image_path)
        self.load()
        self.filter_points3D(min_track_len=min_track_length)


    @property
    def get_camera_positions(self):
        out = []
        for i in self.images:
            position = -(self.images[i].t @ self.images[i].R())
            out.append(position)
        np.stack(out)
        return np.stack(out)


# TODO : camera to nerf training batch
# directions, origins, pixels
# pixels = np.moveaxis(np.indices((height, width), dtype=np.float32)[::-1], 0, -1) + 0.5

    
class Camera:
    def __init__(self):
        self.position = None
        self.orientation = None
        self.height = 0.0
        self.width = 0.0
        self.fx = 0.0
        self.fy = 0.0
        self.cx = 0.0
        self.cy = 0.0

        self.k1 = 0.0
        self.k2 = 0.0
        self.k3 = 0.0
        self.p1 = 0.0
        self.p2 = 0.0

        self.skew = 0.0

    def __repr__(self):
        return self.__class__.__name__+ f"({self.__dict__})"

    def from_colmap_opencv(self, colmap_image, colmap_camera):
        """Open_CV type"""
        self.position = -(colmap_image.t @ colmap_image.R())
        self.orientation = colmap_image.R()
        self.__dict__.update(**{k:colmap_camera.__dict__[k] for k in
                                colmap_camera.__dict__ if k in self.__dict__})

    def to_nerf_sfm(self):
        return {
            "orientation":self.orientation,
            "position":self.position,
            "focal_length":self.fx,
            "pixel_aspect_ratio":self.fx/self.fy,
            "principal_point":np.array([self.cx,self.cy], dtype=np.float32),
            "radial_distortion":np.array([self.k1, self.k2, self.k3], dtype=np.float32),
            "tangential":np.array([self.p1, self.p2], dtype=np.float32),
            "skew":self.skew,
            "image_size":np.array([self.width, self.height], dtype=np.float32)
        }

    def from_nerf_sfm(self, cam):
        self.v = cam["orientation"]
        self.position = cam["position"]
        self.fx = cam["focal_length"]
        self.fy = self.fx/cam["pixel_aspect_ratio"]
        self.cx = cam["principal_point"][0]
        self.cy = cam["principal_point"][1]
        self.k1 = cam["radial_distortion"][0]
        self.k2 = cam["radial_distortion"][1]
        self.k3 = cam["radial_distortion"][2]
        self.p1 = cam["tangential"][0]
        self.p2 = cam["tangential"][1]
        self.skew = cam["skew"]
        self.width = cam["image_size"][0]
        self.height = cam["image_size"][1]


    def to_nerf_json(self,  name):
        nerf = self.to_nerf_sfm()
        for k in nerf:
            if isinstance(nerf[k], np.ndarray):
                nerf[k] = nerf[k].tolist()
        with open(name, 'w', encoding='utf8') as _fi:
            json.dump(_fi, nerf)

    def from_nerf_json(self, name):
        with open(name, 'r', encoding='utf8') as _fi:
            nerf = json.load(_fi)
        self.from_nerf_sfm(nerf)

def get_folders(root):
    images = osp.join(root, "rgb-raw")
    scene = osp.join(root, "colmap/sparse/0")
    assert osp.isdir(images), f"image dir {images} not found"
    assert osp.isdir(scene), f"scine dir {scene} not found"
    return images, scene



if __name__ == "__main__":

    raw(*get_folders(sys.argv[1]))
