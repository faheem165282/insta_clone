# Product Requirements Document (PRD): Scalable Video Distribution Web Application

## 1. Project Overview

### 1.1 Purpose
This project aims to design, develop, and deploy a scalable, cloud-native web application that functions as a video distribution platform, similar to Instagram, for sharing photos. The application will be built using Flask, hosted on Azure App Service, and connected to an Azure Flexible MySQL Database. It will incorporate modern development and deployment practices, including scalability mechanisms, authentication, and advanced features to meet the requirements of the COM769 Scalable Advanced Software Systems module.

### 1.2 Scope
The application will support:
- **Creator Accounts**: Users who can upload photos with metadata (title, caption, location, people present).
- **Consumer Accounts**: Users who can view, search, comment, and rate photos.
- **Scalable Architecture**: Hosted on Azure with caching, dynamic DNS routing, and database persistence.
- **Deployment**: Fully deployed on Azure App Service with CI/CD integration.
- **Presentation**: A slide deck and 5-minute video demonstrating the solution.

### 1.3 Learning Outcomes Addressed
1. Demonstrate understanding of modern development and deployment concepts (e.g., cloud-native design, CI/CD).
2. Identify and address deficiencies in architectures and deployment paradigms.
3. Critically evaluate and apply modern development techniques for scalable solutions.

## 2. Functional Requirements

### 2.1 User Roles and Features
#### Creator Users
- **Upload Photos**: Upload photos via a dedicated creator view.
- **Set Metadata**: Add title, caption, location, and people present for each photo.
- **Manage Content**: View and delete their uploaded photos.
- **Authentication**: Secure login with role-based access control.

#### Consumer Users
- **View Photos**: Browse photos in a gallery format.
- **Search Photos**: Search by title, caption, or metadata.
- **Comment on Photos**: Add comments to photos.
- **Rate Photos**: Rate photos (e.g., 1-5 stars).
- **Authentication**: Secure login with role-based access control.

### 2.2 Core Features
- **Static HTML Hosting**: Serve front-end content using Flask templates.
- **REST API**: Backend REST endpoints for CRUD operations (Create, Read, Update, Delete) on photos, comments, and ratings.
- **Database Persistence**: Store user data, photos, and metadata in Azure Flexible MySQL Database.
- **Blob Storage**: Store photo files in Azure Blob Storage.
- **Authentication**: Implement user authentication using Azure Active Directory (AAD) or Flask-Login with role-based access.
- **Scalability Mechanisms**:
  - Caching with Azure Redis Cache for frequently accessed data.
  - Dynamic DNS routing via Azure Traffic Manager.
- **Advanced Features**:
  - Sentiment analysis on comments using Azure Cognitive Services.
  - Media conversion (e.g., image resizing) using Azure Functions.
  - CI/CD pipeline using Azure DevOps for automated deployment.

### 2.3 Non-Functional Requirements
- **Scalability**: Handle up to 1,000 concurrent users with minimal latency.
- **Availability**: 99.9% uptime using Azure App Service.
- **Security**: HTTPS encryption, secure authentication, and data protection.
- **Performance**: Page load time < 2 seconds for 90% of requests.
- **Cost**: Utilize free-tier Azure services where possible to minimize costs.

## 3. Technical Architecture

### 3.1 Tech Stack
- **Framework**: Flask (Python) for backend and front-end templating.
- **Database**: Azure Flexible MySQL Database for structured data.
- **Storage**: Azure Blob Storage for photo files.
- **Authentication**: Azure Active Directory or Flask-Login.
- **Caching**: Azure Redis Cache.
- **CI/CD**: Azure DevOps for continuous integration and deployment.
- **Hosting**: Azure App Service (Linux) for web app hosting.
- **Advanced Services**:
  - Azure Cognitive Services for sentiment analysis.
  - Azure Functions for media conversion.
- **Front-End**: HTML, CSS (Bootstrap), JavaScript for static content.

