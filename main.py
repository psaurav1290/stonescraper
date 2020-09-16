import tkinter as tk
import tkinter.ttk as ttk
from ttkthemes import themed_tk

import webbrowser
from functools import partial
import ctypes
import urllib.parse 					
import urllib
import re								# Regular Expressions
from PIL import ImageTk,Image			# Image processing
from urllib.request import urlopen		# Fetching a web image

import requests
from bs4 import BeautifulSoup

class basicProcesses():
	def progress(self,val):
		self.master.master.tabLowerProgress["value"]=val
		self.master.master.tabLowerProgress.update_idletasks()

	def optimizeSearchInput(self,searchKeys=""):
		searchKeys = searchKeys.strip().lower()
		return urllib.parse.quote(searchKeys)

	def openWebsite(self,link):
		webbrowser.open_new(link)

	def getSoup(self,searchURL,progressFactor=50):
		headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
		source = requests.get(searchURL,headers=headers).content
		self.progress(progressFactor)
		soup = BeautifulSoup(source,'lxml')
		with open("munmmun.html","w",encoding="utf-8") as file:
			file.write(soup.prettify())
		return soup

	def __init__(self,master=None):
		pass


class initResultCardShopping(ttk.Frame,basicProcesses):
	def resultCardShoppingLoadWidgets(self,scrapeShoppingData,thumbName,gridCol,success):
		self.cardShoppingFrameElements[thumbName] = {}
		if success:
			self.cardShoppingFrameElements[thumbName]['name'] = ttk.Label(self,text=scrapeShoppingData['name'],						font = ("Calibri",15,'bold'),wrap=600,style="linkShopping.TLabel")
			self.cardShoppingFrameElements[thumbName]['finalprice'] = ttk.Label(self,text='₹ '+scrapeShoppingData['finalprice'],	font = ("Calibri",19,'bold'),wrap=700,style="textShopping.TLabel")
			self.cardShoppingFrameElements[thumbName]['discount'] =ttk.Label(self,text="Discount - "+scrapeShoppingData['discount'],font = ("Calibri",14),wrap=700,style="textShopping.TLabel")
			self.cardShoppingFrameElements[thumbName]['initialprice'] = ttk.Label(self,text='₹ '+scrapeShoppingData['initialprice'],font = ("Calibri",11,'overstrike'),wrap=700,style="textShopping.TLabel")
			if scrapeShoppingData['rating']=='No Rating':
				self.cardShoppingFrameElements[thumbName]['rating'] = ttk.Label(self,text=scrapeShoppingData['rating'],				font = ("Calibri",13),wrap=700,style="textShopping.TLabel")
			else:
				self.cardShoppingFrameElements[thumbName]['rating'] = ttk.Label(self,text=scrapeShoppingData['rating']+'  ⭐',			font = ("Calibri",14,'bold'),wrap=600,style="textShopping.TLabel")
			if scrapeShoppingData['reviewphrase'] == 'No Review':
				self.cardShoppingFrameElements[thumbName]['reviewphrase'] = ttk.Label(self,text=scrapeShoppingData['reviewphrase'],	font = ("Calibri",13),wrap=600,style="textShopping.TLabel")
			else:
				self.cardShoppingFrameElements[thumbName]['reviewphrase'] = ttk.Label(self,text=scrapeShoppingData['reviewphrase'],	font = ("Calibri",13,'bold'),wrap=650,style="textShopping.TLabel")
			self.cardShoppingFrameElements[thumbName]['review'] = ttk.Label(self,text=scrapeShoppingData['review'],					font = ("Calibri",13),wrap=650,style="textShopping.TLabel")
		else:
			self.cardShoppingFrameElements[thumbName]['name'] = ttk.Label(self,text=scrapeShoppingData['name'],					font = ("Calibri",17,'bold'),wrap=600,style="linkShopping.TLabel")	

		self.cardShoppingFrameElements[thumbName]['frameCaptionImage'] = ImageTk.PhotoImage(Image.open(f"images/{thumbName}-caption.png"))
		self.cardShoppingFrameElements[thumbName]['frameCaption'] = ttk.Label(self,image=self.cardShoppingFrameElements[thumbName]['frameCaptionImage'],style="textShopping.TLabel")

		self.cardShoppingFrameElements[thumbName]['searchurl'] = scrapeShoppingData['searchurl']
		self.cardShoppingFrameElements[thumbName]['name'].bind("<Enter>", lambda event : event.widget.config(style="linkShoppingActive.TLabel"))
		self.cardShoppingFrameElements[thumbName]['name'].bind("<Leave>", lambda event : event.widget.config(style="linkShopping.TLabel"))
		self.cardShoppingFrameElements[thumbName]['name'].bind("<Button-1>", lambda event : super(initResultCardShopping,self).openWebsite(self.cardShoppingFrameElements[thumbName]['searchurl']))

		self.cardShoppingFrameElements[thumbName]['frameCaption'].	grid(row=0,column=gridCol*2,columnspan=2,sticky='NW',padx=0,pady=0,ipadx=0,ipady=0)
		self.cardShoppingFrameElements[thumbName]['name'].			grid(row=1,column=gridCol*2,columnspan=2,sticky='NW',padx=3,pady=5,ipadx=0,ipady=0)
		if success:
			self.cardShoppingFrameElements[thumbName]['finalprice'].	grid(row=2,column=gridCol*2+1,sticky='NW',padx=0,pady=0,ipadx=0,ipady=0)
			self.cardShoppingFrameElements[thumbName]['discount'].		grid(row=3,column=gridCol*2+1,sticky='NW',padx=0,pady=0,ipadx=0,ipady=0)
			self.cardShoppingFrameElements[thumbName]['initialprice'].	grid(row=4,column=gridCol*2+1,sticky='NW',padx=0,pady=0,ipadx=0,ipady=0)
			self.cardShoppingFrameElements[thumbName]['rating'].		grid(row=5,column=gridCol*2+1,sticky='NW',padx=0,pady=2,ipadx=0,ipady=0)
			self.cardShoppingFrameElements[thumbName]['reviewphrase'].	grid(row=6,column=gridCol*2,columnspan=2,sticky='NW',padx=3,pady=2,ipadx=0,ipady=0)
			self.cardShoppingFrameElements[thumbName]['review'].		grid(row=7,column=gridCol*2,columnspan=2,sticky='NW',padx=3,pady=0,ipadx=0,ipady=0)

		if not success:
			self.cardShoppingFrameElements[thumbName]['image'] = ImageTk.PhotoImage(Image.open("images/product-not-found-280x280.png"))
		elif scrapeShoppingData['imageurl'] == '':
			self.cardShoppingFrameElements[thumbName]['image'] = ImageTk.PhotoImage(Image.open("images/image-not-available-280x280.png"))
		else: 
			imgFetched = urlopen(scrapeShoppingData['imageurl'])
			imgFetched = Image.open(imgFetched)
			[imgW, imgH] = imgFetched.size
			if (imgW >= imgH and imgW > self.imageSideLength):
				imgWt = imgW
				imgW = self.imageSideLength
				imgH = (self.imageSideLength * imgH) // imgWt
			elif (imgH > imgW and imgH > self.imageSideLength):
				imgHt = imgH
				imgH = self.imageSideLength
				imgW = (self.imageSideLength * imgW) // imgHt
			imgFetched = imgFetched.resize((imgW,imgH), Image.ANTIALIAS)
			self.cardShoppingFrameElements[thumbName]['image'] = ImageTk.PhotoImage(imgFetched)
		self.cardShoppingFrameElements[thumbName]['imageurl'] = ttk.Label(self,image=self.cardShoppingFrameElements[thumbName]['image'])
		self.cardShoppingFrameElements[thumbName]['imageurl'].grid(row=2,column=gridCol*2,rowspan=4,padx=10,pady=10,ipadx=0,ipady=0)

	def printResultsShopping(self,dataset):
		print("{")
		for i in dataset:
			print("\t",i," : ",dataset[i])
		print("}")

	def setScrapeShoppingFlipkartData(self,soupShoppingFlipkartProduct):
		shoppingFlipkartProductProp = soupShoppingFlipkartProduct.select_one("._2_AcLJ")
		if shoppingFlipkartProductProp != None:
			shoppingFlipkartProductProp = re.split("url\(|\?q=",shoppingFlipkartProductProp.attrs["style"])[1] + "?q=100"
			self.scrapeShoppingFlipkartData['imageurl'] = shoppingFlipkartProductProp.replace('/128',f'/{self.imageSideLength}',2)
		shoppingFlipkartProductProp = soupShoppingFlipkartProduct.p
		if shoppingFlipkartProductProp != None:
			shoppingFlipkartProductProp = shoppingFlipkartProductProp.text
			shoppingFlipkartProductProp = re.sub("\n+", "  ", shoppingFlipkartProductProp)
			self.scrapeShoppingFlipkartData['name'] = shoppingFlipkartProductProp
		shoppingFlipkartProductProp = soupShoppingFlipkartProduct.select_one("._1iCvwn")
		if shoppingFlipkartProductProp != None:
			self.scrapeShoppingFlipkartData['discount'] = shoppingFlipkartProductProp.text[:-4]
		shoppingFlipkartProductProp = soupShoppingFlipkartProduct.select_one("._3auQ3N")
		if shoppingFlipkartProductProp != None:
			self.scrapeShoppingFlipkartData['initialprice'] = shoppingFlipkartProductProp.text[1:]
		shoppingFlipkartProductProp = soupShoppingFlipkartProduct.select_one("._1vC4OE._3qQ9m1")
		if shoppingFlipkartProductProp != None:
			self.scrapeShoppingFlipkartData['finalprice'] = shoppingFlipkartProductProp.text[1:]
		shoppingFlipkartProductProp = soupShoppingFlipkartProduct.select_one("._1i0wk8")
		if shoppingFlipkartProductProp != None:
			self.scrapeShoppingFlipkartData['rating'] = shoppingFlipkartProductProp.text
		else:
			self.scrapeShoppingFlipkartData['rating'] = 'No Rating'
		shoppingFlipkartProductProp = soupShoppingFlipkartProduct.select_one("._2xg6Ul")
		if shoppingFlipkartProductProp != None:
			self.scrapeShoppingFlipkartData['reviewphrase'] = shoppingFlipkartProductProp.text.replace("&amp","&")
		shoppingFlipkartProductProp = soupShoppingFlipkartProduct.select_one(".qwjRop div div")
		if shoppingFlipkartProductProp != None:
			shoppingFlipkartProductProp = shoppingFlipkartProductProp.decode_contents()
			shoppingFlipkartProductProp = shoppingFlipkartProductProp.replace('\"',"").replace("&amp","&")
			shoppingFlipkartProductProp = re.sub("\n+", "  ", shoppingFlipkartProductProp)
			self.scrapeShoppingFlipkartData['review'] = re.sub("<.*>","  ",shoppingFlipkartProductProp)[:400]+"..."
		if(self.scrapeShoppingFlipkartData['reviewphrase']=='-' and self.scrapeShoppingFlipkartData['review']=='-'):
			self.scrapeShoppingFlipkartData['reviewphrase'] = 'No Review'
			self.scrapeShoppingFlipkartData['review'] = ''

	def scrapeShoppingFlipkart(self):
		shoppingFlipkartSearchKeys = super().optimizeSearchInput(self.searchKeys)
		shoppingFlipkartSearchURL = f"https://www.flipkart.com/search?q={shoppingFlipkartSearchKeys}&otracker=search&otracker1=search&sort=relevance"
		super().progress(20)
		soupShoppingFlipkart = super().getSoup(shoppingFlipkartSearchURL,40)
		super().progress(50)
		self.scrapeShoppingFlipkartData = {'name':"-",'initialprice':"-",'discount':"-",'finalprice':"-",'rating':"-",'reviewphrase':"-",'review':"-",'imageurl':"",'searchurl':shoppingFlipkartSearchURL}

		with open("flip.html","w",encoding="utf-8") as file:
			file.write(soupShoppingFlipkart.prettify())

		shoppingFlipkartNoResult = soupShoppingFlipkart.select_one(".DUFPUZ")
		if shoppingFlipkartNoResult != None:
			self.scrapeShoppingFlipkartData["name"] = "No product found :("
			return 0
		else:
			shoppingFlipkartSearchURL = soupShoppingFlipkart.select_one("a[target=_blank]").attrs['href']
			shoppingFlipkartSearchURL = f"https://flipkart.com{shoppingFlipkartSearchURL}"
			soupShoppingFlipkartProduct = super().getSoup(shoppingFlipkartSearchURL)

			self.scrapeShoppingFlipkartData['searchurl']=shoppingFlipkartSearchURL
			# with open("amz.html","w",encoding="utf-8") as file:
			with open("flp.html","w",encoding="utf-8") as file:
				file.write(soupShoppingFlipkartProduct.prettify())

			self.setScrapeShoppingFlipkartData(soupShoppingFlipkartProduct)
			self.printResultsShopping(self.scrapeShoppingFlipkartData)
			return 1

	def setScrapeShoppingAmazonData(self,soupShoppingAmazonProduct):
		shoppingAmazonProductProp = soupShoppingAmazonProduct.select_one(".a-dynamic-image")
		if shoppingAmazonProductProp != None:
			# self.scrapeShoppingAmazonData['imageurl'] = shoppingAmazonProductProp.attrs["data-old-hires"]
			self.scrapeShoppingAmazonData['imageurl'] = shoppingAmazonProductProp.attrs["data-a-dynamic-image"].split("\"")[1]
		shoppingAmazonProductProp = soupShoppingAmazonProduct.select_one("#title")
		if shoppingAmazonProductProp != None:
			shoppingAmazonProductProp = shoppingAmazonProductProp.text.strip()
			self.scrapeShoppingAmazonData['name'] = re.sub("\n+", "  ", shoppingAmazonProductProp)
		shoppingAmazonProductProp = soupShoppingAmazonProduct.select_one(".priceBlockSavingsString")
		if shoppingAmazonProductProp != None:
			self.scrapeShoppingAmazonData['discount'] = shoppingAmazonProductProp.text.strip()
		shoppingAmazonProductProp = soupShoppingAmazonProduct.select_one(".priceBlockStrikePriceString")
		if shoppingAmazonProductProp != None:
			self.scrapeShoppingAmazonData['initialprice'] = shoppingAmazonProductProp.text.strip()[2:]
		shoppingAmazonProductProp = soupShoppingAmazonProduct.select_one("#priceblock_ourprice,#priceblock_saleprice,#priceblock_dealprice")
		if shoppingAmazonProductProp != None:
			self.scrapeShoppingAmazonData['finalprice'] = shoppingAmazonProductProp.text.strip()[2:]
		shoppingAmazonProductProp = soupShoppingAmazonProduct.select_one("i.averageStarRating")
		if shoppingAmazonProductProp != None:
			self.scrapeShoppingAmazonData['rating'] = shoppingAmazonProductProp.text.split(" ")[0]
		else:
			self.scrapeShoppingAmazonData['rating'] = 'No rating'
		shoppingAmazonProductProp = soupShoppingAmazonProduct.select_one("a.a-text-bold span")
		if shoppingAmazonProductProp != None:
			self.scrapeShoppingAmazonData['reviewphrase'] = shoppingAmazonProductProp.text.replace("&amp","&")
		# shoppingAmazonProductProp = soupShoppingAmazonProduct.select_one(".a-expander-partial-collapse-content span")
		shoppingAmazonProductProp = soupShoppingAmazonProduct.select_one("#cm-cr-dp-review-list .a-expander-partial-collapse-content span")
		if shoppingAmazonProductProp != None:
			shoppingAmazonProductProp = shoppingAmazonProductProp.decode_contents()
			shoppingAmazonProductProp = shoppingAmazonProductProp.replace('\"',"").replace("&amp","&")
			shoppingAmazonProductProp = re.sub("\n+", "  ", shoppingAmazonProductProp)
			self.scrapeShoppingAmazonData['review'] = re.sub("<.*>","  ",shoppingAmazonProductProp)[:400]+'...'
		if(self.scrapeShoppingAmazonData['reviewphrase']=='-' and self.scrapeShoppingAmazonData['review']=='-'):
			self.scrapeShoppingAmazonData['reviewphrase'] = 'No Review'
			self.scrapeShoppingAmazonData['review'] = ''

	def scrapeShoppingAmazon(self):
		shoppingAmazonSearchKeys = super().optimizeSearchInput(self.searchKeys)
		shoppingAmazonSearchURL = f"http://www.amazon.in/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords={shoppingAmazonSearchKeys}"
		super().progress(20)
		soupShoppingAmazon = super().getSoup(shoppingAmazonSearchURL,40)
		super().progress(50)
		self.scrapeShoppingAmazonData = {'name':"-",'initialprice':"-",'discount':"-",'finalprice':"-",'rating':"-",'reviewphrase':"-",'review':"-",'imageurl':"",'searchurl':shoppingAmazonSearchURL}

		with open("amz(results).html","w",encoding="utf-8") as file:
			file.write(soupShoppingAmazon.prettify())

		shoppingAmazonResult = soupShoppingAmazon.select(".a-link-normal.a-text-normal")
		if shoppingAmazonResult == []:
			self.scrapeShoppingAmazonData["name"] = "No product found :("
			print("1st return",self.scrapeShoppingAmazonData)	
			return 0

		else:
			for anchor in shoppingAmazonResult:
				anchorHref = anchor.attrs["href"]
				if "ssoredirect" not in anchorHref:
					anchorHref = anchorHref.replace("%3D","=")
					anchorHref = anchorHref.replace("%26","&")
					anchorHref = anchorHref.replace("%3"+"F","?")
					shoppingAmazonSearchURL = f"http://www.amazon.in/{anchorHref}"
					break

			if "http://www.amazon.in/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=" in shoppingAmazonSearchURL:
				self.scrapeShoppingAmazonData["name"] = "No product found :("
				print("2nd return", self.scrapeShoppingAmazonData)	
				return 0

			soupShoppingAmazonProduct = super().getSoup(shoppingAmazonSearchURL)
			self.scrapeShoppingAmazonData['searchurl']=shoppingAmazonSearchURL
			with open("amz.html","w",encoding="utf-8") as file:
				file.write(soupShoppingAmazonProduct.prettify())
			self.setScrapeShoppingAmazonData(soupShoppingAmazonProduct)
			self.printResultsShopping(self.scrapeShoppingAmazonData)
			return 1

	def initCardShoppingStyles(self):
		ttk.Style().configure("linkShopping.TLabel",foreground="#001b85",background="#00e6b0")
		ttk.Style().configure("linkShoppingActive.TLabel",foreground="#008cff",background="#00e6b0")
		ttk.Style().configure("frameShopping.TFrame",background="#00e6b0")
		ttk.Style().configure("textShopping.TLabel",background="#00e6b0")
	
	def __init__(self,master=None,searchKeys=""):
		super().__init__(master)
		self.master = master
		self.searchKeys = searchKeys
		self.imageSideLength = 280
		self.cardShoppingFrameElements = {}
		self.initCardShoppingStyles()
		if master.master.master.tabMiddlePane.amazonToggleButtonState:
			super().progress(10)
			successShoppingAmazon = self.scrapeShoppingAmazon()
			self.resultCardShoppingLoadWidgets(self.scrapeShoppingAmazonData,'amazon',0,successShoppingAmazon)
		if master.master.master.tabMiddlePane.flipkartToggleButtonState:
			super().progress(10)
			successShoppingFlipkart = self.scrapeShoppingFlipkart()
			self.resultCardShoppingLoadWidgets(self.scrapeShoppingFlipkartData,'flipkart',1,successShoppingFlipkart)
		
		self.pack(side="bottom",ipadx=0,ipady=5,padx=0,pady=5,expand=1,fill="x")
		self.config(relief="sunken",style="frameShopping.TFrame")
		super().progress(100)

