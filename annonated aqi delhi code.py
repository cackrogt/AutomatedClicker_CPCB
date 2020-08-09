from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC #error handling
from selenium.common.exceptions import TimeoutException #timeout if not found
import os
import re
import time

YEAR = '2017'#the year is set here;
 
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")
options.binary_location = r"C:\chromedriver.exe"


#python_button = driver.find_elements_by_css_selector(".fa.fa")[3].click()
'''
pb = driver.find_elements_by_css_selector(".fa.fa")
print(pb[3])
pb[3].click()
'''

def criteria():# this function sets the time interval criteria, 15 mins
	cr = '%2522%257B%255C%2522criteria%255C%2522%253A%255C%2522'+'15'+'%2520'+'Minute'
	return cr
	
def report(): #this is for tabular or graphical form
	rp = '%255C%2522%252C%255C%2522reportFormat%255C%2522%253A%255C%2522' + 'Tabular'+'%255C%2522%252C%255C%2522'
	return rp
	
def from_d(mon): #this is from date function, it takes in month, also the year is set in this function, 2017 for ex
	x = 'fromDate%255C%2522%253A%255C%2522'+'01-'+str(mon)+'-'+YEAR+'%2520T'+'00%253A00%253A00'+'Z%255C%2522%252C%255C%2522'
	return x

def to_d(mon):#this is to date, the year should be set here as well if changing
	day = 31
	if(mon in [4,6,9,11]):#for deciding 28, 30 or 31 days according to the month;
		day = 30
	elif mon==2:
		day = 28
	y = 'toDate%255C%2522%253A%255C%2522'+str(day)+'-'+str(mon)+'-'+YEAR+'%2520T'+'11%253A59%253A59'+'Z%255C%2522%252C%255C%2522'
	return y
	
def city():#the city is set to delhi 
	c = 'state%255C%2522%253A%255C%2522'+'Delhi'+'%255C%2522%252C%255C%2522city%255C%2522%253A%255C%2522'+'Delhi'+'%255C%2522%252C%255C%2522'
	return c
	
def station(inp):#this sets the stations in a city
	stat = 'station%255C%2522%253A%255C%2522site_'+inp+'%255C%2522%252C%255C%2522'
	return stat
	
def param():#these are the parameters like no2 so2;
	para = 'parameter%255C%2522%253A%255B%255C%2522'+'parameter_215'+'%255C%2522%252C%255C%2522'+'parameter_193'+'%255C%2522%252C%255C%2522'+'parameter_194'+'%255C%2522%252C%255C%2522'+'parameter_312'+'%255C%2522%252C%255C%2522'+'parameter_203'+'%255C%2522%252C%255C%2522'+'parameter_222'+'%255C%2522%255D%252C%255C%2522'+'parameterNames%255C%2522%253A%255B%255C%2522'+'PM10'+'%255C%2522%252C%255C%2522'+'PM2.5'+'%255C%2522%252C%255C%2522'+'NO2'+'%255C%2522%252C%255C%2522'+'SO2'+'%255C%2522%252C%255C%2522'+'CO'+'%255C%2522%252C%255C%2522'+'Ozone'+'%255C%2522%255D%257D%2522'
	return para

def url(inp,mon):#final link creation
	link = 'https://app.cpcbccr.com/ccr/#/caaqm-dashboard/caaqm-view-data-report/'+criteria()+report()+from_d(mon)+to_d(mon)+city()+station(inp)+param()
	return link

nodelist = ['117','1423','1424','109','1425','122','1561','115','1427','1426','1429','105','1428']#,'1431','125','1563','107','124','1430','113','119','1432','1562','1435','1434'] #part list of sites;

for mon in range(1,13):#every month in a year;
	#for i in range(1,len(nodelist)+1):
	i =0
	while(i<len(nodelist)):
		l=nodelist[i]
		i =i+1
		y=url(l,mon)
		#print(y)

		driver = webdriver.Chrome('C:\\Users\\cackr\\chromedriver.exe')
		driver.get(y)
		try:
			wait = WebDriverWait(driver, 60)
			elem = wait.until(EC.presence_of_element_located((By.XPATH,"//i[contains(@class,'fa fa-file-excel-o')]")))
			python_button = driver.find_elements_by_css_selector(".fa.fa")[3].click()
		except TimeoutException:
			driver.close()
			driver.quit()
			i =i-1
			continue
		#time.sleep(10)
		number = 10#tries for ten times and then moves on;
		while(1):
					temporary = 0
					for root, dirs, files in os.walk(r"C:\Users\cackr\Downloads"):
							for x in files:
									print(x)
									if(re.search("^site_"+l+".*xlsx$",x) ):#searches for filename in the download dir, #as a regular expression
											temporary = -1
											print(1)
											if not os.path.exists("C:\\Users\\cackr\\SOP\\"+l+" "+str(mon)+" "+YEAR):#creates folder with required format
													os.makedirs("C:\\Users\\cackr\\SOP\\"+l+" "+str(mon)+" "+YEAR)
											os.rename("C:\\Users\\cackr\\Downloads\\"+x, "C:\\Users\\cackr\\SOP\\"+l+" "+str(mon)+" "+YEAR+"\\"+x)#moves file from downloads to the above created folder;
											print(2)
											break
									else:
											time.sleep(2)
											print(3)
											continue
							break
					number = number -1;
					if(temporary == -1):
							print(4)
							break
					elif(number < 1):
							i = i-1
							break
					else:
							print(5)
							
							continue
					
		driver.close()
		driver.quit()
	
	
#delhi alipur 1 hour 11 to 12 feb
'''
https//app.cpcbccr.com/ccr/#/caaqm-dashboard/caaqm-view-data-report/%2522%257B%255C%2522criteria%255C%2522%253A%255C%25221%2520Hours%255C%2522%252C%255C%2522reportFormat%255C%2522%253A%255C%2522Tabular%255C%2522%252C%255C%2522fromDate%255C%2522%253A%255C%252211-02-2019%2520T00%253A00%253A00Z%255C%2522%252C%255C%2522toDate%255C%2522%253A%255C%252212-02-2019%2520T15%253A13%253A59Z%255C%2522%252C%255C%2522state%255C%2522%253A%255C%2522Delhi%255C%2522%252C%255C%2522city%255C%2522%253A%255C%2522Delhi%255C%2522%252C%255C%2522station%255C%2522%253A%255C%2522site_5024%255C%2522%252C%255C%2522parameter%255C%2522%253A%255B%255C%2522parameter_215%255C%2522%252C%255C%2522parameter_193%255C%2522%252C%255C%2522parameter_194%255C%2522%252C%255C%2522parameter_312%255C%2522%252C%255C%2522parameter_203%255C%2522%252C%255C%2522parameter_222%255C%2522%255D%252C%255C%2522parameterNames%255C%2522%253A%255B%255C%2522PM10%255C%2522%252C%255C%2522PM2.5%255C%2522%252C%255C%2522NO2%255C%2522%252C%255C%2522SO2%255C%2522%252C%255C%2522CO%255C%2522%252C%255C%2522Ozone%255C%2522%255D%257D%2522
'''
