########################################
######## Name: Wenjie Wu ###############
######## Unique Name: wuwenj ###########
########################################

import secrets
import requests
import json
import plotly.express as px
import matplotlib.pyplot as plt
import pandas
from bs4 import BeautifulSoup
import webbrowser
import yaml



# Yelp cache
def getData():
    
    ''' Function that get data from API and save the data as a JSON file
    
    Parameters
    ----------
    none
    
    Returns
    -------
    result: dictionary
        a dictionary of restaurants based on the user input.
    '''
    
    global result
    global result_aggregate
    global API_KEY
    global location
    
    location = str(input('Please enter a city to get the restaurant data.\n'))
    API_KEY = secrets.API_KEY
    baseurl = "https://api.yelp.com/v3/businesses/search?location=" + location
    header = {'authorization': "Bearer " + API_KEY}
    resp = requests.get(baseurl, headers=header)
    result = resp.json()
    
    with open ('yelp_' + location + '.json','w') as fp:
        json.dump(result,fp)
        
    print("============================================ JSON File " + 'yelp_' + location + '.json ' + "Has been stored. =============================================")
    return result
  
        
def tree(result):
        
    ''' Function that organize the data into a tree
    
    Parameters
    ----------
    result: dictionary
        a dictionary that contains restaurant data based on the user input
    
    Returns
    -------
    rest_tree: list
        a list of organized tree of restaurants based on the user input.
    '''
    
    rest_tree = []
    aggregate_dic = {}
    
    for item in result["businesses"]:
        aggregate_dic = {"name":item["name"], "attributes":{}}   # create a dic for each business
        aggregate_dic["attributes"]["rating"] = item["rating"]
        aggregate_dic["attributes"]["price"] = item["price"]
        aggregate_dic["attributes"]["review_count"] = item["review_count"]
        aggregate_dic["attributes"]["url"] = item["url"]
        aggregate_dic["attributes"]["transactions"] = item["transactions"]
        
        rest_tree.append(aggregate_dic)
    return rest_tree

def priceTree(rest_tree):
    
    ''' Function that organize the tree into a dictionary contains pricing level information
    
    Parameters
    ----------
    rest_tree: list
        a list that contains restaurant data based on the user input
    
    Returns
    -------
    priceTree: dictionary
        a dictionary of organized tree of restaurants based on pricing level.
    '''
    
    priceTree = {'$': [], '$$': [], '$$$': [], '$$$$': []}
    for price in rest_tree:
        if price["attributes"]["price"] == '$':
            priceTree['$'].append(price['name'])
        elif price["attributes"]["price"] == '$$':
            priceTree['$$'].append(price['name'])
        elif price["attributes"]["price"] == '$$$':
            priceTree['$$$'].append(price['name'])
        elif price["attributes"]["price"] == '$$$$':
            priceTree['$$$$'].append(price['name'])
    return priceTree
    
def getRestaurant():
    
    ''' Function that get the restaurant name list from the restaurant dictionary
    
    Parameters
    ----------
    none
    
    Returns
    -------
    restaurant_name: list
        a list of restaurant name in the city user chose. 
    '''
    
    restaurant_name = []
    for r in result["businesses"]:
        restaurant_name.append(r['name'])
    return restaurant_name
        
def getReview():
    
    ''' Function that get the restaurant review from API and store information as a JSON file
    
    Parameters
    ----------
    none
    
    Returns
    -------
    review_list: list
        a list of restaurant review in the city user chose. 
    '''
    
    global result
    
    review_list = []
    for r in result["businesses"]:
        # Get review for each restaurant
        baseurl = "https://api.yelp.com/v3/businesses/" + r["id"] + "/reviews"
        header = {'authorization': "Bearer " + API_KEY}
        resp_review = requests.get(baseurl, headers=header)
        review = resp_review.json()

        review_dic = {"name": r["name"], "reviews":[]}
        for review in review["reviews"]:
            review_dic["reviews"].append(review["text"])

        review_list.append(review_dic)
        
        with open ('review_' + location + '.json','w') as fp:
            json.dump(review_list,fp)
    return review_list

