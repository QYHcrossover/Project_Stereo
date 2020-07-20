import cv2
import numpy as np
import glob

def singleCalibration(path,w,h):
    '''
    function for singleCalibration
    Parameters:
        - path : input for glob,image path
        - w,h : number of points in length or width
    returns:
        - itsmtx : intrinsics matrix
        - dist : distortion coefficients;
        - etsmtxs : extrinsics matrix for each picture
    '''
    
    # 设置寻找亚像素角点的参数，采用的停止准则是最大循环次数30和最大误差容限0.001
    criteria = (cv2.TERM_CRITERIA_MAX_ITER | cv2.TERM_CRITERIA_EPS, 30, 0.001)
    # 获取标定板角点的位置
    objp = np.zeros((h * w, 3), np.float32)
    objp[:, :2] = np.mgrid[0:w, 0:h].T.reshape(-1, 2)  # 将世界坐标系建在标定板上，所有点的Z坐标全部为0，所以只需要赋值x和y
    obj_points = []  # 存储3D点
    img_points = []  # 存储2D点
    #寻找图片
    images = glob.glob(path)
    for fname in images:
        img = cv2.imread(fname)
        cv2.imshow('img',img)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        size = gray.shape[::-1]
        ret, corners = cv2.findChessboardCorners(gray, (h, w), None)
        if ret:
            obj_points.append(objp)
            corners2 = cv2.cornerSubPix(gray, corners, (5, 5), (-1, -1), criteria)  # 在原角点的基础上寻找亚像素角点
            #print(corners2)
            if [corners2]:
                img_points.append(corners2)
            else:
                img_points.append(corners)
            cv2.drawChessboardCorners(img, (w-1,h), corners, ret)  # 记住，OpenCV的绘制函数一般无返回值
            cv2.imshow('img', img)
            cv2.waitKey(100)
    cv2.destroyAllWindows()
    ret, itsmtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, size, None, None)
    etsmtxs = [] #存储外参矩阵
    for rvec,tvec in zip(rvecs,tvecs):
        etsmtx = np.zeros([4,4])
        R,_ = cv2.Rodrigues(rvec)
        etsmtx[:3,:3] = R #旋转矩阵
        etsmtx[3,:3] = np.squeeze(tvec) #平移向量
        etsmtx[3,3] = 1 #1
        etsmtxs.append(etsmtx)

    return itsmtx,dist,etsmtxs

if __name__ == "__main__":
    path = "./Project_Stereo_left/left/*.jpg"
    itsmtx,dist,etsmtxs = singleCalibration(path,9,6)
    print("内参矩阵:\n", itsmtx) # 内参数矩阵
    print("畸变矩阵:\n", dist)  # 畸变系数   
    print("外参矩阵:\n", etsmtxs)  #外参数矩阵 list包含n个外参数矩阵，矩阵维数是(4,4)
    print(len(etsmtxs)) #13
    print(etsmtxs[0].shape) #(4,4)

