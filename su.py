import cv2
import numpy as np
from flask import Flask, request, render_template_string
from utlis import *
import os
import json

heightImg = 450
widthImg = 450 
N=9
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)



html_templ = """
<!DOCTYPE html>
<html>
<head>
<title>Image Upload Viewer</title>
<style>
    .all {
  background-color:black;
}
#SudokuSolver {
  color: white;
  display: flex;
  justify-content: center;
}
#sudoku-image {
  border: 2px solid white;
  color: white;
  border-radius: 5px;
}
#form{
  display: flex;
  justify-content: center;
} 
#img{
  width: 144px;
  height: 108px;
}
</style>
</head>
<body class="all">
    <div>
    </div>
    <h1 id="SudokuSolver">Sudoku Solver</h1>
    <form method="POST" enctype="multipart/form-data" id="form">
        <input type="file" name="image" accept="image/*" required id="sudoku-image">
        <button type="submit">Upload</button>
    </form>
    
</body>
</html>
"""

html_temp = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Upload Viewer</title>
    <style>
        .all {
            background-color: black;
        }
        #SudokuSolver {
            color: white;
            display: flex;
            justify-content: center;
        }
        #sudoku-image {
            border: 2px solid white;
            color: white;
            border-radius: 5px;
        }
        #form {
            display: flex;
            justify-content: center;
        } 
        #table {
            display: flex;
            justify-content: center;
            color: white;
        }
        #SudokuGrid {
            display: flex;
            justify-content: center;
            color: white;
        }
        td {
            border: 1px solid black;
            padding: 7px;
            margin: -5px;
            text-align: center;
            border-color: white;
            width: 15px;
            font-size: 10px;
        }
        #img{
            width: 144px;
            height: 108px;
        }
        #text{
        color: white;
        }
    </style>
</head>
<body class="all">
    <h1 id="SudokuSolver">Sudoku Solver</h1>
    <form method="POST" enctype="multipart/form-data" id="form">
        <input type="file" name="image" accept="image/*" required id="sudoku-image">
        <button type="submit">Upload</button>
    </form>
    <h3 id="SudokuGrid">Sudoku Grid</h3>
    <div id="table">
        <table>
            <tbody id="sudokuTable"></tbody>
        </table>
    </div>
    <h3>
        <tbody id="text"></tbody>
    </h3>
    <script>
        const grid = {{grid}}; // Convert grid to JSON for JavaScript
        console.log('=>', grid, '<=');
        const tableBody = document.getElementById('sudokuTable');
        for (let i = 0; i < {{N}}; i++) {
            const row = document.createElement('tr');
            for (let j = 0; j < {{N}}; j++) {
                const cell = document.createElement('td');
                cell.textContent = grid[i][j] !== 0 ? grid[i][j] : ''; // Show empty cells as blank
                row.appendChild(cell);
            }
            tableBody.appendChild(row);
        }
</script>
</body>
</html>
"""
@app.route('/upload', methods=['GET', 'POST'])
def upload_image():
    image_url = None
    grid = None
    grid_json=None
    text="text"
    N=9
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'image' not in request.files:
            return 'No file part'
        file = request.files['image']
        
        # If user does not select file, browser also submit an empty part without filename
        if file.filename == '':
            return 'No selected file'
        if file:
            # Save the file to the upload folder
            print('here')
            filename = file.filename
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            
            # Create the URL for the uploaded image to be displayed in the HTML
            image_url = f"/{filepath}"
            # print ('=>',image_url,'<=')
            # If you want to process the image (e.g. Sudoku), you can call sudo function here:
            grid,N,text = sudo(filepath, widthImg, heightImg)  # Assuming 'sudo' is the function you call for processing
            grid_json = json.dumps(grid.tolist())
            print('111')
            return render_template_string(html_temp, grid=grid_json,text=text,N=N)
            
    print (3333)
    return render_template_string(html_templ, image_url=image_url,grid=grid_json,text=text,N=N)

if __name__ == '__main__':
    app.run(debug=True)
