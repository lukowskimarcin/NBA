from actions import EKW, PassAction, ReOgnivo, ReZus, Teren, ActionModel
from node import NodeState, Node

SQL_CONNECTION_STR = "DRIVER={ODBC Driver 18 for SQL Server};SERVER=127.0.0.1,5433;Encrypt=no;DATABASE=msdb;UID=sa;PWD=sa!234#sa$%"

MAX_COST = 14  # Maksymalny koszt
MAX_TIME = 18  # Maksymalny czas zycia sprawy

ROOT_NODE = Node(0, 0, "ROOT", NodeState.PERFORMED, 0, 0)

ACTION_MODELS: list[ActionModel] = [
    ReZus(),
    ReOgnivo(),
    Teren(),
    EKW(),
    # PassAction(),
]