### 3.2 System Architecture
- **Front-End**: Static HTML pages served by Flask, interacting with REST APIs.
- **Backend**: Flask application handling REST endpoints, business logic, and database/storage interactions.
- **Database**: Azure Flexible MySQL Database storing user profiles, photo metadata, comments, and ratings.
- **Storage**: Azure Blob Storage for photo files, integrated with Flask via Azure SDK.
- **Authentication**: Azure AD or Flask-Login for user management and role-based access.
- **Scalability**:
  - Azure Redis Cache for caching photo metadata and user sessions.
  - Azure Traffic Manager for load balancing and dynamic DNS routing.
- **CI/CD**: Azure DevOps pipeline for automated testing and deployment.

### 3.3 Data Model
- **Users**:
  - `user_id` (PK), `username`, `email`, `password_hash`, `role` (creator/consumer).
- **Photos**:
  - `photo_id` (PK), `user_id` (FK), `title`, `caption`, `location`, `people`, `blob_url`, `upload_date`.
- **Comments**:
  - `comment_id` (PK), `photo_id` (FK), `user_id` (FK), `content`, `sentiment_score`, `created_at`.
- **Ratings**:
  - `rating_id` (PK), `photo_id` (FK), `user_id` (FK), `rating` (1-5), `created_at`.

## 4. Development Plan

### 4.1 Step-by-Step Implementation Guide
#### Step 1: Project Setup
1. **Set Up Local Environment**:
   - Install Python 3.9+ and pip.
   - Create a virtual environment: `python -m venv venv`.
   - Activate virtual environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows).
   - Install dependencies: `pip install flask flask-login flask-sqlalchemy azure-storage-blob azure-identity gunicorn`.
2. **Initialize Flask Project**:
   - Create project directory: `mkdir video-distribution-app && cd video-distribution-app`.
   - Create file structure:
     ```
     /video-distribution-app
     ├── /static
     │   ├── /css
     │   ├── /js
     │   ├── /images
     ├── /templates
     │   ├── base.html
     │   ├── creator_upload.html
     │   ├── consumer_view.html
     ├── /app
     │   ├── __init__.py
     │   ├── routes.py
     │   ├── models.py
     ├── requirements.txt
     ├── app.py
     ├── config.py
     ```
3. **Generate Requirements File**:
   - Run `pip freeze > requirements.txt`.

#### Step 2: Database and Storage Setup
1. **Create Azure Flexible MySQL Database**:
   - Log in to Azure Portal.
   - Create a new Azure Database for MySQL Flexible Server.
   - Configure firewall rules to allow local and Azure App Service access.
   - Note down connection details (host, username, password, database name).
2. **Set Up Azure Blob Storage**:
   - Create a storage account in Azure Portal.
   - Create a container for photo storage.
   - Obtain connection string or use managed identity for access.
3. **Configure Flask-SQLAlchemy**:
   - In `config.py`, set MySQL connection: `SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://<username>:<password>@<host>/<database>'`.
   - Define models in `app/models.py` for Users, Photos, Comments, and Ratings.
   - Initialize database: `flask db init`, `flask db migrate`, `flask db upgrade`.

#### Step 3: Implement Core Features
1. **Authentication**:
   - Use Flask-Login for session management.
   - Implement login, logout, and role-based access in `app/routes.py`.
   - Optionally, integrate Azure AD using `azure.identity`.
2. **Creator Features**:
   - Create upload form in `templates/creator_upload.html`.
   - Implement REST endpoint `/api/photos/upload` to handle photo uploads and metadata.
   - Store photos in Azure Blob Storage and metadata in MySQL.
3. **Consumer Features**:
   - Create gallery view in `templates/consumer_view.html`.
   - Implement REST endpoints:
     - `/api/photos` (GET): List photos.
     - `/api/photos/search` (GET): Search photos by metadata.
     - `/api/photos/<id>/comment` (POST): Add comment.
     - `/api/photos/<id>/rate` (POST): Add rating.
4. **Front-End**:
   - Use Bootstrap for responsive design.
   - Implement JavaScript for dynamic interactions (e.g., search, comment submission).

#### Step 4: Add Advanced Features
1. **Sentiment Analysis**:
   - Integrate Azure Cognitive Services Text Analytics.
   - Analyze comments on submission and store sentiment score in Comments table.
2. **Media Conversion**:
   - Create an Azure Function to resize uploaded images.
   - Trigger function on Blob Storage upload event.
