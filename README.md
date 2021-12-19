# Fall 2021 SI 507 Final Project
## Instruction
This project uses interactive command shell to search the restaurant information in a city. The user can specify which city to search, and get graphs of visualized restaurant information. This project uses API to get data from Yelp and cache the data as a JSON file, and scrap city information from Wikipedia. The visualization techniques include Plotly and Matplotlib. Websites of selcted cities and restaurants will popup automatically. 

## Data Sources
1. Yelp Fusion API: get information of resuaurants in a city. 
  * Link: https://www.yelp.com/developers/documentation/v3/business_search
  * Challenge score: 4. Web API you haven’t used before that requires API key or HTTP Basic authorization
3. Wikipedia website "List of United States cities by population": get inforamtion of the cities. 
  * Link: https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population
  * Challenge score: 4. Scraping a new single page

Total challenge score = 8

## Data Structure
The information of restaurants and cities are structured as a tree. Here is the tree structure:
![截屏2021-12-18 下午3 32 17](https://user-images.githubusercontent.com/49496754/146654800-70bedf71-e802-4ee1-badc-5e65cd586def.png)

## Demo Video
* Link: https://youtu.be/7ShAyLzmwzs

## Getting Start
### Prerequest
Python3, Plotly, JSON, requests, Matplotlib, pandas, BeautifulSoup, webbrowser, data structure, and command line tool

### Step 1: Apply an API Key for Yelp Fusion
1. Go to https://www.yelp.com/developers/documentation/v3/authentication and follow the instruction on the page.
2. Copy and paste the client id and api key into the python file named "secret.py"

### Step 2: Run the program and follow the instruction
Run final.py file and follow the instruction appears in the command line. 
