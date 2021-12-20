import pandas as pd

#We we scrape 'table' contents from the exposure site website using the pandas function pd.read_html(). This handily collects all of the data visible on the page onto a pandas dataframe object.
# Public Exposures
df1 = pd.read_html("http://www.nshealth.ca/covid-exposures")
df2 = pd.read_html("https://www.nshealth.ca/coronavirus-exposures?title=&field_covid_exposure_zone_value=All&page=1")
df3 = pd.read_html("https://www.nshealth.ca/coronavirus-exposures?title=&field_covid_exposure_zone_value=All&page=2")
df4 = pd.read_html("https://www.nshealth.ca/coronavirus-exposures?title=&field_covid_exposure_zone_value=All&page=3")
df5 = pd.read_html("https://www.nshealth.ca/coronavirus-exposures?title=&field_covid_exposure_zone_value=All&page=4")
df6 = pd.read_html("https://www.nshealth.ca/coronavirus-exposures?title=&field_covid_exposure_zone_value=All&page=5")

# Flight and Transit Exposures
df_transit = pd.read_html("https://www.nshealth.ca/coronavirus-exposures-transit")
df_transit = df_transit[0].rename(columns={'Route or flight': "Place"})
#Concatenate all of our dataframes into one to compile all Covid-19 exposures onto one dataframe.
df7 = pd.concat([df1[0],df2[0],df3[0],df4[0],df5[0],df6[0],df_transit], ignore_index = True)

print("Exporting to CSV")
df7.to_csv('./covidlocations.csv')

