## Amazon Web Scrapper
from flask import Flask , render_template , request , jsonify
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import pymongo

app= Flask(__name__)             # initialising the flask app with the name 'app'


@app.route('/',methods=['POST','GET']) # route with allowed methods as POST and GET

def index():
    if request.method== 'POST' :
        searchstring=request.form['content'].replace("","") ## We are entering search string in our HTML Form , so we are fetching that string from here
        try:
            dbconn=pymongo.MongoClient("mongodb://localhost:27017/") ## setting up connection with MongoDB
            db=dbconn['AmazonDB'] ## Connecting to a database called Amazon DB
            reviews = db[searchstring].find({}) #
            if reviews.count() > 0:  # if there is a collection with searched keyword and it has records in it
             return render_template('results.html', reviews=reviews)
            else:
                link="https://www.amazon.in/s?k=" + searchstring
                openlink=uReq(link)  ## Open Connection Request
                amazon=openlink.read() ## Read data from Connection Request
                openlink.close() ## Close connection request
                amazon_html=bs(amazon,"html.parser") ## parsing the webpage as HTML
                box=amazon_html.findAll("div",{"class:sg-col-inner"})
                del box[0:3]
                box1=box[0]
                productlink="https://www.amazon.in/"+box1.div.h2.a['href']
                prodres=request.get(productlink)
                prodres_html=bs(prodres.txt,"html.parser") # parsing text into HTML
                reviewsection=prodres_html.findall('div',{'class':"a-section review aok-relative"}) ## getting into review section
                table=db[searchstring] ## Storing search strings
                reviews=[] # creating a table named reviews

                for reviews in reviewsection:
                    try:
                        name=reviews.div.div.div.div.findall('span',{'class':"a-profile-name"})[0].text
                    except:
                        name='No Name'
                    mydict = {"Product": searchstring, "Name": name}  # saving that detail to a dictionary
                    x = table.insert_one(mydict)  # insertig the dictionary containing the rview comments to the collection
                    reviews.append(mydict)  # appending the comments to the review list
                return render_template('results.html', reviews=reviews)  # showing the review to the user
        except:
            return 'something is wrong'
                # return render_template('results.html')
    else:
        return render_template('index.html')
if __name__ == "__main__":
        app.run(port=8000, debug=True)  # running the app on the local machine on port 8000



