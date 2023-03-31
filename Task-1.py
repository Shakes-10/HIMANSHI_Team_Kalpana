import csv
import curses
import time


def main(scr):
  scr.keypad(True)
  curses.use_default_colors()
  curses.noecho()
  scr.refresh()

  # Get screen width/height
  height,width = scr.getmaxyx()

  mypad_height = 1000
  
  mypad = curses.newpad(mypad_height, width);
  mypad.scrollok(True)
  mypad_pos = 0
  mypad_refresh = lambda: mypad.refresh(mypad_pos+2, 0, 0, 0, height-1, width-1)
  mypad_refresh()

  try:
    with open("data.csv", "r") as file:
        robj = csv.reader(file)
        i = 0
        
        for j in robj:
            data = ",".join(j)
            data = data+"\n"
            mypad.addstr(i, 25, data)
            
            if i > height:
                mypad_pos = min(i - height, mypad_height-height)
                mypad_refresh()
                time.sleep(0.0000005)
            i += 1
            

    # Wait for user to scroll or quit
    running = True
    while running:
        ch = scr.getch()
        if ch == curses.KEY_DOWN and mypad_pos < mypad.getyx()[0] - height - 1:
            mypad_pos += 1
            mypad_refresh()
        elif ch == curses.KEY_UP and mypad_pos > -2:
            mypad_pos -= 1
            mypad_refresh()
        elif ch < 256 and chr(ch) == 'q':
            running = False
        elif ch == curses.KEY_RESIZE:
            height,width = scr.getmaxyx()
            while mypad_pos > mypad.getyx()[0] - height - 1:
              mypad_pos -= 1
            mypad_refresh()
  except KeyboardInterrupt:
    pass
curses.wrapper(main)