class initResultCardGoogle(ttk.Frame,basicProcesses):
	def cardGoogleHoverIn(self,event):
		self.config(style="cardResultFrameActive.TFrame")
		self.cardGoogleTitle.config(style="titleFrameActive.TLabel")
		self.cardGoogleLink.config(style="linkFrameActive.TLabel")
		self.cardGoogleText.config(style="textFrameActive.TLabel")
		if self.success:
			self.cardGoogleFooter.config(style="linkFrameActive.TLabel")
	
	def cardGoogleHoverOut(self,event):
		self.config(style="cardResultFrame.TFrame")
		self.cardGoogleTitle.config(style="titleFrame.TLabel")
		self.cardGoogleLink.config(style="linkFrame.TLabel")
		self.cardGoogleText.config(style="textFrame.TLabel")
		if self.success:
			self.cardGoogleFooter.config(style="linkFrame.TLabel")

	def resultCardGoogleLoadWidgets(self):
		print(self.scrapeGoogleData)
		self.cardGoogleTitle = ttk.Label(self,text=self.scrapeGoogleData["title"],justify="left",font=("Calibri",15),wrap=1300,style="titleFrame.TLabel")
		self.cardGoogleLink = ttk.Label(self,text=self.scrapeGoogleData["link"],justify="left",font=("Calibri",12,'underline'),wrap=1300,style="linkFrameActive.TLabel")
		self.cardGoogleText = ttk.Label(self,text=self.scrapeGoogleData["text"],justify="left",font=("Calibri",13),wrap=1300,style="textFrameActive.TLabel")
		self.cardGoogleFooter = ttk.Label(self,text=f"Google search results for {self.searchKeys}",justify="left",font=("Calibri",13),wrap=1300,style="linkFrameActive.TLabel")
		
		self.cardGoogleTitle.grid(row=0,column=0,sticky='W',padx=20)
		self.cardGoogleLink.grid(row=1,column=0,sticky='W',padx=20,pady=3)
		self.cardGoogleText.grid(row=2,column=0,sticky='W',padx=20,pady=3)
		self.cardGoogleFooter.grid(row=3,column=0,sticky='W',padx=20,pady=3)
		self.cardGoogleLink.bind("<Enter>", lambda event : event.widget.config(style="linkActive.TLabel"))
		self.cardGoogleLink.bind("<Leave>", lambda event : event.widget.config(style="linkFrameActive.TLabel"))
		self.cardGoogleLink.bind("<Button-1>", lambda t : super(initResultCardGoogle,self).openWebsite(self.scrapeGoogleData["link"]))
		self.cardGoogleFooter.bind("<Enter>", lambda event : event.widget.config(style="linkActive.TLabel"))
		self.cardGoogleFooter.bind("<Leave>", lambda event : event.widget.config(style="linkFrameActive.TLabel"))
		self.cardGoogleFooter.bind("<Button-1>", lambda t : super(initResultCardGoogle,self).openWebsite(self.googleSearchURL))

	def initCardGoogleStyles(self):
		ttk.Style().configure("cardResultFrame.TFrame",background="#00e6c7",bordercolor="blue",borderwidth=2)
		ttk.Style().configure("cardResultFrameActive.TFrame",background="#00e6b0",bordercolor="blue",borderwidth=2)

		ttk.Style().configure("titleFrame.TLabel",foreground="#ffffff",background="#d40000")
		ttk.Style().configure("titleFrameActive.TLabel",foreground="#ffffff",background="#b50000")
		
		ttk.Style().configure("linkFrame.TLabel",foreground="#001b85",background="#00e6c7",relief='flat')
		ttk.Style().configure("linkFrameActive.TLabel",foreground="#001b85",background="#00e6b0",relief='flat')
		ttk.Style().configure("linkActive.TLabel",foreground="#008cff",background="#00e6b0",relief='flat')
		#1fffca
		ttk.Style().configure("textFrame.TLabel",foreground="black",background="#00e6c7")
		ttk.Style().configure("textFrameActive.TLabel",foreground="black",background="#00e6b0")

	def scrapeGoogle(self):
		googleSearchKeys = super().optimizeSearchInput(self.searchKeys)
		self.googleSearchURL = f"https://www.google.com/search?q={googleSearchKeys}&num=10&ie=utf-8&oe=utf-8&aq=t&rls=org.mozilla:en-US:official&client=firefox-a&channel=fflb"
		super().progress(20)
		soupGoogle = super().getSoup(self.googleSearchURL)
		super().progress(80)
		self.scrapeGoogleData = {'link':"-",'title':"-",'text':"-"}

		topResult = soupGoogle.select_one(".PhiYYd.QBl4oe")
		if topResult!=None:
			self.scrapeGoogleData['link'] = topResult.select_one("a").attrs['href']
			self.scrapeGoogleData['title'] = topResult.select_one("h3").text
			self.scrapeGoogleData['text'] = "Preview Image"
		else:
			topResult = soupGoogle.select_one(".rc")
			if topResult!=None:
				self.scrapeGoogleData['link'] = topResult.select_one("a").attrs['href']
				self.scrapeGoogleData['title'] = topResult.select_one("h3").text
				self.scrapeGoogleData['text'] = topResult.select_one(".s").text
				if self.scrapeGoogleData['text']=="":
					self.scrapeGoogleData['text'] = topResult.parent.previous_sibling.text
			else:
				self.scrapeGoogleData['title'] = "Sorry! No results found  :("
				self.scrapeGoogleData['link'] = self.googleSearchURL
				self.scrapeGoogleData['text'] = f"You searched for - {self.searchKeys}"
				return 0
		return 1

		print(self.scrapeGoogleData)

	def __init__(self,master=None,searchKeys=""):
		super().__init__(master)
		self.master = master
		self.searchKeys = searchKeys
		super().progress(10)
		self.success = self.scrapeGoogle()
		self.initCardGoogleStyles()
		self.resultCardGoogleLoadWidgets()
		super().progress(90)
		self.pack(side="bottom",ipadx=0,ipady=5,padx=0,pady=5,expand=1,fill="x")
		self.config(relief="sunken",style="cardResultFrameActive.TFrame")
		self.bind("<Enter>", self.cardGoogleHoverIn)
		self.bind("<Leave>", self.cardGoogleHoverOut)
		self.bind("<Double-Button-1>", lambda event : super(initResultCardGoogle,self).openWebsite(self.scrapeGoogleData["link"]))
		super().progress(100)

