"""The estimator which is compare images not machine learing
"""
import os
from collections import Counter
from functools import lru_cache
from operator import itemgetter as ig
from pprint import pformat

from future.utils import lfilter, lmap
from itertools import product
from nose.tools import assert_equal

from foxylib.native.builtin_tools import lzip_strict, izip_strict
from foxylib.native.collections_tools import l_singleton2obj
from foxylib.native.file_tools import filepath2utf8_readline
from foxylib.native.logger_tools import LoggerToolkit
from foxylib.pillow.pillow_tools import PillowToolkit
from src.uwo_ps_app.towns_table import TOWNS_TABLE

FILE_PATH = os.path.abspath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)
PACKAGE_DIR = FILE_DIR
PROJECT_DIR = os.path.dirname(PACKAGE_DIR)
RESOURCES_DIR = os.path.join(PROJECT_DIR, "resources")


class MarketRateExtractor:
    FILEPATH_GOODS_PNG = os.path.join(RESOURCES_DIR, "goods.png")
    FILEPATH_GOODS_LABELS = os.path.join(RESOURCES_DIR, "goods.labels")
    FILEPATH_TOWNS_PNG = os.path.join(RESOURCES_DIR, "towns.png")
    FILEPATH_TOWNS_LABELS = os.path.join(RESOURCES_DIR, "towns.labels")
    FILEPATH_RATES_PNG = os.path.join(RESOURCES_DIR, "rates.png")
    FILEPATH_RATES_LABELS = os.path.join(RESOURCES_DIR, "rates.labels")
    FILEPATH_ARROWS_PNG = os.path.join(RESOURCES_DIR, "arrows.png")
    FILEPATH_ARROWS_LABELS = os.path.join(RESOURCES_DIR, "arrows.labels")

    RGB_FRAME = (179, 179, 179,)

    ARROW_PIXEL_XY = (7, 7)
    ARROW_RGB_LIST = [(225, 129, 38), (160, 227, 37), (30, 227, 200)]

    GOODS_RESIZE = (8, 4)

    # IMGSIZE_TRADEGOOD = [38, 24]
    IMGSIZE_TRADEGOOD = [42, 24]
    IMGSIZE_TOWN = [64, 15]
    IMGSIZE_RATE_NUMBER = [26, 13]
    IMGSIZE_ARROW = [13, 13]
    IMGSIZE_RATE_BAR = [190, 1]



    @classmethod
    def filepath2label_list(cls, filepath):
        return list(filepath2utf8_readline(filepath))

    @classmethod
    def img2bytes_list(cls, img, img_count):

        assert_equal(img.height % img_count, 0, pformat({"img.height":img.height, "img_count":img_count,}))

        h_SINGLE = img.height // img_count

        l = []
        for i in range(img_count):
            img_SINGLE = img.crop([0, i * h_SINGLE, img.width, (i + 1) * h_SINGLE])
            l.append(img_SINGLE.tobytes())
            img_SINGLE.close()
        return l

    @classmethod
    def imgdata2name(cls, imgdata):
        return imgdata[0]

    @classmethod
    def imgdata2bytes(cls, imgdata):
        return imgdata[1]

    class NoMatchException(Exception):
        pass

    @classmethod
    def img2name(cls, img, imgdata_list):
        bytes_IMG = img.tobytes()
        # data = im.resize(self.GOODS_RESIZE).tobytes()

        count = len(imgdata_list)
        iList_MATCHED = lfilter(lambda i: cls.imgdata2bytes(imgdata_list[i]) == bytes_IMG, range(count))
        if not iList_MATCHED: return None

        iMATCHED = l_singleton2obj(iList_MATCHED)
        name = cls.imgdata2name(imgdata_list[iMATCHED])
        return name

    @classmethod
    @lru_cache(maxsize=2)
    def imgdata_list_TRADEGOOD(cls):
        name_list = cls.filepath2label_list(cls.FILEPATH_GOODS_LABELS)

        img_TGs = PillowToolkit.filepath2img(cls.FILEPATH_GOODS_PNG)
        bytes_list = cls.img2bytes_list(img_TGs, len(name_list))
        return lzip_strict(name_list, bytes_list)

    @classmethod
    def filter_white(cls, c):
        return c if c==255 else 0


    @classmethod
    @lru_cache(maxsize=2)
    def imgdata_list_TOWN(cls):
        name_list = cls.filepath2label_list(cls.FILEPATH_TOWNS_LABELS)

        img_TOWNs = PillowToolkit.filepath2img(cls.FILEPATH_TOWNS_PNG)

        bytes_list = cls.img2bytes_list(img_TOWNs.point(cls.filter_white), len(name_list))
        return lzip_strict(name_list, bytes_list)

    @classmethod
    @lru_cache(maxsize=2)
    def label_list_TREND(cls):
        name_list = cls.filepath2label_list(cls.FILEPATH_ARROWS_LABELS)
        return name_list


    # @classmethod
    # def image_size2tradegood_point(cls, image_size):
    #     w_IMG, h_IMG = image_size
    #
    #     l_MATCH_EXACT = lfilter(lambda size: abs(size[0] - w_IMG) <= 5 and abs(size[1] - h_IMG) <= 5, cls.SIZE_LIST)
    #     if l_MATCH_EXACT:
    #         assert_equal(len(l_MATCH_EXACT), 1, msg=l_MATCH_EXACT)
    #         w_MATCH, h_MATCH = l_singleton2obj(l_MATCH_EXACT)
    #         p_MATCH = cls._image_size2tradegood_point((w_IMG, h_IMG))
    #         return p_MATCH
    #
    #     l_MATCH_FUZZY = lfilter(lambda size: 0 <= w_IMG - size[0] <= 50 and 20 <= h_IMG - size[1] <= 50, cls.SIZE_LIST)
    #     if not l_MATCH_FUZZY:
    #         raise cls.InvalidScreenSizeException(image_size)
    #
    #     assert_equal(len(l_MATCH_FUZZY), 1, msg=l_MATCH_FUZZY)
    #     w_FUZZY, h_FUZZY = l_singleton2obj(l_MATCH_FUZZY)
    #     (x_FUZZY, y_FUZZY) = cls._image_size2tradegood_point((w_FUZZY, h_FUZZY))
    #     p_FUZZY = (x, y) = (x_FUZZY, y_FUZZY + h_IMG - h_FUZZY)
    #     return p_FUZZY

    PHOTOFRAME_LENGTH = 48

    @classmethod
    def xy_list2photoframe_point_list(cls, xy_list):
        c_X = Counter(map(ig(0), xy_list))
        x_list = [x for x, n in c_X.most_common() if n >= cls.PHOTOFRAME_LENGTH]

        c_Y = Counter(map(ig(1), xy_list))
        y_list = [y for y, n in c_Y.most_common() if n >= cls.PHOTOFRAME_LENGTH]

        def p2is_topleft(p_IN):
            x, y = p_IN
            p_set = set([p
                         for i in range(cls.PHOTOFRAME_LENGTH)
                         for p in [(x + i, y), (x, y + i), (x + cls.PHOTOFRAME_LENGTH - 1, y + i),
                                   (x + i, y + cls.PHOTOFRAME_LENGTH - 1)]]
                        )
            return p_set <= set(xy_list)

        p_list = lfilter(p2is_topleft, product(x_list, y_list))
        p_list_OUT = sorted(p_list, key=lambda p: (p[0], p[1]))
        return p_list_OUT

    PHOTOFRAME_WIDTH = 1
    TRADEGOOD_OFFSET = 2
    @classmethod
    def filepath2marketplace_data(cls, filepath):
        logger = LoggerToolkit.f_class2logger(cls.filepath2marketplace_data)
        logger.info({"filepath": filepath})

        img = PillowToolkit.filepath2img(filepath)
        rgb_ll = PillowToolkit.img2rgb_ll(img)
        xy_list = PillowToolkit.rgb_ll_rgb2xy_list(rgb_ll, cls.RGB_FRAME)
        photoframe_point_list = cls.xy_list2photoframe_point_list(xy_list)

        photoframe_point_TG = photoframe_point_list[0]
        photoframe_point_TOWN_list = photoframe_point_list[1:]

        offset = cls.PHOTOFRAME_WIDTH + cls.TRADEGOOD_OFFSET
        name_TG = cls.img_point2name_TG(img,photoframe_point_TG)
        name_TOWN_list = [cls.img_point2name_TOWN(img, photoframe_point_TOWN)
                          for photoframe_point_TOWN in photoframe_point_TOWN_list]

        rate_list = [cls.img_point2rate(img, photoframe_point)
                     for photoframe_point in photoframe_point_list]

        trend_list = [cls.img_point2trend(img, photoframe_point)
                          for photoframe_point in photoframe_point_list]

        town = cls.neighbors2town(tuple(name_TOWN_list))
        town_list_ALL = [town] + name_TOWN_list

        return (name_TG,
                town_list_ALL,
                rate_list,
                trend_list,
                )

    @classmethod
    def marketplace_data2ptgs_data_list(cls, marketplace_data):
        (name_TG, town_list, rate_list, trend_list,) = marketplace_data

        l = [(name_TG, town, rate, trend)
             for town, rate, trend in izip_strict(town_list, rate_list, trend_list)]
        return l

    @classmethod
    def img_point2name_TG(cls, img, photoframe_point_TG,):
        offset = cls.PHOTOFRAME_WIDTH + cls.TRADEGOOD_OFFSET
        img_TG = img.crop(
            PillowToolkit.point_size2bounds(lmap(lambda x: x + offset, photoframe_point_TG), cls.IMGSIZE_TRADEGOOD))
        name_TG = cls.img2name(img_TG, cls.imgdata_list_TRADEGOOD())
        return name_TG

    @classmethod
    def img_point2name_TOWN(cls, img, photoframe_point_TOWN):
        offset = (52, 6)
        p = PillowToolkit.point_offset2move(photoframe_point_TOWN, offset)

        img_TOWN = img.crop(PillowToolkit.point_size2bounds(p, cls.IMGSIZE_TOWN))
        name_TOWN = cls.img2name(img_TOWN.point(cls.filter_white), cls.imgdata_list_TOWN())
        return name_TOWN

    @classmethod
    def neighbors2town(cls, neighbors):
        return TOWNS_TABLE.get(tuple(neighbors))


    # @classmethod
    # def img2name_TG(cls, point):
    #     data = im.resize(self.GOODS_RESIZE).tobytes()
    #     try:
    #         name = self.goods_labels[self.goods_data.index(data)]
    #     except:
    #         name = "WhatIsThis"
    #     finally:
    #         return name

    @classmethod
    def rgb_ll2tradegood_point(cls, rgb_ll):

        xy_list = PillowToolkit.rgb_ll_rgb2xy_list(rgb_ll, cls.RGB_FRAME)
        photoframe_point_list = cls.xy_list2photoframe_point_list(xy_list)
        return photoframe_point_list[0]

    @classmethod
    def pixel2has_saturation(cls, pixel):
        #_, rgb = pixels
        return any([pixel[0] >= 75,
                    pixel[1] >= 75,
                    pixel[2] >= 75,
                    ])


    @classmethod
    def img_point2rate(cls, img, photoframe_point):
        offset = (53, 44)
        p = PillowToolkit.point_offset2move(photoframe_point, offset)
        img_RATE_BAR = img.crop(PillowToolkit.point_size2bounds(p, cls.IMGSIZE_RATE_BAR))

        n_pixel_list_WITH_COLOR = lfilter(lambda n_pixel: cls.pixel2has_saturation(n_pixel[1]), img_RATE_BAR.getcolors())
        count, pixel = l_singleton2obj(n_pixel_list_WITH_COLOR)
        rate = count*2+6
        return rate


    # @classmethod
    # def n_pixel_list2count_COLOR(cls, n_pixel_list, pivot_color):
    #
    #     count_COLOR = 0
    #     for n,pixel in n_pixel_list:
    #         PillowToolkit.rgb_pair2dist_squared(pixel, pivot_color) <

    ARROW_PIXEL_XY = (7,7)
    @classmethod
    def img_point2trend(cls, img, photoframe_point):
        offset = (228, 28)
        p = PillowToolkit.point_offset2move(photoframe_point, offset)
        img_ARROW = img.crop(PillowToolkit.point_size2bounds(p, cls.IMGSIZE_ARROW))
        PillowToolkit.img2file(img_ARROW, "/home/yerihyo/tmp/a.png")

        pixel = img_ARROW.getpixel(cls.ARROW_PIXEL_XY)

        trend_count = len(cls.ARROW_RGB_LIST)
        iTrend = min(range(trend_count),
                     key=lambda i:PillowToolkit.rgb_pair2dist_squared(cls.ARROW_RGB_LIST[i],pixel))


        str_TREND = cls.label_list_TREND()[iTrend]
        return str_TREND

    @classmethod
    def rgb2count_nearby(cls, rgb, n_pixel_list,):
        dist_thres = 3

        n_SUM = 0
        for n,pixel in n_pixel_list:
            if PillowToolkit.rgb_pair2dist_squared(rgb,pixel)<=dist_thres**2:
                continue
            n_SUM += n

        return n_SUM
