from math import log


class Metric():
    def __init__(self, grade, n=None, max_grade=3, p_break=0.15):
        self.n = n
        if n is None:
            self.n = len(grade)
        assert n <= len(grade), "'n' mustn't be more then grade number"
        self.grade = grade[:self.n]
        self.max_grade = max_grade
        self.p_break = p_break

    def __call__(self):
        p_rel = []
        p_look = []
        p_found = 0
        dcg = 0
        z = 0
        for i in range(self.n):
            p_rel.append(0 if self.grade[i] == 0
                         else 0.5 * 2**(self.grade[i] - self.max_grade))
            p_look.append((1-self.p_break) *
                          (1 if i == 0 else p_look[i-1] * (1-p_rel[i-1])))
            p_found += p_look[-1] * p_rel[-1]
            dcg += (2**self.grade[i]-1) / (log(i+3))
            z += (2**self.max_grade - 1) / (log(i+3))
        n_dcg = dcg / z
        return {"PFound": p_found, "DCG": dcg, "NDCG": n_dcg}


def main():
    n = int(input())
    grade = list(map(int, input().split()))
    print(Metric(grade, n)())

main()