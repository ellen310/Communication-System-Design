import numpy as np

num_data=10
data=np.random.randint(0,2,num_data)
noise_power=0.2
noise=np.random.randn(num_data)*noise_power
rcv_data=data+noise
demod_data=(rcv_data>0.5)*1

print("원래데이터:", data)
print("수신데이터:", demod_data)
print("오류데이터 수:", np.sum(demod_data-data))