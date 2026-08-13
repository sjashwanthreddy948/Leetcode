class SegmentTree:
    def __init__(self, s):
        self.n = len(s)
        self.tree = [None] * (4 * self.n)
        self.s = s
        self.build(1, 0, self.n - 1)

    def make_node(self, ch, length=1):
        return [ch, ch, length, length, length, length]
        # left_char, right_char, left_len, right_len, best, length

    def build(self, node, l, r):
        if l == r:
            self.tree[node] = self.make_node(self.s[l])
            return

        mid = (l + r) // 2
        self.build(node * 2, l, mid)
        self.build(node * 2 + 1, mid + 1, r)

        self.tree[node] = self.merge(
            self.tree[node * 2],
            self.tree[node * 2 + 1]
        )

    def merge(self, a, b):
        left_char = a[0]
        right_char = b[1]

        left_len = a[2]
        right_len = b[3]

        best = max(a[4], b[4])
        total_len = a[5] + b[5]

        if a[1] == b[0]:
            best = max(best, a[3] + b[2])

            # Entire left segment has the same character
            if a[2] == a[5]:
                left_len = a[5] + b[2]

            # Entire right segment has the same character
            if b[3] == b[5]:
                right_len = b[5] + a[3]

        return [
            left_char,
            right_char,
            left_len,
            right_len,
            best,
            total_len
        ]

    def update(self, node, l, r, idx, ch):
        if l == r:
            self.tree[node] = self.make_node(ch)
            return

        mid = (l + r) // 2

        if idx <= mid:
            self.update(node * 2, l, mid, idx, ch)
        else:
            self.update(node * 2 + 1, mid + 1, r, idx, ch)

        self.tree[node] = self.merge(
            self.tree[node * 2],
            self.tree[node * 2 + 1]
        )

    def query_best(self):
        return self.tree[1][4]


class Solution:
    def longestRepeating(self, s: str, queryCharacters: str, queryIndices: list[int]) -> list[int]:
        seg = SegmentTree(s)
        ans = []

        for ch, idx in zip(queryCharacters, queryIndices):
            seg.update(1, 0, len(s) - 1, idx, ch)
            ans.append(seg.query_best())

        return ans