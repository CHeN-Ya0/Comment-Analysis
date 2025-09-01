
from openai import OpenAI
from openai._exceptions import OpenAIError, AuthenticationError

# Create client with your API key
client = OpenAI(api_key="REDACTED")

try:
    # Simple test request to GPT-3.5
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if your key allows
        messages=[
            {"role": "user", "content": "Hello! Can you confirm the API is working?"}
        ]
    )

    print("✅ Success! Response:")
    print(response.choices[0].message.content)

except AuthenticationError:
    print("❌ Authentication failed: Please check your API key.")

except OpenAIError as e:
    print("❌ OpenAI API returned an error:", e)

except Exception as e:
    print("❌ An unexpected error occurred:", e)