class initTabLowerOutput(ttk.Frame):
	def removeResultCard(self):
		if self.tabResultCardNumber > self.master.master.cardNumberMax:
			self.tabResultCards[self.tabResultCardNumber-self.master.master.cardNumberMax-1].destroy()

	def createResultCard(self,cardType,searchKeys):
		self.tabResultCards[self.tabResultCardNumber] = cardType(self,searchKeys)
		self.tabResultCardNumber+=1
		self.removeResultCard()

	def lowerOutputLoadWidgets(self):
		self.tabResultsPlaceholder = ttk.Label(self,text="",font=("Calibri",10),justify="center",width=200)
		self.tabResultsPlaceholder.pack(side="bottom",ipadx=0,ipady=0,padx=0,pady=0)
		self.tabResultCardNumber = 0
		self.tabResultCards = {}

	def __init__(self,master=None):
		super().__init__(master)
		self.master = master
		self.grid(row=0,column=1,sticky="N",ipadx=0,ipady=0,padx=15,pady=0)
		# self.lowerOutputStyle = ttk.Style()
		# self.lowerOutputStyle.configure("Output.TFrame",background="blue")
		# self.config(style="Output.TFrame")
		self.lowerOutputLoadWidgets()

class initTabLowerPane(ttk.Frame):
	def lowerPaneLoadWidgets(self):
		self.tabLowerProgress = ttk.Progressbar(self,length=540,value=0,orient="vertical")
		self.tabLowerProgress.grid(row=0,column=0,ipadx=1,ipady=0,padx=0,pady=0)
		self.tabLowerOutput = initTabLowerOutput(self)
	
	def __init__(self,master=None):
		super().__init__(master)
		self.master = master
		self.pack(side="top",ipadx=0,ipady=0,padx=0,pady=0)
		# self.lowerPaneStyle = ttk.Style()
		# self.lowerPaneStyle.configure("Lower.TFrame",background="red")
		# self.config(style="Lower.TFrame")
		self.lowerPaneLoadWidgets()

