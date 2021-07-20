import matplotlib.pyplot as plt
import numpy as np

data_size=1000000
max_snr=14 #최대 SNR 13db까지 실험
ber=[]

for snr_db in range(0,max_snr):
    real_signal=np.random.randint(0,2,data_size)*2-1 #-1과 1을 발생
    imag_signal=np.random.randint(0,2,data_size)*2-1

    qpsk_sym=(real_signal+1j*imag_signal)/np.sqrt(2) #에너지가 1짜리인 qpsk심볼
    noise_std=10**(-snr_db/20)
    noise=np.random.randn(data_size)*noise_std/np.sqrt(2)+1j*np.random.randn(data_size)*noise_std/np.sqrt(2)
    rcv_signal=qpsk_sym+noise

    real_detected_signal=((rcv_signal.real>0)+0)*2-1
    imag_detected_signal=((rcv_signal.imag>0)+0)*2-1

    num_error=np.sum(np.abs(real_signal-real_detected_signal))/2+np.sum(np.abs(imag_signal-imag_detected_signal))/2
    ber.append(num_error/(data_size*2)) #BER 데이터사이즈는 심볼의 숫자. 하나의 qpsk는 두개의 비트를 가지므로 2로 나눠줌

snr=np.arange(0,max_snr)
plt.semilogy(snr, ber)
plt.show()