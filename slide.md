# PhotoShare: Easy Media Sharing Platform for Photos and Videos

## Student Name: [Your Name]
## Student Number: [Your Student Number]

---

## Slide 1: Problem Statement

Today, people want to share many photos and videos online. This creates many problems that need solving:

- Different types of users need different permissions (creators who upload, consumers who view)
- Need to show both photos and videos in good quality
- Website must work well on all devices like mobiles and computers
- Users must login safely with password protection
- System must store many big files without becoming slow
- All this must work in cloud for good performance

---

## Slide 2: Scalability Challenges

When we make a website like PhotoShare, we face many challenges:

- **Storage problems**: How to save many photos and videos as users upload more
- **Database problems**: How to connect users, photos, comments and likes without slowness
- **Login problems**: How to let many users log in at same time with different roles
- **Photo and video problems**: How to handle different file types and control their size
- **Speed problems**: How to send photos and videos to users quickly
- **Location problems**: How to make website fast for users in different countries

---

## Slide 3: Technical Architecture Overview

For PhotoShare, we used these technologies:

- **Frontend**: We used HTML/CSS with Bootstrap to make website look good on mobile
- **Backend**: We used Python Flask because it is easy to organize code
- **Database**: We used Azure flexible MySQL database (with education subscription limits)
- **App Hosting**: We used Azure App Service with Python 3.12 runtime
- **User system**: We made simple login system with role-based access
- **Website organization**: We separated system into different parts to make it easier

---

## Slide 4: Core Components and Implementation

**User System**:
- Two types of users: creators (who upload) and consumers (who view)
- Passwords saved securely with hashing so no one can see them
- Flask-Login helps remember user when they come back to website

**Photo and Video System**:
- Users can upload both photos and videos with titles and descriptions
- Size limits to protect server (5MB for photos, 50MB for videos)
- System checks if files are correct type to prevent bad files

**Comment and Like System**:
- Users can write comments on photos and videos
- Users can like content (easier than star ratings)
- Search box helps find photos by title, location or people

---

## Slide 5: Database Design and Data Flow

**Database Tables**:
- User table: Stores usernames, emails, passwords and roles
- Photo table: Stores photos, videos and their details
- Comment table: Stores what users say about photos and videos
- Like table: Records which users liked which photos

**How Data Moves**:
- Upload process: Check file → Save file → Add to database
- View process: Find in database → Get file → Show to user
- Comment process: Write comment → Save to database → Show to everyone

---

## Slide 6: Azure Cloud Services We Used

We deployed PhotoShare using Azure services with education subscription:

- **Azure App Service**: This runs our Python 3.12 web application code
- **Azure Flexible MySQL Database**: This stores all our user data and photo information
- **File storage system**: We save photos and videos in organized folders
- **Web security**: We protect our app with login system
- **Python libraries**: We used Flask framework to build website faster
- **Limited resources**: We carefully managed education subscription limits

---

## Slide 7: Special Features: Photo and Video Handling

**Smart Media System**:
- Website knows difference between photos and videos automatically
- Videos play directly in browser with easy controls
- Photos and videos resize to fit any screen size
- System checks file types to make sure they are safe

**Extra Information for Media**:
- Users can add location to show where photo was taken
- Users can tag people who appear in photos
- Search works on titles, locations and people names
- System shows upload date so newest content appears first

---

## Slide 8: Making Website Fast

**How We Made Website Fast**:
- Pages load quickly without waiting for all content
- Made photo and video files smaller but still good quality
- Made database run faster with proper organization
- Used different ways to make website faster:
  - Browser remembers things it already downloaded
  - Important parts of website load first
  - Database remembers common questions
  - Azure services help deliver content faster

---

## Slide 9: Limitations Because of Education Subscription

**Current Limitations**:
- Can only use few types of photo and video formats
- Simple search that cannot do complex filtering
- No system to check for bad content
- Cannot see advanced statistics of website usage
- Simple login system without extra security
- Limited Azure resources with education subscription

---

## Slide 10: How Our Website Can Grow

**Features That Help Website Grow**:
- Keeping photos separate from main website code
- Database can handle many users at same time
- Size limits stop users from using too much space
- Database tables are organized well
- Code is divided into small parts for easy updates

**How We Can Make Website Bigger**:
- Azure App Service can add more power when needed
- Azure MySQL can handle more data as website grows
- Can use storage in different locations for faster speed
- Can work with limited education subscription resources

---

## Slide 11: Demonstration of Our Website

In this video I will show:

1. How users register and log in
2. How creators upload photos and videos
3. How creators add titles and descriptions
4. How consumers view and search for photos
5. How consumers comment and like content
6. How website looks on mobile and computer
7. How we deployed to Azure with Python 3.12 and MySQL

[5-minute video will be embedded here]

---

## Slide 12: Conclusion

PhotoShare is a good website for sharing photos and videos because:

- It has two types of users - creators who upload and consumers who view
- It can handle both photos and videos with proper size limits
- It works well on both mobile phones and computers
- It uses Azure cloud services (App Service and MySQL database)
- It keeps user information safe with password protection
- It can be improved and made bigger in the future
- It works within the limits of education subscription

---

## Slide 13: References

- Azure App Service: https://docs.microsoft.com/en-us/azure/app-service/
- Azure Database for MySQL: https://docs.microsoft.com/en-us/azure/mysql/
- Python Flask: https://flask.palletsprojects.com/
- Bootstrap: https://getbootstrap.com/docs/
- SQLAlchemy: https://docs.sqlalchemy.org/
- HTML5 Video: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/video
