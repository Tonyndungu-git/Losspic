# Losspic

Losspic is a web application for compressing images using Singular Value Decomposition (SVD). This project is built with Django and incorporates a simple user interface for uploading images, performing SVD compression, and downloading the compressed images.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Image Compression:** Losspic utilizes Singular Value Decomposition to compress images efficiently.
- **User-Friendly Interface:** Simple and intuitive web interface for uploading, compressing, and downloading images.
- **Responsive Design:** The application is designed to be responsive and user-friendly on various devices.

## Installation

To run Losspic locally, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/Losspic.git
    ```

2. Navigate to the project directory:

    ```bash
    cd Losspic
    ```

3. Create a virtual environment (optional but recommended):

    ```bash
    # For Linux users
    python -m venv venv
    ```

4. Activate the virtual environment:

    - **Windows:**

        ```bash
        venv\Scripts\activate
        ```

    - **Linux/macOS:**

        ```bash
        source venv/bin/activate
        ```

5. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

6. Run the Django development server:

    ```bash
    python manage.py runserver
    ```

The application will be accessible at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## Usage

1. Access the Losspic application at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).
2. Upload an image using the provided form.
3. Click the "Compress" button to perform SVD compression on the image.
4. Download the compressed image.

## Contributing

Contributions are welcome! Follow these steps to contribute:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature`.
3. Commit your changes: `git commit -m 'Add a new feature'`.
4. Push to the branch: `git push origin feature/your-feature`.
5. Submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

