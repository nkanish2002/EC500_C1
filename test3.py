from main import main
import timeit
import tracemalloc

#t = timeit.Timer("main(\"asdasda\", 2)", "from main import main")
#print(t.timeit(1))

#tracemalloc.start()
try:
	main(screen_name="asdasda", limit=2)
except Exception as e:
	print(str(e))
#print("Current: %d, Peak %d" % tracemalloc.get_traced_memory())