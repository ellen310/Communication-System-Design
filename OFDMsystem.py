import matplotlib.pyplot as plt
import numpy as np

data_size=64 #하나의 OFDM 심볼에 한번에 전송되는 QPSK 심볼의 수
max_snr=20 #최대 SNR 13db까지 실험
ber=[]

for snr_db in range(20, 21):
    real_signal = np.random.randint(0,2,data_size)*2-1 #-1과 1을 발생
    imag_signal = np.random.randint(0, 2, data_size) * 2 - 1

    qpsk_sym=(real_signal+1j*imag_signal) / np.sqrt(2) #data_size 개의 QPSK
    ofdm_sym=np.fft.ifft(qpsk_sym)*np.sqrt(data_size) #심볼이 64개 모여가지고 IFFT에 넣은거
    #ofdm_sym=np.fft.ifft(qpsk_sym) #파이썬에서는 IFFT하면 qpsk 심볼 에너지가 data_size 배 감소한다.
    noise_std=10**(-snr_db/20)
    noise=np.random.randn(data_size)*noise_std/np.sqrt(2)+1j*np.random.randn(data_size)*noise_std/np.sqrt(2)
    rcv_signal=ofdm_sym+noise
    rcv_signal=np.fft.fft(rcv_signal) / np.sqrt(data_size) #IFFT할때 곱해줬으니 FFT할땐 나눠주기

plt.subplot(2,2,1)
plt.plot(np.abs(qpsk_sym)**2) #64개의 qpsk심볼의 에너지. 애초에 1로 맞춰뒀었으니 1로 일정한 그래프
plt.subplot(2,2,2)
plt.plot(np.abs(ofdm_sym)**2) #qpsk심볼을 IFFT한 녀석의 평균 에너지
plt.subplot(2,2,3)
plt.scatter(ofdm_sym.real,ofdm_sym.imag) #IFFT통과한 qpsk심볼의 성상도. 여기저기 흩뿌려진 신호로 보임. 얘가 FFT통과하면 원래 qpsk심볼이 복원됨
plt.subplot(2,2,4)
plt.scatter(rcv_signal.real,rcv_signal.imag) #FFT 통과했으므로 깔끔하게 원래의 qpsk심볼이 나옴 (노이즈 비율이 적을수록 깔끔해짐)


plt.show()
