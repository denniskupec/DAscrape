# 2017 Dennis Kupec | MIT
# dascrape.py

import os, sys, shutil, re, requests, time
import xml.etree.ElementTree as ET


if len(sys.argv) < 2:
	exit("Usage: dascrape.py [username]")


feed = requests.get('http://backend.deviantart.com/rss.xml', params={
	'type': 'deviation',
	'q': 'by:' + sys.argv[1] + ' sort:time meta:all'
})

root = ET.fromstring(feed.text)


if not os.path.isdir(sys.argv[1]): # sanitizing is for chumps
	os.mkdir(sys.argv[1])
else:
	exit("Folder already exists.")


for work in root.iter('item'):
	id = work.find('link').text[-9:]
	title = re.sub('[^\w\-_\.\d]', '', work.find('title').text)
	url = work.find('{http://search.yahoo.com/mrss/}content') # namespace

	if url.get('medium') != "image": # links are their own type
		continue

	print("{0} [{1}].jpg".format(title, id))


	image = requests.get(url.get('url'), stream=True)
	image.raw.decode_content = True

	with open("{0}/{1} [{2}].jpg".format(sys.argv[1], title, id), "wb") as file: 
		shutil.copyfileobj(image.raw, file)

	del image

	time.sleep(0.1)

