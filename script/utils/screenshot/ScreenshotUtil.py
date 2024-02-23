import pyautogui


class ScreenshotUtil:
    @staticmethod
    def is_application_fullscreen(window):
        screen_width, screen_height = pyautogui.size()
        return (window.width, window.height) == (screen_width, screen_height)

    @staticmethod
    def get_window_region(window):

        return (window.left , window.top, window.width, window.height)
    @staticmethod
    def get_window_region_by_title(title):
        windows = pyautogui.getWindowsWithTitle(title)
        if windows:
            window = windows[0]
            return (window.left , window.top, window.width, window.height)
        return False

    @staticmethod
    def get_window(title):
        windows = pyautogui.getWindowsWithTitle(title)
        if windows:
            window = windows[0]
            return window
        return False

    @staticmethod
    def take_screenshot(title, crop=(0, 0, 0, 0)):
        window = ScreenshotUtil.get_window(title)
        if window:
            if crop == (0, 0, 0, 0):
                screenshot_pos = ScreenshotUtil.get_window_region(window)
            else:
                left, top, width, height = ScreenshotUtil.get_window_region(window)
                screenshot_pos = left + width * crop[0], top + height * crop[1], width * crop[2], height * crop[3]

            screenshot = pyautogui.screenshot(region=screenshot_pos)
            return screenshot, screenshot_pos

        return False
