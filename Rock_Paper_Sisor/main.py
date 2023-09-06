import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
import random

# 0 is the number of the camera
cap = cv2.VideoCapture(0)
cap.set(3, 640) # property_3(Width) = 640px
cap.set(4, 480) # property_4(Height) = 480px

detector = HandDetector(maxHands= 1)

timer = 0
stateResult = False
startGame = False
scores = [0, 0]  # [ IA , Player]

while True:
    # bring the backgrond of the game
    imgBG = cv2.imread("Rock_Paper_Sisor\Resources\BG.png")
    # read the camera
    success, img = cap.read()

    # Scalling the camera image to fit the square in the game background (divide from the greatest value)
    imgScalled = cv2.resize(img, (0,0), None, 0.875, 0.875)
    imgScalled = imgScalled[: , 80:480]

    # Find Hands
    hands, img = detector.findHands(imgScalled)

    if startGame:
        if stateResult is False:    # if we have not reach the end of the timer
            timer = time.time() - initialTime
            cv2.putText(imgBG, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (255,0,255), 4)

            if timer > 3:
                stateResult = True  # stop the timer
                timer = 0

                if hands:
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    if fingers == [0, 0, 0, 0, 0]:
                        playerMove = 1
                    if fingers == [1, 1, 1, 1, 1]:
                        playerMove = 2
                    if fingers == [0, 1, 1, 0, 0]:
                        playerMove = 3

                    randomNumber = random.randint(1, 3)
                    imgIA = cv2.imread(f'Rock_Paper_Sisor/Resources/{randomNumber}.png', cv2.IMREAD_UNCHANGED)
                    imgBG = cvzone.overlayPNG(imgBG, imgIA, (149, 310))

                    # IA wins
                    if (playerMove == 1 and randomNumber == 3) or \
                        (playerMove == 2 and randomNumber == 1) or \
                         (playerMove == 3 and randomNumber == 2):   
                            scores[1] += 1

                    # Player wins
                    if (playerMove == 3 and randomNumber == 1) or \
                        (playerMove == 1 and randomNumber == 2) or \
                         (playerMove == 2 and randomNumber == 3):   
                            scores[0] += 1

    # put the imgScalled inside the game box
    imgBG[234:654 , 795:1195] = imgScalled

    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, imgIA, (149, 310))
 

    cv2.putText(imgBG, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255,255,255), 6)
    cv2.putText(imgBG, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255,255,255), 6)


    # show  
    # cv2.imshow("camera", img)
    cv2.imshow("imgBG", imgBG)
    # cv2.imshow("scalled", imgScalled)
    


    keyPressed = cv2.waitKey(1)  # 1ms
    if keyPressed == ord('s'):
        startGame = True
        initialTime = time.time()
        stateResult = False        # to restart again and renew the imgIA

    if keyPressed == ord('q'):
        break   