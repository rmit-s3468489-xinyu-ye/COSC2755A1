#!/usr/bin/python3

import MySQLdb
from functools import wraps

# the imformation of database connection
HOST = "localhost"
USER = "pi"
PASSWORD = "secret"
DATABASE = "SenseHatData"

connection = MySQLdb.connect(HOST,USER,PASSWORD,DATABASE)

#create table method, if table exist, drop and recreate it
def createTable():
    with connection.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS MonitorData")
        cursor.execute("CREATE TABLE MonitorData(id INT AUTO_INCREMENT PRIMARY KEY,time VARCHAR(50), temparature DECIMAL(8,2), humidity DECIMAL(8,2), pressure DECIMAL(8,2))")
        cursor.execute("DROP TABLE IF EXISTS Report")
        cursor.execute("CREATE TABLE Report(datetime VARCHAR(50), status VARCHAR(100))")
        connection.commit()

#logger detector, used for recording the basic logging       
def logger(original_func):
    import logging, time, os
    root_path = os.path.dirname(os.path.abspath(__file__))
    logging.basicConfig(filename="{}.log".format(os.path.join(root_path,"Log_File/Project")),level=logging.INFO)
    @wraps(original_func)
    def wrapper(*args,**kwargs):
        if bool(kwargs):
            logging.info("Function {} ran with argument: {}, and keyword argument: {}".format(original_func.__name__,args,kwargs))
        else:
            logging.info("Function {} ran with argument: {}, and keyword argument: None".format(original_func.__name__,args))
        start_time = time.time()
        result = original_func(*args,**kwargs)
        cost_time = time.time() - start_time
        logging.info("Function {} ran suceessful and it ran in: {} seconds".format(original_func.__name__,cost_time))
        return result
    return wrapper

#get the smooth result
def get_smooth_result(x):
    if not hasattr(get_smooth_result, "r"):
        get_smooth_result.r = [x,x,x]
    
    get_smooth_result.r[2] = get_smooth_result.r[1]
    get_smooth_result.r[1] = get_smooth_result.r[0]
    get_smooth_result.r[0] = x

    return (get_smooth_result.r[0] + get_smooth_result.r[1] + get_smooth_result.r[2]) / 3

if __name__ == "__main__":
    createTable()
