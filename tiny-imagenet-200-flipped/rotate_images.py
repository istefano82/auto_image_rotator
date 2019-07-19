from pathlib import Path, PurePath
import os
from PIL import Image

IMAGE_DIR = Path(__file__).parent
print(IMAGE_DIR.resolve())

TRAIN_DIR = Path(IMAGE_DIR, 'train')
VAL_DIR = Path(IMAGE_DIR, 'val')
TEST_DIR = Path(IMAGE_DIR, 'test')


TRAIN_IMAGES = (file for file in os.listdir(TRAIN_DIR)
         if os.path.isfile(os.path.join(TRAIN_DIR, file)))
VAL_IMAGES = (file for file in os.listdir(VAL_DIR)
         if os.path.isfile(os.path.join(VAL_DIR, file)))
TEST_IMAGES = (file for file in os.listdir(TEST_DIR)
         if os.path.isfile(os.path.join(TEST_DIR, file)))


def rotate_images(image_list, image_dir):
    total_images = len(image_list)
    upright = {'images': image_list[:total_images // 4], 'angle': 0}
    left = {'images': image_list[total_images // 4 : total_images // 2],
            'angle': 90}
    upsidedown = {'images': image_list[total_images // 2: (total_images //
                                                              4) * 3],
                  'angle': 180}
    right = {'images':image_list[(total_images // 4) * 3: ], 'angle': 270}
    all_images = [upright, left, right, upsidedown]
    for image_type in all_images:
        print(image_type['angle'], len(image_type['images']))
        # assert len(image_type['images']) == total_images // 4

    for image_rotation_type in all_images:
        rotate_image_from_angle(image_rotation_type['images'],
                                image_rotation_type['angle'],
                                image_dir)



def rotate_image_from_angle(images, angle, base_dir):
    '''Rotates image upright based on it current direction.'''
    save_dir_angle_mapping = {0: 'upright', 90: 'left', 180: 'upsidedown',
                              270: 'right'}
    for image in images:
        img_path = Path(base_dir, image)
        img = Image.open(img_path)
        out = img.rotate(angle, expand=True)
        try:
            os.mkdir(Path(base_dir, save_dir_angle_mapping[angle]), )
        except:
            pass
        save_path = Path(base_dir, save_dir_angle_mapping[angle], image)
        out.save(save_path)

if __name__ == '__main__':
    rotate_images(list(TRAIN_IMAGES), TRAIN_DIR)
    rotate_images(list(VAL_IMAGES), VAL_DIR)
    rotate_images(list(TEST_IMAGES), TEST_DIR)
