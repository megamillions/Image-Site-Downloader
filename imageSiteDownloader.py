#! python3
# imageSiteDownloader.py - Goes to your favorite image site,
# then downloads specified search results of images.

import bs4, os, requests, sys

# Cap number of images to open, as necessary.
cap = 5

# Abort script if no search terms passed in argument.
if len(sys.argv) < 2:
	print('Please enter your search terms in the argument and try again.')
	quit()

# Edit relevant Unsplash URLs and tags, per your chosen site.
print('Searching on Unsplash...')
search = ' '.join(sys.argv[1:])
res = requests.get('https://unsplash.com/search/photos/' + search)

# Check that the request was fetched successfully.
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, features='html.parser')

# Create save directory in wherever the script was run from.
os.makedirs('unsplash', exist_ok=True)

# Generates list of links from search results.
linkElems = soup.select('a[itemprop="contentUrl"]')
numOpen = min(cap, len(linkElems))

for i in range(numOpen):

	# Fetching information about search result.
	res = requests.get('https://unsplash.com' + linkElems[i].get('href'))
	res.raise_for_status()
	soup = bs4.BeautifulSoup(res.text, features='html.parser')

	# Find the URL of image to download.
	imageUrl = soup.select('._2zEKz')[0].get('src')
	r = requests.get(imageUrl)
	r.raise_for_status()
	print('Downloading image from %s...' % (imageUrl))

	# Save image to /unsplash
	imageFile = open(os.path.join('unsplash', os.path.basename(search + ' ' + str(i) + '.png')), 'wb')

	for chunk in r.iter_content(100000):
		imageFile.write(chunk)

	imageFile.close()

print('All done!')