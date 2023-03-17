from django.shortcuts import render
import requests
from bs4 import BeautifulSoup as bs

# Create your views here.

def home(request):
    return render(request, "home.html")

def search(request):
    if request.method == "POST":
        #check the input field (in our html file) with name 'search' for query string
        search = request.POST['search']
        url = "https://www.ask.com/web?q="+search
        res = requests.get(url)
        soup = bs(res.text, "lxml")
        result_listings = soup.find_all("div", {"class": "PartialSearchResults-item"})

        final_result = []
        for result in result_listings:
            result_title = result.find(class_="PartialSearchResults-item-title").text
            result_url = result.find('a').get('href')
            result_description = result.find(class_="PartialSearchResults-item-abstract").text

            final_result.append((result_title,result_url,result_description))
        
        # context we pass into the html page with our search results, urls, and descriptions
        context = {
            "final_result": final_result
        }
        return render(request, 'search.html', context=context)
    else:
        return render(request, 'search.html')