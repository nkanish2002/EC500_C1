from main import main
import timeit
import tracemalloc

t = timeit.Timer("main(\"HDWallpaperFree\", 2)", "from main import main")
print(t.timeit(1))

tracemalloc.start()
main(screen_name="HDWallpaperFree", limit=2)
print("Current: %d, Peak %d" % tracemalloc.get_traced_memory())