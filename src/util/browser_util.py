import subprocess


def open_url(url):
    subprocess.run('start ' + str(url), shell=True, capture_output=True)