class initTabMiddlePane (ttk.Frame):
	def amazonToggle(self,event):
		self.amazonToggleButtonState = not self.amazonToggleButtonState
		if self.amazonToggleButtonState:
			self.amazonToggleButton.config(image=self.amazonEnabled)
		else:
			self.amazonToggleButton.config(image=self.amazonDisabled)
		if (not self.amazonToggleButtonState and not self.flipkartToggleButtonState):
			self.flipkartToggle("Toggle")

	def flipkartToggle(self,event):
		self.flipkartToggleButtonState = not self.flipkartToggleButtonState
		if self.flipkartToggleButtonState:
			self.flipkartToggleButton.config(image=self.flipkartEnabled)
		else:
			self.flipkartToggleButton.config(image=self.flipkartDisabled)
		if (not self.flipkartToggleButtonState and not self.amazonToggleButtonState):
			self.amazonToggle("Toggle")

	def middlePaneLoadWidgets(self,tabName):
		if tabName == "Google Search":
			self.middlePaneTagImage = ImageTk.PhotoImage(Image.open("images/google-middle-pane-600x50.png"))
			self.middlePaneTagLabel = ttk.Label(self,image=self.middlePaneTagImage)
			self.middlePaneTagLabel.pack(side="top",ipadx=0,ipady=0,padx=0,pady=0)
		elif tabName == "Online Shopping":
			self.amazonEnabled = ImageTk.PhotoImage(Image.open("images/amazon-enabled.png"))
			self.amazonDisabled = ImageTk.PhotoImage(Image.open("images/amazon-disabled.png"))
			self.flipkartEnabled = ImageTk.PhotoImage(Image.open("images/flipkart-enabled.png"))
			self.flipkartDisabled = ImageTk.PhotoImage(Image.open("images/flipkart-disabled.png"))

			self.amazonToggleButtonState = True
			self.flipkartToggleButtonState = True
			self.amazonToggleButton = ttk.Label(self,image=self.amazonEnabled,style="TLabel")
			self.flipkartToggleButton = ttk.Label(self,image=self.flipkartEnabled,style="TLabel")

			self.amazonToggleButton.bind("<Button-1>",self.amazonToggle)
			self.flipkartToggleButton.bind("<Button-1>",self.flipkartToggle)

			self.amazonToggleButton.pack(side='left')
			self.flipkartToggleButton.pack(side='left')
		
	def __init__(self,master=None,tabName="Tab"):
		super().__init__(master)
		self.master = master
		self.pack(side="top",ipadx=0,ipady=0,padx=0,pady=10)
		self.middlePaneLoadWidgets(tabName)