def getCategories():
    
    ''' Function that get the restaurant category in the city the user chose.
    
    Parameters
    ----------
    none
    
    Returns
    -------
    category_list: list
        a list of restaurant category in the city user chose. 
    '''
    
    global result
    global category_list
    
    category_list = []
    
    for r in result["businesses"]:
        category_dic = {"name": r["name"], "categories":[]}
        for c in r["categories"]:
            category_dic["categories"].append(c["alias"])

        category_list.append(category_dic)
        
    return category_list

def getUniqueCategories():
    
    ''' Function that get the unique restaurant category in the city the user chose.
    
    Parameters
    ----------
    none
    
    Returns
    -------
    unique_list: list
        a list of unique restaurant category in the city user chose. 
    '''
    
    global result
    unique_list = []
    
    for r in result["businesses"]:
        for c in r["categories"]:
            if c["alias"] not in unique_list:
                unique_list.append(c["alias"])
        
    return unique_list

def drawCategory():
    
    ''' Function that draw the graph of category.
    
    Parameters
    ----------
    none
    
    Returns
    -------
    count_dic: dictionary
        a dictionary of restaurant category and numbers of appearing in the city user chose. 
    '''
    
    count_dic = {}
    unique_list = []

    for r in getCategories():
        for c in r["categories"]:
            if c not in unique_list:
                unique_list.append(c)
                count_dic[c] = 1
            else:
                count_dic[c] += 1 
    return count_dic

def drawRating(result):
    
    ''' Function that draw the graph of rating.
    
    Parameters
    ----------
    none
    
    Returns
    -------
    rate_dict: dictionary
        a dictionary of restaurant rating and numbers of appearing in the city user chose. 
    '''
    
    rate_dict = {}
    unique_list = []

    for t in tree(result):
        if t['attributes']['rating'] not in unique_list:
            unique_list.append(t['attributes']['rating'])
            rate_dict[t['attributes']['rating']] = 1
        else:
            rate_dict[t['attributes']['rating']] += 1 
    return rate_dict

def cityDictionary():
    
    ''' Function that scrapes the wikipedia page and save as a dictionary
    
    Parameters
    ----------
    none
    
    Returns
    -------
    city_dict: list
        a list of 326 different cities with the organized relevant information
    '''
    
    city_dict = []
    site_url = 'https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population'
    response = requests.get(site_url)
    url_text = response.text
    soup = BeautifulSoup(url_text, 'html.parser')
    tr_list = soup.find('table', class_='wikitable sortable').find('tbody').find_all('tr')[1:] # total 314 cities in the list, each in a row
    for tr in tr_list: # each tr is a city row, td is the data in each column
        td_list = tr.find_all('td')
        th_list = tr.find_all('th')
        
        id_pos = int(th_list[0].text.strip())
        
        name = str(td_list[0].find('a').text.strip())
        
        try:
            state = str(td_list[1].find('a').text.strip())
        except:
            state = td_list[1].text.strip()
            
        population = int(td_list[2].text.strip().replace(',', ''))
        
        change_text = td_list[4].text.strip().split('%')[0]
        if "+" in change_text:
            change = round((100 + float(change_text.split('+')[1]))/100,2)
        elif "-" in change_text:
            change = round((100 - float(change_text.split('−')[1]))/100,2)

        area = float(td_list[5].text.strip().split('\xa0')[0].replace(',', ''))
        
        city = {"rank": id_pos, "name":name, "state":state, "population": population, "change in population": change, "area":area }
        city_dict.append(city)
    
    return city_dict


