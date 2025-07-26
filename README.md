# Personal Finance Tracker 💰🇮🇳 

A **modern, full-stack web application** built with Flask for tracking personal finances with **Indian Rupee (₹) support**, complete **REST API**, **JWT authentication**, **PostgreSQL support**, and **Docker deployment**.

## Features ✨

- **Indian Rupee (₹) Support** - All amounts displayed in Indian Rupees
- **REST API** - Complete RESTful API with Flask-RESTX and Swagger documentation
- **JWT Authentication** - Token-based API authentication with access/refresh tokens
- **User Authentication** - Secure web and API registration/login system
- **PostgreSQL Support** - Production-ready database with migrations (Alembic)
- **Docker Support** - Complete containerization with Docker Compose
- **CSV Upload** - Import financial data from CSV files with automatic processing
- **Interactive Dashboard** - View transactions with beautiful Plotly charts and analytics
- **PDF Reports** - Generate and download comprehensive financial reports with ₹ symbols
- **Email Reports** - Send PDF reports via email (with fallback to download)
- **Data Visualization** - Pie charts for categories, bar charts for monthly trends
- **Transaction Management** - Add, view, edit, and delete transactions via web and API
- **Real-time Analytics** - Category breakdown, monthly totals, and financial summaries
- **Responsive Design** - Modern Bootstrap 5 UI that works on all devices
- **Database Migrations** - Alembic-powered database schema management
- **CORS Support** - Cross-origin resource sharing for frontend applications

## Installation 🚀

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Personal-finance-tracker
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables for email (optional)**
   
   **For Email Reports Feature:**
   ```bash
   # Option 1: Set environment variables directly
   export MAIL_USERNAME="your_email@gmail.com"
   export MAIL_PASSWORD="your_app_password"
   
   # Option 2: Create a .env file (recommended)
   cp .env.example .env
   # Then edit .env file with your credentials
   ```
   
   **Gmail Setup Instructions:**
   1. Enable 2-factor authentication on your Gmail account
   2. Generate an "App Password" (not your regular password)
   3. Use the app password in MAIL_PASSWORD field
   
   **Note:** Email feature is optional. The app works without email configuration, but email reports will redirect to PDF download instead.

5. **Run the application**
   ```bash
   python run.py
   ```

6. **Access the application**
   - **Web Interface**: http://127.0.0.1:5000
   - **API Documentation**: http://127.0.0.1:5000/api/docs/
   - **API Base URL**: http://127.0.0.1:5000/api/v1/

## Quick Start 🚀

1. **Run the application** (if dependencies are already installed):
   ```bash
   # Activate virtual environment
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   
   # Start the server
   python run.py
   ```

2. **Access at**: http://127.0.0.1:5001

3. **Create account** and start uploading your financial data!

## Usage 📊

### Getting Started
1. **Register** a new account or **Login** with existing credentials
2. **Upload CSV** files containing your transaction data
3. **View Dashboard** with interactive charts and summaries
4. **Generate Reports** in PDF format or send via email

### CSV Format
Your CSV file should contain the following columns (amounts will be displayed in ₹):
```csv
date,category,amount,description
2024-01-01,Food,-500.50,Lunch at restaurant
2024-01-02,Salary,50000.00,Monthly salary
2024-01-03,Transport,-250.30,Auto rickshaw
2024-01-04,Groceries,-1200.00,Weekly shopping
2024-01-05,Investment,5000.00,SIP deposit
```

**Note:** 
- Negative amounts represent expenses
- Positive amounts represent income
- All amounts will be displayed with ₹ symbol in the dashboard

### Email Configuration
To enable email functionality:

1. **For Gmail users:**
   - Enable 2-factor authentication
   - Generate an "App Password" in your Google Account settings
   - Use your Gmail address as `MAIL_USERNAME`
   - Use the app password as `MAIL_PASSWORD`

