# OpenAI Prompt Engineering Lab

Install the dependencies from this directory:

```bash
python3 -m pip install -r requirements.txt
```

Set `OPENAI_API_KEY` in your environment or in a `.env` file in this directory:

```text
OPENAI_API_KEY=your_openai_api_key
```

Optionally set `OPENAI_MODEL` to a model available to your account. The default is `gpt-4o-mini`. Keep your API key private and do not commit your `.env` file.

Run the menu with:

```bash
python3 main.py
```

OpenAI API calls require an API key with access to the chosen model and may incur charges.