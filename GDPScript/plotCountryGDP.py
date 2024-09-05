from matplotlib import pyplot as plt
import numpy as np
import requests
import sys
import tradingeconomics as te

arguments = sys.argv

if len(arguments) < 3:
    raise ValueError("Not enough arguments were given.  You must give your api key followed by a country name.  This can be followed either by a single year, or by two years that are separated by spaces that represent a range.  For example: your_api_key \"new zealand\" 1990 2002")


if len(arguments) > 5:
    raise ValueError("Too many arguments were given.  You must give your api key followed by a country name.  This can be followed either by a single year, or by two years that are separated by spaces that represent a range.  For example: your_api_key \"new zealand\" 1990 2002")

api_key = arguments[1]
# Country names that are more than one word must 
country = arguments[2]

year = [arguments[3], arguments[4]] if len(arguments) == 5 else [arguments[3]] if len(arguments) == 4 else None

if year and len(year) == 2 and int(year[1]) < int(year[0]):
    raise ValueError("The second year must be greater than or equal to the first year.  ")

beginmm_dd = "-01-01"
begin = "1800-01-01" if (year == None) or (len(year) == 1) else str(year[0]) + "-01-01"
end = None if (year == None) else str(year[0]) + "-12-31" if len(year) == 1 else str(year[1]) + "-12-31"



print("Begin: ", begin)
print("End: ", end)

te.login(api_key)
gdp_list = te.getHistoricalData(country=country, indicator="gdp", initDate=begin, endDate=end)
domain = []
gdps = []
begin_year = None
end_year = None
for i in gdp_list:
    if i["Country"].lower() != country.lower():
        continue
    domain.append(int(i["DateTime"][:4]))
    gdps.append(i["Value"])

plt.plot(domain, gdps)
plt.title(f"GDP of {country.upper()} from {domain[-1]} to {domain[0]}")
plt.xlabel("Years")
plt.ylabel("GDP (millions)")
plt.show()

for i in gdp_list:
    if i["Country"].lower() != country.lower():
        continue
    print(i)
