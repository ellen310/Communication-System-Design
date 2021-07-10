from matplotlib import pyplot as plt
import numpy as np

t=np.arange(0.0001, 1.0001, 0.0001) #1초까지 보기
c_f=50 #기존신호에 곱해줄 임의의 높은 주파수. 실제로는 50보다도 훨 큼

signal=np.sin(2*np.pi*2*t)-2*np.sin(2*np.pi*3*t)+1.5*np.sin(2*np.pi*4*t)
plt.subplot(611)
plt.plot(t, signal)

carrier=np.cos(2*np.pi*c_f*t)
plt.subplot(612)
plt.plot(t, carrier)

plt.subplot(613)
plt.plot(t, signal*carrier)

carrier=np.sin(2*np.pi*c_f*t)
rcv_sig=carrier*signal*carrier
plt.subplot(614)
plt.plot(t, rcv_sig)

LPF_f=50 #렉탱귤러 모양의 넓이. 너무 작으면(좁으면) 원래신호까지 잘리고, 너무 넓으면 고주파 신호까지 잡힘. 잘 설정해야.
t_lpf=np.arange(-0.5,0.5,0.0001) #LowPassFilter의 길이
LPF=[]
for t2 in t_lpf:
    if(t2==0): #시간값이 0이 되는 순간에 sinc function은 무한대가 된다. 이를 표현하기 위해 임의로 1로 설정하는 것.
        tmp_LPF=1
    else:
        tmp_LPF=np.sin(2*np.pi*LPF_f*t2)/(2*np.pi*LPF_f*t2) #sinc function을 만들어준다.
    LPF.append(tmp_LPF) #10000개의 필터값이 저장될것이다.
LPF_sig=np.convolve(rcv_sig, LPF, 'same') #컨볼루션 해주는 연산
filtered_sig=LPF_sig/np.sum(LPF)*2
plt.subplot(615)
plt.plot(t,filtered_sig)

plt.subplot(616)
plt.plot(t,(rcv_sig-filtered_sig)) #수신한신호에서 복원된 신호를 빼내면 어떤 모양인지.

plt.show()