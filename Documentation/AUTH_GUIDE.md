## 🔐 SafeBank AI - Authentication System Guide

## Overview

SafeBank AI now includes a **secure authentication system** with login, signup, and user profile management. The system uses SQLite for local storage and SHA-256 for password hashing.

---

## 🚀 Quick Start

### Launch with Authentication

```bash
# Windows
run_with_auth.bat

# Or manually
streamlit run app_with_auth.py
```

### Access
```
http://localhost:8501
```

---

## ✨ Features

### 🔐 Login Page
- **Clean fintech design** with gradient background
- **Email and password** authentication
- **"Forgot Password"** link (placeholder)
- **"Remember me"** checkbox
- **Switch to signup** option
- **Form validation** with error messages
- **Secure authentication** using SHA-256 hashing

### 📝 Signup Page
- **Full name, email, password** fields
- **Confirm password** validation
- **Password strength** indicator
- **Email format** validation
- **Duplicate account** prevention
- **Terms of service** checkbox
- **Auto-redirect** to login after successful signup
- **Success animation** with balloons

### 👤 Profile Page
- **User avatar** with initial
- **Profile information** card
- **Account details** (ID, email, member since, last login)
- **Edit profile** functionality
- **Update name** feature
- **Logout** button

### 🛡️ Dashboard (After Login)
- **Full access** to all fraud detection features
- **User info** in header
- **Sidebar navigation** with user profile
- **Single Transaction** analysis
- **Batch Processing** with CSV upload
- **Analytics** dashboard
- **System Info** monitoring
- **Quick logout** from sidebar

---

## 🔧 Technical Architecture

### Database Structure

**SQLite Database**: `auth/users.db`

**Users Table Schema**:
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,  -- SHA-256 hashed
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active INTEGER DEFAULT 1
)
```

### File Structure

```
FRAUD_DETECTION/
├── app_with_auth.py           # Main authenticated app
├── run_with_auth.bat           # Launcher script
├── auth/
│   ├── database.py            # Database operations
│   ├── auth_styles.py         # Custom CSS styles
│   └── users.db               # SQLite database (created automatically)
├── ui/                        # Existing UI components
├── src/                       # Backend modules
└── AUTH_GUIDE.md              # This file
```

### Security Features

✅ **Password Hashing**: SHA-256 encryption  
✅ **SQL Injection Protection**: Parameterized queries  
✅ **Email Validation**: Regex pattern matching  
✅ **Password Strength**: Minimum 8 characters with complexity  
✅ **Session Management**: Streamlit session state  
✅ **Duplicate Prevention**: Unique email constraint  
✅ **Active User Tracking**: Last login timestamp  

---

## 📋 User Flow

### First Time User

1. **Visit Application** → Login page appears
2. **Click "Sign Up"** → Signup page
3. **Fill Details**:
   - Full Name
   - Email
   - Password (min 8 chars, uppercase, lowercase, numbers)
   - Confirm Password
4. **Agree to Terms** → Click "Create Account"
5. **Success!** → Auto-redirect to login
6. **Login** with credentials
7. **Access Dashboard** → Full fraud detection features

### Returning User

1. **Visit Application** → Login page
2. **Enter Credentials** → Email + Password
3. **Click "Login"** → Authenticated
4. **Dashboard Access** → All features available

---

## 🎨 Design Highlights

### Color Scheme
- **Background**: Purple gradient (`#667eea` to `#764ba2`)
- **Cards**: White with soft shadows
- **Primary**: Navy Blue (`#1e3a8a`)
- **Accent**: Gold (`#fbbf24`)
- **Text**: Dark gray (`#374151`)

### Typography
- **Font**: Poppins (Google Fonts)
- **Weights**: 300, 400, 500, 600, 700

### Components
- **Auth Cards**: Centered, rounded (20px), animated
- **Input Fields**: Rounded (12px), focus effects
- **Buttons**: Gradient, hover effects, full width
- **Profile Avatar**: Circular, gradient background
- **Responsive**: Mobile and desktop optimized

---

## 🔐 Password Requirements

