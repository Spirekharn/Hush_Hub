# Hush Hub

Hush_Hub is a mental health site were people can share their problems anonymously and receive the help they require.
## Features

*   **User Roles**: Distinct roles for **Patients** and **Therapists** to tailor the experience.
*   **Anonymous Posting**: Share thoughts and experiences without revealing your identity.
*   **Community Feed**: Engage with the broader community through posts, likes, and comments.
*   **Private Chat**: Secure, real-time messaging for private conversations between connected users.
*   **Connection System**: Send and accept connection requests to build your support network.
*   **Gamification**: Earn points and badges (Bronze, Silver, Gold) for active participation and support.
*   **Self-Care Tools**:
    *   **Mood Tracker**: Log and monitor your emotional well-being over time.
    *   Breathing Exercises (integrated in self-care section).
*   **Profile Management**: View your progress, badges, and activity history.

## Tech Stack

*   **Backend**: Django 5.2.6 (Python)
*   **Database**: SQLite (Default)
*   **Frontend**: HTML, CSS (Django Templates)

## Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd Hush_Hub
    ```

2.  **Create a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install django
    ```

4.  **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

6.  **Access the application:**
    Open your web browser and go to `http://127.0.0.1:8000/`.

## Usage

1.  **Register** a new account as a Patient or Therapist.
2.  **Login** to access the dashboard.
3.  Navigate to the **Community** tab to view and interact with posts.
4.  Use the **Create Post** button to share your thoughts (anonymously or publicly).
5.  Visit the **Self-Care** section to log your mood.
6.  Connect with other users and start a **Chat**.

## Contributing

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/YourFeature`).
3.  Commit your changes (`git commit -m 'Add some feature'`).
4.  Push to the branch (`git push origin feature/YourFeature`).
5.  Open a Pull Request.
