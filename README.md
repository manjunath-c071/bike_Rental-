# RideNova - Bike Rental Web Application

A full-stack bike rental web application inspired by Royal Brothers, built with Django, Bootstrap, and SQLite.

## ✨ New Advanced Features (v2.0)

### 🎛️ Admin Dashboard & Inline Editing
- **Web-based Admin Panel**: Manage bikes and locations directly from website pages
- **Admin Toolbar**: Purple admin toolbar appears when logged in as admin
- **Inline Editing**: Edit content with modal popups (no Django admin panel needed)
- **Admin-only Access**: Controls only visible to superusers with staff permissions
- **Real-time Updates**: Changes apply immediately with page reload

### 💳 Payment System
- **Payment Processing**: Complete payment workflow after bookings
- **Multiple Payment Methods**: Cards, UPI, Digital Wallets, Checks
- **Payment Tracking**: Track payment status (Pending, Processing, Completed, Failed, Refunded)
- **Payment History**: Users can view all their payments with details
- **Admin Refunds**: Admins can process refunds for completed payments
- **Transaction IDs**: Unique tracking for each payment

### 🔐 Enhanced Security & Authorization
- **Role-based Access**: Different permissions for users vs admins
- **Admin Decorators**: `@admin_required` decorator for protected endpoints
- **CSRF Protection**: All AJAX requests validated
- **User Isolation**: Users only see their own data
- **API Endpoints**: Secure RESTful API for inline editing

## Features

### User Features
- **User Authentication**: Sign up, login, and logout functionality
- **User Profiles**: Complete profile management with driving license details
- **Bike Browsing**: Browse available bikes with advanced filtering options
- **Bike Filtering**: Filter bikes by city, type, and price
- **Booking System**: Easy and intuitive booking with date/time selection
- **Location Selection**: Multiple pickup and return location options with modal interface
- **Booking History**: View complete booking history with status tracking
- **Insurance Options**: Add insurance protection to bookings
- **Cost Calculation**: Real-time cost calculation based on rental duration
- **Payment Processing**: Secure payment after booking confirmation
- **Payment History**: View all payments and transactions

### Admin Features (NEW ✨)
- **Admin Dashboard**: Comprehensive dashboard with statistics and analytics
- **Inline Bike Management**: Edit bikes directly from website pages (no Django admin)
- **Inline Location Management**: Edit locations with inline editing
- **User Management**: View and manage all users
- **Booking Management**: View and manage all bookings
- **Payment Management**: View all payments and process refunds
- **Analytics**: View revenue, booking trends, and top-performing bikes
- **Web-based Controls**: Admin toolbar with edit mode toggle

## Tech Stack

- **Backend**: Django 6.0.3
- **Frontend**: HTML5, CSS3, Bootstrap 4.5
- **JavaScript**: Vanilla JavaScript + AJAX for interactive features
- **Database**: SQLite
- **Package Manager**: pip
- **Payment Ready**: Easy integration with payment gateways

## Project Structure

```
RideNova/
├── config/                 # Django project configuration
│   ├── __init__.py
│   ├── settings.py        # Django settings
│   ├── urls.py            # Main URL configuration
│   ├── wsgi.py            # WSGI configuration
│   ├── asgi.py            # ASGI configuration
│   └── admin_urls.py      # Admin dashboard URLs
├── users/                  # User app
│   ├── models.py          # UserProfile model
│   ├── views.py           # Authentication and profile views
│   ├── forms.py           # User forms
│   ├── urls.py            # User app URLs
│   ├── admin.py           # Admin customization
│   └── signals.py         # Django signals for profile creation
├── bikes/                  # Bikes app
│   ├── models.py          # Bike model
│   ├── views.py           # Bike listing and detail views
│   ├── admin_views.py     # Admin dashboard views
│   ├── urls.py            # Bikes app URLs
│   ├── admin.py           # Admin customization
├── bookings/              # Bookings app
│   ├── models.py          # Booking model
│   ├── views.py           # Booking views
│   ├── urls.py            # Bookings app URLs
│   ├── admin.py           # Admin customization
├── templates/             # HTML templates
│   ├── base.html          # Base template with navbar and footer
│   ├── home.html          # Home page
│   ├── users/             # User templates
│   ├── bikes/             # Bikes templates
│   ├── bookings/          # Bookings templates
│   └── admin/             # Admin dashboard templates
├── static/                # Static files (CSS, JavaScript, images)
│   ├── css/               # CSS files
│   └── js/                # JavaScript files
├── media/                 # User-uploaded files
├── manage.py              # Django management script
├── db.sqlite3             # SQLite database
└── requirements.txt       # Python dependencies
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone or download the project**
   ```bash
   cd RideNova
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv virt
   # On Windows
   .\virt\Scripts\Activate.ps1
   # On macOS/Linux
   source virt/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install django pillow
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser for admin**
   ```bash
   python manage.py createsuperuser
   ```

