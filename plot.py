import matplotlib.pyplot as plt;
fontsize = 20
ax =plt.subplot()
ax.plot([1,2])
ax.locator_params(nbins=3)

ay=plt.subplot()
ay.plot([2,9])
ay.locator_params(nbins=3)



plt.show()