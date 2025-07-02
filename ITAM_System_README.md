# ITAM System - IT Asset Management Solution

## Overview

This is a complete IT Asset Management (ITAM) system built with Django REST Framework backend and Vue.js frontend. The system provides comprehensive asset tracking, management, and reporting capabilities for organizations.

## Features

### Core ITAM Functionality
- **Asset Management**: Complete lifecycle tracking of IT assets
- **Category Management**: Organize assets by categories with hierarchical structure
- **Location Management**: Track asset locations and movements
- **Vendor Management**: Manage vendor relationships and contracts
- **User Management**: Role-based access control
- **Assignment Tracking**: Asset check-in/check-out functionality
- **Maintenance Scheduling**: Preventive and corrective maintenance tracking
- **Dashboard & Analytics**: Real-time statistics and insights
- **History & Audit Trail**: Complete asset history tracking

### Technical Features
- **Modern UI**: Material Design with Vuetify components
- **Responsive Design**: Works on desktop, tablet, and mobile
- **REST API**: Comprehensive API for all operations
- **Real-time Updates**: Live dashboard statistics
- **Search & Filtering**: Advanced search capabilities
- **Data Export**: Export capabilities for reporting
- **Barcode/QR Support**: Asset tagging and scanning

## Technology Stack

### Backend
- **Django 5.2.3**: Web framework
- **Django REST Framework**: API development
- **SQLite**: Database (easily upgradeable to PostgreSQL)
- **Django CORS Headers**: Cross-origin resource sharing

### Frontend
- **Vue.js 3**: Progressive JavaScript framework
- **Vuetify 3**: Material Design component library
- **TypeScript**: Type-safe JavaScript
- **Axios**: HTTP client for API communication
- **Pinia**: State management
- **Vue Router**: Client-side routing

## Installation & Setup

### Prerequisites
- Python 3.11+
- Node.js 20+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd itam_backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install django djangorestframework django-cors-headers
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start development server:**
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd itam-frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```

4. **Access the application:**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000/api/v1/itam/api/
   - Django Admin: http://localhost:8000/admin/

## API Endpoints

### Assets
- `GET /api/v1/itam/api/assets/` - List all assets
- `POST /api/v1/itam/api/assets/` - Create new asset
- `GET /api/v1/itam/api/assets/{id}/` - Get asset details
- `PUT /api/v1/itam/api/assets/{id}/` - Update asset
- `DELETE /api/v1/itam/api/assets/{id}/` - Delete asset
- `POST /api/v1/itam/api/assets/{id}/assign/` - Assign asset
- `POST /api/v1/itam/api/assets/{id}/unassign/` - Unassign asset
- `GET /api/v1/itam/api/assets/{id}/history/` - Get asset history

### Categories
- `GET /api/v1/itam/api/categories/` - List categories
- `POST /api/v1/itam/api/categories/` - Create category
- `PUT /api/v1/itam/api/categories/{id}/` - Update category
- `DELETE /api/v1/itam/api/categories/{id}/` - Delete category

### Locations
- `GET /api/v1/itam/api/locations/` - List locations
- `POST /api/v1/itam/api/locations/` - Create location
- `PUT /api/v1/itam/api/locations/{id}/` - Update location
- `DELETE /api/v1/itam/api/locations/{id}/` - Delete location

### Vendors
- `GET /api/v1/itam/api/vendors/` - List vendors
- `POST /api/v1/itam/api/vendors/` - Create vendor
- `PUT /api/v1/itam/api/vendors/{id}/` - Update vendor
- `DELETE /api/v1/itam/api/vendors/{id}/` - Delete vendor

### Dashboard
- `GET /api/v1/itam/api/dashboard/stats/` - Get dashboard statistics
- `GET /api/v1/itam/api/dashboard/alerts/` - Get system alerts

### Users
- `GET /api/v1/itam/api/users/` - List users

### Assignments
- `GET /api/v1/itam/api/assignments/` - List assignments
- `POST /api/v1/itam/api/assignments/` - Create assignment

### Maintenance
- `GET /api/v1/itam/api/maintenance/` - List maintenance records
- `POST /api/v1/itam/api/maintenance/` - Create maintenance record
- `PUT /api/v1/itam/api/maintenance/{id}/` - Update maintenance record
- `DELETE /api/v1/itam/api/maintenance/{id}/` - Delete maintenance record

## Database Schema

### Asset Model
- `asset_tag`: Unique identifier
- `name`: Asset name
- `description`: Detailed description
- `category`: Foreign key to AssetCategory
- `brand`: Manufacturer brand
- `model`: Model number
- `serial_number`: Serial number
- `status`: Current status (available, assigned, maintenance, etc.)
- `condition`: Physical condition
- `location`: Foreign key to Location
- `assigned_to`: Foreign key to User
- `vendor`: Foreign key to Vendor
- `purchase_date`: Purchase date
- `purchase_cost`: Purchase cost
- `warranty_start_date`: Warranty start
- `warranty_end_date`: Warranty end
- `notes`: Additional notes

### AssetCategory Model
- `name`: Category name
- `description`: Category description
- `icon`: Material Design icon
- `is_active`: Active status

### Location Model
- `name`: Location name
- `address`: Physical address
- `city`: City
- `state`: State/Province
- `country`: Country
- `postal_code`: Postal code
- `contact_person`: Contact person
- `contact_email`: Contact email
- `contact_phone`: Contact phone

### Vendor Model
- `name`: Vendor name
- `contact_person`: Contact person
- `email`: Email address
- `phone`: Phone number
- `address`: Address
- `website`: Website URL
- `notes`: Additional notes

## Configuration

### Environment Variables
Create a `.env` file in the backend directory:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

### Frontend Configuration
Update `src/services/api.ts` for production:

```typescript
const api = axios.create({
  baseURL: 'https://your-api-domain.com/api/v1/itam/api',
  // ... other config
})
```

## Production Deployment

### Backend Deployment
1. Use a production WSGI server like Gunicorn
2. Configure a reverse proxy (Nginx)
3. Use PostgreSQL for production database
4. Set up SSL certificates
5. Configure environment variables

### Frontend Deployment
1. Build the production version:
   ```bash
   npm run build
   ```
2. Deploy the `dist` folder to a web server
3. Configure routing for SPA

## Security Considerations

- Change default secret keys
- Use HTTPS in production
- Implement proper authentication
- Set up CSRF protection
- Configure CORS properly
- Regular security updates

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please contact the development team or create an issue in the repository.

---

**Built with ❤️ for efficient IT Asset Management**

