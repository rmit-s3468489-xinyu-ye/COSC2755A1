#Author: s3468489 Xinyu Ye
import matplotlib.pyplot as plt
from project_config import connection
import json,os





"""This class is used for analyze data store in the table MonitorData, 
and generate the graphs."""
class Graph():

    def __init__(self):
        self.connection = connection
        self.root_path = os.path.dirname(os.path.abspath(__file__))

    #get data from database
    def getTheData(self):
        dataset= list()
        stmt = "SELECT * FROM MonitorData"
        with self.connection.cursor() as cursor:
            cursor.execute(stmt)
            for row in cursor.fetchall():
                dataset.append(row)
        return dataset
    #grouping the temp and humidity data from the database
    def analyzeTheData(self):
        min_temp=0
        max_temp=0
        min_hum=0
        max_hum=0
        temp_range=0
        hum_range = 0
        data = self.getTheData()
        file_path = os.path.join(self.root_path,"config.json")
        with open(file_path,'r') as fp:
            data_range = json.load(fp)
        for row in data:
            if row[2] < data_range['min_temprature']:
                min_temp += 1
            if row[2] > data_range['max_temprature']:
                max_temp += 1
            if row[2] < data_range['max_temprature'] and row[2] > data_range['min_temprature']:
                temp_range += 1
            if row[3] < data_range['min_humidity']:
                min_hum += 1
            if row[3] > data_range['max_humidity']:
                max_hum += 1
            if row[3] < data_range['max_humidity'] and row[3] > data_range['min_humidity']:
                hum_range += 1
        labels = ["Exceed max temp","Exceed min temp","Exceed max humidity","Exceed min humidity","In temp range","In humidity range"]
        values = [max_temp,min_temp,max_hum,min_hum,temp_range,hum_range]
        return values,labels

    #generate pie chats
    def generatePieChats(self):
        plt.figure(figsize=(15,15))
        values,labels = self.analyzeTheData()    
        plt.pie(values,labels=labels)
        filename_pie = os.path.join(self.root_path,"pie_chat.png")
        plt.savefig(filename_pie)

    #generate scatter plots
    def generateScatterPlots(self):   
        plt.figure(figsize=(15,15))
        values,labels = self.analyzeTheData() 
        plt.scatter(labels,values, label='datascat', color= 'r', marker='x')
        plt.xlabel('status')
        plt.ylabel('value')
        filename_sca = os.path.join(self.root_path,"scatter.png")
        plt.savefig(filename_sca)

    #generate Bar charts and Histograms
    def generateBarCharts(self): 
        plt.figure(figsize=(15,15))
        values,labels = self.analyzeTheData() 
        plt.bar(labels,values,label='DataBars',color='b')
        plt.xlabel('status')
        plt.ylabel('value')
        plt.legend()
        filename_bar = os.path.join(self.root_path,"bar.png")
        plt.savefig(filename_bar)

    #generate Line plots
    def generateLinePlots(self): 
        plt.figure(figsize=(15,15))
        values,labels = self.analyzeTheData() 
        plt.plot(labels,values)
        filename_line = os.path.join(self.root_path,"line.png")
        plt.savefig(filename_line)

 
if __name__ == "__main__":
    graph = Graph()
    graph.generateBarCharts()
    graph.generateLinePlots()
    graph.generatePieChats()
    graph.generateScatterPlots()
 
