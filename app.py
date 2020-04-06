# Tutorial to use ==> (1) https://dzone.com/articles/restful-web-services-with-python-flask
#                     (2) https://www.geeksforgeeks.org/flask-creating-first-simple-application/
#                     (3) https://www.tutorialspoint.com/flask/index.htm

# for Run ==>  " Python firstApi.py "

# Importing flask module in the project is mandatory 
# An object of Flask class is our WSGI application. 
from flask import Flask 
from flask import jsonify
from flask import request

# Flask constructor takes the name of  
# current module (__name__) as argument. 
app = Flask(__name__) 
  
# The route() function of the Flask class is a decorator,  
# which tells the application which URL should call  
# the associated function.

empDB=[
 {
 'id':'101',
 'name':'Saravanan S',
 'title':'Technical Leader'
 },
 {
 'id':'201',
 'name':'Rajkumar P',
 'title':'Sr Software Engineer'
 }
 ]

@app.route('/empdb/employee',methods=['GET'])
def getAllEmp():
    return jsonify({'emps':empDB})

@app.route('/empdb/employee/<empId>',methods=['GET'])
def getEmp(empId):
    usr = [ emp for emp in empDB if (emp['id'] == empId) ] 
    return jsonify({'emp':usr})

@app.route('/empdb/employee/<empId>',methods=['PUT'])
def updateEmp(empId):
    em = [ emp for emp in empDB if (emp['id'] == empId) ]
    if 'name' in request.json : 
        em[0]['name'] = request.json['name']
    if 'title' in request.json:
        em[0]['title'] = request.json['title']
    return jsonify({'emp':em[0]})

@app.route('/empdb/employee',methods=['POST'])
def createEmp():
    dat = {
    'id':request.json['id'],
    'name':request.json['name'],
    'title':request.json['title']
    }
    empDB.append(dat)
    return jsonify(dat)

@app.route('/empdb/employee/<empId>',methods=['DELETE'])
def deleteEmp(empId):
    em = [ emp for emp in empDB if (emp['id'] == empId) ]
    if len(em) == 0:
       abort(404)
    empDB.remove(em[0])
    return jsonify({'response':'Success'})


@app.route('/predict/values/test', methods=['GET'])  
def predictedValueTest():
    student1 ={'name':'sasadara','Maths':85,'Chemistry':95,'Physics':80}
    student1['name'] = 'sahas'
    student1['English']=100
    student2 ={'name':'sasadara','Maths':99,'Chemistry':95,'Physics':96}
    student2['name'] = 'sasadara'
    student2['English']=100
    myList = []
    myList.append(student1)
    myList.append(student2)
    return jsonify(myList)


############################################################################################
#()()()()()()()()()()()(+++++++ Covid Prediction JPS +++++++  )()()()()()()()()()()()()()()()
############################################################################################
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
@app.route('/predict/values', methods=['POST'])  
def predictedValue():
   # {
   #    "day":21
   # }

    dataset=pd.read_csv('COVID-19 SL 03-11 to 03-24.csv').values
    data=dataset[:,0].reshape(-1,1)
    target=dataset[:,1].reshape(-1,1)
    poly=PolynomialFeatures(degree=4,include_bias=False)
    data_new=poly.fit_transform(data)
    algorithm=LinearRegression()
    algorithm.fit(data_new,target)
    #print('Coefficients:',algorithm.coef_)
    #print('Intercept:',algorithm.intercept_)
    
    dayNo = request.json['day']
        
    test_data_new=poly.fit_transform([[dayNo]])
    predicted_target_next_days=algorithm.predict(test_data_new)
    
    return str(predicted_target_next_days[0][0])
###########################################################################################
#()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()
###########################################################################################



# main driver function 
if __name__ == '__main__': 
  
    # run() method of Flask class runs the application  
    # on the local development server. 
    app.run() 
