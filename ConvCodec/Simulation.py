import numpy as np
import ConvCodec as cc
import matplotlib.pyplot as plt

data_size=200
max_snr=11
ber_usedCodec=[]
ber_unUsedCodec=[]

for snr_db in range(0, max_snr):
    data=np.random.randint(0,2,data_size) #0,1 데이터
    encoded_bit = cc.Encoder(data) #2행 1021열, 0과 1로 구성

    real_signal = encoded_bit[0,:] * 2 - 1 #-1과 1을 발생
    imag_signal = encoded_bit[1,:] * 2 - 1 #-1과 1을 발생

    qpsk_sym=(real_signal+ 1j*imag_signal) / np.sqrt(2) #data_size 개의 QPSK
    ofdm_sym=np.fft.ifft(qpsk_sym) * np.sqrt(data_size)

    noise_std = 10 ** (-snr_db / 20)
    noise = np.random.randn(data_size+3) * noise_std/np.sqrt(2) + 1j*np.random.randn(data_size + 3)*noise_std/np.sqrt(2)
    rcv_signal = np.fft.fft(ofdm_sym) / np.sqrt(data_size) + noise

    real_detected_signal = np.array(((rcv_signal.real > 0) + 0)).reshape(1, data_size + 3)
    imag_detected_signal = np.array(((rcv_signal.imag > 0) + 0)).reshape(1, data_size + 3)

    dec_input=np.vstack([real_detected_signal, imag_detected_signal])
    decoded_bit=cc.ViterbiDecoder(dec_input)
    print(np.sum(np.abs(dec_input - encoded_bit))) #오류정정 전
    print(np.sum(np.abs(data - decoded_bit))) #오류 정정 후

    ber_unUsedCodec.append(np.sum(np.abs(dec_input - encoded_bit))/2 / (data_size*2))
    ber_usedCodec.append( np.sum(np.abs(data - decoded_bit))/2 / (data_size * 2))

snr=np.arange(0,max_snr)
plt.subplot(2,1,1)
plt.semilogy(snr, ber_usedCodec)
plt.subplot(2,1,2)
plt.semilogy(snr, ber_unUsedCodec)

plt.show()