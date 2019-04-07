#Author: s3468489 Xinyu Ye
from sense_hat import SenseHat
from datetime import datetime
import os, json, time, requests
from project_config import logger,get_smooth_result,connection

"""
    this class is used for get accurate temperature, humidity, pressure from
    rasperberry pi and monitor the data, uploaded it to the database, if the 
    data exceed the range, it will send notification through pushbullet
"""
class Sending():

    def __init__(self):
        self.sense = SenseHat()
        self.connection = connection
        self.root_path = os.path.dirname(os.path.abspath(__file__))
    
    #get sense hat data, such as temp, humidity, pressure
    @logger
    def getSenseHatData(self):
        result = os.popen("vcgencmd measure_temp").readline()
        cpu_temp = float(result.replace("temp=","").replace("'C\n",""))

        temp_from_humdity = self.sense.get_temperature_from_humidity()
        temp_from_pressure = self.sense.get_temperature_from_pressure()
        
        temp = (temp_from_pressure + temp_from_humdity) / 2
        temp_corr = temp - ((cpu_temp-temp)/1.5)
        temp_corr = get_smooth_result(temp_corr)

        tim = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        humidity = self.sense.get_humidity()
        pressure = self.sense.get_pressure()

        return tim,temp_corr,humidity,pressure
    
    #upload the dataset to the database 
    @logger
    def uploadToDatabase(self):
        tim,temp,hum,pres = self.getSenseHatData()
        dataset = (tim,temp,hum,pres)
        stmt = "INSERT INTO MonitorData(time,temparature,humidity,pressure) VALUES (%s,%s,%s,%s)"
        with self.connection.cursor() as cursor:
            cursor.execute(stmt,dataset)
            self.connection.commit()
    
    #record the data from the latest uploading
    @logger
    def recordData(self):
        dataset = list()
        stmt = "SELECT * from MonitorData where id=(SELECT MAX(id) from MonitorData)"
        with self.connection.cursor() as cursor:
            cursor.execute(stmt)
            for row in cursor.fetchall():
                for i in row:
                    dataset.append(i)
        return dataset
    
    #append useful data to the data extract from database
    @logger
    def analyzeData(self):
        dataset = []
        file_path = os.path.join(self.root_path,"config.json")
        with open (file_path,'r') as fp:
            data_range = json.load(fp)  
        for i in range(1440): 
            time.sleep(60) 
            self.uploadToDatabase()
            data = self.recordData()
            if data[2] < data_range['min_temprature']:
                data.append('min_temp')
                data.append(data_range['min_temprature'] - data[2])
            if data[2] > data_range['max_temprature']:
                data.append('max_temp')
                data.append(data[2] - data_range['max_temprature'])
            if data[3] < data_range['min_humidity']:
                data.append('min_hum')
                data.append(data_range['min_humidity'] - data[3])
            if data[3] > data_range['max_humidity']:
                data.append('max_hum')
                data.append(data[3] - data_range['max_humidity'])
            dataset.append(data)
            
        return dataset

    #send the notification through the pushbullet        
    @logger
    def sendNotification(self):
        data_list = self.analyzeData()
        
        good = data_list[len(data_list)-1][1]

        bad_result = list()
        
        for row in data_list:
            if len(row) > 5:
                bad_result.append(row)
        if not bad_result:
            self.send(good,"OK")
            self.upload((good,"OK"))
        else:
            worse_one = 0
            worse_key = None
            worse_result = list()
            for record in bad_result:
                if record[6] > worse_one:
                    worse_one = record[6]
                    worse_result = record
                    worse_key = record[5]
                if len(record) == 9:
                    if record[8] > worse_one:
                        worse_one = record[8]
                        worse_result = record
                        worse_key = record[7]
            bad = worse_result[1]
            if worse_key == "min_temp":
                body = "BAD: {} *C below minimum temperature".format(worse_one)
                self.send(bad,body)
                self.upload((bad,body))
            elif worse_key =="max_temp":
                body = "BAD: {} *C above maximum temperature".format(worse_one)
                self.send(bad,body)
                self.upload((bad,body))
            elif worse_key =="min_hum":
                body = "BAD: {} *C below minimum humidity".format(worse_one)
                self.send(bad,body)
                self.upload((bad,body))
            elif worse_key =="max_hum":
                body = "BAD: {} *C above maximum humidity".format(worse_one)
                self.send(bad,body)
                self.upload((bad,body))
    
    #upload the data to the table report
    def upload(self,dataset):
        with self.connection.cursor() as cursor:
            stmt = "INSERT INTO Report(datetime,status) VALUES (%s,%s)"
            cursor.execute(stmt,dataset)
            self.connection.commit()

    #send through the pushbullet
    @staticmethod
    def send(title,body):
        ACCESS_TOKEN = "o.0J7h9XEfTrBCt0MF5aZIfQ8bkXznMfsc"
        data_send = {"type": "note", "title": title, "body": body}
        res = requests.post('https://api.pushbullet.com/v2/pushes',
        data = json.dumps(data_send), headers={'Authorization': 'Bearer '+ ACCESS_TOKEN,
        'Content-Type': 'application/json'})
        
        if res.status_code != 200:
            raise Exception('Sending failed!')
        else:
            print('Complete sending!')



if __name__ == "__main__":
    send = Sending()
    send.sendNotification()




