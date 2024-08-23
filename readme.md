# Multiple Face Recognition Based Attendance System

## Introduction

The Multiple Face Recognition Based Attendance System is an advanced solution designed to automate classroom attendance using cutting-edge facial recognition technology. Unlike traditional systems that may struggle with accuracy and scalability, our system leverages a deep learning model to enhance both precision and efficiency. By recognizing multiple faces simultaneously, it reduces manual effort and provides comprehensive, accurate attendance reports.

## Features

- **Automated Attendance Tracking**: Efficiently records student attendance by recognizing multiple faces in a single image.
- **Excel Reports**: Generates detailed attendance records in Excel format for easy management.
- **PDF Summaries**: Creates visually informative PDF reports with attendance details and images of detected faces.
- **User-Friendly Interface**: Offers a simple web interface for uploading images and managing attendance.

## How to Run

1. **Prepare the Dataset**

   - Place all student images in the `dataset` folder.
   - Organize images into subdirectories named after each student according to the `student_names` list provided in `app.py`.

2. **Resize Images**

   - Run the `resize_images.py` script to resize all images in the `dataset` folder.
   - Resized images will be stored in the `resized_data` folder.

3. **Create the Model**

   - Use the `create_model.ipynb` Jupyter notebook to train and save the facial recognition model.
   - The trained model will be saved as an `.h5` file.

4. **Run the Flask Application**

   - Execute `app.py` to start the Flask server.
   - Access the application at `http://localhost:8000` in your web browser.

5. **Using the Application**

   - Upload an image of the classroom containing the students.
   - The application will automatically update the attendance in an Excel file and generate a PDF summary.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Presentation and Publication

This project was presented at the 10th National Conference on Advancements in Information Technology on April 30, 2024, and published in the Journal of Artificial Neural Networks and Learning Systems, MAT Journals.

[View the publication](https://matjournals.net/engineering/index.php/JoANNLS/article/view/704)

## Collaborators and Authors

1. **Aishwarya G:** Assistant Professor, Department of Information Science and Engineering, R N S Institute of Technology
2. **Suraj R S, Srihari M, Vaishnavi M:** Undergraduate Students, Department of Information Science and Engineering, R N S Institute of Technology

## Citation

Srihari M, et al. (2024). Comprehensive Smart Attendance Management System Utilizing Advanced Multi-Facial Recognition Technology. *Journal of Artificial Neural Networks and Learning Systems*, 1(2), 25-29.

## Why This System Stands Out

Our Multiple Face Recognition Based Attendance System offers a superior approach compared to traditional single-face recognition systems. By being able to recognize multiple faces simultaneously, it handles crowded classroom scenarios with higher accuracy and efficiency. This capability significantly reduces manual intervention and ensures that attendance records are reliable and comprehensive.
