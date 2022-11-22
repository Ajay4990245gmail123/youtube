# import few libraries
from requests_html import HTMLSession                                 #import requests_html
from bs4 import BeautifulSoup as bs
from flask import Flask,render_template,request
import re
import json
app=Flask(__name__)  #add flask
@app.route("/",methods=["GET"])
def You_detail():
    return render_template("index1.html")
@app.route('/details',methods=["GET","POST"])
def TubeDetail():
    if request.method == "POST":
        try:
            Result = []
            searchString = request.form['content'] # html input area
            video_url =searchString
            session = HTMLSession()   #
            response = session.get(video_url) # getting link information
            UrlLink = bs(response.html.html, "html.parser") # information  convert into redable content and save urllink
            MetaLink=UrlLink.find_all("meta")  # get  the all  meta information
            data = re.search(r"var ytInitialData = ({.*?});",str(UrlLink)).group(1)
            data_json = json.loads(data) # convert html data to json data
            videoPrimaryInfoRenderer=data_json['contents']['twoColumnWatchNextResults']['results']['results']['contents'][0]['videoPrimaryInfoRenderer']
            # get video subscribers using json data
            videoSecondInfo=data_json['contents']['twoColumnWatchNextResults']['results']['results']['contents'][1]['videoSecondaryInfoRenderer']
            #get likes using json data
            likes_label=videoPrimaryInfoRenderer['videoActions']['menuRenderer']['topLevelButtons'][0]['segmentedLikeDislikeButtonRenderer']['likeButton']["toggleButtonRenderer"]["toggledText"]["accessibility"]['accessibilityData']['label']
            #get channel name json data in variable of urllink
            Channel=UrlLink.find("meta", itemprop="name")["content"]
            # get video views using json data
            views=UrlLink.find("meta", itemprop="interactionCount")['content']
            discription=UrlLink.find("meta", itemprop="description")['content']
            #get video  channel name
            channel_name =UrlLink.find("span", itemprop="author").next.next['content']
            #get video upload date
            UploadDate=UrlLink.find("meta", itemprop="uploadDate")['content']
            channel_url = searchString
            #get  subsccribers
            channel_subscribers =videoSecondInfo['owner']['videoOwnerRenderer']['subscriberCountText']['accessibility'][ 'accessibilityData']['label']
            #save all information  dictionary formate
            MyResult={"title":Channel, "views":views, "discription":discription,'name': channel_name,"UploadDate":UploadDate,'url': channel_url, 'subscribers': channel_subscribers,"likes":likes_label}
            # append the dictionary  values  in Result
            Result.append(MyResult)
            print(Result)
            # using flask   templates
            return render_template("results1.html",reviews=Result[0:1])

        except:
             return  "something went wrong"
    else:
         "some thing"

if __name__=="__main__":
    app.run( debug=True)
