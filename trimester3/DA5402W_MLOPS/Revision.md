

## Week 8 -- Version Control and Collaboration

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

THIS LECTURE DONE.