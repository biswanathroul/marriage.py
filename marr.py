import math
import random
from matplotlib import pyplot

# 'Array' is based on code taken from the demo file sortvisu.py from
# the python source code, and is released under the python 2.6.2 license:
# http://www.python.org/download/releases/2.6.2/license/
class Array:
    def __init__(self, data=None):
        self.items = []
        self.size = 0
        self.ncompares = 0
        self.nswaps = 0
        if data:
            self.setdata(data)

    def setdata(self, data):
        self.items = data[:]
        self.size = len(data)
        self.reset()

    def getsize(self):
        return self.size

    def swap(self, i, j):
        if i == j: return
        self.countswap()
        item = self.items[i]
        other = self.items[j]
        self.items[i], self.items[j] = other, item

    def compare(self, i, j):
        self.countcompare()
        item = self.items[i]
        other = self.items[j]
        return cmp(item, other)

    def reset(self):
        self.ncompares = 0
        self.nswaps = 0

    def countswap(self):
        self.nswaps = self.nswaps + 1

    def countcompare(self):
        self.ncompares = self.ncompares + 1

    def printreport(self):
        text = "%d cmps, %d swaps" % (self.ncompares, self.nswaps)
        print text

    def report(self):
        return self.ncompares, self.nswaps

# The Marriage Sort algorithm
def marriagesort(array):
    array.reset()

    # Pick the maximum entry from the array, tracking the number of compares
    # performed. Uses entries [start, end)
    def pickMax(array, start, end):
        if start >= end: return None
        bestPos = start
        i = start + 1
        while i < end:
            if array.compare(i, bestPos) > 0:
                bestPos = i
            i += 1
        return bestPos

    aEnd = array.getsize()
    skip = int(math.sqrt(aEnd) - 1)

    # Repeatedly loop over the list, pulling out the expected "biggest" entries
    # and placing them at the end.
    while skip > 0:
        bestPos = pickMax(array, 0, skip)
        i = skip

        while i < aEnd:
            if array.compare(i, bestPos) >= 0:
                array.swap(i, aEnd-1)
                aEnd -=1
            else:
                i+= 1
        array.swap(bestPos, aEnd-1)
        aEnd -= 1
        skip = int(math.sqrt(aEnd) - 1)

    insertionsort(array, False)
    return array.report()

# Sorting algorithms following are taken from the demo file sortvisu.py from
# the python source code, and are released under the python 2.6.2 license:
# http://www.python.org/download/releases/2.6.2/license/
def insertionsort(array, reset=True):
    end = array.getsize()
    if reset:
        array.reset()
    for i in range(1, end):
        j = i-1
        while j >= 0:
            if array.compare(j, j+1) <= 0:
                break
            array.swap(j, j+1)
            j = j-1
    return array.report()

def quicksort(array, reset=True):
    size = array.getsize()
    if reset:
        array.reset()
    stack = [(0, size)]
    while stack:
        first, last = stack[-1]
        del stack[-1]
        if last-first < 5:
            for i in range(first+1, last):
                j = i-1
                while j >= first:
                    if array.compare(j, j+1) <= 0:
                        break
                    array.swap(j, j+1)
                    j = j-1
            continue
        j, i, k = first, (first+last)//2, last-1
        if array.compare(k, i) < 0:
            array.swap(k, i)
        if array.compare(k, j) < 0:
            array.swap(k, j)
        if array.compare(j, i) < 0:
            array.swap(j, i)
        pivot = j
        left = first
        right = last
        while 1:
            right = right-1
            while right > first and array.compare(right, pivot) >= 0:
                right = right-1
            left = left+1
            while left < last and array.compare(left, pivot) <= 0:
                left = left+1
            if left > right:
                break
            array.swap(left, right)
        array.swap(pivot, right)
        n1 = right-first
        n2 = last-left
        if n1 > 1: stack.append((first, right))
        if n2 > 1: stack.append((left, last))
    return array.report()

# Run both marriage sort and quicksort with a series of powers-of-2 sized
# arrays, returning the number of swaps and compares for each.
def gettimings():
    sizes = []
    mt = []
    qt = []

    for i in range(0, 13):
        size = 2**i
        print("generating size", size)
        sizes.append(size)
        a = list(range(size))
        random.shuffle(a)

        ma = Array(a)
        mcount = marriagesort(ma)
        mt.append(mcount)

        qa = Array(a)
        qcount = quicksort(qa)
        qt.append(qcount)

        print("Marriage sort", mcount, "quicksort", qcount)
    return sizes, mt, qt

# Takes the number of swaps and compares returned by gettimings, and displays
# them on a couple plots for easy comparison.
def plottimings():
    sizes, mt, qt = gettimings()

    pyplot.figure(1)
    ax = pyplot.subplot(121)
    pyplot.loglog(sizes, list(map(lambda x:x[0], mt)), 'g', label="Marriage Sort")
    pyplot.loglog(sizes, list(map(lambda x:x[0], qt)), 'b', label="Quicksort")
    pyplot.loglog(sizes, list(map(lambda x:x*math.log(math.log(x)+1, 2), sizes)), 'k', label="nloglogn")
    pyplot.loglog(sizes, list(map(lambda x:x*x, sizes)), 'k--', label="n^2")
    pyplot.loglog(sizes, list(map(lambda x:math.pow(x, 1.5), sizes)), 'k-.', label="n^1.5")
    pyplot.loglog(sizes, list(map(lambda x:x*math.log(x, 2), sizes)), 'k:', label="nlogn")
    pyplot.title("Comparisons")
    pyplot.legend()

    pyplot.subplot(122)
    pyplot.loglog(sizes, list(map(lambda x:x[1], mt)), 'g', label="Marriage Sort")
    pyplot.loglog(sizes, list(map(lambda x:x[1], qt)), 'b', label="Quicksort")
    pyplot.loglog(sizes, list(map(lambda x:x*math.log(math.log(x)+1, 2), sizes)), 'k', label="nloglogn")
    pyplot.loglog(sizes, list(map(lambda x:x*x, sizes)), 'k--', label="n^2")
    pyplot.loglog(sizes, list(map(lambda x:math.pow(x, 1.5), sizes)), 'k-.', label="n^1.5")
    pyplot.loglog(sizes, list(map(lambda x:x*math.log(x, 2), sizes)), 'k:', label="nlogn")
    pyplot.title("Swaps")
    pyplot.legend()
    pyplot.show()
    pyplot.close()

if __name__ == "__main__":
    plottimings()
