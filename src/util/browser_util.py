import subprocess


def open_url(url):
    # os.system('start ' + str(url))
    subprocess.run('start ' + str(url), shell=True, capture_output=True)
