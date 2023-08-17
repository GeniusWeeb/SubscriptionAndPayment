from flask import Flask , request , jsonify
import sqlite3 as db
from datetime import datetime , timedelta
from plans import Plan
from Payment import Payments



app =  Flask(__name__)


class Subscription: 

    def __init__(self):
        print(f"Running subscriptions")

      
        
    #sqlite3 => Auto done as soon as the class is created
    #creates a db if it doesnt exist   
        self.conn =  db.connect('subscriptions.db')
        self.conn.execute('CREATE TABLE IF NOT EXISTS subscriptions (client_id TEXT PRIMARY KEY, plan TEXT , endDate TEXT)')
        self.conn.execute('CREATE TABLE IF NOT EXISTS plans (id TEXT PRIMARY KEY, planName TEXT , days TEXT, description TEXT , cost TEXT)')
        self.conn.execute('CREATE TABLE IF NOT EXISTS payment (client_id TEXT PRIMARY KEY, planName TEXT , paymentRef TEXT, date TEXT , amount TEXT)')


        self.conn.commit()

    #User comes in -> wants to join  -> use this


#region EXPOSE API


    def Subscribe(self , data):
        #only 1st time entry allowed
       
        print(f"New User")
        print(datetime.now)


        #-----------------------------
        client_id = data.get('client_id')
        plan =  data.get('plan')
        if self.GetUserExists(client_id):
            return jsonify({'message': f' This user already subscribed to plan'}), 999
        
        self.conn =  db.connect('subscriptions.db')
        cursor = self.conn.cursor()  
        query  = "SELECT cost FROM plans where planName = ?"
        cursor.execute(query , (plan ,))
        result = cursor.fetchone()
        planDaysToAdd = result[0]
      
        endDateStr  =  datetime.now() + timedelta(days=float(planDaysToAdd))
        endDate =  str(endDateStr)
        endDate = endDate.split(" ")
        endDate[-1] = endDate[-1][:8]
        endDate = " ".join(endDate)

       # if not client_id:
         #   return jsonify ( {'message': 'client_id is required'}),400
        
      #  if not plan or plan not in self.:
            #return jsonify({'message': 'Invalid subscription plan'}), 400
     
        cursor.execute('INSERT OR IGNORE INTO subscriptions (client_id, plan, endDate) VALUES (?, ? , ?)', (client_id, plan ,endDate ))
        self.conn.commit()
        return jsonify({'message': f'Subscribed client_id: {client_id} with plan: {plan}'}), 201
    
    #GET CURRENT PLAN  -  EXPOSE - JSON - STRINGS
    def GetCurrentPlan(self, data):

        client_id =  data.get('client_id')
     


         
        self.conn =  db.connect('subscriptions.db')
        cursor = self.conn.cursor()
        cursor.execute('SELECT plan, endDate FROM subscriptions WHERE client_id = ?' , (client_id, ))
        result =  cursor.fetchone()
        if(result):
           # print(f"plan name is ?",(result[0]))
           # print(f"end Date is ?",(result[1]))
            plan  =  result[0] ,   
            endDate  =  result[1]
            endDate = endDate.split(" ")
            endDate[-1] = endDate[-1][:8]
            endDate = " ".join(endDate)
            responseData = {
                'plan' : plan[0] , 
                'endDate': endDate  
          } 
            self.CheckPlanStatus(data.get('client_id'))
            return jsonify(responseData)
        
        else: 
            return jsonify("User has not subbed to any plans") 
        
       
        #return plan , endDate    


    def EndSubscription(self  , client_id):
        if not self.GetUserExists(client_id):
            return 
        
        self.conn =  db.connect('subscriptions.db')
    
        self.conn.cursor().execute('DELETE from subscriptions WHERE client_id = ?' , (client_id , ))
        self.conn.commit()

        return jsonify({'message': f'Subscription for client_id {client_id} has been ended'}), 200

        #tuple w single elements
        

   
#endregion    

#region internal
    def GetUserExists(self ,client_id) :
        self.conn =  db.connect('subscriptions.db')
        cursor = self.conn.cursor()
        cursor.execute('SELECT client_id FROM subscriptions WHERE client_id = ?' , (client_id, ))
        existingclient_id =  cursor.fetchone()
        cursor.close()
         #None or client_id with tuple
        if(existingclient_id):
            print(existingclient_id[0])
            return True
        else:
            return False
          
   
    def CheckPlanStatus(self, client_id):
           #Check if subscription is already over
         endDateStr = self.GetEndDate(client_id)  # Assuming this returns a string
         endDate = datetime.strptime(endDateStr, "%Y-%m-%d %H:%M:%S")  # Convert to datetime.datetime
         if datetime.now() > endDate:
            self.EndSubscription(client_id)
            return jsonify({'message': f'Subscribed has ended'}), 201
       
    def GetEndDate(self, currentclient_id):

        if not self.GetUserExists :
            return

        cursor = self.conn.cursor()
        cursor.execute('SELECT endDate FROM subscriptions WHERE client_id = ?', (currentclient_id,))
        result = cursor.fetchone()
        if result:
            endDate =  result[0]
            return endDate
#endregion   


subApp =  Subscription()
subPlan = Plan()
payment = Payments()




@app.route('/api/subscribe' , methods = ['POST'])
def SubscribeAPI():
    data =  request.get_json()
    if not data :
        return jsonify({'message': f'request body is invalid '}), 666
    
    return subApp.Subscribe(data)



@app.route('/api/endSub' , methods = ['POST'])
def EndSubscription():
    data =  request.get_json()
    if not data :
        return jsonify({'message': f'request body is invalid '}), 666
    client_id =  data.get('client_id')
    return subApp.EndSubscription(client_id)
   

@app.route('/api/currentSubPlan' , methods = ['POST'])
def GetCurrentSubPlan():
    data = request.get_json()  
    if not data :
        return jsonify({'message': f'request body is invalid '}), 666
    return subApp.GetCurrentPlan(data)




@app.route('/api/add_plan' , methods = ['POST'])
def AddPlan():
    data = request.get_json()
    if not data:
        return jsonify({'message': f'request body is invalid '}), 666

    return subPlan.CreatePlan(data) 

@app.route('/api/get_plan' , methods = ['GET'])
def ReadPlan():
    return subPlan.GetReadPlans()


@app.route('/api/update_plan' , methods = ['POST'])
def UpdatePlans():
    data = request.get_json()
    if not data:
        return jsonify({'message': f'request body is invalid '}), 666

    return subPlan.UpdatePlanInternal(data)


@app.route('/api/delete_plan' , methods = ['POST'])
def DeletePlan():
    data = request.get_json()
    if not data:
        return jsonify({'message': f'request body is invalid '}), 666

    return subPlan.DeletePlanInternal(data)


@app.route('/api/make_payment' , methods = ['POST'])
def MakePayment():
    data = request.get_json()
    if not data:
        return jsonify({'message': f'request body is invalid '}), 666

    return payment.MakePaymentInternal(data)


@app.route('/api/get_payments' , methods = ['POST'])
def GetAllPayments():
    data = request.get_json()
    if not data:
        return jsonify({'message': f'request body is invalid '}), 666

    return payment.GetAllPaymentsInternalPerUser(data)






if __name__ == "__main__":
    app.run( port=8000 ,debug= True , host="0.0.0.0")



    #docker run -p 8000:8000 barotemus/subpay
    
  
  
