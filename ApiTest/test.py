from datetime import datetime
import math
dt = datetime.now()
timestamp = 1666209109
t2d = datetime.fromtimestamp(timestamp)

diff = dt - t2d
# getting the timestamp
hours = diff.seconds/3600


print(math.trunc(hours))