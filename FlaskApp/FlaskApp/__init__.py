import json

from flask import Flask, render_template
import pandas as pd
import pygal

app = Flask(__name__)
e = 'This is an error message'


@app.route("/")
def index():
    df = pd.read_csv('output.csv')
    chart_data = df.to_dict(orient='records')
    chart_data = json.dumps(chart_data, indent=2)
    data = {'chart_data': chart_data}
    return render_template("index.html", data=data)


@app.route('/pygalexample/')
def pygalexample():
    try:
        graph = pygal.Line()
        graph.title = '% Change Coolness of programming languages over time.'
        graph.x_labels = ['2011','2012','2013','2014','2015','2016']
        graph.add('Python',  [15, 31, 89, 200, 356, 900])
        graph.add('Java',    [15, 45, 76, 80,  91,  95])
        graph.add('C++',     [5,  51, 54, 102, 150, 201])
        graph.add('All others combined!',  [5, 15, 21, 55, 92, 105])
        graph_data = graph.render_data_uri()
                return render_template("graphing.html", graph_data)
    except Exception, e:
        return(str(e))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