### Minimum Requirements
- ✅ At least **8 characters** long
- ✅ Contains **uppercase** letters (A-Z)
- ✅ Contains **lowercase** letters (a-z)
- ✅ Contains **numbers** (0-9)
- ⭐ **Recommended**: Special characters (!@#$%^&*)

### Password Strength Levels
- **Weak**: < 2 criteria met (rejected)
- **Medium**: 2-3 criteria met (accepted)
- **Strong**: All 4 criteria met (recommended)

---

## 📊 Database Operations

### Create User
```python
db = AuthDatabase()
success, message = db.create_user(name, email, password)
```

### Verify Login
```python
success, user_data = db.verify_user(email, password)
```

### Get User Info
```python
user = db.get_user_by_email(email)
```

### Update Profile
```python
success, message = db.update_user_profile(email, new_name)
```

### Change Password
```python
success, message = db.change_password(email, old_pass, new_pass)
```

---

## 🎯 Session Management

### Session State Variables

```python
st.session_state.authenticated  # True/False
st.session_state.user           # User data dict
st.session_state.page           # Current page
st.session_state.dashboard_page # Dashboard sub-page
```

### User Data Structure

```python
user = {
    'id': 1,
    'name': 'John Doe',
    'email': 'john@example.com',
    'created_at': '2024-01-15 10:30:00'
}
```

---

## 🚨 Error Handling

### Login Errors
- ❌ **Empty fields**: "Please fill in all fields"
- ❌ **Invalid email**: "Please enter a valid email address"
- ❌ **Wrong credentials**: "Invalid email or password"

### Signup Errors
- ❌ **Empty fields**: "Please fill in all fields"
- ❌ **Invalid email**: "Please enter a valid email address"
- ❌ **Password mismatch**: "Passwords do not match"
- ❌ **Weak password**: "Password must contain uppercase, lowercase, and numbers"
- ❌ **Duplicate email**: "Email already registered"
- ❌ **Terms not agreed**: "Please agree to the Terms of Service"

---

## 🔧 Customization

### Change Database Location

Edit `auth/database.py`:
```python
def __init__(self, db_path="custom/path/users.db"):
```

### Modify Password Requirements

Edit `app_with_auth.py` → `validate_password()` function

### Customize Styling

Edit `auth/auth_styles.py` → `get_auth_css()` function

### Add More User Fields

1. Update database schema in `auth/database.py`
2. Add fields to signup form in `app_with_auth.py`
3. Update `create_user()` method

---

## 🔄 Integration with FastAPI (Future)

The authentication system is designed for easy FastAPI integration:

### Planned Endpoints

```python
POST /api/auth/register
POST /api/auth/login
POST /api/auth/logout
GET  /api/auth/profile
PUT  /api/auth/profile
POST /api/auth/change-password
POST /api/auth/forgot-password
```

### Migration Steps

1. Create FastAPI endpoints in `src/module4_deployment/`
2. Replace `AuthDatabase` calls with API requests
3. Use JWT tokens for session management
4. Add token refresh mechanism
5. Implement password reset via email

---

## 📱 Responsive Design

### Desktop (> 768px)
- Centered auth cards (450px max width)
- Full sidebar navigation
- Multi-column layouts

### Mobile (< 768px)
- Full-width auth cards
- Stacked layouts
- Optimized touch targets
- Smaller avatars and fonts

---

## 🎓 Usage Examples

### Example 1: Create Account

1. Click "Sign Up"
2. Enter:
   - Name: `John Doe`
   - Email: `john@safebank.ai`
   - Password: `SecurePass123!`
   - Confirm: `SecurePass123!`
3. Check "I agree to terms"
4. Click "Create Account"
5. Success! → Redirected to login

### Example 2: Login

1. Enter email: `john@safebank.ai`
2. Enter password: `SecurePass123!`
3. Click "Login to Dashboard"
4. Authenticated! → Dashboard loads

### Example 3: View Profile

1. After login, click "My Profile" in sidebar
2. View account details
3. Edit name if needed
4. Click "Update Profile"

### Example 4: Logout

1. Click "Logout" button (sidebar or profile page)
2. Session cleared
3. Redirected to login page

---

## 🐛 Troubleshooting

### Issue: Database not found

**Solution**:
```bash
# Database is created automatically on first run
# If issues persist, delete and recreate:
del auth\users.db
# Restart application
```

### Issue: Can't login after signup

**Solution**:
- Ensure password meets requirements
- Check email format is valid
- Verify database file exists in `auth/users.db`

### Issue: "Module not found" error

**Solution**:
```bash
# Ensure all dependencies installed
pip install streamlit

# Check file structure
dir auth\
# Should show: database.py, auth_styles.py
```

### Issue: Styling not applied

**Solution**:
- Clear browser cache
- Hard refresh (Ctrl + F5)
- Check `auth_styles.py` exists

---

## 🔐 Security Best Practices

### For Production

1. **Use HTTPS**: Always use SSL/TLS in production
2. **Environment Variables**: Store secrets in `.env` file
3. **Rate Limiting**: Implement login attempt limits
4. **Password Hashing**: Consider bcrypt instead of SHA-256
5. **JWT Tokens**: Use for API authentication
6. **Email Verification**: Verify email addresses
7. **2FA**: Add two-factor authentication
8. **Session Timeout**: Implement auto-logout
9. **Audit Logging**: Log all authentication events
10. **Regular Updates**: Keep dependencies updated

### Current Implementation

✅ Password hashing (SHA-256)  
✅ SQL injection protection  
✅ Email validation  
✅ Session management  
✅ Duplicate prevention  
⚠️ **Not for production** without additional security measures  

---

## 📊 Database Management

### View Users

```python
import sqlite3
conn = sqlite3.connect('auth/users.db')
cursor = conn.cursor()
cursor.execute("SELECT id, name, email, created_at FROM users")
print(cursor.fetchall())
conn.close()
```

### Reset Database

```bash
# Delete database file
del auth\users.db

# Restart application (creates new database)
run_with_auth.bat
```

### Backup Database

```bash
# Copy database file
copy auth\users.db auth\users_backup.db
```

---

## 🎉 Features Comparison

### Without Authentication (`app_premium.py`)
- ✅ All fraud detection features
- ❌ No user accounts
- ❌ No access control
- ❌ No user tracking

### With Authentication (`app_with_auth.py`)
- ✅ All fraud detection features
- ✅ User accounts with login/signup
- ✅ Access control (must login)
- ✅ User tracking and profiles
- ✅ Session management
- ✅ Secure authentication

---

## 🚀 Quick Commands

### Launch Application
```bash
run_with_auth.bat
```

### Access Application
```
http://localhost:8501
```

### Custom Port
```bash
streamlit run app_with_auth.py --server.port 8502
```

### View Database
```bash
sqlite3 auth/users.db
.tables
SELECT * FROM users;
.quit
```

---

## 📞 Support

### Common Questions

**Q: Can I use this in production?**  
A: Not recommended without additional security measures (HTTPS, bcrypt, rate limiting, etc.)

**Q: How do I reset a password?**  
A: Currently no reset feature. Use database directly or implement forgot password flow.

**Q: Can I add more user fields?**  
A: Yes! Update database schema and signup form.

**Q: Is the password secure?**  
A: Uses SHA-256 hashing. For production, use bcrypt or Argon2.

**Q: Can I integrate with FastAPI?**  
A: Yes! Code is structured for easy API integration.

---

## 🎯 Next Steps

### Immediate
1. Launch application: `run_with_auth.bat`
2. Create an account
3. Login and explore features

### Short Term
1. Customize styling in `auth_styles.py`
2. Add more user profile fields
3. Implement password reset
4. Add email verification

### Long Term
1. Integrate with FastAPI
2. Add JWT authentication
3. Implement 2FA
4. Add role-based access control
5. Deploy to production with HTTPS

---

**🛡️ SafeBank AI with Authentication v2.0**  
*Secure, Professional, Production-Ready*

**Get Started:**
```bash
run_with_auth.bat
```

**Happy Secure Banking! 🔐**
