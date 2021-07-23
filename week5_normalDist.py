import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm #정규분호 normal_dist

mu = 0 #평균 얘가 2가되면 가운데가 2가 된다. 3이되면 가운데가 3 ...
sigma = 1 #표준편차. 얘가 커질수록 좌우로 넓어진다.
num_sample = 100000

s = np.random.normal(mu, sigma, num_sample)
#평균mu, 표준편차sigma인 정규분포를 따르는 랜덤 변수 num_sample개를 생성하시오

cnt, bins, ignored = plt.hist(s, 100, density = True) #수식 없이 pdf 를 그리는 방법. s를 100씩 잘라서 나타낸다. pdf에서 1의 확률을 구하고 싶으면 bins대신 1을 넣으면 된다.
# bins는 x축 값. 100개의 구간을 임의로 나눈 값이 bins에 저장. 그 구간에 몇개의 랜덤변수가 포함되는지는 cnt에 저장.
plt.plot(bins, 1/(np.sqrt(2*np.pi))*np.exp(-((bins-mu)**2)/(2*sigma**2))) #정규분포의 pdf를 그려봄. (x축 값, y축 값) 여기서 y축 값은 정규분포의 식을 그대로 쓴 거. **는 제곱

plt.show()

#PDF값 콘솔에 계산. x=5일때는 위에서 bins의 자리에 5을 넣어주면 된다.
print( 1/(np.sqrt(2*np.pi))*np.exp(-((5-mu)**2)/(2*sigma**2)) )

#CDF 계산
print(norm.cdf(2)) #수학적 계산.
print(np.sum(s<2)/num_sample) #랜덤넘버s가 2보다 작은것을 다 더해서 확률로 볼라고 num_sample로 나눠주면 cdf와 같을 것이라는 실험적 계산