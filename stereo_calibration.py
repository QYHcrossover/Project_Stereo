import cv2
import numpy as np
import glob
from single_calibration import detection

def binocularCalibrate(leftpath,rightpath,w,h):
	#step1 分别找出棋盘中的格点位置
	objectPoints,imagePoints1,imageSize = detection(leftpath,w,h)
	_,imagePoints2,_ = detection(rightpath,w,h)
	#step2 先进行单目标定
	ret1, cameraMatrix1, distCoeffs1, rvecs1, tvecs1 = cv2.calibrateCamera(objectPoints,imagePoints1,imageSize,None,None)
	ret2, cameraMatrix2, distCoeffs2, rvecs2, tvecs2 = cv2.calibrateCamera(objectPoints,imagePoints1,imageSize,None,None)
	#step3 再进行双目标定
	retval, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, R, T, E, F = cv2.stereoCalibrate(objectPoints, imagePoints1, imagePoints2, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, imageSize)
	return retval, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, R, T, E, F

if __name__ == "__main__":
	#step0 参数设置
	w,h = 9,6
	leftpath = "./Project_Stereo_left/left/*.jpg"
	rightpath = "./Project_Stereo_right/right/*.jpg"

	retval, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, R, T, E, F = binocularCalibrate(leftpath,rightpath,w,h)
	print("R:\n",R) #旋转矩阵
	print("T:\n",T) #平移矩阵
	print("E:\n",E) #本征矩阵
	print("F:\n",F) #基础矩阵
	