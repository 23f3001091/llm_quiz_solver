import json
import requests

def test_local_quiz():
    url = "https://llm-quiz-solver-2yti.onrender.com/quiz"

    payload = {
        "email": "23f3001091@ds.study.iitm.ac.in",
        "secret": "my7secret",
        "url": "https://tds-llm-analysis.s-anand.net/demo2"
    }

    print("\nSending request to local FastAPI server...\n")
    print("Payload:", json.dumps(payload, indent=4))

    try:
        response = requests.post(url, json=payload, timeout=120)
        print("\nResponse Status:", response.status_code)

        try:
            print("\nResponse JSON:")
            print(json.dumps(response.json(), indent=4))
        except Exception:
            print("\nRaw Response:", response.text)

    except Exception as e:
        print("\n Error while sending request:", str(e))


if __name__ == "__main__":
    test_local_quiz()
