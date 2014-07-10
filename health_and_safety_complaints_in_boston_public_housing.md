#Health and safety complaints in Boston public housing

<br>

##Overview

Having read the Center for Investigative Reporting series on [unsafe and unsanitary conditions at public housing developments](http://cironline.org/tags/public-housing) in the Bay Area, I wanted to investigate similar issues within public and subsidized housing in Boston. 

<br>

##Data sources
<br>

**1) City of Boston code violations database** 

The City of Boston maintains an open data site (<https://data.cityofboston.gov/>), which includes a central dump of all health and safety code violations, enforcement actions, and [citizen complaints and service requests](http://www.cityofboston.gov/mayor/24/).

The database is available for web viewing [here](https://data.cityofboston.gov/City-Services/Mayor-s-24-Hour-Hotline-Service-Requests/awu8-dc52) and API download [here](http://data.cityofboston.gov/resource/awu8-dc52.json). (The Socrata API documentation is available [here](http://dev.socrata.com/).) All entries include an address, which is what allows cross-referencing to public and subsidized housing units. 

As accessed on July 8, 2014, the database contained 438,194 entries from July 1, 2011 through July 6, 2014, which included requests for bulk item pickup along with complaints of rat infestation. This larger database was pared down to confirmed violations as well as serious/relevant complaints, for a total of 70,166 entries for cross-referencing against public and subsidized housing units. 

**The code for pulling serious health and safety violations and complaints from the City of Boston open data API can be found [here](https://github.com/shawnmusgrave/boston_bha_code_violations/blob/master/serious_complaints_parser.py). The data pulled can be found [here](https://raw.githubusercontent.com/shawnmusgrave/boston_bha_code_violations/master/data/serious_complaints.csv).**

<br>

**2) Boston Housing Authority listing of public housing developments**

The Boston Housing Authority website includes a [searchable listing of all developments](http://bostonhousing.org/en/Housing-Communities/Assessment-Result.aspx), including subsidized/voucher units as well as municipally- and federally-funded developments.

However, the listing database is written in JavaScript, which I do not know how to scrape. Luckily, each individual development also has a unique info page (for example, [this page for the Brighton-Allston Apartments](http://www.bostonhousing.org/en/HousingDevelopmentDetail.aspx?hid=7)), which allowed scraping via a simple for loop and Beautiful Soup. 

**The code for scraping the BHA website can be found [here](https://github.com/shawnmusgrave/boston_bha_code_violations/blob/master/bha_scrape.py). The scraped output can be found [here](https://github.com/shawnmusgrave/boston_bha_code_violations/blob/master/data/developments_scraped.csv).**

<br>

Once scraped, this list of 174 housing developments 
had to be cleaned up manually to standardize address formatting, as well as to correctly capture all addresses associated with a particular unit. 

The scraped addresses included the following variants:

	104 First Ave, Charlestown, MA 02129
	4-6 Bloomfield Street, Dorchester, MA 02124
	37, 39, 41 Bowdoin Street, Boston, MA 02116
	209-219-221-223 Heath Street,  Jamaica Plain, MA 02130
	
Note the inconsistencies in comma usage, as well as the aggregation of multiple street addresses into a single indicator. 

Additionally, a number of developments also listed "Other Addresses" as a separate field – compare, for example, [this page for the Brighton-Allston Apartments](http://www.bostonhousing.org/en/HousingDevelopmentDetail.aspx?hid=7) with [this page for Building 104](http://www.bostonhousing.org/en/HousingDevelopmentDetail.aspx?hid=8). This added another layer of complexity to the scraping, as well as to cleaning the data to build a comprehensive listing of all public housing. 

The list of housing development addresses was been expanded to include all relevant street addresses (and combinations thereof, including the original scraped formatting) for which code violations and complaints might be listed. 

The list of 404 address possibilities then needed to be formatted for comparison to the violation/complaint database, which uses the following format for addresses: 
	
	104 First Ave Charlestown MA 02129

That is, the database uses two spaces ("␣␣") rather than commas to separate address components (street address, neighborhood, state and zipcode). 

A number of street types also needed to be reformatted (for example, "Street" changed to "St", and "Avenue" to "Ave"), and some common street name abbreviations expanded (for example, "Mass Ave" expanded to "Massachusetts Ave"). 

All cleaning was done by hand (and using "find and replace") in Google Drive, rather than via regular expressions, given the relatively small number of entries and wide range of modifications required. 

**The final, cleaned reference listing of BHA development addresses can be found [here](https://github.com/shawnmusgrave/boston_bha_code_violations/blob/master/data/developments_cleaned.csv).**

<br>

##Cross-referencing the databases and uploading the results

Now that the development addresses are in the same format, we can cross-reference them to narrow the larger dataset solely to complaints and code violations that correspond to public and subsidized housing units. The result -- 448 complaints -- are saved to a new list of dictionaries and .csv files, as well as inserted into a MongoDB database on my EC2 server. 

**The code for pulling out the violations and complaints associated with BHA public and subsidized housing developments can be found [here](https://github.com/shawnmusgrave/boston_bha_code_violations/blob/master/bha_violations_parser.py).**

I will provide an API URL and syntax in class. 


