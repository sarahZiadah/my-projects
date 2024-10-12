import cv2
import numpy as np
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\tesseract\tesseract.exe'


def preprocess_image(square_img): # this one to preprocess the small box image 
    # cv2.imshow("0",square_img)
    # # cv2.waitKey(0)
    # kernel = np.ones((2,2),np.uint8)
    # square_img = cv2.erode(square_img,kernel,iterations= 1)
    # # # # square_img = cv2.dilate(square_img,kernel,iterations= 1)
    # cv2.imshow("1",square_img)
    # cv2.waitKey(0)
    blurred = cv2.GaussianBlur(square_img, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 128, 255, cv2.THRESH_BINARY_INV)
    return thresh


def read_digit(square_img,N):
    if N==9:
        config = r'--oem 3 --psm 10 -c tessedit_char_whitelist=123456789'
    else:
        config = r'--oem 3 --psm 10 -c tessedit_char_whitelist=0123456789'
    text = pytesseract.image_to_string(square_img, config=config)
    # Clean up the output
    digit = text.strip()
    if digit.isdigit():
        return int(digit)  # Return the detected number
    else:
        return 0  # If no number is detected

#### 1 - Preprocessing Image
def preProcess(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # CONVERT IMAGE TO GRAY SCALE
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)  # ADD GAUSSIAN BLUR
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, 1, 1, 11, 2)  # APPLY ADAPTIVE THRESHOLD
    return imgThreshold


#### 3 - Reorder points for Warp Perspective
def reorder(myPoints):
    myPoints = myPoints.reshape((4, 2))
    myPointsNew = np.zeros((4, 1, 2), dtype=np.int32)
    add = myPoints.sum(1)
    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] =myPoints[np.argmax(add)]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] =myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]
    return myPointsNew


#### 3 - FINDING THE BIGGEST COUNTOUR ASSUING THAT IS THE SUDUKO PUZZLE
def biggestContour(contours):
    biggest = np.array([])
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 50:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            if area > max_area and len(approx) == 4:
                biggest = approx
                max_area = area
    return biggest,max_area


