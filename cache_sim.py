import sys, os, string, re
from simulator import CacheSimulator

numMisses = 0
numAccesses = 0


if len(sys.argv) < 2:
    print("Usage: sys.argv[0] infile <options>")
    print("Options:")
    print("<-l1-usize num_bytes>    : total size in bytes")
    print("<-l1-ubsize num_bytes>   : block size in bytes")
    print("<-l1-uassoc num_levels>   : associativity level")
    print("<-l1-urepl type>         : replacement policy, 'l' - LRU, 'r'-random, 'f' fifo")
    print("<-l1-uwalloc type>      : write allocation policy, 'a' - always, 'n'-never")
    sys.exit(-1)

fname = sys.argv[1]

usize = 0
ubsize = 0
uassoc = 0
urepl = 'f'
uwalloc = 'a'

i = 2
while i < len(sys.argv):
    if sys.argv[i] == '-l1-usize':
        i += 1
        usize = int(sys.argv[i])
    elif sys.argv[i] == '-l1-ubsize':
        i += 1
        ubsize = int(sys.argv[i])
    elif sys.argv[i] == '-l1-uassoc':
        i += 1
        uassoc = int(sys.argv[i])
    elif sys.argv[i] == '-l1-urepl':
        i += 1
        urepl = sys.argv[i]
    elif sys.argv[i] == '-l1-uwalloc':
        i += 1
        uwalloc = sys.argv[i]
    else:
        print("Ignoring unrecognized option: ", sys.argv[i])
        
    i += 1


s = "Running with input: %s, l1-usize=%d,  l1-ubsize=%d,  l1-assoc=%d,  l1-repl=%s,  l1-uwalloc=%s \n" % (fname,usize,ubsize,uassoc,urepl,uwalloc)

print(s)

sim = CacheSimulator(fname, usize, ubsize, uassoc, urepl, uwalloc)
print("Cache lines: ", sim.num_cache_lines)
sim.simulate()

print("Demand Accesses  ",sim.trace_count)
print("Demand Hits ", sim.hit_count)
print("Demand Misses ",sim.miss_count)



