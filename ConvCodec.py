import numpy as np

def Encoder(data):
    data = np.append(data, [0,0,0]) #데이터 끝에 tail달아주는거. 000
    dataSize = np.shape(data)[0]
    shiftReg = [0,0,0] #k=3 인 Shift Register
    encoded_bit = np.zeros((2, dataSize)) #R=1/2. 1비트 들어오면 2비트 출력=>2행

    for i in range(dataSize):
        shiftReg[2]=shiftReg[1]
        shiftReg[1]=shiftReg[0]
        shiftReg[0]=data[i]
        encoded_bit[0, i]=np.logical_xor(np.logical_xor(shiftReg[0], shiftReg[1]), shiftReg[2])
        encoded_bit[1, i]=np.logical_xor(shiftReg[0],shiftReg[2])

    return encoded_bit

def ViterbiDecoder(encoded_bit):
    ref_out = np.zeros((2, 8))
    ref_out[0, :] = [0, 1, 1, 0, 1, 0, 0, 1]
    ref_out[1, :] = [0, 1, 0, 1, 1, 0, 1, 0]

    dataSize= np.shape(encoded_bit)[1] #2 by 원래데이터길이+3[0,0,0]
    cumDist=[0,100,100,100] #초기값 설정 00/01/10/11
    prevState = []

    for i in range(dataSize):
        tmpData = np.tile(encoded_bit[:, i].reshape(2, 1), (1, 8))
        dist = np.sum(np.abs(tmpData - ref_out), axis=0)
        # 0 1 1 0 1 0 0 1
        # 0 1 0 1 1 0 1 0
        # 0 2 1 1 2 0 1 1  ==>  dist계산결과
        tmpDist = np.tile(cumDist, (1, 2)) + dist
        # [0 100 100 100 0 100 100 100] + [0 2 1 1 2 0 1 1]
        tmpPrevState = [] #과거의 state가 뭔지 기록
        for a in range(4): #state 수가 4니까
            if tmpDist[0, 2 * a + 0] <= tmpDist[0, 2 * a + 1]:
                cumDist[a] = tmpDist[0, 2 * a + 0]
                tmpPrevState.append((a % 2) * 2 + 0)
            else:
                cumDist[a] = tmpDist[0, 2 * a + 1]
                tmpPrevState.append((a % 2) * 2 + 1)
        prevState.append(tmpPrevState)

        state_index = np.argmin(cumDist) #cumDist에서 젤 작은걸 선택한다.
        decoded_bit = [] #decoding bit을 저장할 배열

    for b in range(dataSize -1, -1, -1): #디코딩은 역순
        decoded_bit.append(int(state_index/2)) #가장 작은녀석을 보는데 절반으로 나누면 절반을 중심으로 밑인지 위인지 확인 가능함. 그래서 2로 나눈거
        state_index=prevState[b][state_index]
    data_size = np.shape(decoded_bit)[0]
    decoded_bit=np.flip(decoded_bit)[0:data_size - 3]

    return decoded_bit