2. **Set environment variables:**
   ```bash
   # Linux/Mac
   export MAIL_USERNAME="your_email@gmail.com"
   export MAIL_PASSWORD="your_app_password"
   
   # Windows
   set MAIL_USERNAME=your_email@gmail.com
   set MAIL_PASSWORD=your_app_password
   ```

## Indian Rupee (₹) Support 🇮🇳

This application is specifically designed for Indian users with complete Rupee support:

### Currency Features
- **All amounts displayed in ₹** - Dashboard, charts, and reports
- **Indian number formatting** - Comma-separated thousands (₹1,00,000)
- **Localized charts** - Plotly charts with ₹ symbols in tooltips and axes
- **PDF reports** - Professional reports with ₹ formatting
- **Email reports** - Currency-aware email content

### Typical Indian Categories Supported
- Salary, Business Income, Investments
- Groceries, Dining, Food & Beverages  
- Transport, Petrol, Auto/Taxi
- Shopping, Electronics, Clothing
- Bills, Rent, Utilities
- Healthcare, Insurance
- Entertainment, Travel
- Education, Books

## File Structure 📁

```
Personal-finance-tracker/
├── app/
│   ├── __init__.py          # Flask app factory with API and web support
│   ├── config.py            # Environment-based configuration
│   ├── models.py            # Database models (User, Transaction)
│   ├── routes.py            # Web routes with ₹ formatting
│   ├── auth.py              # Web authentication routes
│   ├── api/                 # REST API package
│   │   ├── __init__.py      # API initialization
│   │   ├── auth.py          # JWT authentication endpoints
│   │   ├── transactions.py  # Transaction CRUD endpoints
│   │   └── reports.py       # Report generation endpoints
│   ├── templates/           # HTML templates with Bootstrap 5
│   │   ├── base.html        # Base template with navigation
│   │   ├── index.html       # Landing page
│   │   ├── dashboard.html   # Main dashboard with charts
│   │   ├── upload.html      # CSV upload interface
│   │   ├── email_report.html # Email configuration
│   │   └── auth/            # Authentication templates
│   │       ├── login.html
│   │       └── register.html
│   ├── uploads/             # Uploaded CSV files
│   └── __pycache__/         # Python cache files
├── migrations/              # Database migrations (Alembic)
│   ├── env.py              # Migration environment
│   └── versions/           # Migration scripts
├── instance/
│   └── finance_tracker.db  # SQLite database (development)
├── .venv/                   # Virtual environment
├── .env.example            # Environment configuration template
├── docker-compose.yml      # Docker Compose configuration
├── Dockerfile              # Docker container definition
├── nginx.conf              # Nginx reverse proxy configuration
├── requirements.txt        # Python dependencies
├── pyproject.toml         # Project configuration
├── run.py                 # Application entry point
├── demo.py                # Demo setup script
├── test_api.py            # API testing script
├── sample_data.csv        # Sample data for testing
└── README.md             # This file
```

## Technologies Used 🛠️

- **Backend:** Flask 2.3.3, SQLAlchemy 2.0.32, Flask-Login 0.6.3
- **API:** Flask-RESTX 1.3.0, Flask-JWT-Extended 4.6.0, Swagger/OpenAPI 3.0
- **Database:** PostgreSQL 15+ (production), SQLite (development)
- **Migrations:** Alembic 1.12.1, Flask-Migrate 4.0.5
- **Frontend:** Bootstrap 5, Plotly.js 5.17.0, Responsive Design
- **PDF Generation:** ReportLab 4.0.4
- **Data Processing:** Pandas 2.0+
- **Email:** SMTP (Gmail/Outlook compatible)
- **Authentication:** JWT tokens, Flask-Login sessions
- **Deployment:** Docker, Docker Compose, Gunicorn
- **Reverse Proxy:** Nginx (optional)
- **Currency:** Indian Rupee (₹) support throughout
- **Python:** 3.13+ compatible
- **CORS:** Flask-CORS for API access

## Features in Detail 🔍

