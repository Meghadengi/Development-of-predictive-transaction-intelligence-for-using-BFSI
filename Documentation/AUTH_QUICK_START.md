# 🔐 Authentication System - Quick Start

## 🚀 Launch in 3 Steps

### Step 1: Run the Application
```bash
run_with_auth.bat
```

### Step 2: Create Account
1. Click **"Sign Up"**
2. Fill in:
   - Name: `Your Name`
   - Email: `your@email.com`
   - Password: `SecurePass123!`
3. Click **"Create Account"**

### Step 3: Login
1. Enter your email and password
2. Click **"Login to Dashboard"**
3. **Done!** Access all features

---

## 📋 Quick Reference

### Login Page
- **URL**: `http://localhost:8501`
- **Fields**: Email + Password
- **Features**: Remember me, Forgot password

### Signup Page
- **Fields**: Name, Email, Password, Confirm Password
- **Requirements**: 8+ chars, uppercase, lowercase, numbers
- **Validation**: Real-time password strength

### Profile Page
- **View**: User info, account details
- **Edit**: Update name
- **Action**: Logout

### Dashboard
- **Access**: After login
- **Features**: All fraud detection tools
- **Navigation**: Sidebar with user profile

---

## 🎯 Password Requirements

✅ Minimum 8 characters  
✅ Uppercase letters (A-Z)  
✅ Lowercase letters (a-z)  
✅ Numbers (0-9)  
⭐ Special characters (recommended)

**Example**: `SecurePass123!`

---

## 🔧 Files Created

```
auth/
├── database.py          # Database operations
├── auth_styles.py       # Custom CSS
└── users.db            # SQLite database (auto-created)

app_with_auth.py        # Main authenticated app
run_with_auth.bat       # Launcher script
AUTH_GUIDE.md           # Complete guide
AUTH_QUICK_START.md     # This file
```

---

## 🎨 Features

### ✨ Login Page
- Clean fintech design
- Email/password validation
- "Forgot password" link
- Switch to signup

### ✨ Signup Page
- Full name, email, password
- Password strength indicator
- Duplicate prevention
- Auto-redirect after signup

### ✨ Profile Page
- User avatar with initial
- Account information
- Edit profile
- Logout button

### ✨ Dashboard
- Full fraud detection features
- User info in header
- Sidebar navigation
- Quick logout

---

## 🔐 Security

✅ SHA-256 password hashing  
✅ SQL injection protection  
✅ Email validation  
✅ Session management  
✅ Duplicate prevention  

---

## 🚨 Troubleshooting

### Can't login?
- Check email format
- Verify password meets requirements
- Ensure account was created successfully

### Database error?
- Database auto-creates on first run
- Check `auth/users.db` exists

### Styling issues?
- Clear browser cache
- Hard refresh (Ctrl + F5)

---

## 📞 Quick Help

**Launch**: `run_with_auth.bat`  
**Access**: `http://localhost:8501`  
**Guide**: See `AUTH_GUIDE.md`  
**Support**: Check error messages

---

## 🎉 You're Ready!

**Launch command:**
```bash
run_with_auth.bat
```

**First time?** Create an account → Login → Explore!

**🛡️ SafeBank AI - Secure & Professional**
