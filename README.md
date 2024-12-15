# sad
 Supply chain attack detection tool

## setup
for db
```
docker-compose up --build
```

frontend (change lib/utils.tsx, API_URL to http://localhost)
```
cd frontend
npm i
npm run dev
```


backend
```
cd backend
python3 -m pip install -r requirements.txt
python3 main.py
```

create a `config.py` in backend folder
```
import string
import random

DB_HOST="localhost:3313"
DB_USERNAME=""
DB_PASSWORD=""
DB_NAME="sad"

# random 64 character hex
SECRET_KEY = ''.join(random.choices(string.ascii_letters + string.digits, k=64))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7

MAKERSUITE_API_KEY = ""
GITHUB_APP_SECRET = ""
GITHUB_WEBHOOK_URL = "/webhooks/github"
GITHUB_APP_NAME = "hm-sad"
GITHUB_APP_CLIENT_ID = ""
GITHUB_APP_CLIENT_SECRET = ""
```