### Dashboard Analytics
- **Financial Overview:** Total income, expenses, and net balance in ₹
- **Category Breakdown:** Spending patterns by category with rupee amounts
- **Monthly Trends:** Time-based financial analysis with ₹ formatting
- **Interactive Charts:** Plotly-powered visualizations with hover tooltips in ₹
- **Real-time Calculations:** Automatic updates when new data is uploaded
- **API Integration:** Chart data available via REST API endpoints

### Report Generation
- **PDF Reports:** Comprehensive financial summaries with ₹ symbols
- **Email Delivery:** Automated report distribution (with fallback to download)
- **API Reports:** JSON format reports for external integrations
- **Transaction Details:** Complete transaction listings in tabular format
- **Visual Formatting:** Professional report layout with Indian currency formatting
- **Export Options:** Download via web or API endpoints

### API Features (New!)
- **RESTful Design:** Complete CRUD operations for all resources
- **JWT Authentication:** Secure token-based API access
- **Swagger Documentation:** Interactive API explorer at `/api/docs/`
- **CORS Enabled:** Cross-origin requests for frontend applications
- **Rate Limiting:** Built-in protection against API abuse
- **Versioning:** API versioned at `/api/v1/` for future compatibility
- **Error Handling:** Consistent JSON error responses
- **Pagination:** Efficient data retrieval for large datasets

### Database & Infrastructure
- **Multi-Database Support:** SQLite (dev) + PostgreSQL (production)
- **Database Migrations:** Alembic-powered schema management
- **Docker Support:** Complete containerization with orchestration
- **Environment Configuration:** Flexible config for different deployments
- **Health Checks:** Application and database health monitoring
- **Reverse Proxy:** Nginx configuration for production

### Security Features
- **User Authentication:** Secure login system
- **Data Isolation:** Users only see their own data
- **Password Hashing:** Secure password storage
- **Session Management:** Automatic session handling

## Troubleshooting 🔧

### Common Issues and Solutions

**Port 5001 already in use:**
```bash
# Kill existing Flask processes
pkill -f "python.*run.py"
# Then restart
python run.py
```

**Email not working:**
- Email feature is optional - app works without it
- If email fails, reports will automatically download as PDF
- Check `.env.example` for setup instructions

**CSV upload issues:**
- Ensure CSV has columns: date, category, amount, description
- Date format should be YYYY-MM-DD
- Amount should be numeric (negative for expenses)

**Database issues:**
```bash
# Delete and recreate database
rm instance/finance_tracker.db
python run.py  # Will recreate automatically
```

**Virtual environment issues:**
```bash
# Recreate virtual environment
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**API-related issues:**
```bash
# Test API endpoints
python test_api.py

# Check API documentation
# Visit: http://127.0.0.1:5000/api/docs/

# Verify JWT tokens
curl -X GET http://127.0.0.1:5000/api/v1/auth/profile \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Docker issues:**
```bash
# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up

# Check container logs
docker-compose logs web
docker-compose logs db
```

**Database migration issues:**
```bash
# Reset migrations
rm -rf migrations/
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## Performance & Scaling 📈

### Optimization Tips

**Database Optimization:**
- Use PostgreSQL for production (better performance than SQLite)
- Add database indexes for frequently queried fields
- Use connection pooling for high-traffic applications
- Regular database maintenance and VACUUM operations

**API Performance:**
- Implement caching for frequently accessed data
- Use pagination for large datasets
- Consider API rate limiting for production
- Monitor API response times and optimize slow endpoints

**Docker Performance:**
- Use multi-stage builds to reduce image size
- Implement health checks for better orchestration
- Use volume mounts for persistent data
- Configure resource limits for containers

### Scaling Considerations

**Horizontal Scaling:**
- Load balance multiple Flask instances
- Use Redis for session storage across instances
- Implement API gateway for request distribution
- Database read replicas for improved performance

**Monitoring & Logging:**
- Application performance monitoring (APM)
- Centralized logging with ELK stack
- Database performance monitoring
- API usage analytics and monitoring

## Contributing 🤝

We welcome contributions! Here's how you can help:

### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/yourusername/Personal-finance-tracker.git
   cd Personal-finance-tracker
   ```

