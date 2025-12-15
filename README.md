This project is a Django-based fitness tracking web application designed to log strength training workouts and visualize progress over time.

The application provides a structured alternative to unstructured workout notes by allowing users to:
- Define exercises (e.g., Bench Press, Squat)
- Log workout sessions with weight and reps
- Visualize progress using a dynamic chart (Chart.js)
- Export workout data to an Excel (XLSX) file

The application uses two primary models: Exercise, which represents a lift or movement, and SessionSet, which records individual workout sessions associated with an exercise.

To use this application, run the following command from the fitness_tracker folder: python manage.py runserver

Then open the link to view the UI: http://127.0.0.1:8000/

In this link, you can see options to upload different exercises and session sets as well as visualize progress over time. In the visualization section, there is an option to export data as an excel file.

You can also view the admin profile with the following link: http://127.0.0.1:8000/admin/, but is not required to use the application (all functionality is in main page).

The admin profile will allow you to remove existing entries in the database for exercises and session sets.


See ERD below.





