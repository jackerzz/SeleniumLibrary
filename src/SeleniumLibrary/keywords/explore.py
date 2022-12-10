import os
import base64
import time
import cv2
from pynput.keyboard import Key
from pynput.mouse import Button

from airtest.core.settings import Settings as ST
from airtest import aircv


from airtest.aircv import get_resolution
from airtest.core.error import TargetNotFoundError
from airtest.core.cv import Template

from robot.utils import get_link_path
from selenium.webdriver import ActionChains
from SeleniumLibrary.base import LibraryComponent, keyword
from SeleniumLibrary.utils.cv_utils import Scroll
from SeleniumLibrary.utils.cv_utils import loop_find, loop_find_pro
import pyautogui

class ExploreLearn(LibraryComponent):

    @keyword
    def click_close(self):
        buttonx,buttony=pyautogui.locateCenterOnScreen('D:\\number_smart\\test_bi\\tag\\reportlist\\305.png') #寻找图片
        pyautogui.click(buttonx,buttony)
        print(buttonx,buttony)

    @keyword
    def upload_file(self,filepath):
        pyautogui.write(filepath)
        time.sleep(2)
        pyautogui.press('enter',2)

    @keyword
    def switch_windows(self,index):
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[index])

    @keyword
    def mouse_drag(self,img_pth, threshold, rgb, dx,dy,file_path=None):
        v = Template(img_pth, threshold=threshold, rgb=rgb)
        if isinstance(v, Template):
            _pos = loop_find(v, timeout=ST.FIND_TIMEOUT, driver=self)
        else:
            _pos = v
        x, y = _pos
        pos = self._get_left_up_offset()
        pos = (pos[0] + x, pos[1] + y)
        self._move_to_pos(pos)
        if file_path:
            self.screenshot(file_path, _pos)
        pyautogui.moveTo(x,y,0.1)
        pyautogui.dragTo(dx,dy,2,pyautogui.easeOutQuad)

    @keyword
    def mouse_move(self,img_pth, threshold, rgb, dx,dy,file_path=None):
        '''
        支持通过鼠标点击目标，动滑动至制定位置
        仅支持：线性的滑动，
        扩展：多条，短的线性滑动，实现非线性的滑动
        '''
        v = Template(img_pth, threshold=threshold, rgb=rgb)
        if isinstance(v, Template):
            _pos = loop_find(v, timeout=ST.FIND_TIMEOUT, driver=self)
        else:
            _pos = v
        x, y = _pos
        pos = self._get_left_up_offset()
        pos = (pos[0] + x, pos[1] + y)
        self._move_to_pos(pos)
        if file_path:
            self.screenshot(file_path, _pos)
        self.mouse.press(Button.left)
        time.sleep(2)
        self.mouse.move(dx,dy)
        time.sleep(1)
        self.mouse.release(Button.left)

    @keyword
    def search_menu(self,search,img_pth, threshold, rgb, file_path=None):
        '''
        搜索菜单框滑动,滑动到底部
        :param search:
        :param img_pth:
        :param file_path:
        :param threshold:
        :param rgb:
        :return:
        '''
        self.touch_keyboard(img_pth, threshold, rgb,search,file_path,True)
        self.mouse.scroll(0, -1)

    @keyword
    def slide_alignment(self, iframe_xpath=None, scroll_xpath=None):
        '''
        slide alignment :滑动对齐
        定位并滑动使得页面中间对齐
        :param iframe_xpath:
        :param scroll_xpath:
        :return:
        '''
        if iframe_xpath:
            ele_iframe = self.driver.find_element_by_xpath(iframe_xpath.replace('xpath=',''))
            self.driver.switch_to.frame(ele_iframe)
        if iframe_xpath:
            sc = Scroll(self.driver)
            element = self.driver.find_element_by_xpath(scroll_xpath.replace('xpath=',''))
            sc.scroll_to_element_center(element)

    @keyword
    def slide_login_dorado(self,slide=37):
        '''
            这里仅dorado web 可以使用，出现问题@周智开
            :slide: 滑动偏移量
        '''
        self.down_image('//*[@id="slideVerify"]/canvas[1]', 'result/slideVerify1.png')
        self.down_image('//*[@id="slideVerify"]/canvas[2]', 'result/slideVerify2.png')
        _pos = self._touch_pro_dorado(
            "result/slideVerify2.png", 0.5,False,
            "result/slideVerify1.png"
        )
        track = [5, 5, _pos[0] - slide]
        slider = self.driver.find_element_by_xpath('//*[@id="slideVerify"]/div[3]/div/div')
        self.move_to_gap(slider, track)

    def _touch_pro_dorado(self, img_pth, threshold, rgb, screen_path, file_path=None):
        '''
        仅登陆dorado 使用目前
        :param img_pth
        :param threshold
        :param rgb
        :param screen_path
        :param file_path:
        :return:
        '''
        v = Template(img_pth, threshold=threshold, rgb=rgb)
        if isinstance(v, Template):
            _pos = loop_find_pro(v, timeout=ST.FIND_TIMEOUT, driver=self, screen=aircv.imread(screen_path))
        else:
            _pos = v
        x, y = _pos
        pos = self._get_left_up_offset()
        pos = (pos[0] + x, pos[1] + y)
        self._move_to_pos(pos)
        if file_path:
            self.screenshot(file_path, _pos)
        self._click_current_pos()
        time.sleep(1)
        # self._embed_to_log_as_base64(img_pth,file_path,800)
        self._embed_to_log_as_file(img_pth, file_path, 800)
        return _pos

    @keyword
    def touch(self, img_pth, threshold, rgb, file_path=None):
        '''
        # 点击目标图片（小图片）
        :param img_pth:
        :param threshold:
        :param rgb:
        :param file_path:
        :return:
        '''
        v=Template(img_pth, threshold=threshold, rgb=rgb)
        if isinstance(v, Template):
            _pos = loop_find(v, timeout=ST.FIND_TIMEOUT, driver=self)
        else:
            _pos = v
        x, y = _pos
        pos = self._get_left_up_offset()
        pos = (pos[0] + x, pos[1] + y)
        self._move_to_pos(pos)
        if file_path:
            self.screenshot(file_path, _pos)
        self._click_current_pos()
        time.sleep(1)
        # self._embed_to_log_as_file(img_pth,file_path,800)
        self._embed_to_log_as_base64(img_pth,file_path,800)
        return _pos


    @keyword
    def touch_keyboard_del(self, img_pth, threshold,rgb=True,file_path=None, is_double=False):
        '''
        # 支持双击删除选项框内容
        :param img_pth:
        :param threshold:
        :param rgb:
        :param file_path:
        :return:
        '''
        v=Template(img_pth, threshold=threshold, rgb=rgb)
        if isinstance(v, Template):
            _pos = loop_find(v, timeout=ST.FIND_TIMEOUT, driver=self)
        else:
            _pos = v
        x, y = _pos
        pos = self._get_left_up_offset()
        pos = (pos[0] + x, pos[1] + y)
        self._move_to_pos(pos)
        if file_path:
            self.screenshot(file_path, _pos)
        self._click_current_pos(is_double)
        time.sleep(1)
        self._embed_to_log_as_base64(img_pth,file_path,800)
        return _pos

    @keyword
    def touch_keyboard(self, img_pth, threshold, rgb, keyboard, file_path=None, enter=None, is_double=False):
        '''
        操作键盘输入文字
        :param img_pth:    目标截图
        :param threshold:  相似度分值
        :param rgb:       三原色bool值
        :param keyboard:  新输入的数据
        :param file_path: 结果图片存放地址
        :param enter: 是否按回车键
        :param is_double: 是否双击（不太稳定）
        :return:
        '''
        v = Template(img_pth, threshold=threshold, rgb=rgb)
        if isinstance(v, Template):
            _pos = loop_find(v, timeout=ST.FIND_TIMEOUT, driver=self)
        else:
            _pos = v
        x, y = _pos
        pos = self._get_left_up_offset()
        pos = (pos[0] + x, pos[1] + y)
        self._move_to_pos(pos)
        if file_path:
            self.screenshot(file_path, _pos)
        self._click_current_pos(is_double)
        self._sendkey_current_pos(keyboard, enter)
        time.sleep(1)
        self._embed_to_log_as_base64(img_pth,file_path,800)
        return _pos

    @keyword
    def touch_pro(self, img_pth, threshold, rgb, screen_path, file_path=None):
        '''
        仅登陆dorado 使用目前
        :param img_pth
        :param threshold
        :param rgb
        :param screen_path
        :param file_path:
        :return:
        '''
        v = Template(img_pth, threshold=threshold, rgb=rgb)
        if isinstance(v, Template):
            _pos = loop_find_pro(v, timeout=ST.FIND_TIMEOUT, driver=self, screen=aircv.imread(screen_path))
        else:
            _pos = v
        x, y = _pos
        pos = self._get_left_up_offset()
        pos = (pos[0] + x, pos[1] + y)
        self._move_to_pos(pos)
        if file_path:
            self.screenshot(file_path, _pos)
        self._click_current_pos()
        time.sleep(1)
        self._embed_to_log_as_base64(img_pth,file_path,800)
        return _pos

    @keyword
    def assert_template(self, img_pth, threshold, rgb, msg=""):
        '''
        仅针对图片，断言当前操作后的结果可符合预期；判断页面上的相似度比较高的比如
        '''
        v = Template(img_pth, threshold=threshold, rgb=rgb)
        if isinstance(v, Template):
            try:
                pos = loop_find(v, timeout=ST.FIND_TIMEOUT, driver=self)
            except TargetNotFoundError:
                raise AssertionError("Target template not found on screen.")
            else:
                return pos
        else:
            raise AssertionError("args is not a template")

    @keyword
    def assert_existing_error(self, img_pth, threshold, rgb, msg=""):
        '''
        仅针对图片，断言当前操作后的结果可符合预期；判断页面上的相似度比较高的比如
        '''
        v = Template(img_pth, threshold=threshold, rgb=rgb)
        if isinstance(v, Template):
            try:
                pos = loop_find(v, timeout=ST.FIND_TIMEOUT, driver=self)
                if pos:
                    raise AssertionError("页面存在异常")

            except TargetNotFoundError:
                raise AssertionError("传入的图片未找到")
        else:
            raise AssertionError("args is not a template")

    def _sendkey_current_pos(self,keyboard,enter=None):
        self.key_mouse.type(keyboard)
        if enter:
            self.key_mouse.press(Key.enter)
            self.key_mouse.release(Key.enter)

    def _click_current_pos(self,is_double=False):
        if is_double:
            self.mouse.click(Button.left, 4)
            self.key_mouse.press(Key.backspace)
            self.key_mouse.release(Key.backspace)
        else:
            self.mouse.click(Button.left, 1)

    def screenshot(self, file_path=None, pos=None):
        if file_path:
            self.driver.save_screenshot(file_path)
            if pos:
                self._frame(file_path, pos)
        else:
            if not ST.LOG_DIR:
                file_path = "temp.jpg"
            else:
                file_path = os.path.join(ST.LOG_DIR, "temp.jpg")
            self.driver.save_screenshot(file_path)
            screen = aircv.imread(file_path)
            return screen

    def _move_to_pos(self, pos):
        self.mouse.position = pos

    def _get_left_up_offset(self):
        window_pos = self.driver.get_window_position()
        window_size = self.driver.get_window_size()
        screen = self.screenshot()
        screen_size = get_resolution(screen)
        offset = window_size["width"] - \
                 screen_size[0], window_size["height"] - screen_size[1]
        pos = (int(offset[0] / 2 + window_pos['x']),
               int(offset[1] + window_pos['y'] - offset[0] / 2))
        return pos

    def _frame(self, file_path, pos):
        picture = aircv.imread(file_path)
        x, y = pos
        cv2.putText(picture, "target img", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
        cv2.rectangle(picture, (x, y), ((x + 40, y + 40)), (0, 255, 0), 2)
        cv2.circle(picture, (x, y), 60, (0, 0, 255), 0)
        cv2.imwrite(file_path, picture)


    def toBse64(self,filepath):
        with open(filepath, 'rb') as f1:
            base64_str = base64.b64encode(f1.read())
            str = base64_str.decode('utf-8')  # str
            return str
    def _embed_to_log_as_base64(self, tag_path,reult_path, width):
        self.info(
            '</td></tr><tr><td colspan="3">'
            '<img alt="screenshot" class="tag_path" '
            f'src="data:image/png;base64,{self.toBse64(tag_path)}" width="100px">'
            f'<img alt="screenshot" class="reult_path" '
            f'src="data:image/png;base64,{self.toBse64(reult_path)}" width="{width}px">',
            html=True,
        )


    def _embed_to_log_as_file(self,tag_path,reult_path, width):
        tag_src = "../"+tag_path
        reult_src = get_link_path(reult_path, self.log_dir).replace('result/', '')
        self.info(
            '</td></tr><tr><td colspan="3">'
            f'<a href="{tag_src}"><img src="{tag_src}" "></a>'
            f'<a href="{reult_src}"><img src="{reult_src}" width="{width}px"></a>',
            html=True,
        )
    def down_image(self, xpath, path):
        '''
        下载canva 图片
        :param xpath:
        :param path:
        :return:
        '''
        canvas = self.driver.find_element_by_xpath(xpath)
        canvas_base64 = self.driver.execute_script("return arguments[0].toDataURL('image/png').substring(21);", canvas)
        output_image = base64.b64decode(canvas_base64)
        with open(path, 'wb') as f:
            f.write(output_image)

    def get_track(self, distance):
        """
        根据偏移量获取移动轨迹
        :param distance: 偏移量
        :return: 移动轨迹
        """
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 4 / 5
        # 计算间隔
        t = 0.2
        # 初速度
        v = 90

        while current < distance:
            if current < mid:
                # 加速度为正 2
                a = 2
            else:
                # 加速度为负 3
                a = -3
            # 初速度 v0
            v0 = v
            # 当前速度 v = v0 + at
            v = v0 + a * t
            # 移动距离 x = v0t + 1/2 * a * t^2
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move))
        return track

    def move_to_gap(self, slider, tracks):
        """
        拖动滑块到缺口处
        :param slider: 滑块
        :param tracks: 轨迹
        :return:
        """
        ActionChains(self.driver).click_and_hold(slider).perform()
        for x in tracks:
            ActionChains(self.driver).move_by_offset(xoffset=x, yoffset=0).perform()
        ActionChains(self.driver).release(slider).perform()