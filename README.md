# 🌆 Taipei-Day-Trip

Taipei Day Trip is a web application for travelers exploring Taipei, providing features for attraction booking, itinerary planning, and more. Users can browse attractions along Taipei's MRT lines, login/register, add trips to a shopping cart, proceed with credit card payments, and confirm their itinerary upon successful payment.

This project showcases my skills in both **frontend and backend development**, as well as my proficiency with **AWS services**. The complete development and learning period for this project spanned from June to July 2024.

🔗 [https://raphaelfang.com/tdt/v1/](https://raphaelfang.com/tdt/v1/)

## 🎥 Demo

![the gif demo for Taipei-Day-Trip project](https://github.com/user-attachments/assets/c5b6f036-1ddf-472c-be1c-884278f849eb)

## 🛠️ System Architecture Diagram
![SysArch](https://github.com/user-attachments/assets/8d2032d2-19cf-4581-8553-2c87e05fadf5)


## 🧰 Tech Stack

- **Backend Framework**: FastAPI - following RESTful API principles, asynchronous
- **Database**: MySQL - connection pool, asynchronous
- **Caching**: Redis - stores user cart data, TTL settings, connection pool, asynchronous
- **Frontend**: HTML, CSS, JavaScript, RWD
- **Third-Party Authentication**: Google OAuth
- **Third-Party Payment**: TapPay SDK
- **CORS Configuration**: cross-origin requests
- **Authentication Management**: uses Cookies to handle JWT token
- **Containerization**: Docker
- **CI/CD Pipeline**: GitHub Actions
- **ENV**: GitHub Secrets

## 👤 User Flow

1. **Browse Attractions**: Users can browse attraction details and search by attraction's keywords.
2. **Log In / Register / Reset Password**: Users can log in or register to access additional features.
3. **Manage Cart**: After logging in, users can add/delete trips at their shopping cart.
4. **Complete Payment**: Users complete the transaction through a third-party payment service.
5. **View Purchased Trips**: Upon successful payment, users can review all purchased trips.
