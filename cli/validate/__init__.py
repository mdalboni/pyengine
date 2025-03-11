import subprocess
import sys


def validate():
    """
    Validates the project. The specific validation steps are not implemented in this function.
    """
    cmd = 'python validate.py'
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=False)
    out, err = p.communicate()
    invalid_scenes = out.decode().split('#' * 10)[-2].split('\n')[1:-1]
    if invalid_scenes:
        print("The following scenes are invalid:")
        for scene in invalid_scenes:
            print(scene)
        print('Please check them...')
        sys.exit(-1)
