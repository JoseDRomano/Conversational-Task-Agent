import os
from typing import Optional, Tuple, List, Type

from example.dialog_factory.dialog_elements import AbstractState


def get_flow(state: Type[AbstractState]) -> Optional[str]:
    flow = [parent_class.__name__ for parent_class in state.__mro__ if "flow" in parent_class.__name__.lower()]
    if len(flow) > 0:
        return flow[0]
    raise Exception("State doesn't follow the correct rules of implementation. Please check the documentation.")


def create_dot_dict(states: List[Type[AbstractState]]) -> Tuple[dict, dict]:
    dot_aux_dict = dict()
    dummy_flow_nodes = dict()

    states = [state for state in states if state.__name__ != "LaunchState"]
    for state in states:
        # get flow of the state and create a new entry in the dict if it doesn't exist
        flow = get_flow(state)
        if flow not in dot_aux_dict:
            dummy_flow_nodes[flow] = f"{flow}DummyNode"
            dot_aux_dict[flow] = dict()

        # add transitions to the state in the dict
        state_transitions = state.register_transitions_in()
        if state_transitions:
            for last_state, events in state_transitions.items():
                in_state = state.__name__
                out_state = last_state.__name__
                if out_state != "LaunchState":
                    # treats special case in which the in state is from the backbone flow and out state isn't
                    out_state_flow = get_flow(last_state)
                    flow_cluster = out_state_flow if flow == "BackboneFlow" and out_state_flow != flow else flow
                    if flow_cluster not in dot_aux_dict:
                        dummy_flow_nodes[flow] = f"{flow}DummyNode"
                        dot_aux_dict[flow_cluster] = dict()
                    dot_aux_dict[flow_cluster][(out_state, in_state)] = dict()
                    dot_aux_dict[flow_cluster][(out_state, in_state)]["events"] = [event.__name__ for event in events]

        # add transitions from subflow to the state in the dict
        state_transitions = state.register_subflow_transitions_in()
        if state_transitions:
            for accepted_flow, events in state_transitions.items():
                in_state = state.__name__
                accepted_flow = accepted_flow.__name__
                dummy_node = dummy_flow_nodes[accepted_flow] if accepted_flow in dummy_flow_nodes else None
                dot_aux_dict[flow][(dummy_node, in_state)] = dict()
                dot_aux_dict[flow][(dummy_node, in_state)]["events"] = [event.__name__ for event in events]
                dot_aux_dict[flow][(dummy_node, in_state)]["flow"] = accepted_flow

    return dot_aux_dict, dummy_flow_nodes


def print_dot(states: List[Type[AbstractState]]):
    dot_aux_dict, dummy_flow_nodes = create_dot_dict(states)

    graphviz_path = os.path.join(os.getcwd(), "graph_visualizer")
    os.makedirs(graphviz_path, exist_ok=True)

    f = open(f"{graphviz_path}/state_machine.dot", "w")
    f.write("digraph {\n")
    f.write("   compound=true;\n")
    f.write("   fontsize=14;\n")
    f.write("   edge[weight=0.3, fontsize=12];\n")
    f.write("   node[fontsize=13];\n")
    f.write("   nodesep=1;\n")
    f.write("   ranksep=0.5;\n")
    for _, dummy in dummy_flow_nodes.items():
        f.write("   "+dummy+"[style=invis, width=0, height=0, label=\"\"];\n")

    for flow, transitions in dot_aux_dict.items():
        f.write("\n   subgraph cluster_" + flow + " {")
        f.write("\n      label = \"" + flow + "\";")
        f.write("\n      " + dummy_flow_nodes[flow] + ";\n")
        for (out_state, in_state), info in transitions.items():
            events = info["events"]
            if "flow" in info:
                if info["flow"] == "AbstractState":
                    for out_flow, dummy in dummy_flow_nodes.items():
                        f.write("      " + dummy + " -> " + in_state + " [label=\"" + "\\n ".join(
                            events) + "\", ltail= \"cluster_" + out_flow + "\"];\n")
                else:
                    f.write("      "+out_state + " -> " + in_state + " [label=\"" + "\\n ".join(events) + "\", ltail= \"cluster_" + info["flow"] + "\"];\n")
            else:
                f.write("      "+out_state + " -> " + in_state + " [label=\"" + "\\n ".join(events) + "\"];\n")
        f.write("   }")

    f.write("\n}")
    f.close()
