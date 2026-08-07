from collections import Counter

class Solution:
    def smallestNumber(self, num: str, t: int) -> str:
        FACT = {
            0: Counter(),
            1: Counter(),
            2: Counter({2: 1}),
            3: Counter({3: 1}),
            4: Counter({2: 2}),
            5: Counter({5: 1}),
            6: Counter({2: 1, 3: 1}),
            7: Counter({7: 1}),
            8: Counter({2: 3}),
            9: Counter({3: 2}),
        }

        # factorize t
        need = Counter()
        x = t
        for p in (2, 3, 5, 7):
            while x % p == 0:
                need[p] += 1
                x //= p
        if x != 1:
            return "-1"

        def subtract(a, b):
            c = Counter(a)
            for k, v in b.items():
                c[k] = max(0, c[k] - v)
            return c

        def enough(a, b):
            for k in (2, 3, 5, 7):
                if a[k] > b[k]:
                    return False
            return True

        def factorCount(cnt):
            cnt = Counter(cnt)

            c8 = cnt[2] // 3
            r2 = cnt[2] % 3

            c9 = cnt[3] // 2
            r3 = cnt[3] % 2

            c4 = r2 // 2
            c2 = r2 % 2

            c6 = 0
            if c2 and r3:
                c2 = 0
                r3 = 0
                c6 = 1

            if r3 and c4:
                c4 = 0
                r3 = 0
                c2 = 1
                c6 = 1

            res = Counter()
            res[2] = c2
            res[3] = r3
            res[4] = c4
            res[5] = cnt[5]
            res[6] = c6
            res[7] = cnt[7]
            res[8] = c8
            res[9] = c9
            return res

        def construct(fc):
            ans = []
            for d in range(2, 10):
                ans.extend(str(d) * fc[d])
            return "".join(ans)

        totalNeed = factorCount(need)

        if sum(totalNeed.values()) > len(num):
            return "1" * (sum(totalNeed.values()) - sum(totalNeed.values()) + len(num)+1-sum(totalNeed.values())) + construct(totalNeed)

        prefix = Counter()
        for ch in num:
            prefix += FACT[int(ch)]

        firstZero = num.find('0')
        if firstZero == -1:
            firstZero = len(num)
            if enough(need, prefix):
                return num

        pref = Counter(prefix)

        for i in range(len(num) - 1, -1, -1):
            d = int(num[i])
            pref -= FACT[d]
            space = len(num) - i - 1

            if i > firstZero:
                continue

            for nd in range(d + 1, 10):
                rem = subtract(subtract(need, pref), FACT[nd])
                fc = factorCount(rem)

                if sum(fc.values()) <= space:
                    fill = space - sum(fc.values())
                    return (
                        num[:i]
                        + str(nd)
                        + "1" * fill
                        + construct(fc)
                    )

        fc = factorCount(need)
        fill = len(num) + 1 - sum(fc.values())
        return "1" * fill + construct(fc)