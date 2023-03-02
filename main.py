from flask import Flask,render_template,request,send_file,after_this_request
from bs4 import BeautifulSoup
import requests
import re




server = Flask(__name__)

@server.route("/")

def index():
    return render_template("index.html")

@server.route("/search",methods=["POST"])

def search():
    form_data= request.form
    filtered_links ={}
    mname=form_data["url"]
    API_KEY = 'AIzaSyD4wgD217rChlezK3d7asdQyE6Q21qPY_w'
    
# replace SEARCH_QUERY with your search query
    SEARCH_QUERY = mname+' -inurl:(htm|html|php|pls|txt) intitle:index.of (mp4|wma|aac|avi|mkv)'

    # define the API endpoint
    API_ENDPOINT = 'https://www.googleapis.com/customsearch/v1'

    # define the search parameters
    params = {
        'key': API_KEY,
        'cx': 'c5a6a940d934a45a2',
        'q': SEARCH_QUERY
    }

    # make a request to the API and get the JSON response
    response = requests.get(API_ENDPOINT, params=params)
    json_data = response.json()

    # extract the search results from the JSON response
    search_results = json_data['items']

    # print out the title and URL of each search result
    i=0
    for result in search_results:
        if(i>5):
            break
            
    
        
        
        website_url = result['link']
     
        try:
            response = requests.get(website_url,timeout=10)

            soup = BeautifulSoup(response.content, 'html.parser')
            
            if(soup):
                pres=soup.find_all('body')

                if pres is not None:
                    j=0
                    for pre in pres:
                        a_tags = pre.find_all('a')
                    #  for pre in pres:
                    #     print(pre)
                        
                        # print out the href attributes of each a tag
                        if(a_tags is not None):
                            
                        
                            for a in a_tags:
                                    
                                    
                                        link=a['href']
                                        print(j)

                                       
                                        if (link.endswith('.mkv') or link.endswith('.mp4') or link.endswith('.avi')):
                                            STRING=a.text
                                            WORD=mname
                                            
                                            word_list = re.findall(r'\b\w+\b', STRING)
                                            lowercase_word_list = [word.lower() for word in word_list]


                                            word_list1 = WORD.split()
                                            lword_list1=[word.lower() for word in word_list1]

                                            common_words = set(lword_list1).intersection(set(lowercase_word_list))
                                            if(common_words):

                                                filtered_links[a.text]=website_url+link
                                                print(a.text)
                                                j+=1
                                            
                                        if(j>5):
                                            break

                                
                        
                        
                else:
                    print("Soup null")
            else:
                print('response null')
            i+=1
        except requests.Timeout:
           print(f'Request timed out after 15 seconds')
                        
   # return filtered_links
    return render_template("search.html",title=mname,links=filtered_links)



server.run(debug=True)