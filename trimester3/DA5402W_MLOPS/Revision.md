

## Week 8

### Version Control and Collaboration

ML Experiment = Code + Data + Configuration + Environment + Randomness

Code (git), Data (dvc / git lfs), Model versioned together (dvc / git lfs / model registry)

Git merge conflict: No fast forward VS fast forward VS squash commits

Git flow (long-lived main, develop, release-candidate branches) VS Github flow (main + feature branches merged in PR) VS Trunk based flow (direct commits to main, needs strong CI, short-lived branches - similar to Github flow)

* keep data (version, preprocessing etc.) and model changes on separate branches - i.e. DON'T change both at once in same branch
* Released models marked with *annotated tags* (immutable pointers to exact commit) - combined with DVC, pins code + data + config - fully reproducible model

Git LFS:

```bash
$ sudo apt install git-lfs

# init repo
$ git lfs install && git add .gitattributes
$ git lfs track "*.pt"

# git add; commit; push

$ git lfs ls-files
$ git lfs status
$ git lfs pull --include="models/production/*"   
$ GIT_LFS_SKIP_SMUDGE=1 git clone <repo>         # clone without pulling LFS objects
$ git lfs migrate import --include="*.pt" --everything && git push --force     # migrate existing repo. WARNING: rewrites history
$ git lfs prune
```

DVC extra features over Git LFS:
- Git LFS tied to Github (free tier has 1 GB storage + 1 GB / month bandwidth), in DVC you have to choose your own remote (Google Drive, AWS S3 or other cloud, self-hosted or local setup)
   - NOTE: Google Drive remote of dvc doesn't actually work! "Access to this app is blocked by Google". They say to instead "create a new app" - that basically means Google Cloud which is also paid :(
     So doesn't look useful for me.
- Has directory of *shards*, train / validation / test split, data lineage
- Experiment / stage awareness (this data produced this model via this step)
- Cloud: data governance, egress cost, access control

DVC:

```bash
$ pip install dvc       # or: pip install "dvc[s3]"
$ dvc init && git commit
$ dvc remote add -d myremote PATH   # PATH is: s3://mybucket/mypath , or: (local folder) /path/to/folder , or different remote path

$ dvc add data/raw/some_file.csv    
$ git add data/raw/some_file.csv.dvc data/raw/.gitignore && git commit -m 'add data'  # commit DVC generated files

# in addition to (NOT replacement) for git push, git pull
$ dvc push        # upload to remote
$ dvc pull        # run on fresh clone

$ dvc install     # installs git hook pre-push so that `dvc push` auto runs before `git push`. But `dvc pull` must still be run seperately

$ git checkout COMMIT_ID_OR_BRANCH
$ dvc checkout
```

DVC pipeline *dvc.yaml* (run with `dvc repro` only the changed parts, or do nothing if no change - internally DVC builds a dependency graph) :

```yaml
stages:
    prepare:
        cmd: command
        deps: [dep_file1, dep_file2]
        outputs: [out_file1, out_file2]
    train:
        cmd: command
        deps: [dep1, dep2]
        outputs: [out1, out2]
```

How does `dvc repro` know if anything changed? Via auto-generated *dvc.lock* file - it records hashes of every stage's params, deps, outs.
*dvc.lock* and *dvc.yaml* - committed to git - together pin the pipeline.

`dvc exp` lets you experiment without branch clutter using "hidden" commits.
- `dvc exp show` shows metrics-vs-params comparision table.
- reproducible experiments: each experiment records params and links to the dvc.lock file that produced it.

DVC pipeline example: `dvc stage add -n prepare -d src/prepare.py -o data/dataset.csv python src/prepare.py`

### Container Orchestration

Process Virtualization (eg. Java JVM) vs System Virtualization (heavy-weight full VMs on Hypervisor on Host OS on Physical Machine)

Containers: light VMs without guest OS, Isolation between processes, using:
* Namespaces: isolated view of file system, network resources, process table etc.
* cgroups: Resource limits per process / container

Docker:
* server daemon and client
* Image (eg. from Docker Registry) and Container
* Docker Networking: networking between containers eg. bridge

Docker Alternatives: Buildah (build container images for Podman as it can't do it itself), RunC, LXC, Podman (daemon-less, systemd integration), Kaniko

```bash
$ docker pull python:3.7
$ docker run nginx
$ docker inspect CONTAINER_ID_OR_NAME       # outputs a very detailed JSON about container, including running status, ports, networks, environment variables etc.
$ docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" | sort -hr -k 3   # find docker images taking most disk space
$ docker history IMAGE_ID_OR_NAME        # shows all image layers -- can see from this which layer takes most memory spaces
$ docker system prune -a      # delete all images

# publish Docker image:
# 1. Log in (use a Quay robot account token, not your password)
docker login quay.io -u <quay-username>
# Password prompt
# 2. Tag for Quay: quay.io/<namespace>/<repo>:<tag>
docker tag ml-app:v1 quay.io/myorg/ml-app:0.1.0
# 3. Push

docker ps # containers currently running
docker ps -a # all containers, including stopped ones
docker run -it ubuntu bash # start an interactive Ubuntu shell in a container
docker build -t myapp . # build an image from a Dockerfile in the current directory
docker stop <container_id> # stop a running container
docker rm <container_id> # remove a stopped container
docker rmi <image_id> # remove an image
docker logs <container_id> # view a container's output
```

See cpu, memory etc. stats of running Docker containers:

```bash
$ docker stats
CONTAINER ID   NAME          CPU %     MEM USAGE / LIMIT   MEM %     NET I/O         BLOCK I/O   PIDS
5c83c9038e1c   happy_gauss   0.00%     956KiB / 219.7GiB   0.00%     1.05kB / 126B   0B / 0B     1
```

Docker Compose -- allows running multi-container apps (you specify multiple docker images and it brings them all up. Sets up a single network, all containers join in it so they can communicate.)

Dockerfile -- each RUN, COPY, ADD is a new layer; layer captures only file system diff from previous layer; layers are shared across images

When container is run, a new writeable container layer is created while all other layers remain read-only

Build image with Dockerfile & run container on port 8000:

```bash
docker build -t ml-app:v1 . 
docker run -d --name mycontainer1 -p 8000:8000 ml-app:v1
```

ADDITIONAL ASIDE: In Dockerfile `FROM scratch` -- scratch isn't an actual image but a built-in keyword that basically means, empty image using just the linux kernel. Distro images like ubuntu start from this, and import rootfs and add other basic needed utilities.


## Week 6 is Code only -- Mlflow, Ray

Mlflow (start mlflow server with `mlflow ui`)

```python
mlflow.set_experiment("name")          # create / switch experiment
with mlflow.start_run(run_name="..."):       # open a run context
  mlflow.log_param("k", v)            # one hyperparameter
  mlflow.log_metric("rmse", 1.23)     # one scalar metric
  mlflow.log_metric("loss", v, step=i)# metric series (convergence curve)
  mlflow.log_artifact("file.png")     # attach any file
  mlflow.sklearn.log_model(m, "model")# serialise + store model
  mlflow.set_tag("env", "dev")        # searchable label
mlflow.autolog()                       # auto-instrument library
mlflow.search_runs(experiment_ids=[]) # DataFrame of all runs
mlflow.sklearn.load_model("runs:/id/model")     # reload model
mlflow.register_model(uri, name)      # add to Registry
client.transition_model_version_stage(...)      # promote to Staging/Production
mlflow.sklearn.load_model("models:/name/stage") # load from Registry
```

TODO: skipped Ray code notebook
