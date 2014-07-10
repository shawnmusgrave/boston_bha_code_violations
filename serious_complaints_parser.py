# the code below uses the API of the City of Boston open data site to pull out 
# serious health and safety violations and complaints 
#
# the web interface for this data can be found at:
# data.cityofboston.gov/City-Services/Mayor-s-24-Hour-Hotline-Service-Requests/awu8-dc52

import json
import urllib2
import pandas as pd

# define the list of violation/complaint types to pull out of the larger dataset
# generally, these are unsafe/unsanitary conditions, pests, overcrowding, disability access issues, etc
# relevant to residential properties
relevant_types = ['Unsafe Dangerous Conditions', 'Poor Conditions of Property', 'Rodent Activity',\
                  'Pigeon Infestation', 'Unsatisfactory Living Conditions', 'Breathe Easy', 'Bed Bugs',\
                  'No Utilities Residential - Electricity',  'No Utilities Residential - Water',\
                  'Unsanitary Conditions - Food', 'Chronic Dampness/Mold', 'Squalid Living Conditions',\
                  'ADA', 'Illegal Rooming House', 'Sidewalk Repair (Make Safe)',\
                  'Rat Bite', 'Mice Infestation - Residential', 'Pest Infestation - Residential',\
                  'Carbon Monoxide', 'Lead', 'Mosquitoes (West Nile)', 'Power Outage'\
                  'Poor Ventilation', 'Sewage/Septic Back-Up', 'Improper Storage of Trash (Barrels)',\
                  'Overcrowding', 'Student Overcrowding', 'Rental Unit Delivery Conditions',\
                  'Unsanitary Conditions - Establishment', 'Big Buildings Enforcement',\
                  'Building Inspection Request', 'Electrical', 'Protection of Adjoining Property',\
                  'Maintenance Complaint - Residential', 'Unsanitary Conditions - Employees',\
                  'Illegal Occupancy', 'Overflowing or Un-kept Dumpster', 'Maintenance - Homeowner',\
                  'Plumbing', 'Heat - Excessive  Insufficient', 'Egress', 'No Utilities Residential - Gas',\
                  'Unsatisfactory Utilities - Electrical  Plumbing', 'Big Buildings Resident Complaint',\
                  'Food Alert - Confirmed', 'Food Alert - Unconfirmed', 'Occupying W/Out A Valid CO/CI',\
                  'Water in Gas - High Priority', 'Watermain Break', 'Flooding Residential/Commercial',\
                  'Downed Wire', 'Snow/Ice Control', 'Snow Emergency']


# use the Socrata API to pull the data
# API documentation available at http://dev.socrata.com/
# the default pull limit for this API is 1000
base_url = "http://data.cityofboston.gov/resource/awu8-dc52.json?$offset="

for each_page in range(0,440): # as of June 9, 2014, the total number of enquiries is 438194 -- 438194 / 1000 + 1 = 439, so range is up to 440
    print 
    print "==============="
    print "==============="
    print 
    print "Reviewing page: " + str(each_page)
    
    # the offset is set by individual entry, rather than by page number 
    offset = 1000 * each_page
    response_str = urllib.urlopen(base_url + str(offset)).read()
    response_dicts = json.loads(response_str)

    for each_enquiry in response_dicts:
        # capture all instances where a violation was confirmed by the city, regardless of type
        if each_enquiry.get("closure_reason") is not None:
            if (each_enquiry["closure_reason"] == "Case Closed VIOISS: Violation Filed ")\
            or (each_enquiry["closure_reason"] == "Case Closed VIOCOR: Violation Corrected "):
                each_enquiry["confirmed_violation"] = "Y"
                serious_complaints.append(each_enquiry)
                continue
		
		# capture serious complaints/violations/allegations that haven't been explicitly confirmed in the data
		# see above for listing of relevant_types
        if each_enquiry["type"] in relevant_types:
            serious_complaints.append(each_enquiry)
        
# convert to a dataframe for spotchecking 
serious_complaints_df = pd.DataFrame(serious_complaints)

# save as .csv to EC2 instance
serious_complaints_df.to_csv("serious_complaints.csv")