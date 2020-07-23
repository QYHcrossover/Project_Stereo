[toc]

## 项目环境

- Python 3.6.5

- opencv-python 4.2.0
- numpy 1.16.0

## 项目概述

计算机视觉方向，有关于双目视觉、双目测距的基础工作研究；完成的内容包括：

- 单目相机标定，去畸变
- 双目相机标定
- 立体校正
- SGBM算法求视差

收集到一份张正友标定的python源码：

## 项目内容

### single_calibration

- 提取棋盘格点的位置，主要函数为`findChessboardCorners`，提取格点位置

  ![image-20200722094108256](https://cdn.jsdelivr.net/gh/QYHcrossover/blog-imgbed/blogimg/20200722094109.png)

- 单摄像机标定，主要函数是`calibrateCamera`,由于返回的是弧度制表示的旋转向量和平移矩阵，自己通过简单公式计算出了**外参矩阵**

  ![image-20200722094324491](https://cdn.jsdelivr.net/gh/QYHcrossover/blog-imgbed/blogimg/20200722094325.png)

- 去畸变测试，主要用的函数是`undistort`,效果如下好像也没什么区别

  ![image-20200722094833265](https://cdn.jsdelivr.net/gh/QYHcrossover/blog-imgbed/blogimg/20200722095709.png)

由于双相机标定的时候也需要用到单相机标定的内容，所以我将提取角点这个过程封装成函数`detection`,方便后续调用

### stereo_calibration

主要完成的是双相机标定的任务，除了单相机标定的(**内参矩阵、畸变系数、旋转矩阵、平移向量**)外；双相机标定了左右两坐标间转换的**旋转矩阵**和**平移向量**，另外还包括**本征矩阵**和**基础矩阵**；主要用到的API是`stereoCalibrate`结果如图：

![image-20200722095441292](https://cdn.jsdelivr.net/gh/QYHcrossover/blog-imgbed/blogimg/20200722095442.png)

将双目标定的过程封装成函数`binocularCalibrate`方便以后调用

### stereoRectify

这部分完成的是立体校正的内容，即通过计算两个映射矩阵将左右两相机的视角相统一；在立体校正前也应该完成畸形校正，主要用到的API是`stereoRectify`、`initUndistortRectifyMap`和`remap` ；效果如图:

![image-20200722100508361](https://cdn.jsdelivr.net/gh/QYHcrossover/blog-imgbed/blogimg/20200722100509.png)

效果还可以，因为没有裁切所以图片边缘有”空黑“

### SGBM

利用opencv提供的`StereoSGBM_create`求左右两图像的视差，目的是测距；效果如下：

首先输出的是SGBM算法经过畸变校正和立体校正后的结果，和我刚才分步实现的效果差不多，只不过这里经过了裁切

![image-20200722101120010](https://cdn.jsdelivr.net/gh/QYHcrossover/blog-imgbed/blogimg/20200722101121.png)

然后是参数调节面板和视差图：

![image-20200722101424905](https://cdn.jsdelivr.net/gh/QYHcrossover/blog-imgbed/blogimg/20200722101426.png)

### Zhang's method

能跑通，结果和opencv实现的差不多

![image-20200723221134578](https://cdn.jsdelivr.net/gh/QYHcrossover/blog-imgbed/blogimg/20200723221135.png)