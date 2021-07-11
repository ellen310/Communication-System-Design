from matplotlib import pyplot as plt
import numpy as np

step = 0.002 #1초에 500개 들어가게.
t=np.arange(step, 1+step, step)
fs=20 #샘플링 주파수. 1초에 20번 샘플링
ts=1/fs
ds=ts/step
num_samples=np.shape(t)[0]

signal=np.sin(2*np.pi*2*t)-2*np.sin(2*np.pi*5*t+3) #최대 주파수는 5임(5*t있으니까). 나이키스트이론: 샘플링주파수는 최대주파수의 2배이상해야.==>여기서 최대주파수5니까 샘플링주파수(fs)는 최소 10은 넘어야 함.20으로 설정했으니 가능
impulse_train=np.zeros(num_samples) #우선 0을 500개 넣어준다(임펄스트레인 만들거임)
count=0
for i in impulse_train: #500번의 0 사이에 1을 넣어주는 과정. 그 간격은 ds
    if(count%int(ds))==(int(ds)-1):
        impulse_train[count]=1   #ds간격으로 한번씩 1을 넣어준다.
    count+=1

sampled_signal=impulse_train*signal #샘플링한 신호=임펄스트레인X신호
rect_sig=[0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0]

plt.subplot(911)
plt.plot(t, signal) #원래신호

plt.subplot(912)
plt.stem(t, impulse_train) #임펄스 트레인. plot대신 stem을 쓰면 막대그래프 그려줌

plt.subplot(913)
plt.stem(t, sampled_signal)  #샘플링한 신호

freq_signal=np.abs(np.fft.fftshift(np.fft.fft(signal))) #원래 신호의 주파수영역
plt.subplot(914)
plt.plot(t, freq_signal)

freq_signal=np.abs(np.fft.fftshift(np.fft.fft(sampled_signal))) #샘플링한 신호의 주파수 영역 : 시간영역에서 임펄스트레인과 곱했으므로, 주파수영역에선 컨볼루션(쫙 복사됨. 레플리카)
plt.subplot(915)
plt.plot(t, freq_signal)

plt.subplot(916)
tmpSig=np.convolve(rect_sig, sampled_signal, 'same') #직사각형신호와 샘플링한 신호를 컨볼루션. 길이는 동일하게(same)
plt.plot(t,tmpSig)

freq_signal=np.abs(np.fft.fftshift(np.fft.fft(tmpSig)))
plt.subplot(917)
plt.plot(t, freq_signal)


LPF_f=10
t_lpf=np.arange(-0.5,0.5,step)
LPF=[]
for t2 in t_lpf:
    if(t2==0):
        tmp_LPF=1
    else:
        tmp_LPF=np.sin(2*np.pi*LPF_f*t2)/(2*np.pi*LPF_f*t2)
    LPF.append(tmp_LPF)
LPF_sig=np.convolve(tmpSig, LPF, 'same') #주파수영역에서 LPF씌우기 위해서 시간영역신호를 sincFunction과 컨볼루션
filtered_sig=LPF_sig/np.sum(LPF)*2
plt.subplot(918)
plt.plot(t,filtered_sig)

freq_signal=np.abs(np.fft.fftshift(np.fft.fft(filtered_sig))) #주파수영역에서 가운데만 잘라낸 모습
plt.subplot(919)
plt.plot(t, freq_signal)

plt.show()