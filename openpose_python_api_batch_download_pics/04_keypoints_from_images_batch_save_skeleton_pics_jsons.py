# From Python
# It requires OpenCV installed for Python
import sys
import cv2
import os
from sys import platform
import argparse
import time
import codecs, json

try:
    # Import Openpose (Windows/Ubuntu/OSX)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print("dir_path", dir_path)
    try:
        # Windows Import
        if platform == "win32":
            # Change these variables to point to the correct folder (Release/x64 etc.)
            sys.path.append(dir_path + '/../../python/openpose/Release');
            os.environ['PATH']  = os.environ['PATH'] + ';' + dir_path + '/../../x64/Release;' +  dir_path + '/../../bin;'
            import pyopenpose as op
        else:
            # Change these variables to point to the correct folder (Release/x64 etc.)
            sys.path.append('../../python');
            # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
            # sys.path.append('/usr/local/python')
            from openpose import pyopenpose as op
    except ImportError as e:
        print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
        raise e

    # Flags
    # parser.add_argument("--image_dir", default=r"請輸入自己的圖片資料夾讀取路徑",help="")
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_dir", default=r"D:\tt_group_total_pics\0510_5290_9000\0510_input_resize256x256_5290_9000", help="Process a directory of images. Read all standard formats (jpg, png, bmp, etc.).")
    parser.add_argument("--no_display", default=False, help="Enable to disable the visual display.")
    args = parser.parse_known_args()

    # Custom Params (refer to include/openpose/flags.hpp for more parameters)
    params = dict()
    params["model_folder"] = "../../../models/"
    params["net_resolution"] = "-1x160"
    params["model_pose"] = "COCO"
    # 將背景關掉，只印骨架 skeleton
    params["disable_blending"] = True


    # Add others in path?
    for i in range(0, len(args[1])):
        curr_item = args[1][i]
        if i != len(args[1])-1: next_item = args[1][i+1]
        else: next_item = "1"
        if "--" in curr_item and "--" in next_item:
            key = curr_item.replace('-','')
            if key not in params:  params[key] = "1"
        elif "--" in curr_item and "--" not in next_item:
            key = curr_item.replace('-','')
            if key not in params: params[key] = next_item

    # Construct it from system arguments
    # op.init_argv(args[1])
    # oppython = op.OpenposePython()

    # Starting OpenPose
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()

    # Read frames on directory
    imagePaths = op.get_images_on_directory(args[0].image_dir);
    start = time.time()
    count = 0
    wrong_pic_fn_list = []
    for imagePath in imagePaths:
        datum = op.Datum()
        imageToProcess = cv2.imread(imagePath)
        # print(imageToProcess.shape)
        # pics = cv2.imread(imagePath)
        # scale_percent = 10
        # print(pics.shape)
        # width = pics.shape[1]
        # height = pics.shape[0]
        # width = int(width * scale_percent / 100)
        # height = int(height * scale_percent / 100)
        # dim = (256, 256)
        # print(dim)
        # imageToProcess = cv2.resize(pics , dim, interpolation=cv2.INTER_CUBIC)
        datum.cvInputData = imageToProcess
        opWrapper.emplaceAndPop(op.VectorDatum([datum]))

        # print("datum.poseKeypoints:", datum.poseKeypoints)
        # 取出每張圖的檔名：
        path_list = imagePath.split("\\")
        pic_fn_type = path_list[-1]
        pic_fn = pic_fn_type.split(".")[0]
        pic_fn = pic_fn.zfill(4)
        print("圖片檔名:", pic_fn)
        # print(type(pic_fn))

        try:
            # 取出每張圖各節點的x,y,score 的np.arrary
            keypoint_x_y_score_arr = (datum.poseKeypoints)
            # 取出每張圖各節點的x,y 的np.arrary
            keypoint_x_y_arr = (datum.poseKeypoints[0][:, [0, 1]])
            # 將每張圖的個各節點的x,y array 存成 list
            keypoint_x_y_arrtolist = keypoint_x_y_arr.tolist()
            print(keypoint_x_y_arrtolist)
            # keypoint_x_y_list_mat = mat(keypoint_x_y_arrtolist)
            # print("keypoint_x_y_arrtolist:\n", keypoint_x_y_arrtolist

        except TypeError as e:
            print(e)
            print('這是張不合格照片：', pic_fn)
            count += 1
            print('第', count, '次錯誤照片')
            wrong_pic_fn_list.append(pic_fn)
            continue

         # Store_fn(原始檔名)
         # base：為存檔路徑，請改成自己的目標位置
        base = r"D:\tt_group_total_pics\0510_5290_9000\0510_out_resize256x256_5290_9000_skeleton_add_people"
        if not os.path.exists(base):
            os.makedirs(base)
        # 將x,y的骨架依檔案名稱存承json檔
        fn = base + "/" + pic_fn + ".json"
        json.dump(keypoint_x_y_arrtolist, codecs.open(fn, 'w', encoding='utf-8'), separators=(',', ':'),indent=4)

        # 將有骨架圖的圖片依檔案名稱存檔
        fn = base + "/" + pic_fn + ".jpg"
        cv2.imwrite(fn, datum.cvOutputData)

        print("Body keypoints_(x,y):\n", keypoint_x_y_arr)
        # print(args[0])

        if not args[0].no_display:
            # cv2.imshow("OpenPose 1.7.0 - Tutorial Python API", datum.cvOutputData)
            key = cv2.waitKey(15)
            # 圖片跟圖片間會暫停，案任一件下一頁
            # key = cv2.waitKey(0)
            if key == 27: break

    end = time.time()
    print("OpenPose demo successfully finished. Total time: " + str(end - start) + " seconds")
    print("wrong_pic_fn_list:", wrong_pic_fn_list)
except Exception as e:
    print(e)
    sys.exit(-1)

