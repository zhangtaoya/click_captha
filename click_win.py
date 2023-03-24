import asyncio
import time
import pyautogui
import pyperclip
import tornado.web
from tornado import gen

print(pyautogui.size())
pyautogui.FAILSAFE = False
PEnterRefresh = (647, 52)
PRefresh = (85, 53)
PCheck = (308, 290)
PClear = (46, 318)
PConsoleUrl = (34, 454)
PMenuCpy = (86, 259)
PMenuCpySel = (319, 258)
PMenuCpySelBash = (320, 559)  # coy HAR parsed log

MYIP = ""


def time_str(ts=None):
    if not ts:
        ts = time.time()
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))


XRate = 1512 / 1024.0
YRate = 944 / 768.0


async def move_to(pose, dur=0.1, slp=0.1):
    x, y = pose[0] / XRate, pose[1] / YRate
    pyautogui.moveTo(x, y, duration=dur)
    if slp > 0:
        await asyncio.sleep(slp)


async def move_to_left_click(pose, dur=0.1, slp=0.1):
    x, y = pose[0] / XRate, pose[1] / YRate
    pyautogui.moveTo(x, y, duration=dur)
    pyautogui.click(x, y)
    if slp > 0:
        await asyncio.sleep(slp)


async def move_to_right_click(pose, dur=0.1, slp=0.1):
    x, y = pose[0] / XRate, pose[1] / YRate
    pyautogui.moveTo(x, y, duration=dur)
    pyautogui.rightClick(x, y)
    if slp > 0:
        await asyncio.sleep(slp)


async def blur_click():
    await move_to_left_click(PEnterRefresh, slp=1)
    pyautogui.keyDown("enter")
    await asyncio.sleep(0.5)
    pyautogui.keyUp("enter")
    await asyncio.sleep(20)
    # pyautogui.sleep(20)
    await move_to(PClear)
    await move_to_left_click(PCheck, dur=1, slp=10)


async def cpy_curl():
    await move_to_left_click(PClear)
    await move_to_left_click(PRefresh, slp=5)
    await move_to_right_click(PConsoleUrl, slp=1)
    await move_to(PMenuCpy, slp=1)
    await move_to(PMenuCpySel, slp=1)
    await move_to_left_click(PMenuCpySelBash, dur=1, slp=0.5)
    data = pyperclip.paste()
    return data


ON_CLICK = False


async def click_and_report():
    global ON_CLICK
    if ON_CLICK:
        print(time_str(), "now click doing, bypass")
        return ""
    ON_CLICK = True
    print(time_str(), "now click_and_report")

    await blur_click()
    data = await cpy_curl()
    ON_CLICK = False

    # print(MYIP, data)
    print(time_str(), "click_and_report done")
    print(data)
    return data


asyncio.run(click_and_report())
