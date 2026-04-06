# 🏛️ GovtTrack ERP: Unified Public Works Governance

**Hackathon Project | Odoo x Institutional ERP**

Built on: Odoo 19 | Python | PostgreSQL

---

## 📌 Project Overview

GovtTrack ERP is a governance-focused ERP module designed to bring **transparency, accountability, and efficiency** to public infrastructure projects.

Inspired by real-world **MPLADS-style workflows**, the platform unifies:
- Project lifecycle tracking  
- Budget monitoring  
- Citizen grievance management  

…into a single, centralized system.

---

## 🎯 The Problem

Public infrastructure projects often suffer from:
- Fragmented data across departments  
- Lack of real-time monitoring  
- Delayed issue resolution  
- Minimal citizen visibility  

---

## 💡 Our Solution

GovtTrack ERP provides a **unified system** that enables:

- 📊 **Visual Accountability**  
  Real-time tracking with automatic **delay detection**

- 💰 **Financial Transparency**  
  Monitor budget allocation and utilization across projects

- 🧾 **Citizen Feedback Integration**  
  Link grievances directly to specific infrastructure projects

---

## 🛠️ Key Features

### 📊 Executive Dashboard
- Total projects overview  
- Budget utilization insights  
- Active grievance tracking  

### 📌 Smart Project Management
- Kanban-based workflow  
- Status tracking: Draft → Review → Approved → In Progress → Completed  
- Automatic **Delayed Project detection**

### ⚠️ Grievance Redressal System
- Citizen complaint logging  
- Severity classification (High / Medium / Low)  
- Officer assignment & resolution tracking  

### 🌍 Constituency-Based Tracking
- Projects grouped by regions  
- Managed by MPs / administrative authorities  

### 📈 Analytics & Insights
- Budget vs actual spend analysis  
- Project performance indicators  
- Accountability metrics  

---

## 🏗️ Technical Architecture

| Component   | Technology |
|------------|-----------|
| Backend     | Python (Odoo Framework) |
| Frontend    | XML, QWeb, Custom CSS |
| Database    | PostgreSQL |

### Core Models

- `govttrack.project` → Project lifecycle & tracking  
- `govttrack.constituency` → Regional mapping  
- `govttrack.category` → Project classification  
- `govttrack.grievance` → Citizen feedback system  

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/coolprash06/govttrack-erp.git
