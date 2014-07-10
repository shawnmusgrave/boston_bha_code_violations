# The code below compares health and safety violations and complaints to a reference file
# of addresses associated with public and subsidized housing units in Boston. 
#
# For more information, see: 
# https://github.com/shawnmusgrave/boston_bha_code_violations/blob/master/health_and_safety_complaints_in_boston_public_housing.md
#



# import necessary libraries and initialize database connection 
# note that this connection is specific to my EC2 instance, and will not work for others
import pymongo 
conn = pymongo.Connection("localhost")
db = conn['lede_program']
bha_violations_collection = db['bha_violations']

# create an empty list - we will fill this with dictionaries of each violation/complaint
# that matches an address associated with a public or subsidized housing unit
# along with an annotation of which development the violation/complaint matches
public_housing_violations = []

# these are all of the fields pulled from the City of Boston open data API
fields = ("case_enquiry_id", "case_status", "case_title", "city_council_district", "closed_dt",\
"closure_reason", "confirmed_violation", "department", "fire_district",\
"geocoded_location", "land_usage", "latitude", "location", "location_street_name",\
"location_zipcode", "longitude", "neighborhood", "neighborhood_services_district",\
"open_dt", "police_district", "precinct", "property_id", "property_type", "pwd_district",\
"queue", "reason", "source", "subject", "type", "ward")


# pull in the reference file of all public or subsidized housing unit addresses 
# these were scraped from the Boston Housing Authority website 
# see https://github.com/shawnmusgrave/boston_bha_code_violations/blob/master/bha_scrape.py
developments_address_df = pd.read_csv('./developments_cleaned.csv', sep=",")

# pull in the serious complaints pulled from the City of Boston open data API
# see https://github.com/shawnmusgrave/boston_bha_code_violations/blob/master/serious_complaints_parser.py
serious_complaints_df = pd.read_csv('./serious_complaints.csv', sep=",")

# use a for loop to compare each complaint/violation to each address associated with a public or subsidized 
# housing unit, and save the matches to the list of dictionaries as well as a MongoDB database
for each_complaint in range(0,len(serious_complaints_df)):
    
    # initialize an empty dictionary for each complaint/violation
    complaint = {}
    
    # use a for loop to compare the given complaint/violation to each public/subsidized housing address 
    for each_development in range(0, len(developments_address_df)):
        if serious_complaints_df["location"][each_complaint] == developments_address_df["formatted_address"][each_development]:
            print "Complaint number %s is a match! Adding to database." % serious_complaints_df["case_enquiry_id"][each_complaint]
            
            # save each field pulled from the API to the complaint dictionary
            for each_field in fields:
                complaint[each_field] = serious_complaints_df[each_field][each_complaint]
            
            # save the development name and ID number to the complaint dictionary
            complaint["development_name"] = developments_address_df["development_name"][each_development]
            complaint["development_id"] = developments_address_df["development_id"][each_development]
            
            # add the information to the public_housing_violations list of dictionaries
            public_housing_violations.append(complaint)
            
            # insert a document of the same data into the 
            bha_violations_collection.insert(complaint)
            

# convert to a dataframe for spotchecking 
bha_violations_df = pd.DataFrame(public_housing_violations)

# save as .csv to EC2 instance
bha_violations_df.to_csv("bha_violations.csv")