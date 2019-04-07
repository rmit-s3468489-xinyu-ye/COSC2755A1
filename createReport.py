#Author: s3634919 Renning Liu
import csv, os
from project_config import logger, connection

#this class is used for creating csv file
class create():
    def __init__(self):
        self.connection = connection
        self.root_path = os.path.dirname(os.path.abspath(__file__))

    #get all of the data from the Report table
    def readFromDatabase(self):
        dataset = list()
        stmt = "SELECT * from Report"
        with self.connection.cursor() as cursor:
            cursor.execute(stmt)
            for row in cursor.fetchall():
                dataset.append(row)
        return dataset

    #write into the csv file
    def createCSV(self):
        file_path = os.path.join(self.root_path,"report.csv")
        data = self.readFromDatabase()
        with open(file_path,'w') as fp:
            file_writer = csv.writer(fp)
            file_writer.writerow(["Time","Status"])
            for value in data:
                file_writer.writerow([value[0],value[1]])
        

if __name__ == "__main__":
    cr = create()
    cr.createCSV()



