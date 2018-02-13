from main import main
import timeit
import tracemalloc

t = timeit.Timer("main(\"isigov95\", 4)", "from main import main")
print(t.timeit(1))

tracemalloc.start()
main(screen_name="isigov95", limit=4)
print("Current: %d, Peak %d" % tracemalloc.get_traced_memory())