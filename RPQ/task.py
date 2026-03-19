class Task:
    def __init__(self, id, r, p, q):
        self.id = id
        self.r = r
        self.p = p
        self.q = q

    def __lt__(self, other):
        return self.r < other.r

    def __repr__(self):
        return f"T{self.id}(r:{self.r}, p:{self.p}, q:{self.q})"