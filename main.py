import numpy as np
import matplotlib.pyplot as plt

print(np.random.randint(10))

plt.style.use("dark_background")
plt.figure(figsize=(10,8))
plt.plot([1.0, 10.0], [2.0, 5.0])
plt.xlabel("X Axis")
plt.ylabel("Y Axis")