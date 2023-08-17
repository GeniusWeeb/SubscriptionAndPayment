
# make payment and get a response 
# send result to the database 
# retrieve some data from database
import sqlite3 as db
from flask import  jsonify
from datetime import datetime 
import random



class Payments :
    
    def MakePaymentInternal(self ,data ):

        self.conn =  db.connect('subscriptions.db')
        cursor = self.conn.cursor()  
        #id is clientId
        id  = data.get('client_id')
        name = data.get('planName')
        query  = "SELECT cost FROM plans where planName = ?"
        cursor.execute(query ,( name,))
        result = cursor.fetchone()
        amount = result[0]
       
        currentDate =  datetime.now()
        ran = random.randint (0,1000)
        payRef = str(id)  + str(ran) + str(name)


        self.conn =  db.connect('subscriptions.db')
        cursor = self.conn.cursor()  
        cursor.execute('INSERT OR REPLACE INTO payment (client_id, planName , paymentRef , amount, date) VALUES (?, ? , ? ,?, ?)', (id, name ,payRef, amount , currentDate))
        self.conn.commit()

        responseData = {

        #client_id: id, 
        'status' : "Success" , 
        'payRef' : payRef , 
        #'date': currentDateFinal

        }

        return jsonify({'message': f'Payment successful  {responseData} '}), 201

        
    def GetAllPaymentsInternalPerUser(self, data):
        
        client_id = data.get('client_id')
        self.conn =  db.connect('subscriptions.db')
        cursor = self.conn.cursor()  
        cursor.execute('SELECT * from payment where client_id = ?' , (client_id , ))
        rows =  cursor.fetchall()  

        if not rows :
             return jsonify({'message': f'No Payments'}), 200

        results= [] 
        for row in rows:
            result = {

                'id' : row[0] , 
                'planName' :  row[1], 
                'PayRef': row[2], 
                'amount': int(row[4]), 
                'date':  row[3], 

                }
            results.append(result)
        self.conn.close()  
        

        return jsonify(results) 





if __name__ == "__main__":
    print(f"Payment file")