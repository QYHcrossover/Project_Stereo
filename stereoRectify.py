import cv2
import numpy as np
import glob
from single_calibration import detection

if __name__ == "__main__":
	#step0 参数设置
	w,h = 9,6
	leftpath = "./Project_Stereo_left/left/*.jpg"
	rightpath = "./Project_Stereo_right/right/*.jpg"

	#step1 分别找出棋盘中的格点位置
	objectPoints,imagePoints1,imageSize = detection(leftpath,w,h)
	_,imagePoints2,_ = detection(rightpath,w,h)

	#step2 先进行单目标定
	ret1, cameraMatrix1, distCoeffs1, rvecs1, tvecs1 = cv2.calibrateCamera(objectPoints,imagePoints1,imageSize,None,None)
	newCameraMatrix1, roi1 =cv2.getOptimalNewCameraMatrix(cameraMatrix1,distCoeffs1,(w,h),0,(w,h))
	ret2, cameraMatrix2, distCoeffs2, rvecs2, tvecs2 = cv2.calibrateCamera(objectPoints,imagePoints1,imageSize,None,None)
	newCameraMatrix2, roi2 =cv2.getOptimalNewCameraMatrix(cameraMatrix2,distCoeffs2,(w,h),0,(w,h))

	#step3 再进行双目标定
	retval, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, R, T, E, F = cv2.stereoCalibrate(objectPoints, imagePoints1, imagePoints2, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, imageSize)
	
	#step4 根据双目标定结果,计算立体校正参数
	R1, R2, P1, P2, Q, validPixROI1, validPixROI2 = cv2.stereoRectify(cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, imageSize, R, T)
	
	#step5 根据双目标参数，计算映射矩阵mapx,mapy
	mapl1, mapl2 = cv2.initUndistortRectifyMap(cameraMatrix1, distCoeffs1, R1, newCameraMatrix1,imageSize,cv2.CV_32FC1)
	mapr1, mapr2 = cv2.initUndistortRectifyMap(cameraMatrix2, distCoeffs2, R2, newCameraMatrix2,imageSize,cv2.CV_32FC1)
	
	#step6 读取一组照片并完成立体矫正
	imgpath1 = "./Project_Stereo_left/left/left01.jpg"
	imgpath2 = "./Project_Stereo_right/right/right01.jpg"
	img1 = cv2.imread(imgpath1)
	img2 = cv2.imread(imgpath2)
	newimg1 = cv2.undistort(img1,cameraMatrix1, distCoeffs1,None,newCameraMatrix1)
	newimg2 = cv2.undistort(img2,cameraMatrix2, distCoeffs2,None,newCameraMatrix2)
	newimg1 = cv2.remap(newimg1,mapl1,mapl2,cv2.INTER_LINEAR)
	newimg2 = cv2.remap(newimg2,mapr1,mapr2,cv2.INTER_LINEAR)
	print(newimg1)
	print(newimg2)
	cv2.imshow("newimg1",newimg1)
	cv2.waitKey(500)
	cv2.imshow("newimg2",newimg2)
	cv2.waitKey(0)