from PIL import ImageGrab, ImageChops, Image
from dataclasses import dataclass
import win32gui

@dataclass
class ScreenshotBounds:
    # Goes x, y, width, height
    width = 0
    height = 0
    app = None
    crop_bounds = {
                'snickerstream':[0, 26, width, height],
                'snickerstream_3ds_top_screen':[2, 30, width - 1, (height / 1.90899) - 1],
                'snickerstream_3ds_bottom_screen':[43, (height / 1.90899) - 1, width - 43, height - 3],
                'obs_windowed_projector':[6, 31, width - 6, height - 6],
                'custom': None,
             }
    
    def configure_size(self, width, height):
        self.width = width
        self.height = height
        self.update_bounds()
    
    def configure_app(self, app):
        if app.find('Snickerstream') != -1 and app.find('3DS') != -1:
            app = 'Snickerstream'
        elif app.find('OBS') != -1:
            app = 'Windowed Projector'
        self.app = app.lower()

    def set_custom_bounds(self, x, y, width, height):
        self.crop_bounds['custom'] = [x, y, x + width, y + height]

    def update_bounds(self):
        self.crop_bounds = {
                    'snickerstream':[0, 26, self.width , self.height],
                    'snickerstream_3ds_top_screen':[2, 26, self.width - 1, (self.height / 1.90899) - 1],
                    'snickerstream_3ds_bottom_screen':[43, (self.height / 1.90899) - 1, self.width - 43, self.height - 3],
                    'obs_windowed_projector':[6, 31, self.width - 6, self.height - 6],
                    'custom': self.crop_bounds['custom'],
                }
        
def take_screenshot(path, settings, x, y, width, height, name='current.png', crash_check=False):
    if crash_check:
        crash_img = Image.open(f'data/{path}/crash.png')

    bounds = ScreenshotBounds()
    if settings.hunt['streaming_app'] == 'Custom':
        bounds.configure_app(settings.hunt['custom_app'])
        bounds.set_custom_bounds(int(x), int(y), int(width), int(height))
    else:
        bounds.configure_app(settings.hunt['streaming_app'])

    winlist = []
    def enum_cb(hwnd, result):
        winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
    win32gui.EnumWindows(enum_cb, None)

    for hwnd, title in winlist:
        if title.lower().find(bounds.app.lower()) != -1:
            window = (hwnd, title)
            break

    win32gui.SetForegroundWindow(window[0])
    location = win32gui.GetWindowRect(window[0])
    img = ImageGrab.grab(location)

    width, height = img.size
    bounds.configure_size(width, height)
    selection = settings.hunt['streaming_app'].replace('(','').replace(' ','_').replace(')','').lower()
    img = img.crop((bounds.crop_bounds[selection][0], bounds.crop_bounds[selection][1], 
                    bounds.crop_bounds[selection][2], bounds.crop_bounds[selection][3]))
    
    if crash_check:
        diff = ImageChops.difference(img, crash_img)
        if not diff.getbbox():
            crashed = True
        else: crashed = False
    else:
        crashed = False

    img.save(f'data/{path}/{name}', 'png')
    return crashed