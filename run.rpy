#!/env/python3

from pathlib import Path, PurePosixPath
from subprocess import Popen, PIPE

# If True, don't actually convert or delete any files
dryRun = True

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

# Types of files to convert
fileExtensions = ["cbz", "zip"]

# Docker command to run in order to convert the comics
cmd = [
 'docker',
 'run',
 '--rm',
 '-v',
 '-v',
 f'./{inputDirectory}:/input',
 f'ghcr.io/ciromattia/kcc:{kccVersion}'
]
inputPath = Path(inputDirectory)

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
		for f in filesToConvert:
			cmd.append(f'/{str(f)}')
			# Then run the command. Or not, if dryRun is True
			if not dryRun:
				process = Popen(cmd, stdout=PIPE)
				output, error = process.communicate()
			cmd.pop()
