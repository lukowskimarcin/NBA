from graph import NBAGraph
import pyodbc
import json


class GraphRepository:

    def __init__(self) -> None:
        self.connection_string = "DRIVER={ODBC Driver 18 for SQL Server};SERVER=127.0.0.1,5433;Encrypt=no;DATABASE=msdb;UID=sa;PWD=sa!234#sa$%" 


    def find_all(self) -> list[NBAGraph]:
        graphs = []
        conn = pyodbc.connect(self.connection_string)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM NBA")
        rows = cursor.fetchall()
        for row in rows:
            graph = NBAGraph(row.client_id, row.dlum_id, row.initial_wps, row.current_wps, row.best_action_path, row.is_action_performed, row.is_active)
            graphs.append(graph)
        conn.close()
        return graphs


    def save(self, graph: NBAGraph):
        conn = pyodbc.connect(self.connection_string)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM NBA WHERE client_id = ? AND dlum_id = ?", (graph.client_id, graph.dlum_id))
        existing_record_count = cursor.fetchone()[0]

        nodes_path = []
        for n in graph.best_action_path_nodes:
            nodes_path.append(n.to_dict())
        best_action_path = json.dumps(nodes_path)

        if existing_record_count > 0:
            cursor.execute("UPDATE NBA SET initial_wps = ?, current_wps = ?, best_action_path = ?, is_action_performed = ?, is_active = ? WHERE client_id = ? AND dlum_id = ?",
                        (graph.initial_wps, graph.current_wps, best_action_path, graph.is_action_performed, graph.is_active, graph.client_id, graph.dlum_id))
        else:
            cursor.execute("INSERT INTO NBA (client_id, dlum_id, initial_wps, current_wps, best_action_path, is_action_performed, is_active) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (graph.client_id, graph.dlum_id, graph.initial_wps, graph.current_wps, best_action_path, graph.is_action_performed, graph.is_active))
        conn.commit()
        conn.close()


    def findById(self, client_id, dlum_id) -> NBAGraph:
        conn = pyodbc.connect(self.connection_string)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM NBA WHERE client_id = ? AND dlum_id = ?", (client_id, dlum_id))
        row = cursor.fetchone()

        if row:
            graph = NBAGraph(row.client_id, row.dlum_id, row.initial_wps, row.current_wps, row.best_action_path, row.is_action_performed, row.is_active)
            conn.close()
            return graph
        else:
            conn.close()
            return None
        


if __name__ == "__main__": 
    repository = GraphRepository()
    
    for nba in repository.find_all():
        print(f"{nba}")

   