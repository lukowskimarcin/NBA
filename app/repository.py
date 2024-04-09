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
            graph = NBAGraph(row.client_id, row.dlum_id, row.initial_wps, row.current_wps, row.best_action_path, row.is_action_performed)
            graphs.append(graph)
        conn.close()
        return graphs


    def save(self, graph: NBAGraph):
        conn = pyodbc.connect(self.connection_string)
        cursor = conn.cursor()
        
        nodes_path = []
        for n in graph.best_action_path_nodes:
            nodes_path.append(n.to_dict())
        best_action_path = json.dumps(nodes_path)

        cursor.execute("INSERT INTO NBA (client_id, dlum_id, initial_wps, current_wps, best_action_path, is_action_performed) VALUES (?, ?, ?, ?, ?, ?)",
                       (graph.client_id, graph.dlum_id, graph.initial_wps, graph.current_wps, best_action_path, graph.is_action_performed))
        conn.commit()
        conn.close()


    def findById(self, client_id, dlum_id) -> NBAGraph:
        conn = pyodbc.connect(self.connection_string)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM NBA WHERE client_id = ? AND dlum_id = ?", (client_id, dlum_id))
        row = cursor.fetchone()

        if row:
            graph = NBAGraph(row.client_id, row.dlum_id, row.initial_wps, row.current_wps, row.best_action_path, row.is_action_performed)
            conn.close()
            return graph
        else:
            conn.close()
            return None
        


if __name__ == "__main__": 
    repository = GraphRepository()
    
    for nba in repository.find_all():
        print(f"{nba}")

    single = repository.findById(1, 1)
    print(f"\nsingle: {single}")


    graph = NBAGraph(4,5,1000,500,None,'T')
    repository.save(graph)
    saved = repository.findById(4, 4)
    print(f"\nsaved: {saved}")
