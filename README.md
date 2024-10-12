# Project Overview

## What is the project?

This project is a web-based Sudoku solver that allows users to upload an image of a Sudoku puzzle. The system analyzes the image using OpenCV, solves the puzzle, and displays the solution on the website if one is found.

## Project Description:
This project addresses the problem of recognizing Sudoku grids from images using computer vision techniques. It converts an image of a Sudoku puzzle into a digital matrix that can be solved using algorithms and then displays the solution to the user in a visual format.

To achieve this, we researched libraries and tools for accurate number recognition and grid extraction. We used the OpenCV library for image processing and Tesseract (OCR) to recognize the numbers. Once the numbers were extracted, we applied puzzle-solving algorithms to obtain the final solution.

Our project supports both 9x9 and 16x16 Sudoku grids, expanding its capabilities beyond the standard grid size. We found that using these tools provides an optimal balance between performance accuracy and execution speed. Additionally, we are exploring the integration of an Arduino-based robotic hand to physically write the solution.

The next steps for development are based on our study so far, including further improvements to grid recognition and expanding support for even larger puzzles

## Challenges

One of the main challenges was the limited time compared to the amount of things that needed to be learned for the project (Python, OpenCV, NumPy, Pytesseract, 3D printing, and Arduino).

We faced several issues with Pytesseract, such as inaccurate number recognition and difficulties in configuring it for optimal performance, which required additional troubleshooting. Additionally, problems with the 3D printer caused delays, eventually leading to the cancellation of the robotic hand feature. As a result, we replaced it with a website to display the solution instead

## How does it work?

1. Upload a Sudoku puzzle image.
2. Detect and recognize the Sudoku grid using OpenCV.
3. Solve the Sudoku puzzle programmatically.
4. Display the solution on the website.

## What languages and libraries does it use?

### Frontend:
- **HTML**
- **CSS**
- **JavaScript**
- **os**
- **json**
- [**Flask**](https://flask.palletsprojects.com/) (framwork)

### Backend:
- **Python**
- [**OpenCV**](https://opencv.org/) (library)
- [**Pytesseract**](https://github.com/madmaze/pytesseract) for OCR (library)
- [**NumPy**](https://numpy.org/) (library)


## Future Improvements

- We plan to complete the Arduino-powered robotic hand that will take the solved Sudoku puzzle and physically write the solution on paper.

## Backend Algorithm Overview

### 1. Analyzing the Image

1. **Read the Image**  
   - Load the image from the provided file path using the OpenCV library.

2. **Determine the Grid Size**  
   - Use the `count_vertical_columns()` function to detect the number of vertical columns in the image.
      1. **Convert to Grayscale**  
         - Transform the image to grayscale to simplify processing.

      2. **Thresholding**  
         - Apply a threshold to binarize the image and make grid lines more distinct.

      3. **Detect Vertical Lines**  
         - Use a vertical kernel with morphological operations to highlight vertical lines in the image.

      4. **Find and Filter Contours**  
         - Detect contours corresponding to the vertical lines and filter out small ones that aren't part of the grid.

      5. **Count Vertical Columns**  
         - Count the remaining contours to determine the number of vertical columns in the grid.
   - Depending on the number of columns detected:
     - If there are 4 columns, the grid is assumed to be **9x9**.
     - If there are 5 columns, the grid is assumed to be **16x16**.
   - Raise an error if the number of columns does not match the expected values.

3. **Preprocess the Image**  
   - Convert the image to grayscale using `cv2.cvtColor()`.
   - Apply Gaussian blur with `cv2.GaussianBlur()` to reduce image sharpness and noise.
   - Use `cv2.adaptiveThreshold()` to make the image suitable for varying lighting conditions, enhancing the contrast between digits and background.

4. **Find the Contours**  
   - Detect all contours in the processed image using `cv2.findContours()`. This helps in identifying the edges and shapes of the Sudoku grid.

5. **Warp the Image**  
   - Obtain a perspective transform to warp the image, making the Sudoku grid viewable as a rectangular area.

6. **Split the Image into Parts**  
   - Depending on the detected grid size:
     - For a 9x9 grid, split the image into 81 parts using `np.vsplit()` for vertical sections and `np.hsplit()` for horizontal sections.
     - For a 16x16 grid, split the image into 256 parts using the same approach, adapted for the larger grid.

7. **Extract the Numbers**  
   - **Preprocess the Parts**: Each individual part is preprocessed using a specific function (e.g., resizing, thresholding).
   - **Extract Digits**: Apply `pytesseract.image_to_string()` to recognize and extract the digits from each of the 81 parts.
   - **Store in a Matrix**: Populate a matrix with the extracted digits, representing the Sudoku puzzle.

### 2. Sudoku Solver

1. **Check for Empty Cells**  
   - Identify the empty cells in the Sudoku grid (cells with 0 value) using a function that scans through the grid.

2. **Try Possible Numbers**  
   - For each empty cell, test possible numbers:
     - For a 9x9 grid, numbers range from 1 to 9.
     - For a 16x16 grid, numbers range from 1 to 16.
   - Use a helper function to check if placing a number is valid according to Sudoku rules:
     - The number should not exist in the same row, column, or sub-grid (3x3 for 9x9, 4x4 for 16x16).

3. **Backtracking Algorithm**  
   - If the number is valid, place it in the cell and recursively attempt to solve the rest of the puzzle.
   - If a solution is not found, backtrack by removing the number and trying the next possibility.

4. **Display the Solution**  
   - Once the grid is solved, display the completed Sudoku puzzle.