2. **Set up development environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env
   ```

3. **Initialize database**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

4. **Run tests**
   ```bash
   python test_api.py
   pytest  # If you add unit tests
   ```

### Contribution Guidelines

- **Code Style**: Follow PEP 8 Python style guidelines
- **API Design**: Maintain RESTful principles for new endpoints
- **Documentation**: Update README and API docs for new features
- **Testing**: Add tests for new functionality
- **Currency**: Ensure all amounts display with ₹ symbol
- **Backward Compatibility**: Don't break existing web or API interfaces

### Areas for Contribution

- 🔐 **Security Enhancements**: Rate limiting, input validation
- 📱 **Mobile Support**: React Native or Flutter app using our API
- 📊 **Advanced Analytics**: Machine learning insights, budgeting features
- 🌍 **Internationalization**: Support for multiple currencies and languages
- ⚡ **Performance**: Caching, database optimization
- 🔧 **DevOps**: CI/CD pipelines, automated testing
- 🎨 **UI/UX**: Modern frontend framework integration

### Submitting Changes

1. Create a feature branch (`git checkout -b feature/amazing-feature`)
2. Make your changes with proper commit messages
3. Test thoroughly (web interface + API)
4. Update documentation if needed
5. Submit a pull request with detailed description

### API Development Guidelines

When adding new API endpoints:
- Use appropriate HTTP methods (GET, POST, PUT, DELETE)
- Include proper error handling and status codes
- Add Swagger documentation with `@api.doc()` decorators
- Ensure JWT authentication where required
- Format currency amounts with ₹ symbol
- Add input validation with Flask-RESTX models

## Support & Community 💬

### Getting Help

- **📖 Documentation**: Check this README for comprehensive guides
- **🐛 Issues**: Report bugs via GitHub Issues
- **💡 Feature Requests**: Suggest enhancements via GitHub Issues
- **📧 Contact**: Reach out for deployment or integration support

### FAQ

**Q: Can I use this for my business?**
A: Yes! This is open-source software. The API makes it easy to integrate with existing systems.

**Q: How do I migrate from SQLite to PostgreSQL?**
A: Update your `.env` file with PostgreSQL credentials, then run `flask db upgrade`.

**Q: Can I customize the currency?**
A: Currently optimized for Indian Rupees (₹). To change currency, update the `format_currency()` function in templates and API responses.

**Q: Is the API production-ready?**
A: Yes! It includes JWT authentication, proper error handling, CORS support, and Swagger documentation.

**Q: How do I backup my data?**
A: For SQLite: copy the `.db` file. For PostgreSQL: use `pg_dump` or your hosting provider's backup tools.

### Community Guidelines

- Be respectful and constructive
- Search existing issues before creating new ones
- Provide detailed information for bug reports
- Test your contributions thoroughly
- Help others in the community

### Roadmap 🗺️

- [ ] Mobile application (React Native/Flutter)
- [ ] Advanced budgeting and goal tracking
- [ ] Integration with Indian banks and payment systems
- [ ] Machine learning for expense categorization
- [ ] Multi-user family account support
- [ ] Cryptocurrency portfolio tracking
- [ ] Tax calculation and reporting features

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**What this means:**
- ✅ Commercial use
- ✅ Modification  
- ✅ Distribution
- ✅ Private use
- ❗ Must include license and copyright notice

---

## Acknowledgments 🙏

- **Flask Community** for the excellent web framework
- **Plotly** for beautiful interactive charts
- **Bootstrap** for responsive UI components
- **JWT** for secure API authentication
- **Contributors** who help improve this project
- **Users** who provide valuable feedback

---

*Built with ❤️ for the Indian finance community*

**Version**: 2.0.0 | **Last Updated**: 2024 | **Status**: Active Development

---

## Docker Deployment 🐳

### Quick Start with Docker Compose

1. **Clone and navigate to the repository**
   ```bash
   git clone <repository-url>
   cd Personal-finance-tracker
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start with Docker Compose**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - **Web Interface**: http://localhost
   - **API Documentation**: http://localhost/api/docs/
   - **Direct API**: http://localhost/api/v1/

