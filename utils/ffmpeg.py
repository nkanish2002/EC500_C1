import subprocess


def create_movie(name, folder):
    """
    Creates the movie with all the images present in the given directory
    :param name:
    :param folder:
    :return: result of subprocess
    """
    cmd = ["ffmpeg", "-framerate", "1", "-i", folder + "/pic%04d.png", "-c:v",
           "libx264", "-r", "30", "-pix_fmt", "yuv420p", name]
    return subprocess.call(cmd)
