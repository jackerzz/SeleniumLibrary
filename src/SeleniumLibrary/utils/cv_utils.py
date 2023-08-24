# -*- coding: utf-8 -*-

import time
import os
import base64
from robot.api import logger
from airtest.core.helper import G
from airtest import aircv
from airtest.aircv import get_resolution
from airtest.core.error import TargetNotFoundError
from airtest.core.settings import Settings as ST


class Scroll:
    def __init__(self, driver):
        self.cls = driver

    def scroll(self, x, y):
        """
        移动x,y距离(以 0,0)为坐标
        :param x:
        :param y:
        :return:
        """
        script = f"window.scroll({x},{y})"
        self.cls.execute_script(script)

    def scroll_to_bottom(self):
        """
        移动到底部
        :return:
        """
        full_screen_height = "document.documentElement.scrollHeight"
        script = f"window.scroll(0, {full_screen_height})"
        self.cls.execute_script(script)

    def scroll_to_top(self):
        """
        回到顶部
        :return:
        """
        script = "window.scroll(0, 0)"
        self.cls.execute_script(script)

    def scroll_to_element_top(self, element):
        """
        滑动至顶部对齐
        :param element:
        :return:
        """
        var = element.location_once_scrolled_into_view

    def scroll_to_element_center(self, element):
        """
        滑动至中间对齐
        :param element:
        :return:
        """
        self.cls.execute_script('arguments[0].scrollIntoView({block: "center"})', element)

    def scroll_to_element_bottom(self, element):
        """
        滑动至底部对齐
        :return:
        """
        self.cls.execute_script('arguments[0].scrollIntoView(false)', element)

    def scroll_SlideBar(self):
        self.cls.execute_script("document.querySelector(’.san-sheet’).scrollTo(0,500)")

def loop_find(query,img_pth, driver=None, timeout=10, threshold=None, interval=0.5, intervalfunc=None):
    start_time = time.time()
    while True:
        screen = driver.screenshot()
        query.resolution = get_resolution(screen)
        if screen is None:
            print("Screen is None, may be locked")
        else:
            if threshold:
                query.threshold = threshold
            match_pos = query.match_in(screen)
            if match_pos:
                # try_log_screen(img_pth)
                return match_pos

        if intervalfunc is not None:
            intervalfunc()

        # 超时则raise，未超时则进行下次循环:
        if (time.time() - start_time) > timeout:
            try_log_screen(img_pth)
            raise TargetNotFoundError('Picture %s not found in screen' % query)
        else:
            time.sleep(interval)

# def try_log_screen(screen=None,img_pth=None):
#     if not ST.LOG_DIR:
#         return
#     if screen is None:
#         screen = G.DEVICE.snapshot()
#     filename = "%(time)d.jpg" % {'time': time.time() * 1000}
#     filepath = os.path.join(ST.LOG_DIR, filename)
#     aircv.imwrite(filepath, screen)
#     return filename

def try_log_screen( img_pth):
    logger.info(
            '</td></tr><tr><td colspan="3">'
            '<img alt="screenshot" class="tag_path" '
            f'src="data:image/png;base64,{base64.b64encode(open(img_pth, "rb").read()).decode()}" width="100px">',
            html=True,
    )

def loop_find_pro(query, img_pth, driver=None, timeout=10, threshold=None, interval=0.5, intervalfunc=None, screen=None):
    '''
    :param query:
    :param driver:
    :param timeout:
    :param threshold:
    :param interval:
    :param intervalfunc:
    :param screen:
    :return:
    '''
    start_time = time.time()
    while True:
        query.resolution = get_resolution(screen)
        if screen is None:
            print("Screen is None, may be locked")
        else:
            if threshold:
                query.threshold = threshold
            match_pos = query.match_in(screen)
            if match_pos:
                # try_log_screen(img_pth)
                return match_pos

        if intervalfunc is not None:
            intervalfunc()

        # 超时则raise，未超时则进行下次循环:
        if (time.time() - start_time) > timeout:
            try_log_screen(img_pth)
            raise TargetNotFoundError('Picture %s not found in screen' % query)
        else:
            time.sleep(interval)
