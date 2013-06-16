
import requests
import json

# [2013Ranking, webfriendlyname, official name, pic name (if any), NOTSURE, sales, profits, assets, marketvalue, country, industry, weird dash]
JSON_URL = 'http://www.forbes.com/ajax/load_list/?type=organization&uri=global2000&year=2013'
BASE_URL = 'http://www.forbes.com/global2000/list/#page:{0}_sort:0_direction:asc_search:_filter:All%20industries_filter:All%20countries_filter:All%20states'
BASE_IMG_URL = 'http://i.forbesimg.com/media/lists/companies/{0}_{1}.jpg'
BASE_IMG_SIZE = ['50x50', '100x100', '150x150', '200x200', '300x300', '400x400']
companyInfo = {}  # Dictionary of company information which is primarily accessible by company html-friendly name
companyInfoIndexed = []  # List of company information which is primarily accessible by index number
imgPath = 'images/'
jsonPath = 'json/companyInfo.json'
jsonIndexedPath = 'json/companyInfoIndexed.json'


def toFloat(num):
	return float(num.replace('-', '').replace(',', ''))


# GET ALL COMPANY META DATA BEFORE DOWNLOADING IMAGES
try:
	data = requests.get(JSON_URL)
	print 'Successfully retreived {0}'.format(JSON_URL)
except:
	print 'Error opening BASE_URL.Terminating Program.'

jsonData = json.loads(data.text)
# json data is formatted: # [ascOrder, webfriendlyname, official name, pic name (if any), ranking, sales, profits, assets, marketvalue, country, industry, weird dash]
for item in jsonData:
	companyInfo.update({item[1]: {
									'rank': item[4],
									'name': item[2],
									'picname': item[3],
									'sales': toFloat(item[5]),
									'profits': toFloat(item[6]),
									'assets': toFloat(item[7]),
									'marketvalue': toFloat(item[8]),
									'country': item[9],
									'industry': item[10]}})

for item in jsonData:
	companyInfoIndexed.append({
								'webname': item[1],
								'name': item[2],
								'rank': item[4],
								'picname': item[3],
								'sales': toFloat(item[5]),
								'profits': toFloat(item[6]),
								'assets': toFloat(item[7]),
								'marketvalue': toFloat(item[8]),
								'country': item[9],
								'industry': item[10]})

jInfo = json.dumps(companyInfo)
jInfoIndexed = json.dumps(companyInfoIndexed)

with open(jsonPath, 'wb') as f:
	f.write(jInfo)
with open(jsonIndexedPath, 'wb') as f:
	f.write(jInfoIndexed)

# GET COMPANY LOGOS FROM FORBES.COM
print 'Fetching images...'
for c in companyInfoIndexed:
	if c['picname'] != 'no-pic':
		companyName = c['picname']
		for imgSize in BASE_IMG_SIZE:
			imgURL = BASE_IMG_URL.format(companyName, imgSize)
			imgFile = ''.join([companyName, '_', imgSize, '.jpg'])
			jpgfile = requests.get(imgURL)
			if jpgfile.status_code == 200:
				with open(imgPath + imgFile, 'wb') as f:
					f.write(jpgfile.content)
					print 'Successfully downloaded {0}'.format(imgFile)
			else:
				print 'Error downloading {0}'.format(imgFile)

# extract company info (name, htmlName, sales, profits, assets, marketValue, country) from htmlblock

# something to think about: Should the info below be acquired through current site or main company forbes page?
# (2) Option to obtain additional info: FOUNDING YEAR, CEO, WEBSITE, EMPLOYEE COUNT


print 'Forbes 2000 Coroporate Logo collection complete.'