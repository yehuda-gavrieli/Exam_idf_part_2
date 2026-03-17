from fastapi import FastAPI
import mysql.connector
#import matplotlib

app = FastAPI()


def get_connection():
    return mysql.connector.connect(host="localhost" , port=3308 , user="root" , password="root" , database="digital_hunter")


@app.get("/alert_movments")
def get_alert_movments():
    DB = get_connection()
    cursor = DB.cursor(dictionary=True)
    query1 = """ select entity_id ,target_name,priority_level from targets
where priority_level in (1 , 2) and  movement_distance_km > 5
"""

    cursor.execute(query1)
    result = cursor.fetchall()
    DB.close()
    return result


@app.get("/analysis_sources")
def get_analysis_sources():
    DB = get_connection()
    cursor = DB.cursor(dictionary=True)
    query2 = """ select signal_type , count(*) AS COUNT from intel_signals
group by signal_type
order by count desc
"""

    cursor.execute(query2)
    result = cursor.fetchall()
    DB.close()
    return result




@app.get("/new_targets")
def get_new_targets():
    DB = get_connection()
    cursor = DB.cursor(dictionary=True)
    query3 = """ select entity_id , count(*) AS unknoen_count from intel_signals
WHERE priority_level = 99
group by entity_id 
order by unknoen_count desc
limit 3

"""

    cursor.execute(query3)
    result = cursor.fetchall()
    DB.close()
    return result


@app.get("/test/{entity_id}")
def get_test(entity_id):
    DB = get_connection()
    cursor = DB.cursor(dictionary=True)
    query5 = f"""select reported_lat , reported_lon , timestamp from intel_signals
                WHERE entity_id ='{entity_id}' 
                order by timestampc desc limit 1"""

    cursor.execute(query5)
    result = cursor.fetchone()
    DB.close()
    return {"lat":result["reported_lat"],"lon":result["reported_lon"]}