# August Guang, February 2013
# corpSearch.py
# Takes in an input term (corporation name) and scrapes the InfluenceExplorer

# to run: python corpSearch.py -i <input> -o <output>

from transparencydata import TransparencyData
import sys, getopt
#import requests
import pprint
import itertools
import json

api = TransparencyData('8f0d91c66d4e428da018c0eb0fa571fc')

# reads CRP_Categories.txt
def readIn(inFile):
    with open(inFile, 'r') as fin:
        # format is:
        # Catcode Catname Catorder Industry Sector Sector_Long
        tmp = fin.readlines()
        sectData = tmp[1:]
        return sectData

# sorts CRP_Categories.txt so that all codes are associated with a sector in a dictionary
# this allows us to look up a code in the dictionary
def sectorDict(sectData):
    sectDict = {}
    for i in sectData:
        sector = i.split()[4]
        code = i.split()[0]
        if sector in sectDict:
            sectDict[sector].append(code)
        else:
            sectDict[sector] = [code]
    return sectDict

# writes output from API in format needed for Javascript/D3
# I AM SO UNAMUSED
def writeJSON(APIout, outFile):
    jsonList = []
    for i in APIout:
        jsonList.append(
            { 'cycle' : {
                    "contributor" : {
                        "contributor_name" : i["contributor_name"],
                        "contributor_ext_id" : i["contributor_ext_id"],
                        "contributor_type":
                            {
                            "Corporation" : {
                            "organization_name" : i["organization_name"],
                            "organization_ext_id" : i["organization_ext_id"],
                            "parent_organization_name" : i["parent_organization_name"],
                            "parent_organization_ext_id" : i["parent_organization_ext_id"],
                            "transaction" : {
                                "transaction_namespace" : i["transaction_namespace"],
                                "transaction_id" : i["transaction_id"],
                                "transaction_type" : i["transaction_type"],
                                "transaction_type_description" : i["transaction_type_description"],
                                "filing_id" : i["filing_id"],
                                "is_amendment" : i["is_amendment"],
                                "amount" : i["amount"],
                                "date" : i["date"],
                                "Recipient": {
                                    "recipient_name" : i["recipient_name"],
                                    "recipient_ext_id" : i["recipient_ext_id"],
                                    "recipient_party" : i["recipient_party"],
                                    "recipient_type" : i["recipient_type"],
                                    "recipient_state" : i["recipient_state"],
                                    "recipient_state_held" : i["recipient_state_held"],
                                    "recipient_category" : i["recipient_category"],
                                    "district" : {
                                        "district" : i["district"],
                                        "district_held" : i["district_held"],
                                        "seat" : i["seat"],
                                        "seat_held" : i["seat_held"],
                                        "seat_status" : i["seat_status"],
                                        "seat_result" : i["seat_result"],
                                        }
                                    }
                                }
                            },
                        

                        "Individual" : {
                            "contributor_occupation" : i["contributor_occupation"],
                            "contributor_employer" : i["contributor_employer"],
                            "contributor_gender" : i["contributor_gender"],
                            "contributor_address" : i["contributor_address"],
                            "contributor_city" : i["contributor_city"],
                            "contributor_state" : i["contributor_state"],
                            "contributor_zipcode" : i["contributor_zipcode"],
                                "contributor_category" : i["contributor_category"]
                            }
                            }
                    }}})
    f = open(outFile, 'w')
    jsonData = json.dumps(jsonList)
    print >> f, jsonData
#    f = open(outFile)
#    f.write(jsonData)

    return jsonData

# main argument
def main(argv):
    i = ''
    outFile = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["input=", "output="])
    except getopt.error, msg:
        print "corpSearch.py -i <input> -o <output>"
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-i", "-input"):
            i = arg
        elif opt in ("-o", "-output"):
            outFile = arg

    data = []
    # if user has typed in a month range, such as between 06 and 11
    if i.find("between"):
        a = i.split() # returns [company name, between, ##, and, ##]
        name = a[0]
        dates = "><|2012-" + a[2] + "-01|2012-" + a[4] + "-31"
        data = api.contributions(cycle='2012', contributor_ft=name, date=dates) 
    else:
        data = api.contributions(cycle='2012', contributor_ft=i)
    sectData = readIn("CRP_Categories.txt")
    sectDict = sectorDict(sectData)
    jsonData = writeJSON(data, outFile)

if __name__ == "__main__":
    main(sys.argv[1:])