def openWeb():
    
    ''' Function that open the Wikipedia website of the city the user chose
    
    Parameters
    ----------
    none
    
    Returns
    -------
    none
    
    '''
    
    while True:
        question = input("Do you want to open the Wikipedia of the city? \n")
        if (question == "yes" or question == "Yes" or question == "y" or question == "Y"):
            city = input("Which city? (Format: Ann_Arbor)\n")
            state = input("Which state? (Format: Michigan)\n")
            url = "https://en.wikipedia.org/wiki/" + city + ',_' + state
            webbrowser.open(url, new = 0)
    
        elif (question == "no" or question == "No" or question == "n" or question == "N"):
            tree(getData())
            break
        else:
            print("Please try again. \n")
            break
        
def openRestaurant(web_name,result):
    
    ''' Function that open the Yelp website of the restaurant the user chose
    
    Parameters
    ----------
    web_name: string
        The restaurant name the user chose
    result: dictionary
        a dictionary of restaurants based on the user input.
    
    Returns
    -------
    none
    
    '''
    
    dict = tree(result)
    for i in dict:
        if i['name'] == web_name:
            url = i["attributes"]["url"]
            webbrowser.open(url, new = 0)
        
        
        
######################### Main #######################################
if __name__=='__main__':
    # # get user input
    openWeb()
    yelp_file = open('yelp_' + location + '.json')
    result = json.load(yelp_file)
    
    # show the structure of the tree
    print("===================================== The structure of the tree is blow ===========================================")
    print(yaml.dump(tree(result), default_flow_style=False))
    
    # get the restaurant name of the city
    print("===================================== The restaurant name of the city ===================================================")
    print(getRestaurant())
    
    # get reviews of the restaurant and save as a json file
    print("======================================== The reviews are saved as a JSON file =========================================")
    getReview()
    
    # get category of the restaurant 
    print("======================================== The category of the restaurant =========================================")
    print(getCategories())
    
    # get unique restaurant list of the city
    print("=================================== The unique restaurant list of the city =====================================")
    print(getUniqueCategories())
    
    # Draw category in the city
    draw = drawCategory()
    list(draw.keys())
    labels = list(draw.keys())
    sizes = list(draw.values())
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes,  labels=labels, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()
    print("===================================== The graph should be shown in your browser. =======================================")
    
    # show the information of the city
    print("================================== The information of the city is below. ===============================================")
    print(cityDictionary())
    
    # Draw population of the city
    df_population = pandas.DataFrame(data = cityDictionary())
    fig = px.bar(df_population,x='name',y='population',title='Population of the city')
    fig.show()
    print("================================== The graph should be shown in your browser. ============================================")
    
    # Draw rating chart
    data = drawRating(result)
    rating = list(data.keys())
    count = list(data.values())
    fig = plt.figure(figsize = (10, 5))
    plt.bar(rating, count, color ='maroon', width = 0.4)
    plt.xlabel("Rating")
    plt.ylabel("No. of restaurant")
    plt.title("Number of restaurant in different rating")
    plt.show()
    print("============================ The graph should be shown in a popup window. =====================================")
    
    # Play with the tree - Price
    find_price = input("What price level are you looking for? (e.g. $,$$,$$$,$$$$)\n")
    if find_price == '$':
        print("============================ Here is the name of the restaurant: =====================================")
        for p in priceTree(tree(result))['$']:
            print(p)
    if find_price == '$$':
        print("============================ Here is the name of the restaurant: =====================================")
        for p in priceTree(tree(result))['$$']:
            print(p)
    if find_price == '$$$':
        print("======================= Here is the name of the restaurant: =====================================")
        for p in priceTree(tree(result))['$$$']:
            print(p)
    if find_price == '$$$$':
        print("======================= Here is the name of the restaurant: ========================================")  
        for p in priceTree(tree(result))['$$$$']:
            print(p)
    
    # Play with the tree - Open the website
    choose = input("Do you want to open the wensite of a restaurant? \n")
    if (choose == "yes" or choose == "Yes" or choose == "y" or choose == "Y"):
        web_name = input("Please enter the name of the restaurant. \n")
        openRestaurant(web_name,result)
        print("===================================== A website should be opened =============================================")
    else: 
        print("Bye")
    
    
    

