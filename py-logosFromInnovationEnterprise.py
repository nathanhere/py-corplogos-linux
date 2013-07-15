#### Author: Nathan N.
#### Date: 7.15.2013
#### This script was created to assist in the download of logos from the site:
#### http://theinnovationenterprise.com/summits/big-data-innovation-boston/speakers
#### Unparsed image list was accessed via the Chrome devtool console: document.images

import requests

r = requests

# urlList must be set by manually parsing the links into a list
urlList = []  # <--- Paste manually parsed urlList here

# The list copied from the Chrome console has non standard whitespace characters that must
# be removed (u2026 and u200b)
i = 0

for item in urlList:
	splititem = urlList[i].split(u'\u2026')
	joineditem = ''.join(splititem)
	splititem = joineditem.split(u'\u200b')
	joineditem = ''.join(splititem)
	urlList[i] = joineditem
	i += 1

for link in urlList:
	# Get the name of the image file for saving purposes
	notfound = True
	pos = 0
	while notfound:
		pos = link.find('/', pos)
		if pos >= 0:
			pos += 1
			loc = pos
		else:
			notFound = False
			break

	# Clean unnesessary characters in the original file name
	filename = link[loc:].replace('%26','').replace('%20','').replace('.001','')

	# Some file names did not have extensions--add .jpg if no extension was present
	if filename[-4:].lower() != '.jpg':
		filename += '.jpg'

	# Download actual image file
	data = r.get(link)

	# Save image file to disk
	with open(filename, 'wb') as f:
		f.write(data.content)
