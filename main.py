from fastapi import FastAPI
import mysql.connector
import matplotlib.pyplot as plt
from DigitalHunter_map import plot_map_with_geometry


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


@app.get("/Identifying_sleeping_cells")
def get_Identifying_sleeping_cells():
    DB = get_connection()
    cursor = DB.cursor(dictionary=True)
    query4 = """ select distinct entity_id from intel_signals
            where (timestamp >= '2026-03-15 08:00:00' and timestamp <= '2026-03-15 20:00:00')
            and  distance_from_last = 0
            and entity_id in (select distinct entity_id from intel_signals
            where (timestamp <= '2026-03-15 08:00:00' and timestamp >= '2026-03-15 20:00:00')
            and  distance_from_last >= 10)
            """
    cursor.execute(query4)
    result = cursor.fetchall()
    DB.close()
    return result


@app.get("/test/{entity_id}")
def get_test(entity_id):
    DB = get_connection()
    cursor = DB.cursor(dictionary=True)
    query5 = f"""select reported_lat , reported_lon , timestamp from intel_signals
                WHERE entity_id ='{entity_id}' 
                order by timestamp desc
                """
    cursor.execute(query5)
    result = cursor.fetchall()
    DB.close()

    if not result:
        return {"entity_id not correct"}
    
    all_point = []

    for res in result:
        point = (res["reported_lat"],res["reported_lon"])
        
        all_point.append(point) 

    plot_map_with_geometry(all_point)


# דיברתי עם אוהד(אם אני לא טועה) כי הקובץ תמונה לא עבד לי וגם שהעתקתי את זה כנתיב זה לא עזר
# ולכן הוא אמר להוסיף את זה בהערה שלמטה זה מה שעשיתי בלי הפונקציית עזר ולמעלה זה מה שעם הפונקציה (בלי לבדוק אם זה עובד)
 
 
 
    # all_lat = []
    # all_lon = []

    # for res in result:
    #     lat = res["reported_lat"]
    #     lon = res["reported_lon"]
        
    #     all_lat.append(lat) 
    #     all_lon.append(lon)


    # plt.plot(all_lat, all_lon , color='blue' ,linestyle='solid') 
    # plt.plot(all_lat[0], all_lon[0] , color='green', marker='o' , markersize=5)
    # plt.plot(all_lat[-1], all_lon[-1] , color='red' , marker='o' , markersize=5) 
    # plt.show()      

    # return {"status": "working"}

