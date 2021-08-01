#package add pillow
from PIL import Image
import os
from PIL import ImageFile
# 解決圖片檔案過大的問題
ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None

# original_pics_paths
opps = "D:/tt_groupxxxxx/0519xxxxx/0519_xxxxxxx_pics/"
fn_type_list = os.listdir(opps)

# fn_list
pics_fn_list = []
for fn_type in fn_type_list:
    pics_fn = fn_type.split(".")[0]
    pics_fn_list.append(pics_fn)
# print(pics_fn_list)

count = 1
# resize pics and save pics
for pic_fn in pics_fn_list:

    # image.opem(你的路徑)
    img = Image.open("D:/tt_xxxxx/0516xxxxxx/0516_xxxx/" + pic_fn + ".jpg")
    (w, h) = img.size
    # print('w=%d, h=%d', w, h)
    # img.show()

    new_img = img.resize((256, 256))
    # new_img.show()
    # fn_list.zfill()自動補0

    new_img.save("D:/tt_groupxxxxx/0519_xxxx/0519_xxxxxx/"+ pic_fn.zfill(4) + ".jpg")
    print("第", count ,"張")
    count += 1
print("resize finish")
