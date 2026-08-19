# Janeway

This repository implements USMAI's lightly-customized version of the Janeway open publishing platform. All changes to
Janeway currently are in the realm of styling. This includes a few additional database fields which store information -
the hero image, homepage h1 text, and the optional slogan.

> [!TIP]
> If maintaining a forked Janeway version for style purposes only becomes cumbersome, it would be
> possible to maintain subthemes for each campus instead which would be added to the docker image.
> This approach would be more involved to deploy & the themes would be more complicated to update,
> BUT it would allow us to use Janeway's source code as is. This argument goes away as soon as we
> want to make other changes to Janeway source code.

## Branch Structure

This repository has two important branches: `main` and `janeway-master`. The `main` branch is what you would expect -
the default branch of the repository where production-ready changes should be merged.

The `janeway-master` branch tracks the official Janeway repository's `master` branch. HOWEVER, we should NOT be
synchronizing it with Janeway's master branch. Rather, we should be pulling changes from Janeway's release branches
(e.g., `r-v1.9.x`).

### Recommended Local Git Setup

```
origin  git@github.com:umd-lib/janeway.git (fetch)
origin  git@github.com:umd-lib/janeway.git (push)
upstream        https://github.com/openlibhums/janeway.git (fetch)
upstream        DISABLE (push)
```

## Synchronization Steps

For a full guide on the Janeway upgrade process, please see
the [Janeway Version Upgrade section](#janeway-version-upgrade). In overview, the sync process for upgrading our fork to
the latest Janeway version goes like so:

1. Note the latest commit hash on `main`.
2. Switch to `janeway-master`.
3. Fetch the latest changes with `git fetch`. Do NOT pull, as this will attempt to merge in master!
4. Still on `janeway-master`, merge in the desired feature branch.
5. Push your changes to GitHub.
6. Switch to `main`.
7. Merge in the `janeway-master` branch, resolving any merge conflicts.
8. The commit hash you noted in step 1 will be used to assess what template changes must be made.

### Release Naming

Releases (or rather, the tags that the releases are based on) MUST be named in a specific format, as the dockerfile
publishing action uses the release name to match the Janeway release to use.

An example release name is: `v1.8.0.usmai.0`

The first major-minor-patch string (`v1.8.0`) must match the underlying Janeway release version. The `.usmai` suffix is
used to tell the docker publishing workflow to publish this to OUR docker image repository, not the open-source
repository. Lastly, the trailing integer `.0` is the number used to track our changes. If we make change to this
repository without upgrading the underlying Janeway version, this is the number we should increment. You must reset the
number to `0` when upgrading the underlying Janeway version.

## Local Testing

Local testing uses Janeway's built-in docker-compose setup.

1. In `./db`, create the file `janeway.sqlite3` if not already done.
2. Run `make janeway`.
3. Shell into the web container that eventually comes up.
4. Run the command `src/manage.py install`.
5. When complete, view the Janeway application on localhost.
6. Log in to Janeway as the superuser.
7. Go to the press manager.
8. Under press settings, select the USMAI theme, upload a hero from the shared CLAS drive, add h1 text, and add a press
   logo.
9. Save these changes and go back to the press home. View that they look as expected. Understand that not all styling is
   going to look as you want, as the last styling step is to upload campus-specific CSS using the customstyling plugin,
   which is added in the janeway-warpspeed docker image.

## Janeway Version Upgrade

Upgrading Janeway versions is a multi-step process, but is reasonably straightforward. These steps take place over 4
repositories - this
repository, [USMAI's janeway-warpspeed docker repository](https://github.com/USMAI-Library-Consortium/janeway-warpspeed),
[USMAI's janeway-collective helm chart repository](https://github.com/USMAI-Library-Consortium/janeway-collective), and
UMD's private k8s-janeway repository.

### 1: Upgrading the Forked Janeway Version

1. Follow the instructions in the [Synchronization Steps section](#synchronization-steps)
2. Update the USMAI subtheme with the following steps:
3. Note each HTML file in the [USMAI subtheme](./src/themes/usmai)
4. We will then see what changes the Janeway team has made to each HTML file, and determine whether we should port these
   changes to our subtheme:
5. For each HTML file, navigate to its overridden _counterpart_ [in the OLH theme](./src/themes/OLH), if present, in the
   terminal. It will be in the same relative file location as it is in our theme.
6. Compare the file as it was in the previous version of Janeway we were using, which our subtheme is based on, to the
   version from the fresh version of Janeway. Use the command `git diff old_commit_hash HEAD path/to/html/file.html`.
   This method is a convenience, but you can compare the files any way you prefer.
7. Port all changes over to the subtheme, unless the changes contradict. Some may have to be adapted to match our
   styling changes.
8. Check plugin versions in plugins.txt to see whether a new version of a plugin has been published.
9. Test Janeway using the [local testing instructions](#local-testing)
10. Commit your changes & push them to GitHub.
11. Wait for GitHub Actions to finish running the built-in tests (estimated time ~6 min)
12. Create a new release/tag using the [release naming instructions](#release-naming)

### 2: Upgrading the Docker Image

The docker repository probably won't have to have too many changes between versions, but we do want to keep our eye on
changes to the upgrade process or how Janeway uses environment variables.

1. In the forked Janeway repository (not the docker repository), compare the incoming `.update.sh` script to the old
   version with `git diff b06a4d3 HEAD .update.sh`. Any modifications should be reflected in janeway-warpspeed's
   `commands/upgrade.py` script.
2. Do a similar process for `src/core/janeway_global_settings.py`. Many of these are internal configuration and as such
   do not need to be ported, but there may be some external settings that you might be interested in or some environment
   variables that are changing. This file sets the default settings for Janeway which are then selectively overridden by
   prod_settings.py
3. Test the Janeway application using the instructions included in the janeway-warpspeed repository. You can save
   extensive testing for the Kubernetes test instance, however you many want to test things here that you think might
   not work as it takes a long time to build each image to test on Kubernetes (~40min)
4. Once you are satisfied that the application is likely to work properly, create a new release using the release naming
   instructions in the janeway-warpspeed repository. Release only the USMAI version for now.
5. Wait for the build to complete (~40 minutes)

### 3: If Needed, Update the janeway-collective Helm Chart

Unlike the Docker image, the helm chart does not inherently need updating when you upgrade the Janeway version. You will
want to update it if there's something included with the new Janeway release that requires a deployment config update -
a new cron job, environment variable, etc.

If you make changes, create a release with a release candidate version tag. Remember to update the version in Chart.yaml
before pushing, as that's what will show up in the helm chart repository!

### 4: Kubernetes Cluster Testing

Open the k8s-janeway repository. If you've introduced any new helm changes, update the subchart janeway-umd to use the
new helm chart release candidate. Update whichever helmfile release you're using to use the latest USMAI Janeway docker
image. Go through standard testing procedures, releasing subsiquent fork / docker / helm chart revisions as needed.

### 5: Finish Releasing

Once you are ready to move to production, please do the following steps alongside standard SSDR upgrade procedures:

1. Publish the open-source version of janeway-warpspeed by creating a new 'base' release. The instructions on
   janeway-warpspeed describe this procedure.
2. Update the janeway-collective Helm Chart to a production release (droppign the release candidate tag), while also
   modifying the code in helpers.tpl to select the tag of the new _open source_ docker image. This should happen
   regardless of whether there's been modifications to the Helm Chart (unless we start using the docker 'latest'
   feature.)