#### 4 - TO SPLIT THE IMAGE INTO 81 DIFFRENT IMAGES
def splitBoxes(img,N):
    img_height, img_width = img.shape
    if img_height % N != 0 or img_width % N != 0:
        img = cv2.resize(img, (N * (img_width // N), N * (img_height // N)))
    rows = np.vsplit(img,N)
    boxes=[]
    for r in rows:
        cols= np.hsplit(r,N)
        for box in cols:
            boxes.append(box)
    return boxes


#### 4 - GET PREDECTIONS ON ALL IMAGES
def getNumbers(boxes,N):
    sudoku_grid = np.zeros((N, N), dtype=int) 
    row, col = 0, 0 

    for idx, image in enumerate(boxes):
        preprocessed_img = preprocess_image(image)
        img = np.asarray(preprocessed_img)
        img = img[4:img.shape[0] - 4, 4:img.shape[1] - 4]  
        digit = read_digit(img,N) 
        sudoku_grid[row, col] = digit 

        col += 1 
        if col == N: 
            col = 0
            row += 1

    return sudoku_grid 


def read_cell(cell):
    preprocessed_img = preprocess_image(cell)
    img = np.asarray(preprocessed_img)
    img = img[4:img.shape[0] - 4, 4:img.shape[1] -4]
    return read_digit(img)

def is_possible(grid, row, col, num, N):
    for x in range(N):
        if grid[row][x] == num:
            return False

    for x in range(N):
        if grid[x][col] == num:
            return False

    sub_grid_size = int(np.sqrt(N))  # For 9x9, this is 3; for 16x16, it's 4
    start_row = row - row % sub_grid_size
    start_col = col - col % sub_grid_size
    for i in range(sub_grid_size):
        for j in range(sub_grid_size):
            if grid[i + start_row][j + start_col] == num:
                return False

    return True

def find_empty(grid,N):
    for row in range(N):
        for col in range(N):
            if grid[row][col] == 0:
                return row, col
    return None

def sudoku_solver(grid,N):
    empty = find_empty(grid,N)
    if not empty:
        return True
    row, col = empty

    for num in range(1, N+1):
        if is_possible(grid, row, col, num,N):
            grid[row][col] = num
            if sudoku_solver(grid,N):
                return True
            grid[row][col] = 0

    return False

def count_vertical_columns(img):
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply adaptive thresholding to binarize the image
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    
    # Use a vertical kernel to detect vertical lines
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 20))
    
    # Use morphological operations to isolate vertical lines
    vertical_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel)
    
    # Find contours of the vertical lines
    contours, _ = cv2.findContours(vertical_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter out small contours that are not part of the grid lines
    contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 100]
    
    # Count the number of vertical columns (contours)
    num_columns = len(contours)

    cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
    cv2.imshow('Vertical Lines', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return num_columns

def print_sudoku(grid):
    for row in grid:
        print(" ".join(str(num) for num in row))

def sudo(pathImage,widthImg,heightImg):
    text="text"
    #### 1. PREPARE THE IMAGE
    img = cv2.imread(pathImage)
    print(img.shape)
    image = cv2.resize(img, (550, 550))


    #9 or 16
    num_columns = count_vertical_columns(image)

    print(f'Number of vertical columns: {num_columns}')

    if num_columns == 4:
        N = 9 
        heightImg = 450
        widthImg = 450
    elif num_columns > 4:
        N = 16
        heightImg =850
        widthImg = 850 
    else:
        raise ValueError("Unsupported Sudoku grid size.")

    img = cv2.resize(img, (widthImg, heightImg))  # RESIZE IMAGE TO MAKE IT A SQUARE IMAGE
    # cv2.imshow('n',img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    imgBlank = np.zeros((heightImg, widthImg, 3), np.uint8)  # CREATE A BLANK IMAGE FOR TESTING DEBUGING IF REQUIRED
    imgThreshold = preProcess(img)
    # cv2.imshow('d Images', img)
    # #### 2. FIND ALL COUNTOURS
    imgContours = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
    imgBigContour = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
    contours, hierarchy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # FIND ALL CONTOURS
    cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 3) # DRAW ALL DETECTED CONTOURS
    # cv2.imshow('k',imgContours)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    biggest, maxArea = biggestContour(contours) # FIND THE BIGGEST CONTOUR
    print(biggest)
    if biggest.size != 0:
        biggest = reorder(biggest)
        print(biggest)
        cv2.drawContours(imgBigContour, biggest, -1, (0, 0, 255), 25) # DRAW THE BIGGEST CONTOUR
        pts1 = np.float32(biggest) # PREPARE POINTS FOR WARP
        pts2 = np.float32([[0, 0],[widthImg, 0], [0, heightImg],[widthImg, heightImg]]) # PREPARE POINTS FOR WARP
        matrix = cv2.getPerspectiveTransform(pts1, pts2) # GER
        imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))
        imgDetectedDigits = imgBlank.copy()
        imgWarpColored = cv2.cvtColor(imgWarpColored,cv2.COLOR_BGR2GRAY)


        # Apply histogram equalization to improve contrast
        #### 4. SPLIT THE IMAGE AND FIND EACH DIGIT AVAILABLE
        imgSolvedDigits = imgBlank.copy()
        boxes = splitBoxes(imgWarpColored,N)
        print(len(boxes))
        sudoku_grid = getNumbers(boxes,N)
        print(sudoku_grid) 
    else:
        print("No Sudoku Found")
    if sudoku_solver(sudoku_grid,N):
        print("Solved Sudoku Grid:")
        print_sudoku(sudoku_grid)
    else:
        print("No solution exists.")
    return sudoku_grid,N,text