6. **Load sample data (optional)**
   ```bash
   python load_sample_data.py
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Open your browser and go to: `http://localhost:8000`
   - Admin panel: `http://localhost:8000/admin/`
   - Admin dashboard: `http://localhost:8000/dashboard/` (staff only)

## Default Credentials

After setup, you can use these credentials to test:
- **Admin Username**: admin
- **Admin Password**: admin123

Create test user accounts through the sign-up page.

## Key Models

### User Profile
- Extended user profile with driving license details
- Profile picture support
- Address information
- License verification status

### Bike
- Bike details (brand, model, year, color)
- Type classification (MTB, Road, Hybrid, etc.)
- Pricing (hourly and daily rates)
- City-based location
- Availability status
- Condition tracking

### Booking
- User and bike associations
- Start and end date/time
- Pickup and return location selection
- Automatic cost calculation
- Insurance option
- Status tracking

## Features in Detail

### Bike Filtering
- Filter by city
- Filter by bike type
- Filter by price range
- Real-time filter updates

### Booking System
- Select rental dates and times
- Choose pickup and return locations
- Automatic cost calculation
- Optional insurance (5% of rental cost)
- Booking confirmation and details

### Admin Dashboard
- Overview statistics (users, bikes, bookings, revenue)
- User management
- Bike management and analytics
- Booking management
- Revenue tracking

## Authentication & Authorization

- **Regular Users**: Can browse bikes, make bookings, view booking history, and manage profiles
- **Staff Users**: Can access the admin dashboard to manage bikes, bookings, and users
- **Admin/Superuser**: Full access to Django admin panel
- **Regular users CANNOT access the admin panel** - only staff/superusers can

## Advanced Features (v2.0)

### Payment System

The application now includes a complete payment processing system:

- **Payment Processing**: Users must complete payment after booking
- **Multiple Payment Methods**: Support for Cards, UPI, Wallets, and Checks
- **Payment Status Tracking**: Pending → Processing → Completed/Failed → Refunded
- **Payment History**: Users can view all their payments
- **Admin Refunds**: Admins can process refunds for completed payments
- **Transaction IDs**: Unique identifiers for each payment
- **Easy Gateway Integration**: Ready for Stripe, PayPal, Razorpay integration

**Access Payment Features:**
- User Payment: `http://localhost:8000/payments/booking/<booking_id>/`
- Payment History: `http://localhost:8000/payments/history/`
- Admin Payments: `http://localhost:8000/payments/admin/payments/`

### Admin Inline Editing

Admins can edit bikes and locations directly from website pages without using Django admin:

1. **Login as Admin** - Purple toolbar appears at top
2. **Click "✎ Edit Mode"** - Editable items get blue borders
3. **Hover & Click Edit** - Opens edit modal
4. **Make Changes** - Form opens with current data
5. **Save** - Changes apply immediately

**Editable Elements:**
- **Bikes**: Name, Hourly Price, Availability
- **Locations**: Name, Icon/Emoji, Description

### Admin Dashboard

Enhanced admin dashboard with:
- Real-time statistics (Users, Bikes, Bookings, Revenue)
- Recent bookings display
- Top performing bikes
- Quick management links
- Payment processing overview

**Access Dashboard:**
- Admin Dashboard: `http://localhost:8000/dashboard/`
- Requires login as superuser with staff permissions

## Security & Admin Controls

### Permission System
- `@admin_required` decorator protects admin views
- Admin controls only visible to superusers with staff status
- All admin API endpoints require CSRF tokens
- User isolation - users only see their own data
- Regular users cannot access admin features

### Admin API Endpoints
- `POST /api/admin/bike/<id>/update/` - Update bike
- `POST /api/admin/bike/<id>/delete/` - Delete bike
- `POST /api/admin/location/<id>/update/` - Update location
- `POST /api/admin/location/<id>/delete/` - Delete location

## Future Enhancements

- Real payment gateway integration (Stripe, PayPal, Razorpay)
- Email and SMS notifications
- Advanced analytics with charts
- Multi-language support
- Mobile app
- Real-time location tracking
- Review and rating system
- Admin activity logging
- Bulk operations for admins
- Subscription plans
- API endpoints for mobile app

## Customization

### Adding New Bike Types
Edit `bikes/models.py` and update the `BIKE_TYPES` choices.

### Changing Colors and Styling
Edit `templates/base.html` CSS section or create custom CSS files in `static/css/`.

### Adding New Cities
Edit `bikes/models.py` and update the `CITIES` choices.

## Troubleshooting

### Virtual environment not activating
- Make sure you're in the project root directory
- Try: `python -m pip install --upgrade pip`

### Database issues
- Delete `db.sqlite3` and run migrations again
- Make sure migrations are applied: `python manage.py migrate`

### Static files not loading
- Run: `python manage.py collectstatic`
- Make sure `DEBUG = True` in settings.py

### Port already in use
- Use: `python manage.py runserver 8001` (or another port)

## License

This project is open source and available for educational purposes.

## Support

For issues or questions, please create an issue in the project repository.

---

**Happy bike renting with RideNova!** 🚴‍♂️
