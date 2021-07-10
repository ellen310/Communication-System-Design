from matplotlib import pyplot as plt
import numpy as np

step = 0.004 #1초에 250개 들어가게.
t=np.arange(step, 1+step, step)
c_f=50 #기존신호에 곱해줄 임의의 높은 주파수. 실제로는 50보다도 훨 큼

signal=np.sin(2*np.pi*2*t)-2*np.sin(2*np.pi*3*t)+1.5*np.sin(2*np.pi*4*t)
plt.subplot(811) #8개의 그림을 그린다
plt.plot(t, signal) #시간영역의 기존신호~~

#원래 신호가 주파수 영역에서는 어떻게 생겼는지 확인하기 위해 FFT를 한다.
freq_signal=np.abs(np.fft.fftshift(np.fft.fft(signal))) #fft(signal)을 하면 저주파가 양쪽끝으로 간다. 그래서 저주파가 가운데에 보이도록 shift시켜준다.
plt.subplot(812)
plt.plot(t, freq_signal) #주파수 영역의 기존신호~~기저대역신호(처음 신호의 주파수영역) +주파수영역인데 t를 넣은건 그냥 샘플의 순서를 맞춰주려고.

carrier=np.cos(2*np.pi*c_f*t)
am_sig=signal*carrier
plt.subplot(813)
plt.plot(t, am_sig) # 시간영역의 am신호~~

freq_am_sig=np.abs(np.fft.fftshift(np.fft.fft(am_sig))) #주파수 영역의 am신호~~ 시간영역에서 carrier를 "곱셈"했으니까 주파수영역에서는 컨볼루션(fc만큼+/-쪽으로 이동)
plt.subplot(814)
plt.plot(t, freq_am_sig)

rcv_sig = am_sig*carrier #carrier*signal*carrier 시간 영역의 수신신호~~
plt.subplot(815)
plt.plot(t, rcv_sig)

freq_rcv_sig=np.abs(np.fft.fftshift(np.fft.fft(rcv_sig))) #주파수 영역의 수신신호~~ 가운데는 원래 신호가 나오고, 다른애는 2배로 뜀. 이제 가운데 신호만 LPF씌워서 뺴내면 끝
plt.subplot(816)
plt.plot(t, freq_rcv_sig)


LPF_f=30 #렉탱귤러 모양의 넓이(필터주파수). 너무 작으면(좁으면) 원래신호까지 잘리고, 너무 넓으면 고주파 신호까지 잡힘. 잘 설정해야.
t_lpf=np.arange(-0.5,0.5,step) #LowPassFilter의 길이
LPF=[]
for t2 in t_lpf:
    if(t2==0): #시간값이 0이 되는 순간에 sinc function은 무한대가 된다. 이를 표현하기 위해 임의로 1로 설정하는 것.
        tmp_LPF=1
    else:
        tmp_LPF=np.sin(2*np.pi*LPF_f*t2)/(2*np.pi*LPF_f*t2) #sinc function을 만들어준다.
    LPF.append(tmp_LPF)
LPF_sig=np.convolve(rcv_sig, LPF, 'same') #컨볼루션 해주는 연산. 시간영역의 수신신호를 컨볼루션 하겠다.
filtered_sig=LPF_sig/np.sum(LPF)*2 #얘는 그냥 신호그려보면 너무 크게나와서 평균1정도로 맞춰주려고 조절한거 뿐
plt.subplot(817)
plt.plot(t,filtered_sig)

freq_lpf_sig=np.abs(np.fft.fftshift(np.fft.fft(filtered_sig))) #주파수 영역의 수신신호~~ 가운데는 원래 신호가 나오고, 다른애는 2배로 뜀. 이제 가운데 신호만 LPF씌워서 뺴내면 끝
plt.subplot(818)
plt.plot(t, freq_lpf_sig)

plt.show()