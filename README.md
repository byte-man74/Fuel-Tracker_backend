# Petrol Price Tracking Application (Backend)

This repository contains the backend implementation of a petrol price tracking application built using the Python Django framework. The backend system provides the necessary APIs and functionality to manage user authentication, fuel station data, and price tracking features.

(NOTE: This a demo of the origjnal project and maximum security practices were not employed here. This repository is mainly just a representation of how the original product works and to also show whoever is viewing this that i know how to use Django)

## Features

- User Authentication: Implement user registration, login, and account management functionality.
- Fuel Station Management: Allow the addition, modification, and deletion of fuel stations by authenticated users.
- Price Tracking: Enable users to update and track the prices of fuel at various stations.
- Data Validation and Moderation: Implement mechanisms to validate user-submitted price updates and ensure the accuracy and credibility of the information.
- User Reputation System: Establish a reputation system to identify and promote users who consistently provide accurate price updates.
- Integration with External Data Sources: Integrate reliable external data sources to supplement user-submitted prices and improve data accuracy.
- Admin Dashboard: Develop an admin dashboard to manage and monitor the application, including user management, moderation, and data analysis.

## Installation

1. Clone the repository:


2. Navigate to the project directory:


3. Create a virtual environment:


4. Activate the virtual environment:

- For Linux/macOS:

  ```
  source env/bin/activate
  ```

- For Windows:

  ```
  .\env\Scripts\activate
  ```

5. Install the dependencies:


6. Set up the database:

- Update the database configuration in `settings.py` to match your environment.
- Run the database migrations:

  ```
  python manage.py migrate
  ```

7. Start the development server:


8. Access the backend API at `http://localhost:8000/` or as per the server configuration.

## Contributing

Contributions to this project are welcome. If you have any ideas, suggestions, or bug fixes, please create an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
