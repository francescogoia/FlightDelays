from database.DB_connect import DBConnect
from model.airport import Airport
from model.connessione import Connessione


class DAO():

    @staticmethod
    def getAllAirports():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
        from airports a
        order by a.AIRPORT asc"""

        cursor.execute(query)

        for row in cursor:
            result.append(Airport(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(num_compagnie, idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select tmp.ID , tmp.IATA_CODE ,tmp.AIRPORT, tmp.CITY, tmp.STATE, tmp.COUNTRY, tmp.LATITUDE, tmp.LONGITUDE, tmp.TIMEZONE_OFFSET, count(*) as N_AIRLINES 
                    from (
                                select a.ID , a.IATA_CODE ,a.AIRPORT, a.CITY, a.STATE, a.COUNTRY, a.LATITUDE, a.LONGITUDE, a.TIMEZONE_OFFSET, f.AIRLINE_ID , count(*) as n
                                from airports a , flights f 
                                where a.ID = f.ORIGIN_AIRPORT_ID or a.ID = f.DESTINATION_AIRPORT_ID 
                                group by a.ID , a.IATA_CODE , f.AIRLINE_ID 
                    ) as tmp
                    group by tmp.ID, tmp.IATA_CODE
                    having N_AIRLINES >= %s"""

        cursor.execute(query, (num_compagnie, ))

        for row in cursor:
            result.append(idMap[row["ID"]])     ## aggiungo a result l'aereoporto cercandolo dall'idMap

        cursor.close()
        conn.close()
        return result
    @staticmethod
    def getAllEdgesV1(idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
            select f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID , count(*) as n
            from flights f 
            group by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID 
            order by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID 
        """

        cursor.execute(query)

        for row in cursor:
            result.append(Connessione(
                idMap[row["ORIGIN_AIRPORT_ID"]],
                idMap[row["DESTINATION_AIRPORT_ID"]],
                row["n"]
            ))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdgesV2(idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
            select t1.ORIGIN_AIRPORT_ID, t1.DESTINATION_AIRPORT_ID, coalesce (t1.n, 0) + coalesce (t2.n, 0) as n
            from (select f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID , count(*) as n
                    from flights f 
                    group by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID 
                    order by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID ) as t1
                left join (select f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID , count(*) as n
                            from flights f 
                            group by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID 
                            order by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID ) as t2
                on t1.ORIGIN_AIRPORT_ID = t2.DESTINATION_AIRPORT_ID and t1.DESTINATION_AIRPORT_ID = t2.ORIGIN_AIRPORT_ID
            where t1.ORIGIN_AIRPORT_ID < t1.DESTINATION_AIRPORT_ID or t2.ORIGIN_AIRPORT_ID is null
        """

        cursor.execute(query)

        for row in cursor:
            result.append(Connessione(
                idMap[row["ORIGIN_AIRPORT_ID"]],
                idMap[row["DESTINATION_AIRPORT_ID"]],
                row["n"]
            ))

        cursor.close()
        conn.close()
        return result
