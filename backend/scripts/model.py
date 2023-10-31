import nibabel as nib
import numpy as np
import glob
from keras.layers import Input, Dense, Flatten, Dropout, Reshape, Conv2D, MaxPooling2D, UpSampling2D, Conv2DTranspose
from keras.layers import concatenate
from keras.layers import Activation
from tensorflow.keras.layers import BatchNormalization
from keras.models import Model,Sequential
from keras.callbacks import ModelCheckpoint
from keras.optimizers import Adadelta, RMSprop,SGD,Adam
from keras import regularizers
from keras import backend as K
class segmentation_model:
    def __init__(self):
        self.dice = None

    def three_to_two(self, path, label='FALSE'):
        ff = sorted(glob.glob(path))
        images =[]
        for f in range(len(ff)):
            a = nib.load(ff[f])
            a = a.get_fdata()
            for i in range(a.shape[2]):
                images.append(a[:,:,i])
        images = np.asarray(images)
        return images

    def min_max_norm(self, images):
        m = np.max(images)
        mi = np.min(images)
        images = (images - mi)/ (m - mi)
        return images

    def label_outliers(self, img_labels):
        img_labels[img_labels>1]=1
        img_labels[img_labels<0]=0
        return img_labels
    
    
    
    def conv_block(self, x_in, filters, batch_norm, kernel_size=(3,3)):
        x = Conv2D(filters, kernel_size, padding='same')(x_in)
        if batch_norm=='TRUE':
            x = BatchNormalization()(x)
        x = Activation('relu')(x)
        x = Conv2D(filters, kernel_size, padding='same')(x)
        if batch_norm=='TRUE':
            x = BatchNormalization()(x)
        x = BatchNormalization()(x)
        x = Activation('relu')(x)
        return x

    def conv_2d(self, x_in, filters, batch_norm, kernel_size=(3,3),acti ='relu'):
        x = Conv2D(filters, kernel_size, padding='same')(x_in)
        if batch_norm=='TRUE':
            x=BatchNormalization()(x)
        x= Activation(acti)(x)
        return x

    def pool(self, x_in, pool_size=(2, 2), type='Max'):
        if type=='Max':
            p = MaxPooling2D(pool_size)(x_in)
        return p

    def up(self, x_in, filters, merge, batch_norm, size=(2,2)):
        u = UpSampling2D(size)(x_in)
        conv = self.conv_block(u, filters, batch_norm)
        merge=concatenate([merge, conv],axis=-1)
        return merge

    def model(self, input_layer):
        conv1 = self.conv_block(input_layer, filters=16, batch_norm='TRUE')
        pool1 = self.pool(conv1)

        conv2 = self.conv_block(pool1, filters=32, batch_norm='TRUE')
        pool2 = self.pool(conv2)

        conv3 = self.conv_block(pool2, filters=32, batch_norm='TRUE')
        pool3 = self.pool(conv3)

        conv4 = self.conv_block(pool3, filters=64, batch_norm='TRUE')
        pool4 = self.pool(conv4)

        conv5 = self.conv_2d(pool4, filters=128, batch_norm='TRUE')

        up1 = self.up(conv5,filters=128, merge=conv4, batch_norm='TRUE')
        conv6 = self.conv_2d(up1, filters=128, batch_norm='TRUE')

        up2 = self.up(conv6, filters=128, merge=conv3, batch_norm='TRUE')
        conv7 = self.conv_2d(up2, filters=128, batch_norm='TRUE')

        up3 = self.up(conv7, filters=64, merge=conv2, batch_norm='TRUE')
        conv8 = self.conv_2d(up3, filters=64, batch_norm='TRUE')

        up4 = self.up(conv8, filters=32, merge=conv1, batch_norm='TRUE')
        conv9 = self.conv_2d(up4, filters=32, batch_norm='TRUE')

        conv10 = self.conv_2d(conv9, filters=1, batch_norm='FALSE', acti='sigmoid')

        output_layer = conv10
        model = Model(input_layer, output_layer)

        return model
    
    def preprocessing(self, path):
        img_test = self.three_to_two(path=path)
        x_test = self.min_max_norm(img_test)
        x_test = x_test[:,:,:,np.newaxis]
        return x_test

    
    def segmentation(self):
        path = "../images/file.nii.gz"
        x = self.preprocessing(path)
        print(x.shape)
        input_layer = Input(x.shape[1:])
        model = self.model(input_layer)
        model_weights = "../model/seg.h5"
        model.load_weights(model_weights)
        res = model.predict(x)
        return res

