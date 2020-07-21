----

Q 1: About **intrinsics** and **extrinsics** of a camera and **camera matrix**

Ans 1:  

相机的内参是相机本身的参数，包括 **焦距 focal length**, **image sensor format **缩放大小, **principal point 像主点坐标**；相机的内参是相机的**固有参数**，每次拍摄相机的内参都是一样的；相机的内参其实构成了由**相机坐标系 camera coordinate**到**像素坐标系 pixel coordinate**的内参矩阵**K**,完成的是一种**透视变换和仿射变换**

![image-20200719142109949](https://cdn.jsdelivr.net/gh/QYHcrossover/blog-imgbed/blogimg/20200719142112.png)

相机的外参每次拍摄都不相同，主要和拍摄的位置和角度有关；像素的外参构成了**外参矩阵**extrinsic matrix，它对应的是由**真实世界的坐标系world coordinates**到**相机坐标系camera coordinate**的变换，它是一种**刚体变换**；这种变换可以由三维**旋转**和**平移**得到，所以相机的外参主要就是旋转和平移的参数，可以表示为R1，R2，R3和T

<img src="https://img-blog.csdnimg.cn/20190414095528293.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80Mzg0Mzc4MA==,size_16,color_FFFFFF,t_70" alt="img" style="zoom:67%;" />

**camera matrix**表示的就是将由外参决定的刚体变换和内参决定的透视变换和仿射变换合并为一种变换，这种变换的对应的矩阵就是**camera matrix**,附一张由**世界坐标系**变换到**相机坐标系**，再到**图像坐标系**最后到**像素坐标系**的过程；

![img](https://picb.zhimg.com/80/v2-665648ff84735e54ea26e34ed9096ba8_1440w.jpg)

![img](https://pic3.zhimg.com/80/v2-7813885e0d781a4301feee1ce9f52041_1440w.jpg)

reference：

- https://blog.csdn.net/weixin_43843780/article/details/89294131
- https://en.wikipedia.org/wiki/Camera_resectioning

-----

Q 2: transform a 3D point onto the image plane

Ans 2:

<img src="https://cdn.jsdelivr.net/gh/QYHcrossover/blog-imgbed/blogimg/20200719144908.png" alt="image-20200719144906291" style="zoom: 50%;" />

-----

Q3: 2D image to 3D camera coordinate 

Ans3: 

![img](https://cdn.jsdelivr.net/gh/QYHcrossover/blog-imgbed/blogimg/20200719145244.png)

-----

Q4: About distortion

1. **畸变distortion**发生在**摄像机坐标系到图像坐标系变换**时，在透视变换时由于一些因素导致图像发生畸变，引起原始图像的失真；畸变主要分为**径向畸变**和**切向畸变**两种；

   - **径向畸变**主要是镜头的制造工艺不足，是透镜本身的原因导致的；主要又分为桶形畸变和枕形畸变，数学中常用泰勒公式展开来进行建模，这里会引入k1,k2,k3等径向畸变的参数,公式为

     $$ x_0=x(1+k_1r^2+k_2r^4+k_3r^6) \\ y_0=y(1+k_1r^2+k_2r^4+k_3r^6)$$ 

   - **切向畸变**主要是镜头与像平面不平移造成的，同样的数学上引入p1、p2两个参数来描述：

     $$x_0=2p_1xy+p_2(r^2+2x^2)+1 \\y_0=p_2(r^2+2y^2)+2p_2xy+1$$

2. ![img](https://cdn.jsdelivr.net/gh/QYHcrossover/blog-imgbed/blogimg/20200719155326.png)

references:

- https://www.cnblogs.com/zyly/p/9366080.html
- https://docs.opencv.org/2.4/modules/calib3d/doc/camera_calibration_and_3d_reconstruction.html

-----

Q5:   Describe what the camera calibration does

相机标定**camera calibration**即通过一系列照片来求出相机的内参数、外参数、畸变参数的过程；

相机标定是计算机视觉的一个基础工作，为图片的正畸、测距做准备

-----

Q6：Programming for camera calibration with opencv

Ans6:

单目相机标定代码地址 https://github.com/QYHcrossover/Project_Stereo/blob/master/single_calibration.py

刚开始直接看Opencv的文档有些吃力，主要让我迷糊的是API中的输入和输出对应的是什么，在调用calibrateCamera前应该做哪些预备工作等；于是我就找到了CSDN上的一篇博客，先搞清楚了算法的流程：

```
1. 准备标定图片
2. 对每一张标定图片，提取角点信息
3. 对每一张标定图片，进一步提取亚像素角点信息
4. 在棋盘标定图上绘制找到的内角点（非必须，仅为了显示）
5. 相机标定
```

然后这个博客非常详细，附带了python代码和代码解析；在对源码简单修改后，我便跑通了老师您给的测试图片，成功地标定了相机的内参数、外参数和畸形矩阵；然后我便对应API逐行理解每行代码，通过jupyter逐行输出中间结果，理解起来也没什么太大的障碍；

唯一有些疑问的是最后计算出的外参数中的**R旋转系数**和**T平移系数**，照道理每个图片单应矩阵中的R应该是[R1，R2],是个3 * 2的二维矩阵，计算出的R和T一样居然是3 * 1的向量，~~这让我有所不解。猜测R1和R2彼此正交，且R1R2模都为1，R1定了以后R2也定了（不知道对不对）~~

前面猜测完全错了，后面在双目视觉的时候又回过头看感觉不对，又查了查资料，原来这个向量表示的是3的维的旋转弧度，而不是旋转矩阵中的一个向量！opencv也有专门的函数`Rodrigues()`来进行旋转弧度和旋转向量的转换，所以我将代码整合了一下，通过原先的旋转向量和平移向量计算出外参矩阵，也为后面的双目标定做准备。

Reference：

- https://docs.opencv.org/2.4/modules/calib3d/doc/camera_calibration_and_3d_reconstruction.html
- https://blog.csdn.net/weixin_42653918/article/details/89294957（主要是这篇，写得很详细）
- https://blog.csdn.net/mightbxg/article/details/79363699 opencv中的旋转矩阵和旋转向量

-----

Q7: Undistort the images

对图片去畸变这个在我刚才看到的博客中也提到了，用的opencv的函数是`cv2.undistort()`

```python
dst = cv2.undistort(src, cameraMatrix, distCoeffs[, dst[, newCameraMatrix]]	)
```

或者也可以用`cv2.initUndistortRectifyMap`和`cv2.remap`先计算一个先计算一个从畸变图像到非畸变图像的映射，然后使用这个映射关系对图像进行去畸变。

```python
# undistort
mapx,mapy = cv2.initUndistortRectifyMap(mtx,dist,None,newcameramtx,(w,h),5)
dst = cv2.remap(img,mapx,mapy,cv2.INTER_LINEAR)
```

----

Q8:  programming for Zhang's method

这个编程题应该来说非常难了，

References:

- https://zhuanlan.zhihu.com/p/94244568
- https://blog.csdn.net/qq_40369926/article/details/89251296
- https://blog.csdn.net/u010128736/article/details/52860364

----

Q10：Epipolar Line

Ans10：

<img src="https://cdn.jsdelivr.net/gh/QYHcrossover/blog-imgbed/blogimg/20200719205659.png" alt="image-20200719205657754" style="zoom: 67%;" />

![img](https://cdn.jsdelivr.net/gh/QYHcrossover/blog-imgbed/blogimg/20200719205719.png)

这道题做得有点虚，也不知道对不对；首先我看了资料理解了这个直线就是图中的$e_2x_2$,然后开始求它方程；

主要还是坐标系太混乱了，涉及到左相机的立体坐标系、像素坐标系以及右相机的立体坐标系、像素坐标系等；所以我的思路是统一坐标系，因为题目中求的是在**右相机体系下的直线方程**，所以都需要**统一到右相机的坐标体系**

像素坐标和相机坐标之间的转换挺熟悉了，从左到右的转换就第一次尝试（不知道有没有写反）；这边主要的难点是**平移向量T的几何意义**，实际上对应了$O_1O_2$,这点挺难发现的（不知道对不对）；另外这里还涉及到了**求平面方程**的知识，包括法向量怎么求（向量叉乘）等等，加上我不是完全理解，所以在第3步求平面方程那块$C_{r2}$那边不知道要不要减去一个**t**，知乎上写的是直接$C_{r2}$,我主观觉得两者皆可，都是该平面的向量

References:

- https://zhuanlan.zhihu.com/p/143299493 我觉得这篇挺好理解的

-----

Q11: Fundamental Matrix

求解基础矩阵，这道题的重点和难点还是**坐标体系转换**和求**平面方程**的问题，和上个题目求极线约束类似；从我看到的资料和以我的理解上看，这题的坐标体系应该是要全部统一成**左相机的坐标系**，这个和上一题恰恰相反；

博客中有两处让我大为不解；首先在第二节中，给出$P_l$和$P_r$的关系是$P_r=RP_l+T$从左到右的转换顺序，然后到第三节给出的$P_l$和$P_r$的关系是：$P_r=R(P_l−T_r)$,那可以得出$T$和$T_r$的关系，有 $T = -RT_r$（不知道是否正确）

最让我奇怪的是公式8 $P_r^TRSP_l=0$ ,按照推导来说这式子应该是$R^{-1}$啊，所以到底是$P_r=R(P_l−T_r)$错了还是这个式子错了呢？？

-----

Q12:  Stereo Calibration

代码地址 https://github.com/QYHcrossover/Project_Stereo/blob/master/stereo_calibration.py

这道题被老师标了两星，看了老师给的资料感觉并不难，就是双目标定的基本内容，在两个单目标定的基础上增加了**R和L**，即两个相机坐标之间的转换关系；步骤也很清晰：

1. 先各自求单个相机的内参和外参,分别记作($R_l$,$t_l$),($R_r$,$t_r$)

2. 根据下面的式子求解R和L

   ![image-20200720090131469](https://cdn.jsdelivr.net/gh/QYHcrossover/blog-imgbed/blogimg/20200720090133.png)

References:

- https://blog.csdn.net/xuelabizp/article/details/50417914

----

Q13: 