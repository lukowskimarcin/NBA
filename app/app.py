import random
from constants import MAX_COST, MAX_TIME
from graph import NBAGraph

recalculate_graph = True


if __name__ == "__main__":
    client_id = random.randint(1, 1000)
    dlum_id = random.randint(1, 1000)
    graph = NBAGraph(client_id, dlum_id, 1000, 1000)
    graph.build()

    print(f"graph: {graph}")
    graph.show()

    index = 0
    current_wps = 900

    while current_wps > 0:
        index += 1

        actual_node = graph.determine_next_action()
        if actual_node is not None:
            print(
                f"{index}: next best action: {actual_node.level}-{actual_node.action}"
            )
            graph.show()
            real_cost = random.randint(1, 5)
            real_time = random.randint(1, 3)
            print(
                f"\taction performed with => wps: {current_wps}, real_cost: {real_cost}, real_time: {real_time}"
            )
            graph.action_performed(current_wps, real_cost, real_time, recalculate_graph)
            graph.show()
            current_wps -= random.randint(0, 200)
        else:
            break


print(
    f"Koniec -> zostalo do splaty {graph.current_wps} z {graph.initial_wps} -> cost: {graph.total_cost_spend}/{MAX_COST}, time: {graph.total_time_spend}/{MAX_TIME}"
)
