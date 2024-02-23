from keras.applications.imagenet_utils import preprocess_input
from keras.models import load_model
from keras.optimizers import SGD
import keras.backend as K

import os
import math
import cv2
import numpy as np

model_location = os.path.join('assets', 'models', 'rotnet_street_view_resnet50_keras2.hdf5')


class RotateCaptcha():
    def __init__(self):
        # 加载模型
        self.model = load_model(model_location, custom_objects={'angle_error': self.angle_error})
        self.model.compile(loss='categorical_crossentropy',
                           optimizer=SGD(lr=0.01, momentum=0.9),
                           metrics=[self.angle_error])
        # 图像长宽尺寸，勿改
        self.size = (224, 224)

    def showImg(self, image):
        '''
        展示图片
        '''
        cv2.imshow('image', image)
        cv2.waitKey(0)

    def getImgFromDisk(self, imgPath):
        image = cv2.imread(imgPath)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image

    def predictAngle(self, image):
        diameter = image.shape[0]  # 直径
        side_length = math.floor((diameter / 2) * 1.414)  # 圆内正方形最大边长
        cropped = math.floor((diameter - side_length) / 2)
        image = image[cropped:cropped + side_length, cropped:cropped + side_length]
        image = cv2.resize(image, self.size)

        image = np.expand_dims(image, axis=0)

        x = preprocess_input(image)
        y_pred = np.argmax(self.model.predict(x), axis=1)

        return y_pred[0]

    def rotate(self, image, angle):
        """
        Rotates an OpenCV 2 / NumPy image about it's centre by the given angle
        (in degrees). The returned image will be large enough to hold the entire
        new image, with a black background

        Source: http://stackoverflow.com/questions/16702966/rotate-image-and-crop-out-black-borders
        """
        # Get the image size
        # No that's not an error - NumPy stores image matricies backwards
        image_size = (image.shape[1], image.shape[0])
        image_center = tuple(np.array(image_size) / 2)

        # Convert the OpenCV 3x2 rotation matrix to 3x3
        rot_mat = np.vstack(
            [cv2.getRotationMatrix2D(image_center, angle, 1.0), [0, 0, 1]]
        )

        rot_mat_notranslate = np.matrix(rot_mat[0:2, 0:2])

        # Shorthand for below calcs
        image_w2 = image_size[0] * 0.5
        image_h2 = image_size[1] * 0.5

        # Obtain the rotated coordinates of the image corners
        rotated_coords = [
            (np.array([-image_w2, image_h2]) * rot_mat_notranslate).A[0],
            (np.array([image_w2, image_h2]) * rot_mat_notranslate).A[0],
            (np.array([-image_w2, -image_h2]) * rot_mat_notranslate).A[0],
            (np.array([image_w2, -image_h2]) * rot_mat_notranslate).A[0]
        ]

        # Find the size of the new image
        x_coords = [pt[0] for pt in rotated_coords]
        x_pos = [x for x in x_coords if x > 0]
        x_neg = [x for x in x_coords if x < 0]

        y_coords = [pt[1] for pt in rotated_coords]
        y_pos = [y for y in y_coords if y > 0]
        y_neg = [y for y in y_coords if y < 0]

        right_bound = max(x_pos)
        left_bound = min(x_neg)
        top_bound = max(y_pos)
        bot_bound = min(y_neg)

        new_w = int(abs(right_bound - left_bound))
        new_h = int(abs(top_bound - bot_bound))

        # We require a translation matrix to keep the image centred
        trans_mat = np.matrix([
            [1, 0, int(new_w * 0.5 - image_w2)],
            [0, 1, int(new_h * 0.5 - image_h2)],
            [0, 0, 1]
        ])

        # Compute the tranform for the combined rotation and translation
        affine_mat = (np.matrix(trans_mat) * np.matrix(rot_mat))[0:2, :]

        # Apply the transform
        result = cv2.warpAffine(
            image,
            affine_mat,
            (new_w, new_h),
            flags=cv2.INTER_LINEAR
        )

        return result

    def angle_difference(self, x, y):
        """
        Calculate minimum difference between two angles.
        """
        return 180 - abs(abs(x - y) - 180)

    def angle_error(self, y_true, y_pred):
        """
        Calculate the mean diference between the true angles
        and the predicted angles. Each angle is represented
        as a binary vector.
        """
        diff = self.angle_difference(K.argmax(y_true), K.argmax(y_pred))
        return K.mean(K.cast(K.abs(diff), K.floatx()))


