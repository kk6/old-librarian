from invoke import task


@task
def serve(c, debug=False):
    """Run uvicorn"""
    cmd = "uvicorn api:api"
    if debug:
        cmd = " ".join([cmd, "--debug"])
    with c.cd("librarian/"):
        c.run(cmd)


@task
def debug(c):
    """Run server with debug mode"""
    cmd = "python api.py"
    with c.cd("librarian/"):
        c.run(cmd)


@task
def download(c):
    """Download book data from openBD"""
    with c.cd("librarian/"):
        c.run("python download.py")
