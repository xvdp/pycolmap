"""as used by nerfies

"""
from posix import listdir
import subprocess as sp
import os
import os.path as osp
import numpy as np
from kotools import ObjDict
from vidi import FF

from pycolmap import SceneManager



class VideoCalibration:
    def __init__(self, project_path, video_path=None, **kwargs):
    
        self.paths = ObjDict(project_path=project_path, video_path=video_path)
        self.scene = None
        self.state = ObjDict(images=False, features=False, points=False)

        self.make_project(**kwargs)

    def make_project(self, image_path="images", colmap_path="colmap", out_path="sparse"):
        """ create paths
        video path
        colmap_path, image_path
        """
        self.paths.images = osp.join(self.paths.project_path, image_path)
        self.paths.colmap = osp.join(self.paths.project_path, colmap_path)
        self.paths.out = osp.join(self.paths.colmap,out_path)

        for key in ["images", "colmap", "out"]:
            os.makedirs(self.paths[key], exist_ok=True)

        self.paths.database = osp.join(self.paths.colmap, 'databse.db')
        self.paths.scenes = sorted([f.path for f in os.scandir(self.paths.out) if f.is_dir()])
        self.paths.scene = None if not self.paths.scenes else self.paths.scenes[-1]


        if os.listdir(self.paths.images):
            self.state.images = True
            if osp.isfile(self.paths.database):
                self.state.features = True
                if self.paths.scene is not None:
                    self.state.points = True

    def import_video(self, nb_frames=100, scale=1):
        """ """
        vid = FF(self.paths.video_path)
        stats = vid.get_video_stats()
        step = 1
        if nb_frames is not None and nb_frames < stats["nb_frames"]:
            step = stats["nb_frames"] // nb_frames
        vid.export_frames(step=step, out_name=osp.join(self.paths.images, '%06d.png'), scale=scale)
        return self.paths.images

    def extract_features(self, use_gpu=0, upright=1, camera_model="OPENCV", single_camera=1, overwrite=False):
        """ """
        if osp.isfile(self.paths.database):
            if not overwrite:
                print("database found, to overwrite, pass arg 'overwrite'=True")
                return self.paths.database
            else:
                os.remove(self.paths.database)

        cmd = ["colmap", "feature_extractor", "--SiftExtraction.use_gpu", str(use_gpu), "--SiftExtraction.upright", str(upright)]
        cmd += ["--ImageReader.camera_model", camera_model, "--ImageReader.single_camera", str(single_camera)]
        cmd += ["--database_path", self.paths.database, "--image_path", self.paths.images]

        sp.Popen(cmd, stdin=sp.PIPE, stderr=sp.PIPE)
        print("created database", self.paths.database, osp.isfile(self.paths.database))
        return self.paths.database

    def match_features(self, use_gpu=0):
        cmd = ["colmap", "exhaustive_matcher", "--SiftMatching.use_gpu", str(use_gpu), "--database_path", self.paths.database]
        sp.Popen(cmd, stdin=sp.PIPE, stderr=sp.PIPE)
        self.state.features = True
        return self.paths.database

    def map_features(self, refine_principal_point=1, filter_max_reproj_error=2, tri_complete_max_reproj_error=2, min_num_matches=32):
        """"""
        self.paths.scenes = sorted([f.path for f in os.scandir(self.paths.out) if f.is_dir()])

        cmd = ["colmap", "mapper", "--Mapper.ba_refine_principal_point", str(refine_principal_point)]
        cmd += ["--Mapper.filter_max_reproj_error", str(filter_max_reproj_error)]
        cmd += ["--Mapper.tri_complete_max_reproj_error", str(tri_complete_max_reproj_error)]
        cmd += ["--Mapper.min_num_matches", str(min_num_matches)]
        cmd += ["--database_path", self.paths.database, "--image_path", self.paths.images, "--output_path", self.paths.out]
        sp.Popen(cmd, stdin=sp.PIPE, stderr=sp.PIPE)

        new = [f.path for f in os.scandir(self.paths.out) if f.path not in self.paths.scenes]
        self.paths.scene = new[0]
        self.paths.scenes.append(self.paths.scene)
        self.state.points = True

        return self.paths.scene

    def get_scenemanager(self, min_track_length=10):
        """
            _images = list(self.scene.images.keys())
            _cameras = list(self.scene.cameras.keys())

            # intrinsics for first camera
            _firscam = self.scene.images[_images[0]]
            _camid = _firscam.camera_id
            self.scene.cameras[_camid]
            self.scene.cameras[_camid].__dict__


            # extrinsics
            _firscam.t, _firscam.R()

        """
        self.scene = SceneManager(self.paths.scene, self.paths.images)
        self.scene.load()
        self.scene.filter_points3D(min_track_len=min_track_length)

        self.camera_indices = list(self.scene.images.keys())
        ## camera intrinsics
        # self.scene.cameras[1].__dict__

        ## info

        # self.scene.images[1].__dict__.keys()

        # self.scene.images[1].R() # rotation
        # self.scene.images[1].t   # translation
        # self.scene.images[1].camera_id # rotation

    # def get_camera(self, index):
    #     assert index in self.camera_indices, f"index {index} not in {self.camera_indices}"
    #     camere_id = self.scene.images[index].camera_id #
    #     # > intrinsics




    