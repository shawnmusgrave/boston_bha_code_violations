# The code below scrapes the name and all associated addresses for public and subsidized housing
# units listed on the Boston Housing Authority website: 
#
# http://www.bostonhousing.org/en/Housing-Communities/Assessment-Result.aspx
#
# See the raw output as downloaded on June 9 here:
# TKTK


# import the appropriate libraries
import urllib
from bs4 import BeautifulSoup
import re
import pandas 

# initialize an empty list - we will put one dictionary per public/subsidized housing development into this list
developments_dict_list = []

# poking around the website, it's clear that all development ID #s are between 1 and 300
# use a for loop to scrape each development info page for:
#   1) development name
#   2) development ID number
#   3) primary address associated with the development
#   4) any other addresses associated with the development [ this is a separate field from 3) ]
for each_development in range(1, 300):
    
    # initialize an empty dictionary for each development
    development = {}
    
    # convert html from the given development info page into a BeautifulSoup document
    url = "http://www.bostonhousing.org/en/HousingDevelopmentDetail.aspx?hid=" + str(each_development)
    html_str = urllib.urlopen(url).read()
    document = BeautifulSoup(html_str)
    
    # test to see if the given development exists 
    # note that the site does not actually 404, but redirects automatically and displays text
    # reflecting the error inside a <h1> tag
    # return an error message if the given development info page does not exist
    h1_tag = document.find("h1")
    if h1_tag.string == "Error 404: Page Not Found":
        print "SKIPPING number %d because it doesn't exist!" % each_development
        continue
    
    # if the given development info page exists, proceed with scraping the page
    print "Munging number %d!" % each_development
    
    # assign the development id number to the dictionary -- this is the number we're iterating over via the URL
    development["development_id"] = each_development
    
    # pull the development name and assign to the dictionary 
    span_tag = document.find("span", attrs = {"id": "p_lt_zoneMain_pageplaceholder1_p_lt_ctl01_HousingDevelopmentPage_lblPropertyName"})
    development_name = span_tag.string
    development["development_name"] = str(development_name)
    
    # pull the development address and assign to the dictionary 
    span_tag = document.find("span", attrs = {"id": "p_lt_zoneMain_pageplaceholder1_p_lt_ctl01_HousingDevelopmentPage_lblAddress"})
    address = span_tag.string
    development["address"] = str(address)
    
    
	# pull other listed addresses and assign to the dictionary as unique columns:
	# this introduced issues given the variety of formatting oddities for the few development info pages
	# with an "Other Addresses" field -- specifically, some included arbitrary <p> tags, while others
	# had odd whitespace and tabs that needed to be stripped
    # first, use a regular expression to find the "Other Addresses" tag if it exists
    other_address_tag = document.find(text=re.compile("Other Addresses:"))
    
    # if there is an "Other Addresses" tag, pull out its contents
    if str(other_address_tag).strip() == "Other Addresses:":
    	
    	# the contents of the tag are in list format
        ul_tag = other_address_tag.find_next("ul")
        
        # some have multiple <li>, so use .find_all and a for loop to capture all items
        li_tags = ul_tag.find_all("li")
        for li_tag in range(0, len(li_tags)):
            # to assign a unique variable name to each new <li>, use a counter
            count = str(li_tag)
            
            # handle arbitrary <p> tags
            if li_tags[li_tag].find("p") is None:
            	
            	# assign the stripped contents to the dictionary
                development["other_address" + count] = str(li_tags[li_tag].string.encode('utf-8').strip()).strip("\xc2\xa0")
           
           # assign the stripped contents to the dictionary 
            else: 
                development["other_address" + count] = str(li_tags[li_tag].find("p").string.encode('utf-8').strip()).strip("\xc2\xa0")


    # pull the funding program(s) associated with the development (e.g. "Public Housing - Tax Cred") 
    # and assign to the dictionary
    span_tag = document.find("span", attrs = {"id": "p_lt_zoneMain_pageplaceholder1_p_lt_ctl01_HousingDevelopmentPage_lblPrograms"})
    programs = span_tag.string
    development["programs"] = str(programs)
    
    # append the dictionary 
    developments_dict_list.append(development)
    
# convert list of dictionaries to a DataFrame to spotcheck and confirm formatting 
developments_scraped_df = pd.DataFrame(developments_dict_list)
#developments_scraped_df

# save as .csv to EC2 instance, then download via ssh for cleaning
developments_scraped_df.to_csv("developments_scraped.csv")