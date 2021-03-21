import subprocess

# TODO unit test
def get_max_characters():
    try:
        name_max = subprocess.check_output("getconf NAME_MAX /", shell=True)
        path_max = subprocess.check_output("getconf PATH_MAX /", shell=True)

        return name_max, path_max
    except (ValueError, subprocess.CalledProcessError, OSError):
        # TODO log
        print('calling getconf failed - error:', traceback=True)
