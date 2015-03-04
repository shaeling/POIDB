#coding:utf-8
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import urllib2
import sys
import time
import win32api
import win32con
import os
reload(sys)
sys.setdefaultencoding('utf8')

def GetPage(PageURL):
	headers = {
		'Referer':'http://www.dianping.com/shop/14897313',
	    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
	    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
	    'Connection': 'keep-alive'
	}

	request = urllib2.Request(PageURL, headers=headers)
	ResultContent =urllib2.urlopen(request,timeout=500).read()
	# TransCode for the page
	return ResultContent

'''
	Get all shop urls in Beijing from dianping
	Then write to a static file
'''
def GetAllShopinPK():
	#ShopURLlist = []
	fp = open('DianPingAllShopList.txt','w')
	for x in range(1,49):
		if x == 1 :
			page = GetPage('http://www.dianping.com/search/category/2/20/g119')
		else:
			page = GetPage('http://www.dianping.com/search/category/2/20/g119p'+str(x))
		soup = BeautifulSoup(page)
		name = soup.findAll('a',attrs={'data-hippo-type':'shop'})
		for each in name:
			#ShopURLlist.append(each.get('href'))
			fp.write('http://www.dianping.com'+each.get('href')+'\n')
	fp.close()

'''	
	Get All brand urls
'''
def GetAllBrandUrl(loadfile):
	Filelines = open(loadfile,'r').readlines()
	Filetext = ''.join(Filelines)
	Filetext.replace('\n','')
	Filetext.replace(' ','')
	soup = BeautifulSoup(Filetext)
	soup.prettify()
	BrandURLrs = []

	AllBrand = soup.findAll('div',attrs={'class':'brand-content'},limit=1)
	for brand in AllBrand :
		URLrs = brand.findAll('a')
		for eachURL in URLrs:
			BrandURLrs.append(eachURL.get('href'))
	return BrandURLrs

'''
	Get each brand phone number
'''
def GetPhoneNum(originurl,savefile):
	fp = open(savefile,'w')
	BrandURLrs = GetAllBrandUrl(originurl)

	for eachBrand in BrandURLrs:
		BrandPage = GetPage(eachBrand)
		soup = BeautifulSoup(BrandPage)
		phoneinfo = soup.findAll(attrs={'itemprop':'tel'})
		shopname = soup.find('h1')
		shopname = shopname.contents[0].strip() 
		for eachBrandphone in phoneinfo:
			phone = eachBrandphone.getText()
			print shopname+','+phone
			fp.write(shopname+','+phone+'\n')
	fp.close()
	
'''
	Get each brand brief info
'''
def GetBriefInfo(loadfile,savefile):
	fp = open(savefile,'w')
	BrandURLrs = GetAllBrandUrl(loadfile)
	for eachBrand in BrandURLrs:
		BrandPage = GetPage(eachBrand)
		time.sleep(5)
		soup = BeautifulSoup(BrandPage)
		try:
			briefinfo = soup.findAll('span',attrs={'class':'item'},limit=5)
			shopname = soup.find('span').contents[0].strip()
			print shopname	
			if len(briefinfo[4].getText())>10:
				print shopname,briefinfo[1].getText(),briefinfo[2].getText(),briefinfo[3].getText()
				fp.write(shopname+','+briefinfo[1].getText()+','+\
						briefinfo[2].getText()+','+briefinfo[3].getText()+'\n')
			else:
				print shopname,briefinfo[1].getText(),briefinfo[2].getText(),briefinfo[3].getText(),briefinfo[4].getText()
				fp.write(shopname+','+briefinfo[1].getText()+','+\
						briefinfo[2].getText()+','+briefinfo[3].getText()+','+briefinfo[4].getText()+'\n')
		except Exception:
			pass
	fp.close()

'''
	In Food Tag:Download Plaza page after click every nextpages
'''

def AutoDownloadPage(shopurl):
	driver = webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
	driver.get(shopurl)
	time.sleep(2)
	#choose food tag
	driver.find_element_by_xpath("//a[@data-id='1']").click()
	try:
		find_next = driver.find_element_by_xpath("//a[@class='brand-next']")
		while (find_next):
			find_next.click()
	except Exception:
		#model ctrl+s and enter
		win32api.keybd_event(17,0,0,0) 
		win32api.keybd_event(83,0,0,0)
		win32api.keybd_event(17,0,win32con.KEYEVENTF_KEYUP,0) 
		win32api.keybd_event(83,0,win32con.KEYEVENTF_KEYUP,0)
		time.sleep(2)
		win32api.keybd_event(13,0,0,0)
		win32api.keybd_event(13,0,win32con.KEYEVENTF_KEYUP,0)
		time.sleep(10)
	driver.quit()

def renameFile(path):
	for line in os.listdir(path):
		if '_files' in line:
			name = line.split(',')
			print line,name[0]
			os.rename(path+line,path+name[0])	

if __name__ == "__main__":
	#GetAllShopinPK()
	#for line in open('DianPingAllShopList.txt'):
	#	AutoDownloadPage(line)
	path = 'E:/code/dianping/'
	for line in os.listdir(path):
		if '.html' in line:
			GetBriefInfo(path+line,line+'.txt')
			time.sleep(10)