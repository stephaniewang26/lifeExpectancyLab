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
    canadavalues = []
    usvalues = []
    mexicovalues = []

    for year in years:
        canadavalues.append(data["Canada"][year])
        usvalues.append(data["United States"][year])
        mexicovalues.append(data["Mexico"][year])

    print(years)
    print(canadavalues)
    print(usvalues)
    print(mexicovalues)
    # #Filter and reformat data for ease of access in the template
    # requested_data = data[requested_pet]
    # years = sorted(list(requested_data.keys()))
    # line_endpoints =[]
    # for i in range(len(years)-1): # make it easy to dynamically generate a line graph
    #     start_x = years[i] #generate endpoints for each line segment
    #     stop_x = years[i+1]
    #     line_endpoints.append([requested_data[start_x],requested_data[stop_x]] )

    # return render_template('individual_scores.html', pet=requested_pet, years = years, endpoints = line_endpoints)

    return render_template('index.html',year=requested_year,all_years=years,year_increment = yearsby10,age_increment = agerange)

@app.route('/year')
def year():
    return render_template('year.html')

app.run(debug=True)