class initTabInputPane(ttk.Frame):
	def clearInputFieldFirst(self,event):
		if self.clearInputField :
			self.tabInputField.delete(0,'end')
			self.clearInputField = 0

	def inputPaneLoadWidgets(self):

		self.entryStyle = ttk.Style()
		self.entryStyle.map("Custom.TEntry",foreground=[('!focus', 'grey')])
		self.tabInputField = ttk.Entry(self,width=80,font=("Calibri",15),style="Custom.TEntry")
		self.tabInputField.insert(0,"Enter your search term here")
		self.tabSearchIconImage = ImageTk.PhotoImage(Image.open("images/search-icon-image-disabled-80x80.png"))
		self.tabSearchIcon = ttk.Button(self,image=self.tabSearchIconImage,style="searchIcon.TLabel",command=lambda:self.master.processInput("SearchButton"))

		self.clearInputField = 1
		self.tabInputField.pack(side="left",padx=40,pady=0,ipadx=0,ipady=8)
		self.tabInputField.bind("<Button-1>",self.clearInputFieldFirst)
		self.tabInputField.bind("<Return>",self.master.processInput)
		self.tabSearchIcon.pack(side="left",padx=40,pady=0,ipadx=0,ipady=10)

	def __init__(self,master=None):
		super().__init__(master)
		self.master = master
		self.pack(side="top",ipadx=0,ipady=0,padx=10,pady=0)
		self.inputPaneLoadWidgets()

