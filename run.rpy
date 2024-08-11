#!/env/python3

from pathlib import Path, PurePosixPath
from subprocess import Popen, PIPE
from re import sub
from os import environ

# If True, don't actually convert or delete any files
dryRun = True

# If True, don't print any messages from this script
quiet = False

# For testing purposes only.
# Only converts the first file, then aborts afterwards.
breakAfterFirst = False

# If True, convert the files one at a time.
# If False, do them all in one go.
# Converting them one at a time is slower, but you'll
# be able to see the progress as it runs, and files
# will appear in the output directory one at a time
# instead of all in one go.
oneAtATime = True

# Version of KCC docker image to use.
# Note that this probably won't be up to date, since
# KCC currently has some issues with the docker build
# process which require manual intervention to build
# properly. So the "latest" tag currently breaks regularly.
kccVersion = "5.6.5"

# Directory containing the files to be converted.
# Must currently be a relative directory with a single
# directory in the path.
# eg. "input" is valid, but "/home/user/input" and
# "input/src" are not.
# TODO: add support for multiple directories and absolute
# file paths.
inputDirectory = "input"

# Directory to move the converted files to.
# Can be absolute or relative.
outputDirectory = "output"

# Directory to move input files into if the conversion
# fails.
# Can be absolute or relative.
# Can be set to an empty string if you don't want to
# move the problem files.
# Moving the files to a failed directory is useful if
# this script is automated, so that problem files aren't
# kept in the input directory and re-processed.
failedDirectory = "failed"

# Directory containing the kindlegen binary file.
# The kindlegen binary is usually optional.
# If you aren't using one, just create an empty directory
# and assign that.
kindlegenDirectory = "binary"

# Types of files to convert
fileExtensions = ["cbz", "zip"]

# Docker command to run in order to convert the comics
cmd = [
 'docker',
 'run',
 '--rm',
 '-v',
 f'./{kindlegenDirectory}:/app',
 '-v',
 f'./{inputDirectory}:/input',
 f'ghcr.io/ciromattia/kcc:{kccVersion}'
]

def getBool(key):
	return key in environ and environ[key] == 'true'

def getNumber(key):
	return int(environ[key]) if key in environ else -1

def getString(key):
	return environ[key] if key in environ else ""
# Convert input and output directories to paths
inputPath = Path(inputDirectory)
outputPath = Path(outputDirectory)

# List containing any detected files of the right type
filesToConvert = []

# Look for any files of the expected extensions.
# This is a recursive search
for ext in fileExtensions:
	pathlist = inputPath.glob(f'**/*.{ext}')
	for path in pathlist:

		# Append the file to the list of files to convert
		filesToConvert.append(path)


# If there's at least one file to convert, then...
if len(filesToConvert) > 0:

	if not oneAtATime:

		# Start by appending the input files to the end of the docker command
		for f in filesToConvert:
			cmd.append(f'/{str(f)}')

		if not quiet:
			print(f"Running: {cmd}")

		# Then run the command. Or not, if dryRun is True
		if not dryRun:
			process = Popen(cmd, stdout=PIPE)
			output, error = process.communicate()

	for f in filesToConvert:

		if oneAtATime:

			cmd.append(['--output', outputDirectory])
			cmd.append(f'/{str(f)}')

			if not quiet:
				print(f"Running: {cmd}")

			# Then run the command. Or not, if dryRun is True
			if not dryRun:
				process = Popen(cmd, stdout=PIPE)
				output, error = process.communicate()

			cmd.pop()
			cmd.pop()
			cmd.pop()

		# For each of the converted files, figure out the file paths of the
		# converted .epub (`inEpub`) and the target filepath (`outEpub`)
		# should be.
		# There's probably a better way to do this...
		inEpub = PurePosixPath(inputDirectory)
		outEpub = PurePosixPath(outputDirectory)
		for d in f.parts[1:-1]:
			inEpub = inEpub.joinpath(d)

		# Remove any sequences of non-alphanumeric chars and replace them
		# with a single underscore.
		# eg. "test (20)" would become "test_20_"
		# This is to match the way KCC renames files.
		filename = sub('([^\\w])+', '_', f.stem)

		inEpub = inEpub.joinpath(f"{filename}.kepub.epub")
		outEpub = outEpub.joinpath(f"{filename}.epub") # Removed .kepub while moving
		inEpub = Path(inEpub)
		outEpub = Path(outEpub)

		if inEpub.exists():
			# If inEpub exists, then the conversion was successful

			if not quiet:
				print("epub exists")

			# Move the .epub file from inputDir to outputDir
			inEpub.rename(outEpub)

		else:
			# If inEpub doesn't exist, then the conversion must have failed.
			# Report the error, or move the input file, or do some other thing
			# to flag the failure.
			if not quiet:
				print(f"epub does not exist {str(inEpub)}")

			if len(failedDirectory) > 0:
				failedFile = PurePosixPath(failedDirectory + "/" + str(f.parts[-1]))
				failedFile = Path(failedFile)
				if not dryRun:
					f.rename(failedFile)
		if breakAfterFirst:
			break
