# Auto KCC

[![Docker Image amd64](https://github.com/mcarr823/auto-kcc/actions/workflows/docker-amd64.yml/badge.svg)](https://github.com/mcarr823/auto-kcc/actions/workflows/docker-amd64.yml)
[![Docker Image arm64](https://github.com/mcarr823/auto-kcc/actions/workflows/docker-aarch64.yml/badge.svg)](https://github.com/mcarr823/auto-kcc/actions/workflows/docker-aarch64.yml)

Auto KCC is a docker image which aims to make [KCC (Kindle Comic Converter)](https://github.com/ciromattia/kcc) easier to use in a headless environment.

It checks an input directory for any comic book archives, processes them based on the environment arguments supplied, then moves the results into the output directory.

## Architectures

x86_64 and ARM64 are both supported, with corresponding tags.

- auto-kcc:amd64
- auto-kcc:arm64

## Volumes

This program requires three volumes to be defined: input, output, and failed.

It can also take a fourth volume which points to the kindlegen binary, which is necessary for certain operations of KCC (for MOBI files, not EPUBs) to be performed.

| Volume         | Required         | Description |
| :----------- | :--------------: | :------------------------- |
| /input            | YES | Directory containing the comics to be converted         |
| /output           | YES | Directory into which the converted comics will be moved |
| /failed           | YES | Directory into which comics which couldn't be converted will be moved |
| /app/kindlegen:ro | NO  | kindlegen binary file |

For example:

`docker run --rm -v ./input:/input -v ./output:/output -v ./failed:/failed ghcr.io/mcarr823/auto-kcc:amd64`

## Profile

This program takes several optional arguments.

At the bare minimum, you should specify the PROFILE argument to tell KCC what type of device you're targeting.

See the [KCC documentation](https://github.com/ciromattia/kcc?tab=readme-ov-file#profiles) for a list of supported profiles.

## Environment variables

Arguments are passed to the docker container by using environment variables.

Most of them map directly to CLI arguments supported by KCC.

There are also a few arguments specific to this program.

### Variables for this program

| Variable  | Type    | Default value | Description   |
| :-------- | :------ | :------------ | :------------ |
| DRYRUN    | boolean | false         | List any comics this program finds, but don't actually convert or move them |
| QUIET     | boolean | false         | Disable any log messages   |
| TEST      | boolean | false         | Abort after the first file |

### Variables for KCC

See the [KCC documentation](https://github.com/ciromattia/kcc?tab=readme-ov-file#standalone-kcc-c2epy-usage) for explanations on what they all do.

* Boolean variables should be set to a lower-case string of 'true' to be enabled.

| Variable        | Type    | KCC flag          |
| :-------------- | :------ | :---------------- |
| PROFILE         | string  | --profile         |
| TITLE           | string  | --title           |
| FORMAT          | string  | --format          |
| MANGA           | boolean | --manga-style     |
| HQ              | boolean | --hq              |
| TWOPANEL        | boolean | --two-panel       |
| WEBTOON         | boolean | --webtoon         |
| NOPROCESSING    | boolean | --noprocessing    |
| UPSCALE         | boolean | --upscale         |
| STRETCH         | boolean | --stretch         |
| BLACKBORDERS    | boolean | --blackborders    |
| WHITEBORDERS    | boolean | --whiteborders    |
| FORCECOLOR      | boolean | --forcecolor      |
| FORCEPNG        | boolean | --forcepng        |
| MOZJPEG         | boolean | --mozjpeg         |
| MAXIMIZESTRIPS  | boolean | --maximizestrips  |
| DELETE          | boolean | --delete          |
| TARGETSIZE      | int     | --targetsize      |
| SPLITTER        | int     | --splitter        |
| CROPPING        | int     | --cropping        |
| BATCHSPLIT      | int     | --batchsplit      |
| CUSTOMWIDTH     | int     | --customwidth     |
| CUSTOMHEIGHT    | int     | --customheight    |
| GAMMA           | float   | --gamma           |
| CROPPINGPOWER   | float   | --croppingpower   |
| CROPPINGMINIMUM | float   | --croppingminimum |

## Docker compose

An example docker-compose.yml file has been provided in this repo.

It provides the required volumes and defines a few environment variables.

## Run automatically

This program works by scanning an input directory, processing files, then moving them to a different directory afterwards.

Since the input files get moved after running, it's safe to automate this process.

You are free to automate this in any fashion you want, but I would recommend writing a bash script and using crontab.

For example, let's say your docker-compose.yml file and your docker volumes are setup in `/home/user/containers/kcc`

You could write a bash script (run.sh) of:

```
#!/bin/bash

cd /home/user/containers/kcc
docker compose up
docker compose rm -f
```

And make it executable with `chmod +x run.sh`

That script would cd into the directory where the compose file and volumes are stored, run the program, then remove the image afterwards.

You could then set it up in crontab by running `crontab -e` and setting it up like so:

`0 1 * * * /home/user/containers/kcc/run.sh > /home/user/containers/kcc/log.txt`

That would run the program at 1AM every night and log any output to a log.txt file.

