import random
import math

k  = 1000
kp = 1300
c = 0.1
delta = 0.1

s = c * math.log(k/delta) * math.sqrt(k)
print 'S = ', s
print 'k/s = ', k/s

source = []
for i in range(k):
    source.append(i)

def uniform(lo, hi):
    return lo + int(random.random() * (hi + 1 - lo))

# Sample from the distribution `dist` between `lo` and `hi`
def sample(lo, hi, dist):
    while True:
        x = uniform(lo, hi)
        g = random.random()
        if g < dist(x): return x

# Return the sum of `dist` between `lo` and `hi`
def sumover(lo, hi, dist):
    r = 0
    for x in range(lo, hi+1):
        r += dist(x)
    return r

def ideal_soliton(d):
    if d == 1:
        return 1.0/k
    else:
        return 1.0/(d*(d-1.0))

def tau(d):
    if d < int(k/s + 0.5):
        return float(s)/(k*float(d))
    elif d == int(k/s + 0.5):
        return s/k * math.log(s/delta)
    else:
        return 0

z = sumover(1, k, ideal_soliton) + sumover(1, k, tau)

def robust_soliton(d):
    return (ideal_soliton(d) + tau(d)) / z

def generate_block():
    deg = sample(1, k, robust_soliton)
    input_blocks = []
    for i in range(deg):
        while True:
            block = uniform(1, k) - 1 #0-indexing
            if block not in input_blocks: break # blocks must be distinct
        input_blocks.append(block)
    output = 0
    for b in input_blocks:
        output ^= source[b]
    #print '{}, {}, {}'.format(deg, input_blocks, output)
    return (input_blocks, output)


nodes = []

print 'Generating...'
for i in range(kp):
    nodes.append(generate_block())

def decode(nodes):
    print 'Decoding: ',

    s = [None] * k              # Decoded source block values - None if we haven't decoded it yet
    t = [n[1] for n in nodes]   # Received node values

    t_links = [set(n[0]) for n in nodes]        # t_links[n]: Which source blocks node n is linked to
    s_links = []                                # s_links[b]: Which nodes source block b is linked to
    for i in range(k): s_links.append(set([]))
    for tn, links in enumerate(t_links):
        for sblock in links:
            s_links[sblock].add(tn)

    while None in s:
        # Find check node connected to only one source block
        found = False
        for n, links in enumerate(t_links):
            if len(links) == 1:
                found = True
                b = links.pop()         # Remove links
                s_links[b].remove(n)
                s[b] = t[n]             # Set source block equal to node value
                for tc in s_links[b]:   # Add sb to all connected nodes
                    t[tc] ^= s[b]
                    t_links[tc].remove(b)   # Remove all edges connected to sb
                s_links[b].clear()
                break

        if not found:
            print "Couldn't find a node with only one connected block!"
            return None
            
    print s


decode(nodes)
