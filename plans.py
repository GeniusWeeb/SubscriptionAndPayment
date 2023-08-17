import sqlite3 as db 
from flask import Flask , request , jsonify

class Plan:

#region  Internal functions


    def CreatePlan(self, data):

        id  = data.get('id')
        name = data.get('planName')
        days = data.get('days')
        descrip = data.get('description')
        cost = data.get('cost')
        

       # if not id or name or days or descrip or cost:
          #  return jsonify({'message': f'Incomplete data'}), 201

            

        self.conn =  db.connect('subscriptions.db')
        cursor = self.conn.cursor()  
        cursor.execute('INSERT OR IGNORE INTO plans (id, planName, days , description , cost) VALUES (?, ? , ? ,? , ?)', (id, name ,days ,descrip , cost ))
        self.conn.commit()
        return jsonify({'message': f'Plan created table'}), 201


    def DeletePlanInternal(self, data):
        id = data.get('id')
        self.conn =  db.connect('subscriptions.db')
        cursor = self.conn.cursor()  
        self.conn.cursor().execute('DELETE from plans WHERE id = ?' , (id , ))
        self.conn.commit()

        return jsonify({'message': f'Plan Deleted '}), 201


    def GetReadPlans(self ):
        self.conn =  db.connect('subscriptions.db')
        cursor = self.conn.cursor()  
        cursor.execute('SELECT * from plans')
        rows =  cursor.fetchall()

        if not rows :
             return jsonify({'message': f'Empty table'}), 200

        results= [] 
        for row in rows:
            result = {

                'id' : row[0] , 
                'planName' :  row[1], 
                'days':  int(row[2]), 
                'description':  row[3], 
                'cost': float (row[4]), 

                }
            results.append(result)
        self.conn.close()  
        

        return jsonify(results)

            
    def UpdatePlanInternal(self,data):
       
        id  = data.get('id')
        name = data.get('planName')
        days = data.get('days')
        descrip = data.get('description')
        cost = data.get('cost')

        #if  id or name or days or descrip or cost is None:
         #   return jsonify({'message': f'Incomplete data'}), 201

        self.conn =  db.connect('subscriptions.db')
        cursor = self.conn.cursor()  
        cursor.execute( 'REPLACE INTO plans (id, planName, days, description, cost) VALUES (?, ?, ?, ?, ?)', (id, name, days, descrip, cost))

        self.conn.commit()


        return jsonify({'message': f'Plan updated '}), 201

     
#endregion

        
    
if __name__ == "__main__" :
    pass

        
        