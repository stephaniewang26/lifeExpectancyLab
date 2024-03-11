# flask --app data_server run
from flask import Flask
from flask import request
from flask import render_template
import json

#test
app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def index():
    f = open("data/life_expectancy.json")
    data = json.load(f)
    f.close()

    #check to see if year is in the query string portion of the URL
    requested_year = request.args.get('year')
    if requested_year == None:
        requested_year = "2020" #just in case

    countries = sorted(list(data.keys()))
    years = sorted(list(data["Canada"].keys()))
    yearsby10 = []
    for i in range(0,len(years),10):
        yearsby10.append(years[i])

    agerange = [100,90,80,70,60,50,40]
    canadavalues = data["Canada"]
    usvalues = data["United States"]
    mexicovalues = data["Mexico"]

    print(years)
    print(canadavalues)
    print(usvalues)
    print(mexicovalues)
    # #Filter and reformat data for ease of access in the template
    # requested_data = data[requested_pet]
    # years = sorted(list(requested_data.keys()))
    canada_line_endpoints =[]
    us_line_endpoints =[]
    mex_line_endpoints =[]
    avg_line_endpoints=[]
    for i in range(len(years)-1): # make it easy to dynamically generate a line graph
        start_x = years[i] #generate endpoints for each line segment
        stop_x = years[i+1]
        #print(data["Canada"][start_x],data["Canada"][stop_x])
        canada_line_endpoints.append([canadavalues[start_x],canadavalues[stop_x]])
        us_line_endpoints.append([usvalues[start_x],usvalues[stop_x]])
        mex_line_endpoints.append([mexicovalues[start_x],mexicovalues[stop_x]])

        start_avg = (canadavalues[start_x]+usvalues[start_x]+mexicovalues[start_x])/3
        stop_avg = (canadavalues[stop_x]+usvalues[stop_x]+mexicovalues[stop_x])/3
        avg_line_endpoints.append([start_avg,stop_avg])


    # return render_template('individual_scores.html', pet=requested_pet, years = years, endpoints = line_endpoints)

    return render_template('index.html',year=requested_year,all_years=years,year_increment = yearsby10,age_increment = agerange, canadaendpoints = canada_line_endpoints, usendpoints=us_line_endpoints,mexicoendpoints=mex_line_endpoints, avgendpoints = avg_line_endpoints)

@app.route('/year')
def year():
    f = open("data/life_expectancy.json")
    data = json.load(f)
    f.close()

    #Check to see if year is passed via the query string portion of the URL
    requested_year = request.args.get('year')
    canadavalue = data["Canada"][requested_year]
    canadavalue = (85-canadavalue)*(8/3)+10
    usvalue = data["United States"][requested_year]
    usvalue = (85-usvalue)*(8/3)+10
    mexicovalue = data["Mexico"][requested_year]
    print(mexicovalue)
    mexicovalue = (85-mexicovalue)*(8/3)+10

    print(canadavalue,usvalue,mexicovalue)
    
    # if requested_pet not in data:
    #     requested_pet = "tigers"

    #Filter and reformat data for ease of access in the template
    # requested_data = data[requested_pet]
    # years = sorted(list(requested_data.keys()))
    # line_endpoints =[]
    # for i in range(len(years)-1): # make it easy to dynamically generate a line graph
    #     start_x = years[i] #generate endpoints for each line segment
    #     stop_x = years[i+1]
    #     line_endpoints.append([requested_data[start_x],requested_data[stop_x]] )

    # return render_template('individual_scores.html', pet=requested_pet, years = years, endpoints = line_endpoints)
    return render_template('year.html',year=requested_year,canadavalue=canadavalue,usvalue=usvalue,mexicovalue=mexicovalue)

app.run(debug=True)
