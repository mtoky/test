# Scalingo Python Test Site

A simple Python Flask application for testing deployment on Scalingo hosting platform.

## Application Structure

- `app.py`: Main Flask application file
- `Procfile`: Instructions for Scalingo on how to run the application
- `requirements.txt`: Python dependencies
- `templates/`: Directory containing HTML templates
  - `index.html`: Home page
  - `about.html`: About page
  - `contact.html`: Contact page
- `.python-version`: Specifies Python version (3.11)

## Deployment Instructions

### Prerequisites

- A Scalingo account
- Git installed on your machine
- Scalingo CLI (optional)

### Deployment Steps

1. Login to your Scalingo dashboard at https://dashboard.scalingo.com/

2. Create a new application from the dashboard

3. Connect your repository to Scalingo, or deploy using Git:

```bash
# Initialize git repository if not already done
git init
git add .
git commit -m "Initial commit"

# Add Scalingo remote
git remote add scalingo git@ssh.osc-fr1.scalingo.com:your-app-name.git

# Push to Scalingo
git push scalingo master
```

4. Your application should now be deployed and accessible at the URL provided by Scalingo.

## Local Development

To run this application locally:

1. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
flask run
```

The application will be available at http://localhost:5000/ 