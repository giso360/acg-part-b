from datasketch import HyperLogLog
from probables import CountMinSketch, HeavyHitters


class TweetApproximate:

    def __init__(self, **kwargs):
        if kwargs["method"] == "CMS":
            self.method = CountMinSketch(width=kwargs["width"], depth=kwargs["depth"],
                                         hash_function=kwargs["hash_function"])

        if kwargs["method"] == "HH":
            self.method = HeavyHitters(num_hitters=kwargs["num_hitters"],
                                       width=kwargs["width"], depth=kwargs["depth"],
                                       hash_function=kwargs["hash_function"])

        if kwargs["method"] == "HYP":
            self.method = HyperLogLog()

    def add(self, s):
        if type(self.method) == CountMinSketch or type(self.method) == HeavyHitters:
            self.method.add(s)
            return self

        if type(self.method) == HyperLogLog:
            self.method.update(str(s).encode('utf8'))
            return self

    def check(self, s):
        if type(self.method) == CountMinSketch:
            return self.method.check(s)

        if type(self.method) == HeavyHitters:
            return self.method.heavy_hitters

        if type(self.method) == HyperLogLog:
            return self.method.count()



