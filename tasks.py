from invoke import task


@task
def serve(c, debug=False):
    """Run server"""
    cmd = "uvicorn api:api"
    if debug:
        cmd = " ".join([cmd, "--debug"])
    with c.cd("librarian/"):
        c.run(cmd)
