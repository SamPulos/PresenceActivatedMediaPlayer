import os
import pathlib
from ConfigParser import ConfigParser
from guizero import App, Slider, PushButton, Text, Combo, ListBox

app = App(title="config settings", layout="grid", width=600, height=600)
y = 0

#volume_text = Text(app, text="Volume (unsupported setting):", grid=[0,y], align="left", color = "red")
#volume_slider = Slider(app, start=0, end=100, grid=[1,y])
#y = y + 1

poll_rate_text = Text(app, text="Poll rate (milliseconds):", grid=[0,y], align="left")
poll_rate_slider = Slider(app, start=200, end=1000, grid=[1,y])
y = y + 1

reset_wait_duration_text = Text(app, text="Reset wait duration (seconds):", grid=[0,y], align="left")
reset_wait_duration_slider = Slider(app, start=1, end=60, grid=[1,y])
y = y + 1

image_display_duration_text = Text(app, text="Image display duration (seconds):", grid=[0,y], align="left")
image_display_duration_slider = Slider(app, start=1, end=120, grid=[1,y])
y = y + 1

distance_threshold_text = Text(app, text="Distance threshold (units):", grid=[0,y], align="left")
distance_threshold_slider = Slider(app, start=50, end=500, grid=[1,y])
y = y + 1

trigger_condition_text = Text(app, text="Trigger when:", grid=[0,y], align="left")
trigger_condition_combo = Combo(app, options=["motion", "proximity", "motion and proximity", "motion or proximity"], grid=[1,y])
y = y + 1

reset_condition_text = Text(app, text="Reset when:", grid=[0,y], align="left")
reset_condition_combo = Combo(app, options=["no motion", "no proximity", "no motion and no proximity", "no motion or no proximity"], selected="no motion and no proximity", grid=[1,y])
y = y + 1

media_order_text = Text(app, text="Media order:", grid=[0,y], align="left")
media_order_combo = Combo(app, options=["order added", "alphabetic", "shuffle", "random"], grid=[1,y])
y = y + 1

background_image = ""
def get_background_image():
    global background_image
    background_image = app.select_file(filetypes=[["PNG image", ".png"], ["JPG image", ".jpg"], ["JPEG image", ".jpeg"]])
    background_image_button.text = 'background image is: ' + background_image
background_image_button = PushButton(app, command=get_background_image, text='Select a background image', grid=[0,y,2,1], align="left", width=70)
y = y + 1

def add_displayable_media():
    displayable_media = app.select_file(filetypes=[["MP4 video", ".mp4"], ["PNG image", ".png"], ["JPG image", ".jpg"], ["JPEG image", ".jpeg"]])
    selected_displayable_media_listbox.append(displayable_media)
select_displayable_media_button = PushButton(app, command=add_displayable_media, text='Select a media file to add', grid=[0,y,2,1], align="left", width=70)
y = y + 1
def remove_displayable_media(value):
    selected_displayable_media_listbox.remove(value)
selected_displayable_media_listbox = ListBox(app, command=remove_displayable_media, scrollbar=True, grid=[0,y,2,1], align="left", width=585, height=100)
y = y + 1

def setCurrentValues(dictionary):
    #volume_slider.value = dictionary['volume']
    poll_rate_slider.value = dictionary['poll_rate']
    reset_wait_duration_slider.value = dictionary['reset_wait_duration']
    image_display_duration_slider.value = dictionary['image_display_duration']
    distance_threshold_slider.value = dictionary['distance_threshold']
    trigger_condition_combo.value = dictionary['trigger_condition']
    reset_condition_combo.value = dictionary['reset_condition']
    media_order_combo.value = dictionary['media_order']
    global background_image
    background_image = dictionary['background_image']
    background_image_button.text = 'background image is: ' + background_image
    selected_displayable_media_listbox.clear()
    for path in dictionary['displayable_media']:
        selected_displayable_media_listbox.append(path)

setCurrentValues(ConfigParser().configData)


def confirm_config():
    create_json()
confirm_button = PushButton(app, command=confirm_config, text='confirm', grid=[0,y,2,1], align="left", width=70)
confirm_button.bg = "green"
y = y + 1

def reset_config():
    current_path = os.getcwd()
    defaults = {
        #'volume': 0,
        'poll_rate': 500,
        'reset_wait_duration': 5,
        'image_display_duration': 20,
        'distance_threshold': 150,
        'trigger_condition': "motion",
        'reset_condition': "no motion and no proximity",
        'media_order': "order added",
        'background_image': str(pathlib.Path(__file__).parent.absolute())+"/defaults/background_image.jpg",
        'displayable_media': [(str(pathlib.Path(__file__).parent.absolute())+"/defaults/testVideo.mp4"), (str(pathlib.Path(__file__).parent.absolute())+"/defaults/testImage.png")]
    }
    setCurrentValues(defaults)
reset_button = PushButton(app, command=reset_config, text='reset to default', grid=[0,y,2,1], align="left", width = 70)
reset_button.bg = "yellow"
y = y + 1

def exit_config():
    exit("exit button pressed")
exit_button = PushButton(app, command=exit_config, text='cancel and exit', grid=[0,y,2,1], align="left", width=70)
exit_button.bg = "red"
y = y + 1

def create_json():
    data = '{'
    #data += (' "volume": ' + str(volume_slider.value))
    data += (' "poll_rate": ' + str(poll_rate_slider.value))
    data += (', "reset_wait_duration": ' + str(reset_wait_duration_slider.value))
    data += (', "image_display_duration": ' + str(image_display_duration_slider.value))
    data += (', "distance_threshold": ' + str(distance_threshold_slider.value))
    data += (', "trigger_condition": "' + trigger_condition_combo.value + '"')
    data += (', "reset_condition": "' + reset_condition_combo.value + '"')
    data += (', "media_order": "' + media_order_combo.value + '"')
    data += (', "background_image": "' + background_image + '"')
    data += (', "displayable_media": [')
    first_item = True;
    for i in selected_displayable_media_listbox.items:
        if i != "":
            if not first_item:
                data += ', '
            else:
                first_item = False
            data += ('"' + i + '"')
    data += '] }'
    print(data)
    
    f=open(str(pathlib.Path(__file__).parent.absolute()) + "/config.json","w+")
    f.write(data)
    f.close()
    
app.display()