import networkx as nx
import matplotlib.pyplot as plt
import re

action_rules = []
memory_rules = []

def create_window(fsc_string):
    parse_string(fsc_string)

    graph = nx.DiGraph()
    states = set()
    for rule in action_rules:
        states.add(rule.state)
    for rule in memory_rules:
        states.add(rule.state)
        states.add(rule.next_state)

    for state in states:
        graph.add_node(state)

    for action_rule in action_rules:
        for memory_rule in memory_rules:
            if action_rule.observation == memory_rule.observation and action_rule.state == memory_rule.state:
                graph.add_edge(action_rule.state, memory_rule.next_state, label=str(action_rule.action))

    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_size=2000, node_color="lightblue", font_size=10, font_weight="bold")
    edge_labels = nx.get_edge_attributes(graph, "label")
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=10)
    plt.title("FSC visualisation")
    plt.show()


def parse_string(fsc_string):
    for obs, state, action in re.findall(r'A\(\[o=(\d+)\],(\d+)\)=(\w+)', fsc_string):
        action_rules.append(ActionRule(f"o={obs}", state, action))

    for obs, state, next_state in re.findall(r'M\(\[o=(\d+)\],(\d+)\)=(\d+)', fsc_string):
        memory_rules.append(MemoryRule(f"o={obs}", state, next_state))

class ActionRule:
    def __init__(self, observation, action, state):
        self.observation = observation
        self.state = state
        self.action = action


class MemoryRule:
    def __init__(self, observation, state, next_state):
        self.observation = observation
        self.state = state
        self.next_state = next_state
