在现实世界中的许多应用中，比如图像特效、增强现实都依赖于眼睛位置追踪与虹膜追踪。一旦能获得准确的虹膜跟踪，在不需要任何其他设备的情况下人眼到摄像头的距离可以估算出来。这将提供更多的算法适应场景，比如特效应用中根据距离调整特效部件的大小、手机字体随着人眼距离的增加而增大。
虹膜跟踪是一项具有挑战性的工作，因为计算资源的限制、不同的光照条件、以及头发与眼皮的遮挡。通常专业的计算设备会限制该算法的应用范围。
# 用于虹膜跟踪的机器学习管道
该机器学习管道的第一步依赖于3D面部网格检测算法，这个算法应用了高保证面部landmarks来生成面部结构的大致网格。从这些网格中，我们可以从原始图像中分离出眼部图像，将该图像应用于虹膜跟踪模型。然后问题就被分为两个部分：眼部轮廓估计与虹膜定位。设计一个多任务模型，该模型对每一个任务具有统一的编码器，各任务具有单独组件，该设计允许我们使用特定任务的训练数据。
为了使用裁剪后的眼部区域图像训练该模型，我们手动标注了大约50k张图像，涵盖了各类光照条件与头部姿态的各个国家与地区的人眼图像。
![image.png](https://cdn.nlark.com/yuque/0/2022/png/22656197/1642668384360-8a6fe769-40fa-4e5d-9aff-24b745b1b730.png)
_人眼区域标注，使用红色标注眼皮，蓝色标注虹膜轮廓_


![image.png](https://cdn.nlark.com/yuque/0/2022/png/22656197/1642668738446-fe062743-fb5e-460c-ba8c-fa5f55f07f24.png)


_模型的输入是裁剪后的人眼区域图像，预测结果中通过单独的任务解码器产生人眼landmarks，通过单独任务解码器产生虹膜lanmarks_
​

# **Depth-from-Iris：基于单张图像的虹膜深度估计**
虹膜跟踪模型能够确定人眼与相机的距离，再不需要任何其他额外设备的情况下做到误差不超过10%。这依赖于人类横向虹膜尺寸的一致性，有研究表明，人眼尺寸持续保持在11.7±0.5毫米并且拥有简单的几何结构。如插图所示，针孔摄像机将图像映射到方形区域的传感器上成像。人眼landmarks到摄像头的距离可以通过摄像机的焦距长度估算，摄像机的焦距可以通过图像中的EXIF元信息获得，摄像机的其他参数为固有参数，给定焦距长度，可以直接通过人眼实际尺寸与成像人眼的像素尺寸求得人眼与摄像机的距离。
![image.png](https://cdn.nlark.com/yuque/0/2022/png/22656197/1642670302555-4ba91b40-b841-4312-b0cd-43a647eea45e.png)
_人眼与摄像机的距离（d）可以通过相机焦距（f）人眼固定尺寸以及成像尺寸，结合相似三角形定律求得_
![](https://1.bp.blogspot.com/-5sT_B1DWTGg/Xyw0UM40atI/AAAAAAAAGVM/foqPr2XPszQYxAATdmORKjJ8BK9bu6DFgCLcBGAsYHQ/s0/image2.gif#crop=0&crop=0&crop=1&crop=1&from=url&id=E2lXs&margin=%5Bobject%20Object%5D&originHeight=360&originWidth=398&originalType=binary&ratio=1&rotation=0&showTitle=false&status=done&style=none&title=)
为了量化该方法的准确率，我们将与配备深度摄像头的iPhone11收集的自拍图像进行对比，同步超过200名参与者的视频与深度图像。我们经过使用激光测距设备实验验证，iPone11的深度相机在2米内误差小于2%；实验表明基于虹膜的测距方法平均误差为4.3%，标准差为2.4%。该数据在参与者未佩戴眼睛的情况下测得，若佩戴眼睛测试平均误差提升到4.8%，标准差为3.1%，该方法未在患有眼部疾病的患者身上测试。考虑到不需要任何其他硬件设备，该方法使得大量处于成本考虑的单目相机设备通过单张图像获得距离成为可能。
![image.png](https://cdn.nlark.com/yuque/0/2022/png/22656197/1642738666845-16ac8e0b-5d41-46f6-8027-e2d589b9be32.png)
_左侧为估计误差直方图，右侧为虹膜距离的实际值与估计值的对照_


# MediaPipe Iris发布版本
虹膜检测以及深度估计模型能够在多个平台运行，包括电脑、安卓手机、Web。在Web中，引入了 [WebAssembly](https://en.wikipedia.org/wiki/WebAssembly)和[XNNPACK](https://github.com/google/XNNPACK)在浏览器本地运行机器学习模型，而不是将数据发送到云端。


# 应用场景
## 1、由人脸视频驱动虚拟头像
![](https://1.bp.blogspot.com/-Lpgeiec1LTI/Xywye-E8YOI/AAAAAAAAGUU/bAytHYPS1wIHV_EXWWBAXIdnp3p1H0D1wCLcBGAsYHQ/w640-h252/image3.gif#crop=0&crop=0&crop=1&crop=1&from=url&id=n297a&margin=%5Bobject%20Object%5D&originHeight=252&originWidth=640&originalType=binary&ratio=1&rotation=0&showTitle=false&status=done&style=none&title=)
_中间图像是使用_[_FaceMesh_](https://google.github.io/mediapipe/solutions/face_mesh.html)_驱动的虚拟形象，右侧是引入虹膜跟踪的虚拟形象，相比较之下虚拟形象的活力明显提升_


## 2、人眼虹膜颜色涂色
![](https://1.bp.blogspot.com/-jF_HuzW-smE/Xywy_JurMuI/AAAAAAAAGUc/cMX_9GtWxM4RhOqMhURDYB831eDqJ0ZIwCLcBGAsYHQ/w586-h164/image13.gif#crop=0&crop=0&crop=1&crop=1&from=url&id=RKW9f&margin=%5Bobject%20Object%5D&originHeight=164&originWidth=586&originalType=binary&ratio=1&rotation=0&showTitle=false&status=done&style=none&title=)
_人眼虹膜涂色实例_
## 3、根据距离调节手机字体大小
![](https://1.bp.blogspot.com/-GJxNLlVwxqI/XywzLGfARTI/AAAAAAAAGUg/zkvGnNLmHmwyb_nDQ4j46mi95wPRYyP7gCLcBGAsYHQ/s0/image12.gif#crop=0&crop=0&crop=1&crop=1&from=url&id=sXyiB&margin=%5Bobject%20Object%5D&originHeight=540&originWidth=512&originalType=binary&ratio=1&rotation=0&showTitle=false&status=done&style=none&title=)
_观察到的字体大小保持恒定，与用户的设备距离无关_
​

参考文献：
[MediaPipe Iris: Real-time Iris Tracking & Depth Estimation](https://ai.googleblog.com/2020/08/mediapipe-iris-real-time-iris-tracking.html)
