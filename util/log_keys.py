from pynput import keyboard

pressed = ''
def on_press(key):
    global pressed
    try:
        pressed = key.char
    except AttributeError:
        pass

def on_release(key):
    global pressed
    pressed = ''
    if key == keyboard.Key.esc:
        # Stop listener
        print("listener stopped")
        return False

listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

##Print out the instructions:
def trackTimes(data):
    state = 'init'

    while state != False:
        if state == 'init':
            print("""
    The file is ready, to use this program please read the instructions then press the 'g' key.

    When someone starts to talk press the t key. This will make the program print the line
    of text that it is captioning. When the speaker has finished the printed line release
    the 't' key and wait for the next line to start t be spoken. The program will record
    the start and end of when you press and release the 't' key. When the video is finished
    playing then press the 'e' key to end the program. If at any time you want to restart
    press the 'r' key and it will restart the captioning section.""")
            state = 'waitForGo'
        elif state == 'waitForGo':
            if pressed == 'g':
                print('starting!')
                lineIndex = 0
                line = data[lineIndex]
                lineText = line.text
                print('You are captioning: %s'%lineText)
                from time import time #This would error out if it was at the top of the file
                baseTime = time()
                state = 'wait'
        elif state == 'wait':
            if pressed == 't':
                state = 'listen'
    #        elif pressed == '':
    #            state = 'released'
            elif pressed == 'e':
                state = 'end'
                print(state)
            elif pressed == 'r':
                print("Restarting!")
                state = 'init'
        elif state == 'listen':
            wait = True
            p = False
            while wait:
                if pressed == 't' and not p:
                    timeStart = time()
                    p = True
                elif pressed != 't' and p:
                    timeEnd = time()
                    wait = False
            timeEnd = time()
            line.startTime = timeStart-baseTime
            line.endTime = timeEnd-baseTime
            lineIndex += 1
            if lineIndex == len(data):
                print("That was the last line in the file. Leaving the keylogging.")
                state = 'end'
            else:
                line = data[lineIndex]
                lineText = line.text
                print('You are captioning: %s'%lineText)
                state = 'wait'
        elif state == 'end':
            print("Ending...")
            state = False
        elif state == 'whoops':
            print("""
            AAH! You seem to have run out of lines. If you accidentally pressed the
            't key onw too many times simply press the e key. If your video is
            still going and you have more text to caption please check the format
            of the text file with your captions. Remember that every time there is
            an enter in that file you get to press the 't' key once. This message
            was caused by there not being enough lines in the file to complete the
            action you requested.""")
            print('\nY/n continue and generate the captions with the data that I have?')
            i = input()
            if i.lower() == 'y':
                print("Okay! will do!")
                state = 'end'
            elif i.lower() == 'n':
                print("Okay. this program will now restart and wait until you give it instructions.")
                state = 'init'
            else:
                print("Invalid option... repeating instructions.")
        else:
            print("STATE ERROR")
            print("State = %s"%state)
            print("Restarting program this was caused by an internal error...")
            state = 'init'

    #Zero out the timestamp
    return data

# captioner = GenerateCaptions(data, configData)
# data_to_write = captioner.generate()

# try:
#     write_file('output', 'captions', 'srt', data_to_write)
# except:
#     print(data_to_write)
#     print('Generate test unsuccess.')
    
# print('File saved in %s/%s.%s'%('output', 'captions', 'srt'))
# input("Press the 'Enter' key to finish")