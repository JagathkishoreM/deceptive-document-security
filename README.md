# 🔐 Deceptive Document Security

> Enhancing document security with a dual approach — NLP-based keyword extraction and ECC cryptography, featuring a honeypot mechanism to detect and deceive attackers.

---

## 📌 Table of Contents
- [About the Project](#about-the-project)
- [Key Features](#key-features)
- [System Workflow](#system-workflow)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Security Mechanisms](#security-mechanisms)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

---

## 📖 About the Project

**Deceptive Document Security** is a final year project that implements a multi-layered document protection system. It combines **Elliptic Curve Cryptography (ECC)** for secure file encryption and **TF-IDF based NLP** for keyword extraction, along with a **honeypot deceptive login mechanism** that traps unauthorized users while alerting the legitimate document owner.

Unlike traditional security systems that simply deny access, this system **deceives attackers** by letting them think they've successfully logged in — while serving them fake documents and simultaneously alerting the real user.

---

## ✨ Key Features

- 🛡️ **ECC Encryption** — All uploaded documents are encrypted using Elliptic Curve Integrated Encryption Scheme (ECIES)
- 🧠 **TF-IDF Keyword Extraction** — Top 5 keywords are extracted from each uploaded document using NLP
- 🪤 **Honeypot Login** — Wrong credentials redirect to a fake login page with fake document downloads
- 📧 **Email Alerts** — Users receive login keys, document keywords, and breach alerts via email
- 👨‍💼 **Admin Approval Workflow** — New users must be approved by admin before accessing the system
- 🔑 **Keyword-based Download Authentication** — Only users with the correct keyword can download the real document

---

## 🔄 System Workflow

### 1️⃣ User Registration & Admin Approval
```
Employee Registers → Admin Reviews → 
  ✅ Approved → Login Key sent to Email
  ❌ Rejected → No access granted
```

### 2️⃣ User Login
```
Enter Username + Password + Login Key →
  ✅ All Correct → Original Dashboard (full access)
  ❌ Any Wrong  → Fake Dashboard (honeypot activated)
```

### 3️⃣ Document Upload
```
User Uploads Document (PDF/DOC/TXT) + Description →
ECC Encryption Applied →
TF-IDF extracts 5 Keywords →
Keywords sent to User's Email
```

### 4️⃣ Document Download
```
Legitimate User:
  Enter Keyword received via email → Original document downloaded

Attacker (Fake Login):
  Searches by filename/description → Fake (Lorem Ipsum) document downloaded
  → Alert email sent to the real document owner
```

---

## 🛠️ Tech Stack

| Category | Technology |
|---|---|
| Backend | Python |
| Encryption | ECC (ecies package) |
| NLP | TF-IDF (scikit-learn / custom) |
| Email Service | SMTP (smtplib) |
| File Types Supported | PDF, DOC, TXT |
| Frontend | HTML, CSS, JavaScript |

---

## 📁 Project Structure

```
deceptive-document-security/
│
├── static/                  # CSS, JS, images
│
├── templates/               # HTML templates
│
├── venu/                    # Virtual environment
│
├── App.py                   # Main application entry point
├── main.py                  # Core logic & routing
├── redsav.py                # Document saving & retrieval logic
├── requirements.txt         # Python dependencies
├── .gitignore               # Files excluded from git
└── README.md                # Project documentation
```

---

## ⚙️ Installation

### Prerequisites
- Python 3.8+
- pip

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/your-username/deceptive-document-security.git

# 2. Navigate to the project directory
cd deceptive-document-security

# 3. Create a virtual environment
python -m venv venv

# 4. Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 5. Install dependencies
pip install -r requirements.txt

# 6. Configure environment variables (see below)

# 7. Run the application
python App.py
```

### Environment Variables
Create a `.env` file in the root directory:
```env
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url
```

---

## 🚀 Usage

1. **Admin** — Log in to the admin panel to approve/reject new user registrations
2. **Register** — New users register and wait for admin approval
3. **Login** — Use username + password + login key to access the dashboard
4. **Upload** — Upload a document; you'll receive 5 keywords via email
5. **Download** — Enter one of your keywords to download your original document
6. **Security** — Any unauthorized attempt triggers an alert to the document owner

---

## 🔐 Security Mechanisms

### 🔒 ECC Encryption (ECIES)
All documents are encrypted using Elliptic Curve Integrated Encryption Scheme before storage. Only authorized users can decrypt and access the original content.

### 🧠 TF-IDF Keyword Authentication
Term Frequency-Inverse Document Frequency (TF-IDF) is used to extract the top 5 most significant keywords from each document. These keywords serve as a second authentication factor during download.

### 🪤 Honeypot / Deceptive Login
When incorrect credentials are entered, the system:
- Silently redirects to a **fake dashboard** (looks identical to the real one)
- Allows the attacker to "download" files — but serves **Lorem Ipsum fake documents**
- Immediately **sends an alert email** to the legitimate document owner

---

## 📸 Screenshots

> *(Add screenshots of your application here)*

- [ ] Registration Page
- [ ] Admin Approval Panel
- [ ] User Dashboard
- [ ] File Upload Page
- [ ] Fake Login Page
- [ ] Alert Email

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

```bash
1. Fork the repository
2. Create your feature branch: git checkout -b feature/YourFeature
3. Commit your changes: git commit -m 'Add YourFeature'
4. Push to the branch: git push origin feature/YourFeature
5. Open a Pull Request
```

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

> Final Year Project — *Enhancing Document Security: A Dual Approach with NLP and Cryptographic Techniques*

---

⭐ If you found this project interesting, please give it a star!
