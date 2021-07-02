from matplotlib import pyplot as plt
import numpy as np

t=np.arange(0,1,0.0001)
sig=np.sin(4*t)-2*np.sin(7*t-0.01)+1.5*np.sin(15*t+0.05)
plt.subplot(411)
plt.plot(t, sig)

carrier=np.sin(2*np.pi*100*t)
plt.subplot(412)
plt.plot(t, carrier)

am_sig=sig*carrier
plt.subplot(413)
plt.plot(t, am_sig)

dem_am=am_sig*carrier #기존 신호 도출해내기
plt.subplot(414)
plt.plot(t, dem_am)


plt.show()


