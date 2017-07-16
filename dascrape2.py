# 2017 Dennis Kupec | MIT
# dascrape.py

import os, sys, shutil, re, requests, time
import xml.etree.ElementTree as ET


if len(sys.argv) < 2:
	exit("Usage: dascrape.py [username] <username...>")

if not os.path.isdir("data"):
	os.mkdir("data")

for a in sys.argv[1:]:
	feed = requests.get('http://backend.deviantart.com/rss.xml', params={
		'type': 'deviation',
		'q': 'by:' + a + ' sort:time meta:all'
	})

	root = ET.fromstring(feed.text)

	print("\n" + a)

	if not os.path.isdir("data/" + a): # sanitizing is for chumps
		os.mkdir("data/" + a)
	else:
		print("[!] Folder already exists.\n")
		continue


	for work in root.iter('item'):
		id = work.find('link').text[-9:] # ID is shorter sometimes, adds a hyphen
		title = re.sub('[^\w\-_\.\d]', '', work.find('title').text)
		url = work.find('{http://search.yahoo.com/mrss/}content') # namespace

		# links are their own type
		# and an odd case where NoneType is returned
		ptype = url.get('medium')
		if not ptype or ptype != "image":
			continue

		print("\t[{1}] {0}".format(title, id))


		image = requests.get(url.get('url'), stream=True)
		image.raw.decode_content = True

		with open("data/{0}/{1} [{2}].jpg".format(a, title, id), "wb") as file: 
			shutil.copyfileobj(image.raw, file)

		del image
		#time.sleep(0.065)

print("Done!")

