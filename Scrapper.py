# -*- coding: utf-8 -*-

import geopy
from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup
import requests
import pandas as pd


def scrape_covid_data():

    geolocator = Nominatim(user_agent="example app")

    # URL
    URL = "https://www.nshealth.ca/coronavirus-exposures"

    # Get content
    content = requests.get(URL)

    # Parse
    soup = BeautifulSoup(content.text, 'html.parser')

    # Find last page class tag
    last_page = soup.find("li", {"class": "pager__item pager__item--last"})

    # Find last page link
    last_page_link = last_page.find_all(href=True)

    # Turn link to string
    last_page_link_str = str(last_page_link)

    # Find the page number in the link string
    last_page_num = last_page_link_str.split("page=")

    # Turn the page number into an integer
    last_page_n = int(last_page_num[1][0])

    # Create an empty dictionary to store dataframes
    df_dict = {}

    # Add page 1 as the first(0) element in the dictionary
    df_dict[0] = pd.read_html("http://www.nshealth.ca/covid-exposures")[0]

    # Loop through the URL for later pages, up until the last page
    # Enumerate new dictionary elements based on page number
    for i in range(1, last_page_n):
        df = pd.read_html(
            "https://www.nshealth.ca/coronavirus-exposures?title=&field_covid_exposure_zone_value=All&page={}".format(i))[0]
        df_dict[i] = df

    # Create a final dataframe
    df_final = pd.concat(df_dict.values(), ignore_index=True)

    #########################Manual Changes#########################

    spider = df_final[df_final["Place"].str.contains("Spider-Man")].index
    df_final.loc[spider, "Address"] = "Cineplex Sydney"
    ####Change time structure for Last Updated column############
    df_final["Last Updated"] = df_final["Last Updated"].str.split("-", expand=True)[0].str.split("/")[2][2].strip(" ") \
                               + "-" + df_final["Last Updated"].str.split("-", expand=True)[0].str.split("/")[2][0] \
                               + "-" + df_final["Last Updated"].str.split("-", expand=True)[0].str.split("/")[2][1] \
                               + " " + df_final["Last Updated"].str.split("-", expand=True)[1].str.strip(" ")

    #################################################################
    #####Check the dataframe to see which columns have NaN values####
    #################################################################
    if df_final.isnull().values.any():
        print("Check for NaN values in our columns")
        print("Place: " + str(df_final["Place"].isnull().values.any()))
        print("Potential Exposure Window: " + str(df_final["Potential Exposure Window"].isnull().values.any()))
        print("Address: " + str(df_final["Address"].isnull().values.any()))
        print("Covid Exposure Or Precaution	: " + str(df_final["Covid Exposure Or Precaution"].isnull().values.any()))
        print("Zone: " + str(df_final["Zone"].isnull().values.any()))
        print("Last Updated: " + str(df_final["Last Updated"].isnull().values.any()))

    ##Determine Which Addresses Show up As Null
    # Clean them by replacing the address
    null_addresses = df_final[df_final["Address"].isnull()].index
    for null_address in null_addresses:
        # watch out for the "-" which NS health uses ... wtf
        df_final.iloc[null_address, 2] = df_final.iloc[null_address][0].split("–")[1]

    #################################################################
    #####Check the dataframe to see which columns have NaN values####
    #################################################################
    if df_final.isnull().values.any():
        print("Check for NaN values in our columns")
        print("Place: " + str(df_final["Place"].isnull().values.any()))
        print("Potential Exposure Window: " + str(df_final["Potential Exposure Window"].isnull().values.any()))
        print("Address: " + str(df_final["Address"].isnull().values.any()))
        print("Covid Exposure Or Precaution	: " + str(df_final["Covid Exposure Or Precaution"].isnull().values.any()))
        print("Zone: " + str(df_final["Zone"].isnull().values.any()))
        print("Last Updated: " + str(df_final["Last Updated"].isnull().values.any()))
    else:
        print("There are no NaN values")

    df_final["Exposure_From"] = df_final["Potential Exposure Window"] \
                                    .str.split("to", expand=True)[0] \
                                    .str.split(",", expand=True)[1] \
                                    .str.split("-", expand=True)[0] \
                                    .str.split("/", expand=True)[2].str.strip(" ") \
                                + "-" + df_final["Potential Exposure Window"] \
                                    .str.split("to", expand=True)[0] \
                                    .str.split(",", expand=True)[1] \
                                    .str.split("-", expand=True)[0] \
                                    .str.split("/", expand=True)[0].str.strip(" ") \
                                + "-" + df_final["Potential Exposure Window"] \
                                    .str.split("to", expand=True)[0] \
                                    .str.split(",", expand=True)[1] \
                                    .str.split("-", expand=True)[0] \
                                    .str.split("/", expand=True)[1].str.strip(" ") \
                                + " " + df_final["Potential Exposure Window"].str.split("to", expand=True)[0].str.split(",",
                                                                                                                        expand=True)[
                                    1].str.split("-", expand=True)[1].str.strip(" ")

    # Select days which have exposures in a single day
    one_day = df_final["Potential Exposure Window"].str.split("to", expand=True)[1].str.len() <= 7
    df_final.loc[one_day, "Exposure_To"] = df_final["Potential Exposure Window"] \
                                               .str.split("to", expand=True)[0] \
                                               .str.split(",", expand=True)[1] \
                                               .str.split("-", expand=True)[0] \
                                               .str.split("/", expand=True)[2].str.strip(" ") \
                                           + "-" + df_final["Potential Exposure Window"] \
                                               .str.split("to", expand=True)[0] \
                                               .str.split(",", expand=True)[1] \
                                               .str.split("-", expand=True)[0] \
                                               .str.split("/", expand=True)[0].str.strip(" ") \
                                           + "-" + df_final["Potential Exposure Window"] \
                                               .str.split("to", expand=True)[0] \
                                               .str.split(",", expand=True)[1] \
                                               .str.split("-", expand=True)[0] \
                                               .str.split("/", expand=True)[1].str.strip(" ") \
                                           + " " + \
                                           df_final["Potential Exposure Window"].str.split("to", expand=True)[0].str.split(
                                               ",", expand=True)[1].str.split("-", expand=True)[1].str.strip(" ")

    # Select days that have longer exposure periods
    two_days = df_final["Potential Exposure Window"].str.split("to", expand=True)[1].str.len() >= 7
    df_final.loc[two_days, "Exposure_To"] = df_final["Potential Exposure Window"] \
                                                .str.split("to", expand=True)[1] \
                                                .str.split(",", expand=True)[1] \
                                                .str.split("-", expand=True)[0] \
                                                .str.split("/", expand=True)[2].str.strip(" ") \
                                            + "-" + df_final["Potential Exposure Window"] \
                                                .str.split("to", expand=True)[1] \
                                                .str.split(",", expand=True)[1] \
                                                .str.split("-", expand=True)[0] \
                                                .str.split("/", expand=True)[0].str.strip(" ") \
                                            + "-" + df_final["Potential Exposure Window"] \
                                                .str.split("to", expand=True)[1] \
                                                .str.split(",", expand=True)[1] \
                                                .str.split("-", expand=True)[0] \
                                                .str.split("/", expand=True)[1].str.strip(" ") \
                                            + " " + \
                                            df_final["Potential Exposure Window"].str.split("to", expand=True)[1].str.split(
                                                ",", expand=True)[1].str.split("-", expand=True)[1].str.strip(" ")

    # Create a Geolocation Address column
    df_final['GeolocationAddress'] = df_final['Address'] + ", Nova Scotia, Canada"
    print("Geolocation Address Column Completed")
    print("Creating First Batch of Geocoded Addresses, this might take a while...")
    df_final['GeolocationAddressCoords'] = df_final['GeolocationAddress'].apply(lambda x: geolocator.geocode(x))
    properly_geocoded = df_final.dropna(subset=["GeolocationAddressCoords"])
    improperly_geocoded = df_final[~df_final.index.isin(properly_geocoded.index)]
    df_final["Latitude"] = properly_geocoded["GeolocationAddressCoords"].apply(lambda x: (x.latitude))
    df_final["Longitude"] = properly_geocoded["GeolocationAddressCoords"].apply(lambda x: (x.longitude))
    print("Completed First Batch")

    # Second Fix
    print("Creating Second Batch of Geocoded Addresses, attempt to geocode the ones that failed")
    df_final.loc[improperly_geocoded.index, "GeolocationAddressCoords"] = (
                improperly_geocoded["Place"] + ", Nova Scotia, Canada").apply(lambda x: geolocator.geocode(x))
    properly_geocoded_2 = df_final.dropna(subset=["GeolocationAddressCoords"])
    improperly_geocoded_2 = df_final[~df_final.index.isin(properly_geocoded_2.index)]
    df_final["Latitude"] = properly_geocoded_2["GeolocationAddressCoords"].apply(lambda x: (x.latitude))
    df_final["Longitude"] = properly_geocoded_2["GeolocationAddressCoords"].apply(lambda x: (x.longitude))
    print("Complete")

    print("Drop Remaining rows with NaN, can be cleaned up later/")

    # CREATE FINAL DATA SET WITH NA ROWS REMOVED
    df_final_2 = df_final.dropna()
    df_final_2.reset_index(drop=True, inplace=True)
    df_for_valerie = df_final_2[
        ["Place", "Exposure_From", "Exposure_To", "GeolocationAddress", "Covid Exposure Or Precaution", "Zone",
         "Last Updated", "Latitude", "Longitude"]]
    df_for_valerie.astype(str)

    print("Exporting to CSV")
    print(df_for_valerie.head())
    #df_for_valerie.to_csv('C:/Users/morin/Desktop/output/covidlocations.csv', header=False)


    val2 = df_for_valerie
    val2.update('\"' + df_final_2[
        ["Place", "Exposure_From", "Exposure_To", "GeolocationAddress", "Covid Exposure Or Precaution", "Zone",
         "Last Updated", "Latitude", "Longitude"]].astype(str) + '\"')
    val2.to_csv('C:/Users/morin/Desktop/NS_Covid_Exposures/data.txt', header=False)

    print("CSV Complete")
