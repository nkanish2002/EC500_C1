from main import main
import os

fileName = main(screen_name="HDWallpaperFree", limit=2)

web = open("demo.html", "w")

content = """
<!DOCTYPE html>
<html>
<body>

<video width="320" height="240" controls>
  <source src="%s" type="video/mp4">
  Your browser does not support the video tag.
</video>

</body>
</html>""" % fileName

web.write(content)
web.close()

os.system("open demo.html")