### Manual Docker Build

```bash
# Build the image
docker build -t finance-tracker .

# Run with PostgreSQL
docker run -d --name postgres-db \
  -e POSTGRES_DB=finance_tracker \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=password \
  -p 5432:5432 postgres:15

# Run the application
docker run -d --name finance-app \
  -e DATABASE_URL=postgresql://postgres:password@postgres-db:5432/finance_tracker \
  -p 5000:5000 \
  --link postgres-db \
  finance-tracker
```

## API Usage 🔌

### Authentication

```bash
# Register a new user
curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword"
  }'

# Login to get JWT tokens
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "securepassword"
  }'
```

### Transactions

```bash
# Create a transaction (use token from login)
curl -X POST http://localhost:5000/api/v1/transactions/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "date": "2024-01-15",
    "category": "Food",
    "amount": -500.50,
    "description": "Lunch expense"
  }'

# Get all transactions
curl -X GET http://localhost:5000/api/v1/transactions/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Get financial summary
curl -X GET http://localhost:5000/api/v1/transactions/summary \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Reports

```bash
# Get detailed financial report
curl -X GET http://localhost:5000/api/v1/reports/summary \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Get chart data for visualization
curl -X GET http://localhost:5000/api/v1/reports/charts \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Download PDF report
curl -X POST http://localhost:5000/api/v1/reports/pdf \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  --output financial_report.pdf
```

## Database Migration 🗃️

### PostgreSQL Setup

1. **Install PostgreSQL**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install postgresql postgresql-contrib
   
   # macOS
   brew install postgresql
   ```

2. **Create database**
   ```bash
   sudo -u postgres psql
   CREATE DATABASE finance_tracker;
   CREATE USER finance_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE finance_tracker TO finance_user;
   \q
   ```

3. **Update environment variables**
   ```bash
   export DATABASE_URL=postgresql://finance_user:your_password@localhost:5432/finance_tracker
   ```

### Database Migrations

```bash
# Initialize migrations (first time only)
flask db init

# Create a new migration
flask db migrate -m "Add new feature"

# Apply migrations
flask db upgrade

# Downgrade if needed
flask db downgrade
```

## API Testing 🧪

### Using the Test Script

Run the comprehensive API test suite:

```bash
# Install requests for testing
pip install requests

# Run API tests
python test_api.py
```

The test script will:
- ✅ Register a new user
- ✅ Login and obtain JWT tokens
- ✅ Create sample transactions
- ✅ Test all CRUD operations
- ✅ Generate reports and charts
- ✅ Test authentication flows

### Manual API Testing

**1. Interactive API Documentation**
Visit http://127.0.0.1:5000/api/docs/ for interactive Swagger UI

**2. Command Line Testing**
```bash
# Set base URL
API_BASE="http://127.0.0.1:5000/api/v1"

# Register user
curl -X POST "$API_BASE/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com", 
    "password": "password123"
  }'

# Login (save the access_token from response)
curl -X POST "$API_BASE/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'

# Use token for authenticated requests
TOKEN="your_access_token_here"

# Create transaction
curl -X POST "$API_BASE/transactions/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "date": "2024-01-15",
    "category": "Food",
    "amount": -500.50,
    "description": "Lunch expense"
  }'

# Get financial summary
curl -X GET "$API_BASE/transactions/summary" \
  -H "Authorization: Bearer $TOKEN"
```

## Production Deployment 🚀

### Environment Variables

Create a `.env` file for production:

```bash
# Production Configuration
FLASK_ENV=production
SECRET_KEY=your-super-secure-secret-key-32-chars-min
JWT_SECRET_KEY=your-jwt-secret-key-different-from-above

# PostgreSQL Database
DATABASE_URL=postgresql://username:password@hostname:5432/database_name

# Email Configuration (optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Security (for production)
JWT_ACCESS_TOKEN_EXPIRES=3600  # 1 hour
JWT_REFRESH_TOKEN_EXPIRES=604800  # 7 days
```

