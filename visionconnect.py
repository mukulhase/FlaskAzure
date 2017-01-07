import httplib, urllib, base64, json, urllib2

image_headers = {
	# Request headers
	'Content-Type': 'application/json',
	'Ocp-Apim-Subscription-Key': 'a9c6c3ecc96646d0bea62e3839bb3a7e',
}

translation_headers = {
	"Content-Type": "application/x-www-form-urlencoded",
	"Accept": "application/xml",
	'Ocp-Apim-Subscription-Key': '940a397d030044f299eceab7e9f9f99d',
}

params = urllib.urlencode({
})

# url of image
def getTag(url):
	try:
		conn = httplib.HTTPSConnection('api.projectoxford.ai')
		conn.request("POST", "/vision/v1.0/tag?%s" % params, "{\"url\": \"%s\"}" % url, image_headers)
		response = conn.getresponse().text
		#response = request.get("https://api.cognitive.microsoft.com/sts/v1.0/issueToken", headers=translation_headers)
		data = response.read()
		#print(data)
		conn.close()
		parsed_json = json.loads(data)
		return parsed_json
	except Exception as e:
		print(e)

url = "http://www.ikea.com/PIAimages/0121010_PE277826_S5.JPG"
# tag = getTag(url)
tag = "plant"

#token for translation API, 10 min life.
def getToken():
	try:
		conn = httplib.HTTPSConnection('api.cognitive.microsoft.com')
		conn.request("POST", "/sts/v1.0/issueToken",params, translation_headers)
		response = conn.getresponse()
		token = response.read()
		# print(data)
		conn.close()
		return token
	except Exception as e:
		print(e)
		return


acc_token = getToken()
# print(acc_token)

appid = "Bearer" + " " + acc_token

transParams = urllib.urlencode({
	'appid': appid,
	'text' : tag,
	'from' : 'en-US',
	'to' : 'hi',
	'maxTranslations' : 1,
})

#from, to are language encodings, num = number of max translations
def TranslateWord():
	try:
		conn = httplib.HTTPSConnection('api.microsofttranslator.com')
		conn.request("POST", "/V2/Http.svc/GetTranslations?%s" % transParams, params, translation_headers)
		response = conn.getresponse()
		data = response.read()
		print(data)
		conn.close()
		return
	except Exception as e:
		print(e)
		return

TranslateWord()