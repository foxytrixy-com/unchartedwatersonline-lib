"""The estimator which is compare images not machine learing
"""
import os
from collections import Counter
from functools import lru_cache
from itertools import product
from operator import itemgetter as ig

from PIL import Image
from future.utils import lfilter, lmap
from nose.tools import assert_equal

from foxlib.toolkits.builtin_toolkit import lzip_strict
from foxlib.toolkits.collections_toolkit import l_singleton2obj
from foxlib.toolkits.file_toolkit import filepath2utf8_readline
from foxlib.toolkits.logger_toolkit import LoggerToolkit
from uwo_ps_utils import market_rates_cropper as mrc
from uwo_ps_utils.market_rates_cropper import PillowToolkit

FILE_PATH = os.path.abspath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)
PACKAGE_DIR = FILE_DIR
PROJECT_DIR = os.path.dirname(PACKAGE_DIR)
RESOURCES_DIR = os.path.join(PROJECT_DIR,"resources")

class ImageCompareEstimator:
    FILEPATH_GOODS_PNG = os.path.join(RESOURCES_DIR,"goods.png")
    FILEPATH_GOODS_LABELS = os.path.join(RESOURCES_DIR, "goods.labels")
    FILEPATH_TOWNS_PNG = os.path.join(RESOURCES_DIR, "towns.png")
    FILEPATH_TOWNS_LABELS = os.path.join(RESOURCES_DIR, "towns.labels")
    FILEPATH_RATES_PNG = os.path.join(RESOURCES_DIR, "rates.png")
    FILEPATH_RATES_LABELS = os.path.join(RESOURCES_DIR, "rates.labels")
    FILEPATH_ARROWS_PNG = os.path.join(RESOURCES_DIR, "arrows.png")
    FILEPATH_ARROWS_LABELS = os.path.join(RESOURCES_DIR, "arrows.labels")

    RGB_FRAME = (179,179,179,)



    ARROW_PIXEL_XY = (7, 7)
    ARROW_RGB = [(225, 129, 38), (160, 227, 37), (30, 227, 200)]

    GOODS_RESIZE = (8, 4)

    # def __init__(self, inputs):
    #     """
    #     Arguments:
    #         inputs : list of tuples which are pairs of paths.
    #             [0]: (goods_data, goods_label)
    #             [1]: (towns_data, towns_label)
    #             [2]: (rates_data, rates_label) - this is not used
    #             [3]: (arrows_data, arrows_label) - "arrows_data" is not used
    #     """
    #     self.goods_labels = open(inputs[0][1]).read().splitlines()
    #     self.goods_data = self.__load_goods_data(inputs[0][0])
    #     self.towns_labels = open(inputs[1][1]).read().splitlines()
    #     self.towns_data = self.__load_towns_data(inputs[1][0])
    #     self.arrows_labels = open(inputs[3][1]).read().splitlines()

    @classmethod
    def filepath2label_list(cls, filepath):
        return list(filepath2utf8_readline(filepath))

    @classmethod
    def filepath2bytes_list(cls, filepath, img_count):

        with Image.open(filepath) as img:
            assert_equal(img.height % img_count, 0)

            h_SINGLE = img.height // img_count

            l = []
            for i in range(img_count):
                img_SINGLE = img.crop([0, i * h_SINGLE, img.width, (i + 1) * h_SINGLE])
                l.append(img_SINGLE.tobytes())
                img_SINGLE.close()
            return l

    @classmethod
    def imgdata2name(cls, imgdata): return imgdata[0]
    @classmethod
    def imgdata2bytes(cls, imgdata): return imgdata[1]

    class NoMatchException(Exception): pass
    @classmethod
    def img2name(cls, img, imgdata_list):
        bytes_IMG = img.tobytes()
        #data = im.resize(self.GOODS_RESIZE).tobytes()

        count = len(imgdata_list)
        iList_MATCHED = lfilter(lambda i:cls.imgdata2bytes(imgdata_list[i])==bytes_IMG,range(count))
        if not iList_MATCHED: return None

        iMATCHED = l_singleton2obj(iList_MATCHED)
        name = cls.imgdata2name(imgdata_list[iMATCHED])
        return name

    @classmethod
    @lru_cache(maxsize=2)
    def imgdata_list_GOODS(cls):
        name_list = cls.filepath2label_list(cls.FILEPATH_GOODS_LABELS)
        bytes_list = cls.filepath2bytes_list(cls.FILEPATH_GOODS_PNG)
        return lzip_strict(name_list, bytes_list)

    @classmethod
    @lru_cache(maxsize=2)
    def imgdata_list_TOWNS(cls):
        name_list = cls.filepath2label_list(cls.FILEPATH_TOWNS_LABELS)
        bytes_list = cls.filepath2bytes_list(cls.FILEPATH_TOWNS_PNG)
        return lzip_strict(name_list, bytes_list)

    @classmethod
    def image_size2tradegood_point(cls, image_size):
        w_IMG, h_IMG = image_size

        l_MATCH_EXACT = lfilter(lambda size: abs(size[0] - w_IMG) <= 5 and abs(size[1] - h_IMG) <= 5, cls.SIZE_LIST)
        if l_MATCH_EXACT:
            assert_equal(len(l_MATCH_EXACT), 1, msg=l_MATCH_EXACT)
            w_MATCH, h_MATCH = l_singleton2obj(l_MATCH_EXACT)
            p_MATCH = cls._image_size2tradegood_point((w_IMG, h_IMG))
            return p_MATCH

        l_MATCH_FUZZY = lfilter(lambda size: 0 <= w_IMG - size[0] <= 50 and 20 <= h_IMG - size[1] <= 50, cls.SIZE_LIST)
        if not l_MATCH_FUZZY:
            raise cls.InvalidScreenSizeException(image_size)

        assert_equal(len(l_MATCH_FUZZY), 1, msg=l_MATCH_FUZZY)
        w_FUZZY, h_FUZZY = l_singleton2obj(l_MATCH_FUZZY)
        (x_FUZZY, y_FUZZY) = cls._image_size2tradegood_point((w_FUZZY, h_FUZZY))
        p_FUZZY = (x, y) = (x_FUZZY, y_FUZZY + h_IMG - h_FUZZY)
        return p_FUZZY

    PHOTOFRAME_LENGTH = 48
    @classmethod
    def xy_list2photoframe_point_list(cls, xy_list):
        c_X = Counter(map(ig(0), xy_list))
        x_list = [x for x,n in c_X.most_common() if n >= cls.PHOTOFRAME_LENGTH]

        c_Y = Counter(map(ig(1), xy_list))
        y_list = [y for y, n in c_Y.most_common() if n >= cls.PHOTOFRAME_LENGTH]

        def p2is_topleft(p_IN):
            x,y = p_IN
            p_set = set([p
                         for i in range(cls.PHOTOFRAME_LENGTH)
                         for p in [(x+i,y), (x,y+i), (x+cls.PHOTOFRAME_LENGTH-1,y+i), (x+i,y+cls.PHOTOFRAME_LENGTH-1)]]
                        )
            return p_set <= set(xy_list)

        p_list = lfilter(p2is_topleft, product(x_list,y_list))
        p_list_OUT = sorted(p_list, key=lambda p:(p[0],p[1]))
        return p_list_OUT
        
    @classmethod
    def filepath2rates(cls, filepath):
        img = PillowToolkit.filepath2img(filepath)
        rgb_ll = PillowToolkit.img2rgb_ll(img)
        xy_list = PillowToolkit.rgb_ll_rgb2xy_list(rgb_ll, cls.RGB_FRAME)
        photoframe_point_list = cls.xy_list2photoframe_point_list(xy_list)

        tg_point = photoframe_point_list[0]
        town_point_list = photoframe_point_list[1:]

    @classmethod
    def rgb_ll2tradegood_point(cls, rgb_ll):

        xy_list = PillowToolkit.rgb_ll_rgb2xy_list(rgb_ll, cls.RGB_FRAME)
        photoframe_point_list = cls.xy_list2photoframe_point_list(xy_list)
        return photoframe_point_list[0]

        # l_MATCH_EXACT = lfilter(lambda size: abs(size[0] - w_IMG) <= 5 and abs(size[1] - h_IMG) <= 5, cls.SIZE_LIST)
        # if l_MATCH_EXACT:
        #     assert_equal(len(l_MATCH_EXACT), 1, msg=l_MATCH_EXACT)
        #     w_MATCH, h_MATCH = l_singleton2obj(l_MATCH_EXACT)
        #     p_MATCH = cls._image_size2tradegood_point((w_IMG, h_IMG))
        #     return p_MATCH
        #
        # l_MATCH_FUZZY = lfilter(lambda size: 0 <= w_IMG - size[0] <= 50 and 20 <= h_IMG - size[1] <= 50, cls.SIZE_LIST)
        # if not l_MATCH_FUZZY:
        #     raise cls.InvalidScreenSizeException(image_size)
        #
        # assert_equal(len(l_MATCH_FUZZY), 1, msg=l_MATCH_FUZZY)
        # w_FUZZY, h_FUZZY = l_singleton2obj(l_MATCH_FUZZY)
        # (x_FUZZY, y_FUZZY) = cls._image_size2tradegood_point((w_FUZZY, h_FUZZY))
        # p_FUZZY = (x, y) = (x_FUZZY, y_FUZZY + h_IMG - h_FUZZY)
        # return p_FUZZY


    # def __load_goods_data(self, imgpath):
    #     length = len(self.goods_labels)
    #     im = Image.open(imgpath)
    #     h = int(im.height / length)
    #     data = []
    #
    #     for i in range(length):
    #         goods_im = im.crop([0, i * h, im.width, (i + 1) * h])
    #         data.append(goods_im.resize(self.GOODS_RESIZE).tobytes())
    #         goods_im.close()
    #     im.close()
    #
    #     return data
    #
    # def __load_towns_data(self, imgpath):
    #     length = len(self.towns_labels)
    #     im = Image.open(imgpath).point(self.__clear_except_white)
    #     h = int(im.height / length)
    #     data = []
    #
    #     for i in range(length):
    #         goods_im = im.crop([0, i * h, im.width, (i + 1) * h])
    #         data.append(goods_im.tobytes())
    #         goods_im.close()
    #     im.close()
    #
    #     return data

    def __clear_except_white(self, c):
        return int(c / 250) * 255

    def estimate(self, path):
        logger = LoggerToolkit.f_class2logger(self.estimate)
        logger.info({"path": path})

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

        goods_cell = mrc.get_selected_goods_cell_image(im)
        goods_imgs = mrc.get_images_from_goods_cell(goods_cell)
        goods = self.__estimate_goods(goods_imgs[0])
        rates = self.__estimate_rates(goods_imgs[3])
        arrows = self.__estimate_arrows(goods_imgs[2])
        result = [(goods, rates, arrows)]
        # except:
        #     return []

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

    @classmethod
    def filepath2estimate(cls, filepath):
        logger = LoggerToolkit.f_class2logger(cls.filepath2estimate)
        logger.info({"filepath": filepath})

        img = PillowToolkit.filepath2img(filepath)


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
        #im = Image.open(path)

        goods_cell = mrc.get_selected_goods_cell_image(im)
        goods_imgs = mrc.get_images_from_goods_cell(goods_cell)
        goods = self.__estimate_goods(goods_imgs[0])
        rates = self.__estimate_rates(goods_imgs[3])
        arrows = self.__estimate_arrows(goods_imgs[2])
        result = [(goods, rates, arrows)]
        # except:
        #     return []

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
