# Gatior
![image](https://github.com/user-attachments/assets/46ac8be1-c858-45b1-a57e-570d17100b8e)

![2025-02-20_21-01_1](https://github.com/user-attachments/assets/8516e1ae-5abc-442a-84b2-6d00ad727075)

![2025-02-20_21-01](https://github.com/user-attachments/assets/540ace30-db7e-41a6-b216-2c781402df52)


## Quick installation instructions

Clone the repo
```bash
git clone https://github.com/dark-neonus/gatior.git
```

Create python environment and activate it:
```bash
python -m venv .venv
```

Install required libraries:
```bash
pip install -r requirements.txt
```

Run server:
```bash
./manage.py runserver 0.0.0.0:8000
```

If you need working sockets on site, install docker and run socket server:
```bash
docker run --rm -p 6379:6379 redis:7
```
