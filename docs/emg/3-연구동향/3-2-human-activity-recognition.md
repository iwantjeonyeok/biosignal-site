# 3.2. Human activity recognition


EMG를 활용해, 사람의 움직임을 인식 하는 연구도 활발히 진행되고 있다. 특히, 사람의 움직임을 분석해, 재활분야, 의수(또는 의족) 최적화, 움직임 모니터링과 관련된 연구들이 더욱 활발히 수행되고 있다. 각 분야에 적용시키기 위해 다양한 동작인식 연구들이 수행되고 있다.
(그림 3. a) Ren Y. 와 그 연구진들은 EMG와 IMU (Inertial Measurement Unit)를 통해 얻어진 데이터를 computer vision 기반 CNN (Convolution Nueral Network) 알고리즘을 활용해 사람의 동작을 인식하는 연구를 수행했다 [^33]. 이때 EMG 신호를 spectrogram으로 바꾸어, 그 자체를 이미지로 인식을 해 동작을 구분하는 피처로 사용했다.
(그림 3. b) Bangaru S. S. 와 연구진들은 전완근에 EMG 계측장치를 부착해 데이터를 수집하고, 다양한 feature들을 EMG 신호로부터 추출해, ANN을 통해 작업자의 동작을 인식하는 연구를 수행하였다 [^34]. 제한된 동작이지만, 전완근에서 수집된 EMG 데이터셋만으로도 동작 인식을 높은 성능을 통해 해내는 것을 확인할 수 있다.

![**그림 3.** (a) Computer vision 지식기반 동작 인식 CNN 모델 [^33], (b) ANN을 활용한 EMG 기반 작업자의 움직임 인식 [^34]](images/image-4.png)
