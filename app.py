from flask import Flask, render_template, request, redirect, url_for, send_file
import cv2
import numpy as np
from keras.models import load_model
from keras.preprocessing import image
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import os
import re
import urllib.request

app = Flask(__name__)

# Function to download the Haar Cascade file if not present
def download_haar_cascade(cascade_name):
    """
    Download the Haar Cascade file from OpenCV repository if it doesn't exist locally.
    """
    url = f'https://github.com/opencv/opencv/blob/master/data/haarcascades/{cascade_name}?raw=true'
    local_path = os.path.join(cv2.data.haarcascades, cascade_name)
    if not os.path.exists(local_path):
        print(f"Downloading {cascade_name}...")
        urllib.request.urlretrieve(url, local_path)
        print(f"Downloaded {cascade_name} to {local_path}")

# Download the Haar Cascade file
download_haar_cascade('haarcascade_frontalface_default.xml')

# Load the trained model for face recognition
model = load_model('face_recognition.h5')  # Assuming you have already trained and saved the model

# Load the Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Define student names (replace with actual student IDs or names)
student_names = ['Rachel_Green', 'Monica_Geller', 'Phoebe_Buffay', 'Joey_Tribbiani', 'Chandler_Bing', 'Ross_Geller', 'Janice_Litman', 'Gunther']

# Function to preprocess the image for face detection
def preprocess_image(img):
    """
    Convert the image to grayscale and apply histogram equalization.
    This improves contrast and helps in better face detection.
    """
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    equalized_img = cv2.equalizeHist(gray_img)  # Apply histogram equalization
    return equalized_img

# Function to update attendance in an Excel file
def update_attendance(teacher_name, subject_name, students_present):
    """
    Create an Excel file with attendance information including the time and student presence.
    Returns the filename of the generated Excel file.
    """
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"{teacher_name}_{subject_name}_Attendance_{date_time}.xlsx"
    
    # Create DataFrame with columns for time and student names
    df_columns = ['Time'] + student_names
    df = pd.DataFrame(columns=df_columns)
    
    # Create row with attendance information
    attendance_row = [now.strftime("%H:%M:%S")] + ['1' if student in students_present else '0' for student in student_names]
    
    # Append row to DataFrame
    df.loc[len(df)] = attendance_row
    
    # Write DataFrame to Excel file
    df.to_excel(file_name, index=False)
    
    return file_name

# Function to generate a PDF report of the attendance
def generate_pdf(teacher_name, subject_name, attendance_time, students_present, test_img, faces):
    """
    Generate a PDF report containing attendance details, cropped face images, and a footer with a logo.
    Returns the filename of the generated PDF.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add college name and logo
    pdf.set_font("Arial", size=16, style="B")  # Set font size to 16 and style to bold
    pdf.cell(200, 10, txt="RNS INSTITUTE OF TECHNOLOGY", ln=True, align="C")  # Center-aligned text
    pdf.image('static/images/RNSIT_logo.jpg', x=10, y=10, w=10)  # Adjusted logo size and position
    pdf.ln(30)  # Add space

    # Add attendance details
    pdf.set_font("Arial", size=12)  # Reset font size
    pdf.cell(200, 10, txt=f"Attendance Report for {subject_name} class taken by {teacher_name} on {attendance_time}", ln=True, align="C")
    pdf.ln(10)  # Add space

    # Add student attendance details as a list
    for student in students_present:
        pdf.cell(200, 10, txt=student, ln=True, align="C")

    pdf.ln(10)  # Add space

    # Add date and time
    pdf.cell(200, 10, txt=f"Date and Time: {attendance_time}", ln=True, align="C")
    pdf.ln(10)  # Add space

    # Add cropped images of detected faces in the same line
    img_folder = "detected_faces"
    os.makedirs(img_folder, exist_ok=True)
    x_position = 10  # Initial x position for images
    for i, (x, y, w, h) in enumerate(faces):
        face_img = test_img[y:y+h, x:x+w]
        cv2.imwrite(f"{img_folder}/face_{i}.jpg", face_img)
        pdf.image(f"{img_folder}/face_{i}.jpg", x=x_position, y=pdf.get_y(), w=20, h=20)  # Adjusted image size and position
        x_position += 25  # Increase x position for next image
        if x_position > 170:  # Start new row if image exceeds page width
            pdf.ln(25)  # Add space
            x_position = 10  # Reset x position for new row

    pdf.ln(10)  # Add space

    # Add footer with company logo
    pdf.cell(200, 10, txt="Report generated by", ln=True, align="C")
    pdf.image('static/images/Comp_logo.png', x=50, y=240, w=30)  # Adjusted logo size
    
    # Sanitize the filename to remove invalid characters
    sanitized_attendance_time = re.sub(r'[^a-zA-Z0-9_.-]', '_', attendance_time)
    pdf_output = f"Attendance_Report_{sanitized_attendance_time}.pdf"
    pdf.output(pdf_output)
    return pdf_output

@app.route('/')
def index():
    """
    Render the main page of the application.
    """
    return render_template('index.html')

@app.route('/process_attendance', methods=['POST'])
def process_attendance():
    """
    Process the uploaded image or video frame to detect faces, recognize students, update attendance,
    and generate a PDF report. Return the results to the user.
    """
    if 'file' in request.files:
        file = request.files['file']
        image_data = file.read()
        nparr = np.frombuffer(image_data, np.uint8)
        test_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    else:
        cap = cv2.VideoCapture(0)
        ret, test_img = cap.read()
        cap.release()

    # Preprocess the test image
    preprocessed_img = preprocess_image(test_img)

    # Detect faces in the preprocessed image
    faces = face_cascade.detectMultiScale(preprocessed_img, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Process each detected face
    students_present = []
    for (x, y, w, h) in faces:
        # Crop the detected face from the original image
        face_img = test_img[y:y+h, x:x+w]

        # Resize the face image to 250x250
        resized_face_img = cv2.resize(face_img, (250, 250))

        # Preprocess the image for model prediction
        img_array = image.img_to_array(resized_face_img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0  # Normalize pixel values to [0, 1]

        # Predict the class probabilities
        predictions = model.predict(img_array)

        # Map the predicted class probabilities to class labels
        class_index = np.argmax(predictions)
        
        # If the model's confidence is below a certain threshold, consider it as None
        if np.max(predictions) < 0.5:
            predicted_student = None
        else:
            predicted_student = student_names[class_index]

        # Add the predicted student to the list
        if predicted_student:
            students_present.append(predicted_student)

    # Update attendance in Excel
    teacher_name = request.form.get('teacher_name')
    subject_name = request.form.get('subject_name')
    attendance_file = update_attendance(teacher_name, subject_name, students_present)

    # Generate PDF report
    attendance_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf_report = generate_pdf(teacher_name, subject_name, attendance_time, students_present, test_img, faces)

    # Render the index page with success message and file links
    return render_template('index.html', message="Attendance taken successfully!", attendance_file=attendance_file, pdf_report=pdf_report)

@app.route('/download/<file_name>')
def download(file_name):
    """
    Allow the user to download a file from the server.
    """
    return send_file(file_name, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
