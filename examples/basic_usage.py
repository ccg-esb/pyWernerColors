import matplotlib.pyplot as plt
import wernercolors as wc

print("Available palettes:", wc.list_palettes())
print("Firebirds:", wc.palette("Firebirds"))
print("Scotch Blue:", wc.resolve_names(["Scotch Blue"])[0])
print("Closest colour:", wc.closest_color("#53658f"))

fig, ax = plt.subplots()
wc.set_color_cycle(ax, "Firebirds", n=7)
for i in range(7):
    ax.plot([0, 1], [i, i + 0.5], label=f"series {i + 1}")
ax.legend()
plt.show()
