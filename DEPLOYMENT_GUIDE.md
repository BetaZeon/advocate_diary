# 🌍 Deployment Guide - Case Management System

## 🚀 **Option 1: Streamlit Cloud (Recommended - FREE)**

### **Step 1: Prepare Your Code**
✅ **Already Done!** Your application is ready for deployment.

### **Step 2: Push to GitHub**
1. **Create a GitHub repository:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Case Management System"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/advocate-diary.git
   git push -u origin main
   ```

2. **Make sure these files are included:**
   - ✅ `app.py` (main application)
   - ✅ `requirements.txt` (dependencies)
   - ✅ `.streamlit/secrets.toml` (credentials - will be configured in Streamlit Cloud)
   - ✅ All Python files in `models/`, `views/`, `controllers/`
   - ✅ `config.json` (fallback for local development)

### **Step 3: Deploy on Streamlit Cloud**
1. **Go to [share.streamlit.io](https://share.streamlit.io)**
2. **Sign in with your GitHub account**
3. **Click "New app"**
4. **Fill in the details:**
   - **Repository**: `YOUR_USERNAME/advocate-diary`
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL**: `advocate-diary` (or your preferred name)

5. **Click "Deploy!"**

### **Step 4: Configure Secrets in Streamlit Cloud**
1. **Go to your deployed app dashboard**
2. **Click "Settings" → "Secrets"**
3. **Add your Google Sheets credentials:**
   ```toml
   [google_sheets]
   spreadsheet_id = "1TuahxRtqMvPPDVqbSVIc1MJPt-2Oehq1zP3D-EbbeHI"
   type = "service_account"
   project_id = "advocatediary-426200"
   private_key_id = "656e16f578bab3e2e0538a2c38514a007fd5770e"
   private_key = "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY_HERE\n-----END PRIVATE KEY-----\n"
   client_email = "advocatediary@advocatediary-426200.iam.gserviceaccount.com"
   client_id = "109368407146454484210"
   auth_uri = "https://accounts.google.com/o/oauth2/auth"
   token_uri = "https://oauth2.googleapis.com/token"
   auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
   client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/advocatediary%40advocatediary-426200.iam.gserviceaccount.com"
   universe_domain = "googleapis.com"
   ```

4. **Save and restart your app**

### **Step 5: Access Your Global App**
🌐 **Your app will be available at:** `https://advocate-diary.streamlit.app`

---

## 🌐 **Option 2: Heroku (Paid)**

### **Prerequisites:**
- Heroku account
- Heroku CLI installed

### **Steps:**
1. **Create `Procfile`:**
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Create `runtime.txt`:**
   ```
   python-3.11.0
   ```

3. **Deploy:**
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

---

## ☁️ **Option 3: AWS/GCP/Azure (Advanced)**

### **AWS Elastic Beanstalk:**
- Create `Dockerfile`
- Use `gunicorn` with `streamlit`
- Configure environment variables

### **Google Cloud Run:**
- Containerize with Docker
- Deploy to Cloud Run
- Set up domain mapping

### **Azure App Service:**
- Deploy as Python web app
- Configure app settings

---

## 🔧 **Option 4: VPS/Server (Self-Hosted)**

### **Requirements:**
- Ubuntu/CentOS server
- Domain name (optional)
- SSL certificate

### **Steps:**
1. **Install dependencies:**
   ```bash
   sudo apt update
   sudo apt install python3-pip nginx
   pip3 install -r requirements.txt
   ```

2. **Set up systemd service:**
   ```bash
   sudo nano /etc/systemd/system/advocate-diary.service
   ```

3. **Configure Nginx reverse proxy**
4. **Set up SSL with Let's Encrypt**

---

## 🎯 **Recommended Deployment Path**

### **For Quick Start (FREE):**
1. ✅ **Streamlit Cloud** - Easiest, free, perfect for your use case
2. ⏱️ **Deployment time**: 5-10 minutes
3. 🌍 **Global access**: Yes
4. 💰 **Cost**: Free

### **For Production (PAID):**
1. ✅ **Heroku** - Good balance of features and simplicity
2. ⏱️ **Deployment time**: 15-30 minutes
3. 🌍 **Global access**: Yes
4. 💰 **Cost**: $7-25/month

---

## 🔒 **Security Considerations**

### **✅ Already Implemented:**
- Google Sheets service account authentication
- No hardcoded credentials in code
- Secure credential management

### **🔐 Additional Security (Optional):**
- Add user authentication
- Implement rate limiting
- Use HTTPS only
- Regular security updates

---

## 📊 **Monitoring & Maintenance**

### **Streamlit Cloud:**
- Built-in analytics
- Automatic deployments
- Error logging
- Usage statistics

### **Custom Monitoring:**
- Set up health checks
- Monitor Google Sheets API usage
- Log application errors
- Set up alerts

---

## 🚀 **Next Steps**

1. **Choose your deployment option** (Streamlit Cloud recommended)
2. **Follow the specific steps** for your chosen platform
3. **Test your deployed application**
4. **Share the global URL** with your team

**Your Case Management System will be accessible from anywhere in the world!** 🌍
