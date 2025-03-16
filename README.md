# Bobyard Challenge Backend

## Tech Stack
- **Backend Framework**: FastAPI
- **Database**: PostgreSQL (using SQLAlchemy for ORM)
- **Environment Management**: Python Dotenv
- **Asynchronous Support**: SQLAlchemy Async
- **Dependency Management**: pip with requirements.txt

## Setup Instructions

### Prerequisites
- Ensure you have Python 3.11 or higher installed.
- PostgreSQL should be installed and running on your machine.

### Environment Setup
1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv .venv
   ```

3. **Activate the Virtual Environment**
   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set Up Environment Variables**
   - Create a `.env` file in the root directory of the project and add the following variables:
     ```env
     DATABASE_URL=postgresql+asyncpg://<username>:<password>@<host>:<port>/<database>
     DB_NAME=<your_db_name>
     DB_USER=<your_db_user>
     DB_PASSWORD=<your_db_password>
     DB_HOST=<your_db_host>
     DB_PORT=<your_db_port>
     ```

### Running the Application
1. **Start the FastAPI Server**
   ```bash
   uvicorn main:app --reload
   ```

2. **Access the API**
   - Open your browser and navigate to `http://127.0.0.1:8000/docs` to view the interactive API documentation.

### Database Migration
- The script for populating the data is at /resources directory.
- 