class initRootNbTab (ttk.Frame):
	def processInput(self,event):
		if self.processingInput:
			return
		self.processingInput = True
		self.tabInputPane.tabInputField.config(state='disabled')
		self.tabInputPane.tabSearchIcon.config(state='disabled')
		self.tabLowerPane.tabLowerProgress.update_idletasks()

		if self.tabName == "Google Search":
			self.tabLowerPane.tabLowerOutput.createResultCard(initResultCardGoogle,self.tabInputPane.tabInputField.get())
		elif self.tabName == "Online Shopping":
			self.tabLowerPane.tabLowerOutput.createResultCard(initResultCardShopping,self.tabInputPane.tabInputField.get())

		self.tabInputPane.tabInputField.config(state='normal')
		self.tabInputPane.tabSearchIcon.config(state='normal')
		self.tabInputPane.update_idletasks()
		self.processingInput = False

	def tabLoadWidgets(self):
		self.tabImage = ImageTk.PhotoImage(Image.open(f"images/{self.tabName.replace(' ','-')}-tab-image-1200x220.png"))
		self.tabImageLabel = ttk.Label(self,image=self.tabImage)
		self.tabImageLabel.pack(side="top",ipadx=0,ipady=0,padx=0,pady=0)
		self.searchKeys = None
		self.tabInputPane = initTabInputPane(self)
		self.tabMiddlePane = initTabMiddlePane(self,self.tabName)
		self.tabLowerPane = initTabLowerPane(self)
		self.processingInput = False

	def __init__(self,master=None,tabName="Tab",cardNumberMax=1):
		super().__init__()
		self.master = master
		self.master.add(self,text=tabName)
		self.tabName = tabName
		self.cardNumberMax = cardNumberMax
		self.tabLoadWidgets()

