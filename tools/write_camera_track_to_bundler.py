
from pycolmapwrap import SceneManager

#-------------------------------------------------------------------------------

def main(args):
    scene_manager = SceneManager(args.input_folder)
    scene_manager.load_cameras()
    scene_manager.load_images()

    if args.sort:
        images = sorted(
            scene_manager.images.values(), key=lambda im: im.name)
    else:
        images = scene_manager.images.values()

    with open(args.output_file, "w") as fid:
        with open(args.output_file + ".list.txt", "w") as fid_filenames:
            fid.write("# Bundle file v0.3")
            fid.write(f"{len(images)} {0}")

            for image in images:
                fid_filenames.write(image.name)

                camera = scene_manager.cameras[image.camera_id]
                fid.write(f"{0.5 * (camera.fx + camera.fy)} {0} {0}")

                R, t = image.R(), image.t
                fid.write(f"{R[0, 0]} {R[0, 1]} {R[0, 2]}")
                fid.write(f"{-R[1, 0]} {-R[1, 1]} {-R[1, 2]}")
                fid.write(f"{-R[2, 0]} {-R[2, 1]} {-R[2, 2]}")
                fid.write(f"{t[0]} {-t[1]} {-t[2]}")

#-------------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Saves the camera positions in the Bundler format. Note "
        "that 3D points are not saved.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("input_folder")
    parser.add_argument("output_file")

    parser.add_argument("--sort", default=False, action="store_true",
        help="sort the images by their filename")

    args = parser.parse_args()

    main(args)
