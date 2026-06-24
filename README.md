# 🚦 Smart City Traffic Analytics

**Developer:** Aadil Hasan  
**Registration Number:** 5000  

A full-stack computer vision application designed to transform standard top-down traffic camera feeds into intelligent, real-time diagnostic sensors. Built for modern urban infrastructure, this system eliminates the need for expensive physical road sensors by utilizing edge AI to calculate lane density, monitor congestion, and estimate vehicle velocity on the fly.

---

## 📑 Table of Contents
- [Project Overview](#project-overview)
- [Core Features](#core-features)
- [System Architecture](#system-architecture)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)

---

## 🎯 Project Overview
Urban traffic management traditionally relies on expensive, hardware-heavy infrastructure like radar guns or inductive loops. This project provides a purely software-based alternative. By deploying a custom-trained YOLOv8 object detection model wrapped in a reactive Streamlit frontend, the system processes live video feeds to provide actionable traffic intelligence.

## ✨ Core Features
* **Real-Time Vehicle Tracking:** Utilizes YOLOv8 with persistent ID tracking to detect and follow individual vehicles across multiple frames with high accuracy (97.5% mAP).
* **Spatial Lane Mapping:** Employs OpenCV polygonal masking to dynamically map vehicles to specific physical lanes (Left vs. Right) based on coordinate bounding boxes.
* **Dynamic Density Alerts:** Automatically flags lane status as "Smooth Flow" or "Heavy Congestion" based on real-time vehicle counts.
* **Velocity Estimation:** Calculates vehicle speed (km/h) without radar by measuring pixel displacement over time and converting it to real-world meters using a camera calibration constant.

## 🛠 System Architecture
* **AI & Computer Vision:** Ultralytics YOLOv8, OpenCV, NumPy
* **Frontend Framework:** Streamlit
* **Language:** Python 3.x
* **Environment:** Python Virtual Environment (`venv`)

---

## 🚀 Installation & Setup

Follow these steps to run the application on your local machine.

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/Smart-Traffic-Analytics.git](https://github.com/YOUR_USERNAME/Smart-Traffic-Analytics.git)
cd Smart-Traffic-Analytics