### Deployment Options

**Option 1: Docker Compose (Recommended)**
```bash
# Production deployment
docker-compose -f docker-compose.yml up -d

# With custom environment
docker-compose --env-file .env.prod up -d
```

**Option 2: Manual Deployment**
```bash
# Install dependencies
pip install -r requirements.txt

# Set up PostgreSQL database
createdb finance_tracker

# Run migrations
flask db upgrade

# Start with Gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 4 run:app
```

**Option 3: Cloud Deployment**
- **Heroku**: Works out-of-the-box with PostgreSQL addon
- **AWS ECS**: Use provided Dockerfile
- **Google Cloud Run**: Container-ready deployment
- **DigitalOcean Apps**: Direct GitHub integration

### Security Considerations

- Change all default secrets in production
- Use environment variables for sensitive data
- Enable HTTPS with SSL certificates
- Configure firewall and security groups
- Use strong JWT secret keys (32+ characters)
- Enable database connection encryption
- Regular security updates

## Architecture Overview 🏗️

```
┌─────────────────────────────────────────────────────────────┐
│                    Personal Finance Tracker                  │
│                         Architecture                         │
└─────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   API Clients   │    │   Mobile Apps   │
│   (Bootstrap)   │    │   (External)    │    │   (Future)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
         ┌─────────────────────────────────────────────────┐
         │              Nginx (Reverse Proxy)             │
         │          - SSL Termination                     │
         │          - Load Balancing                      │
         │          - Static File Serving                 │
         └─────────────────────────────────────────────────┘
                                 │
         ┌─────────────────────────────────────────────────┐
         │              Flask Application                  │
         │                                                 │
         │  ┌─────────────────┐  ┌─────────────────────┐    │
         │  │   Web Routes    │  │     REST API        │    │
         │  │                 │  │                     │    │
         │  │ • Dashboard     │  │ • /api/v1/auth/     │    │
         │  │ • Authentication│  │ • /api/v1/trans*/   │    │
         │  │ • Reports       │  │ • /api/v1/reports/  │    │
         │  │ • File Upload   │  │ • Swagger Docs      │    │
         │  └─────────────────┘  └─────────────────────┘    │
         │                                                 │
         │  ┌─────────────────────────────────────────────┐ │
         │  │           Authentication Layer              │ │
         │  │                                             │ │
         │  │ ┌─────────────┐    ┌──────────────────────┐ │ │
         │  │ │ Flask-Login │    │   JWT Authentication │ │ │
         │  │ │ (Web)       │    │   (API)              │ │ │
         │  │ └─────────────┘    └──────────────────────┘ │ │
         │  └─────────────────────────────────────────────┘ │
         │                                                 │
         │  ┌─────────────────────────────────────────────┐ │
         │  │              Business Logic                 │ │
         │  │                                             │ │
         │  │ • Transaction Management                    │ │
         │  │ • Financial Calculations                    │ │
         │  │ • Report Generation                         │ │
         │  │ • Data Validation                           │ │
         │  │ • Currency Formatting (₹)                   │ │
         │  └─────────────────────────────────────────────┘ │
         └─────────────────────────────────────────────────┘
                                 │
         ┌─────────────────────────────────────────────────┐
         │              Data Layer                         │
         │                                                 │
         │  ┌─────────────────┐  ┌─────────────────────┐    │
         │  │   SQLAlchemy    │  │      Alembic        │    │
         │  │     (ORM)       │  │   (Migrations)      │    │
         │  └─────────────────┘  └─────────────────────┘    │
         └─────────────────────────────────────────────────┘
                                 │
    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
    │     SQLite      │    │   PostgreSQL    │    │     Redis       │
    │  (Development)  │    │   (Production)  │    │   (Sessions)    │
    └─────────────────┘    └─────────────────┘    └─────────────────┘
```
