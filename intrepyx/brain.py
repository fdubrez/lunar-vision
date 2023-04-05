import asyncio
from typing import List, Optional

import cv2
import mediapipe as mp
  
# Used to convert protobuf message to a dictionary.
from google.protobuf.json_format import MessageToDict

from models import LanderAction, LanderData, LanderRotation, LanderStatus

# Initializing the Model
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.75,
    min_tracking_confidence=0.75,
    max_num_hands=2)


class Brain():
    player_name: str
    status: LanderStatus = LanderStatus.DEAD
    cycle: int = 0
    previous: Optional[LanderData] = None
    landerAction: LanderAction = None

    def __init__(self, player_name: str):
        # Start capturing video from webcam
        self.player_name = player_name
        cap = cv2.VideoCapture(0)
        success, img = cap.read()
        cv2.imshow('Image', img)
        asyncio.run(self.computerVision(cap))
    
    async def computerVision(self, cap):
        while True:
            thrust = False
            rotate = LanderRotation.NONE

            if cv2.waitKey(1) & 0xff == ord('q'):
                break
            # Read video frame by frame
            success, img = cap.read()
        
            # Flip the image(frame)
            img = cv2.flip(img, 1)
        
            # Convert BGR image to RGB image
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
            # Process the RGB image
            results = hands.process(imgRGB)
        
            # If hands are present in image(frame)
            if results.multi_hand_landmarks:
        
                # Both Hands are present in image(frame)
                if len(results.multi_handedness) == 2:
                        # Display 'Both Hands' on the image
                    cv2.putText(img, 'Both Hands', (250, 50),
                                cv2.FONT_HERSHEY_COMPLEX,
                                0.9, (0, 255, 0), 2)
                    thrust = True
        
                # If any hand present
                else:
                    for i in results.multi_handedness:
                        
                        # Return whether it is Right or Left Hand
                        msgDict = MessageToDict(i)
                        label = MessageToDict(i)['classification'][0]['label']
        
                        if label == 'Left':
                            rotate = LanderRotation.COUNTERCLOCKWISE
                            # Display 'Left Hand' on
                            # left side of window
                            cv2.putText(img, label+' Hand',
                                        (20, 50),
                                        cv2.FONT_HERSHEY_COMPLEX, 
                                        0.9, (0, 255, 0), 2)
        
                        if label == 'Right':
                            rotate = LanderRotation.CLOCKWISE
                            # Display 'Left Hand'
                            # on left side of window
                            cv2.putText(img, label+' Hand', (460, 50),
                                        cv2.FONT_HERSHEY_COMPLEX,
                                        0.9, (0, 255, 0), 2)
        
            # Display Video and when 'q'
            # is entered, destroy the window
            cv2.imshow('Image', img)

            self.landerAction = LanderAction(thrust=thrust, rotate=rotate)
        # gracefull exit program
        exit(0)

    def handleLander(self, players : List[LanderData]) -> LanderAction:
        return self.landerAction
