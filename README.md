# Auto KCC


Auto KCC is a docker image which aims to make [KCC (Kindle Comic Converter)](https://github.com/ciromattia/kcc) easier to use in a headless environment.

It checks an input directory for any comic book archives, processes them based on the environment arguments supplied, then moves the results into the output directory.

## Architectures

x86_64 and ARM64 are both supported, with corresponding tags.

- kcc-watch-dir:amd64
- kcc-watch-dir:arm64

## Volumes

This program requires three volumes to be defined: input, output, and failed.

It can also take a fourth volume which points to the kindlegen binary, which is necessary for certain operations of KCC (for MOBI files, not EPUBs) to be performed.

| Volume         | Required         | Description |
| :----------- | :--------------: | :------------------------- |
| /input            | YES | Directory containing the comics to be converted         |
| /output           | YES | Directory into which the converted comics will be moved |
| /failed           | YES | Directory into which comics which couldn't be converted will be moved |
| /app/kindlegen:ro | NO  | kindlegen binary file |

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
