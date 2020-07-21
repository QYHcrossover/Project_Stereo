import cv2
import numpy as np
import glob

def detection(path,w,h):
    '''
     parameters: w,h 一张图横纵各有几个格点
    return：obj_points,img_points,size
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
            cv2.waitKey(50)
    cv2.destroyAllWindows()
    return obj_points,img_points,size


#从旋转矩阵和平移向量中获得外参矩阵
def extrinsicsMatrix(rvec,tvec):
    etsmtxs = [] #存储外参矩阵
    for rvec,tvec in zip(rvecs,tvecs):
        etsmtx = np.zeros([4,4])
        R,_ = cv2.Rodrigues(rvec)
        etsmtx[:3,:3] = R #旋转矩阵
        etsmtx[3,:3] = np.squeeze(tvec) #平移向量
        etsmtx[3,3] = 1 #1
        etsmtxs.append(etsmtx)
    return etsmtxs

if __name__ == "__main__":
    w,h = 9,6
    path = "./Project_Stereo_left/left/*.jpg"
    #step1 找出棋盘中的格点位置
    obj_points,img_points,size = detection(path,w,h)

    #step2 相机标定
    ret, itsmtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, size, None, None)
    print("内参矩阵:\n", itsmtx) # 内参数矩阵
    print("畸变矩阵:\n", dist)  # 畸变系数   
    etsmtxs = extrinsicsMatrix(rvecs,tvecs)
    print("外参矩阵:\n", etsmtxs)  #外参数矩阵 list包含n个外参数矩阵，矩阵维数是(4,4)

    #step3 选一张图片进行校正
    img = cv2.imread("./Project_Stereo_left/left/left01.jpg")
    cv2.imshow("undistort before",img)
    cv2.waitKey(1000)
    newcameramtx, roi=cv2.getOptimalNewCameraMatrix(itsmtx,dist,(w,h),0,(w,h)) # 自由比例参数
    newimg = cv2.undistort(img,itsmtx,dist,None,newcameramtx)
    cv2.imshow("after undistort",newimg)
    cv2.waitKey(1000)
    x_,y_,w_,h_ = roi
    dst = newimg[y_:y_+h_, x_:x_+w_]
    cv2.imshow("after cut",dst)
    cv2.waitKey(1000)
