import requests
from django.conf import settings

def verify_recaptcha(token, user_action):
    url = settings.RECAPTCHA_PROJECT_URL
    payload = {
        "event": {
            "token": token,
            "expectedAction": user_action,
            "siteKey": settings.REGISTER_RECAPTCHA_PUBLIC_KEY,
        }
    }
    headers = {
        "Content-Type": "application/json",
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        result = response.json()
        score = result.get("riskAnalysis", {}).get("score", 0.0)
        return score >= 0.5, result
    return False, {"error": response.text}
