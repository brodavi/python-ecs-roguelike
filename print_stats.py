import pstats
import sys
file = sys.argv[1]
p = pstats.Stats(file)
p.sort_stats('cumulative').print_stats(10)