3. **Caching**:
   - Set up Azure Redis Cache.
   - Cache photo metadata and user sessions.
4. **CI/CD Pipeline**:
   - Create Azure DevOps project.
   - Set up build pipeline to run tests and package app.
   - Configure release pipeline to deploy to Azure App Service.

#### Step 5: Deploy to Azure
1. **Create Azure App Service**:
   - In Azure Portal, create a new App Service (Linux, Python 3.9).
   - Configure application settings (e.g., MySQL connection string, Blob Storage credentials).
2. **Deploy Application**:
   - Use Azure CLI: `az webapp up -n <app-name> --sku B1 --resource-group <group>`.
   - Alternatively, use Azure DevOps release pipeline.
3. **Configure Scalability**:
   - Enable auto-scaling in App Service (1-5 instances based on CPU usage).
   - Set up Azure Traffic Manager for DNS routing.
4. **Test Deployment**:
   - Access app at `https://<app-name>.azurewebsites.net`.
   - Test all features (upload, view, comment, rate, search).

#### Step 6: Create Presentation and Video
1. **Slide Deck**:
   - Create PowerPoint with 13 slides as per coursework guidelines:
     - Slide 0: Title, student details.
     - Slides 1-2: Problem definition and scalability issues.
     - Slides 3-6: Technical solution overview (architecture diagram, tech stack).
     - Slides 7-8: Advanced features (sentiment analysis, media conversion, CI/CD).
     - Slides 9-10: Limitations and scalability assessment.
     - Slide 11: Video demonstration.
     - Slide 12: Conclusion.
     - Slide 13: References (IEEE format).
2. **Video Demonstration**:
   - Record a 5-minute video using screen recording software (e.g., OBS Studio).
   - Demonstrate:
     - Creator uploading a photo with metadata.
     - Consumer viewing, searching, commenting, and rating photos.
     - Backend operations (e.g., Azure Portal showing Blob Storage, MySQL, Redis).
     - Scalability features (e.g., Traffic Manager, auto-scaling).
   - Embed video in Slide 11.
3. **Upload Deliverables**:
   - Submit slide deck and source code to Blackboard by May 9, 2025.

### 4.2 Development Timeline
- **Week 7-8**: Set up project, database, and storage; implement authentication and core features.
- **Week 9**: Add advanced features (sentiment analysis, media conversion, caching).
- **Week 10**: Set up CI/CD pipeline and deploy to Azure.
- **Week 11**: Test deployment, create slide deck, and record video.
- **Week 12**: Finalize deliverables and submit by May 9, 2025.

## 5. Assessment Criteria Alignment
- **Problem Definition (10%)**: Discuss scalability challenges of photo-sharing apps and justify cloud-native design.
- **Technical Solution (15%)**: Document architecture with diagrams, justify Flask and Azure choices.
- **Advanced Features (20%)**: Implement sentiment analysis, media conversion, and CI/CD.
- **Limitations and Scalability (20%)**: Evaluate free-tier limitations and scalability mechanisms.
- **Video Demonstration (25%)**: Showcase all features and Azure deployment.
- **Concluding Comments (5%)**: Reflect on solution and suggest improvements.
- **Referencing (5%)**: Use IEEE format for all citations.

## 6. Risks and Mitigation
- **Risk**: Free-tier Azure limitations (e.g., database connections, Blob Storage quota).
  - **Mitigation**: Monitor usage, optimize queries, and use caching.
- **Risk**: Deployment errors in Azure App Service.
  - **Mitigation**: Use Azure DevOps for automated testing and rollback.
- **Risk**: Video exceeds 5 minutes.
  - **Mitigation**: Script video to ensure concise delivery.

## 7. References
- [1] Ulster University, "Student Guide," 2025. [Online]. Available: https://www.ulster.ac.uk/connect/guide.
- [2] Microsoft, "Deploy a Python (Django, Flask, or FastAPI) web app to Azure," 2024. [Online]. Available: https://learn.microsoft.com/en-us/azure/app-service/quickstart-python.
- [3] IEEE, "IEEE Citation Reference," 2025. [Online]. Available: https://www.ieee.org/documents/ieeecitationref.pdf.