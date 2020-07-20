from single_calibration import *

def extract(ets):
	'''
	paramter: ets extrinsics matrix for each picture
	return: R,t rotate matrix and translate vector
	'''
	R = ets[:3,:3]
	t = ets[3,:3][:,np.newaxis]
	return R,t

if __name__ == "__main__":
	leftpath = "./Project_Stereo_left/left/*.jpg"
	its_left,dist_left,ets_left = singleCalibration(leftpath,9,6)
	rightpath = "./Project_Stereo_right/right/*.jpg"
	its_right,dist_right,ets_right = singleCalibration(rightpath,9,6)
	# print(its_left,dist_left,ets_left)
	# print(its_right,dist_right,ets_right)

	#分别从两个外参矩阵中提取Rl,tl,Rr,tr并计算R,t
	for i in range(len(ets_left)):
		Rl,tl = extract(ets_left[i])
		Rr,tr = extract(ets_right[i])
		# 计算R
		R = Rr@Rl.T
		t = tr-R@tl
		print(R,t)
