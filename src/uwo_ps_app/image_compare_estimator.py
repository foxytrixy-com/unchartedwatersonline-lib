"""The estimator which is compare images not machine learing
"""
import os

from PIL import Image

from uwo_ps_utils import market_rates_cropper as mrc

class ImageCompareEstimator:
    ARROW_PIXEL_XY = (7, 7)
    ARROW_RGB = [(225, 129, 38), (160, 227, 37), (30, 227, 200)]

    GOODS_RESIZE = (8, 4)

    def __init__(self, inputs):
        """
        Arguments:
            inputs : list of tuples which are pairs of paths.
                [0]: (goods_data, goods_label)
                [1]: (towns_data, towns_label)
                [2]: (rates_data, rates_label) - this is not used
                [3]: (arrows_data, arrows_label) - "arrows_data" is not used
        """
        self.goods_labels = open(inputs[0][1]).read().splitlines()
        self.goods_data = self.__load_goods_data(inputs[0][0])
        self.towns_labels = open(inputs[1][1]).read().splitlines()
        self.towns_data = self.__load_towns_data(inputs[1][0])
        self.arrows_labels = open(inputs[3][1]).read().splitlines()

    def __load_goods_data(self, imgpath):
        length = len(self.goods_labels)
        im = Image.open(imgpath)
        h = int(im.height / length)
        data = []

        for i in range(length):
            goods_im = im.crop([0, i * h, im.width, (i + 1) * h])
            data.append(goods_im.resize(self.GOODS_RESIZE).tobytes())
            goods_im.close()
        im.close()

        return data

    def __load_towns_data(self, imgpath):
        length = len(self.towns_labels)
        im = Image.open(imgpath).point(self.__clear_except_white)
        h = int(im.height / length)
        data = []

        for i in range(length):
            goods_im = im.crop([0, i * h, im.width, (i + 1) * h])
            data.append(goods_im.tobytes())
            goods_im.close()
        im.close()

        return data

    def __clear_except_white(self, c):
        return int(c / 250) * 255

    def estimate(self, path):
        """Estimation function.

        Arguments:
            path (str): Image file path to estimate

        Returns:
            Labels which are estimated
                [0] = (goods_label, rates, arrows)
                [1] = (nearby town1, rates, arrows)
                    ~
                [5] = (nearby town5, rates, arrows)
        """
        im = Image.open(path)
        try:
            goods_cell = mrc.get_selected_goods_cell_image(im)
            goods_imgs = mrc.get_images_from_goods_cell(goods_cell)
            goods = self.__estimate_goods(goods_imgs[0])
            rates = self.__estimate_rates(goods_imgs[3])
            arrows = self.__estimate_arrows(goods_imgs[2])
            result = [(goods, rates, arrows)]
        except:
            return []

        nearby_cells = mrc.get_nearby_towns_cell_images(im)
        for cell in nearby_cells:
            try:
                imgs = mrc.get_images_from_nearby_cell(cell)
                towns = self.__estimate_towns(imgs[0])
                rates = self.__estimate_rates(imgs[3])
                arrows = self.__estimate_arrows(imgs[2])
                result += [(towns, rates, arrows)]
            except:
                continue

        return result

    def __estimate_goods(self, im):
        data = im.resize(self.GOODS_RESIZE).tobytes()
        try:
            name = self.goods_labels[self.goods_data.index(data)]
        except:
            name = "WhatIsThis"
        finally:
            return name

    def __estimate_rates(self, im):
        count, _ = list(filter(self.__colored_pixel, im.getcolors()))[0]
        return str(int(count * 2.13))

    def __colored_pixel(self, pixels):
        _, rgb = pixels
        return not (rgb[0] < 75 and rgb[1] < 75 and rgb[2] < 75)

    def __estimate_arrows(self, im):
        pixel = im.getpixel(self.ARROW_PIXEL_XY)
        diffs = []
        for rgb in self.ARROW_RGB:
            diffs += [self.__get_rgb_diff(pixel, rgb)]

        return self.arrows_labels[diffs.index(min(diffs))]

    def __get_rgb_diff(self, px1, px2):
        diff = 0
        for i in range(3):
            diff += (px1[i] - px2[i]) ** 2
        return diff

    def __estimate_towns(self, im):
        data = im.point(self.__clear_except_white).tobytes()
        try:
            name = self.towns_labels[self.towns_data.index(data)]
        except:
            name = "UNKNOWN"
        finally:
            return name
