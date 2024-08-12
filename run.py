#!/env/python3

from pathlib import Path, PurePosixPath
from subprocess import Popen, PIPE
from os import environ

def getBool(key):
	return key in environ and environ[key] == 'true'

def getNumber(key):
	return int(environ[key]) if key in environ else -1

def getString(key):
	return environ[key] if key in environ else ""

# If True, don't actually convert or delete any files
dryRun = getBool('DRYRUN')

# If True, don't print any messages from this script
quiet = getBool('QUIET')

# For testing purposes only.
# Only converts the first file, then aborts afterwards.
breakAfterFirst = getBool('TEST')

# If True, convert the files one at a time.
# If False, do them all in one go.
# Converting them one at a time is slower, but you'll
# be able to see the progress as it runs, and files
# will appear in the output directory one at a time
# instead of all in one go.
oneAtATime = False

# Types of files to convert
fileExtensions = ["cbz", "zip"]

# Directory into which the exported files should go
outputDirectory = "/output"

# Docker command to run in order to convert the comics
cmd = [
 'python3', '/opt/kcc/kcc-c2e.py',
 '--output', outputDirectory
]


# KCC arguments
# See https://github.com/ciromattia/kcc?tab=readme-ov-file#standalone-kcc-c2epy-usage
profile = getString('PROFILE')
if len(profile) > 0:
	cmd.extend(['--profile', profile])

title = getString('TITLE')
if len(title) > 0:
	cmd.extend(['--title', title])

fmt = getString('FORMAT')
if len(fmt) > 0:
	cmd.extend(['--format', fmt])

if getBool('MANGA'):
	cmd.extend(['--manga-style'])

if getBool('HQ'):
	cmd.extend(['--hq'])

if getBool('TWOPANEL'):
	cmd.extend(['--two-panel'])

if getBool('WEBTOON'):
	cmd.extend(['--webtoon'])

if getBool('NOPROCESSING'):
	cmd.extend(['--noprocessing'])

if getBool('UPSCALE'):
	cmd.extend(['--upscale'])

if getBool('STRETCH'):
	cmd.extend(['--stretch'])

if getBool('BLACKBORDERS'):
	cmd.extend(['--blackborders'])

if getBool('WHITEBORDERS'):
	cmd.extend(['--whiteborders'])

if getBool('FORCECOLOR'):
	cmd.extend(['--forcecolor'])

if getBool('FORCEPNG'):
	cmd.extend(['--forcepng'])

if getBool('MOZJPEG'):
	cmd.extend(['--mozjpeg'])

if getBool('MAXIMIZESTRIPS'):
	cmd.extend(['--maximizestrips'])

if getBool('DELETE'):
	cmd.extend(['--delete'])

targetsize = getNumber('TARGETSIZE')
if targetsize >= 0:
	cmd.extend(['--targetsize', targetsize])

splitter = getNumber('SPLITTER')
if splitter >= 0:
	cmd.extend(['--splitter', splitter])

gamma = getNumber('GAMMA')
if gamma >= 0:
	cmd.extend(['--gamma', gamma])

cropping = getNumber('CROPPING')
if cropping >= 0:
	cmd.extend(['--cropping', cropping])

croppingpower = getNumber('CROPPINGPOWER')
if croppingpower >= 0:
	cmd.extend(['--croppingpower', croppingpower])

croppingminimum = getNumber('CROPPINGMINIMUM')
if croppingminimum >= 0:
	cmd.extend(['--croppingminimum', croppingminimum])

batchsplit = getNumber('BATCHSPLIT')
if batchsplit >= 0:
	cmd.extend(['--batchsplit', batchsplit])

customwidth = getNumber('CUSTOMWIDTH')
if customwidth >= 0:
	cmd.extend(['--customwidth', customwidth])

customheight = getNumber('CUSTOMHEIGHT')
if customheight >= 0:
	cmd.extend(['--customheight', customheight])

# Convert input and failed directories to paths
inputPath = Path("/input")
failedDir = Path("/failed")

# List containing any detected files of the right type
filesToConvert = []

# Look for any files of the expected extensions.
# This is a recursive search
for ext in fileExtensions:
	pathlist = inputPath.glob(f'**/*.{ext}')
	for path in pathlist:

		# Append the file to the list of files to convert
		filesToConvert.append(path)

if len(filesToConvert) == 0:
	if not quiet:
		print("No input files found - Aborting")
	exit()

else:

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

			cmd.append(f'/{str(f)}')

			if not quiet:
				print(f"Running: {cmd}")

			# Then run the command. Or not, if dryRun is True
			if not dryRun:
				process = Popen(cmd, stdout=PIPE)
				output, error = process.communicate()

			cmd.pop()

		# Filename minus the extension
		filename = f.stem

		# For each of the converted files, figure out the file paths of the
		# converted .epub (`inEpub`) and the target filepath (`outEpub`)
		# should be.
		inEpub = Path(f"{outputDirectory}/{filename}.kepub.epub")

		if inEpub.exists():
			# If inEpub exists, then the conversion was successful

			if not quiet:
				print(f"Success: {filename}")

			# Change the .kepub.epub extension to just plain .kepub
			# This is to stop both ebook management software (eg. Calibra)
			# and Kobo devices themselves from mistaking the KEPUB file
			# for a plain old EPUB file.
			# This is mostly important for ensuring that the comic isn't
			# converted twice.
			outEpub = Path(f"{outputDirectory}/{filename}.kepub")
			inEpub.rename(outEpub)

		else:
			# If inEpub doesn't exist, then the conversion must have failed.
			# Report the error and move the input file to flag the failure.
			if not quiet:
				print(f"Failure: {filename}")

			if not dryRun:
				f.rename(failedDir)

		if breakAfterFirst:
			break
