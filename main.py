#import all libraries
import json

from flask import Flask
from flask import request
from flask import render_template
from flask import make_response
from flask import redirect

app = Flask(__name__)

def format_time(time): 
    ms = time[-3:] if time[-3:] != '' else 0
    sec = time[-5:-3] if time[-5:-3] != '' else 0
    min = time[:-5] if time[:-5] != '' else 0

    return (int(min), int(sec), int(ms), f"{int(min):01}:{int(sec):02}.{ms}")

@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/how')
def howpage():
    return render_template('how.html')


@app.route('/extradata', methods = ['GET', 'POST'])
def extradatapage():

    if request.method == 'POST':
        jsondata = json.loads(request.form.get("data"))
        session_num = request.form.get("session_num") if request.form.get("session_num") is not None else "session1"
        
        number_of_solves = request.form.get('solves')

        dnfs = 0
        plus_2s = 0

        minute_solve = 0
        sub_minute_solve = 0
        sub_30_solve = 0
        sub_25_solve = 0
        sub_20_solve = 0
        sub_15_solve = 0
        sub_12_solve = 0
        sub_10_solve = 0

        i = 0
        
        number_of_solves = len(jsondata[session_num])

        for x in range(int(number_of_solves)):

            time = jsondata[session_num][i][0][1]
            i += 1

            min, sec, ms, formated_time = format_time(str(time))

            if jsondata[session_num][x][0][0] == 2000:
                sec += 2
                plus_2s += 1


            if jsondata[session_num][x][0][0] == 0:

                if min >= 1:
                    minute_solve += 1
                
                elif min == 0 and sec > 29:
                    sub_minute_solve += 1
                
                elif min == 0 and sec > 24:
                    sub_30_solve += 1
                
                elif min == 0 and sec > 19:
                    sub_25_solve += 1
                
                elif min == 0 and sec > 14:
                    sub_20_solve += 1
                
                elif min == 0 and sec > 11:
                    sub_15_solve += 1
                
                elif min == 0 and sec > 9:
                    sub_12_solve += 1
                
                else:
                    sub_10_solve += 1

            elif jsondata[session_num][x][0][0] == -1:
                dnfs += 1

        return render_template(
            'extradatapage.html',
            data = 'True',
            form = 'False',

            jsondata = jsondata,
            total_solves = number_of_solves,

            dnfs = dnfs,
            plus_2s = plus_2s,

            minute_solve = minute_solve,
            sub_minute_solve = sub_minute_solve,
            sub_30_solve = sub_30_solve,
            sub_25_solve = sub_25_solve,
            sub_20_solve = sub_20_solve,
            sub_15_solve = sub_15_solve,
            sub_12_solve = sub_12_solve,
            sub_10_solve = sub_10_solve,
        )

    elif request.method == 'GET':
        return render_template(
            'extradatapage.html',
            data = 'False',
            form = 'True',
        )
