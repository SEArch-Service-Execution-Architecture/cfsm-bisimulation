class State:

    def __init__(self, graph, id, theory):
        self.graph = graph
        self.id = id
        self.theory = theory
        self.final = False

    def set_as_final(self):
        self.final = True

    def is_final(self):
        return self.final

    def __repr__(self):
        return str(self.id)

    def get_transitions(self):
        return self.graph.transitions_of(self.id)

    def get_transitions_with(self, label):
        return self.graph.transitions_with_label_of(self.id, label)