class initRootNotebook(ttk.Notebook):
	def notebookLoadWidgets(self):
		self.rootTabGoogle = initRootNbTab(self,"Google Search",3)
		self.rootTabShopping = initRootNbTab(self,"Online Shopping")

	def __init__(self,master):
		super().__init__()
		self.master = master
		self.pack(expand=1,fill="both")
		self.enable_traversal()
		self.notebookLoadWidgets()

class initRootMenu(tk.Menu,basicProcesses):
	def winResize(self,winDim):
		self.master.winWidth = winDim.split("x")[0]
		self.master.geometry(winDim)

	def menuLoadWidgets(self):
		self.master.config(menu=self)

		self.rootMenuFile = tk.Menu(self.master,tearoff=0)
		self.add_cascade(label="File",menu=self.rootMenuFile)
		self.rootMenuFile.add_command(label="Exit\t\t\t\t\t(Alt+F4)",command=self.master.destroy)
		self.rootMenuFile.add_command(label="Contact",command=lambda : super(initRootMenu,self).openWebsite("http://psaurav1290.github.io"))

		self.rootMenuResize = tk.Menu(self.master,tearoff=0)
		self.add_cascade(label="Resize",menu=self.rootMenuResize)
		self.rootMenuResize.add_command(label="Wide",command=lambda:self.winResize("1500x1010"))
		self.rootMenuResize.add_command(label="Narrow",command=lambda:self.winResize("800x1010"))

	def __init__(self,master=None):
		super().__init__()
		self.master = master
		self.menuLoadWidgets()

class initRoot(themed_tk.ThemedTk):
	def rootLoadWidgets(self):
		self.rootMenu = initRootMenu(self)
		self.rootNotebook = initRootNotebook(self)
	
	def __init__(self):
		ctypes.windll.shcore.SetProcessDpiAwareness(1)
		super().__init__()
		self.set_theme("plastik")
		self.geometry("1500x1030+100+0")
		self.title("Stone Scraper")
		self.iconbitmap("favicon.ico")
		self.winWidth = 1500
		self.rootLoadWidgets()

if __name__ == "__main__":

	root = initRoot()
	root.mainloop()