# Assignment #3 — Creative Writer CLI

**Group:** Dionysus  
**Members:** Udit Bhattarai, Lotus Nyaupane, Dipen Gaihre (edit if necessary)  
**LLM:** OpenAI API; default model `gpt-4.1-mini`.

Standalone Python CLI for creative writing: marketing copy, slogans, memes, poems, song lyrics, blog posts, SEO articles and stories. It generates **3 separate versions by default**, using **3 individual API requests**, with different writing angles. It does not use the `n` parameter.

## Set up on Mac / VS Code

```bash
cd Creative_Writer_CLI_OpenAI
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Create an OpenAI API key at https://platform.openai.com/api-keys. Set it securely in your current terminal:

```bash
export OPENAI_API_KEY='paste_your_key_here'
```

Do **not** commit API keys. ChatGPT Plus does not include OpenAI API credit; check API billing and usage separately. Real API requests require internet access and may incur charges.

## Run

Interactive:

```bash
python creative_writer.py --save
```

Command-line prompt:

```bash
python creative_writer.py "Create a catchy marketing campaign for a local bakery" --genre 'marketing material' --audience 'students' --max-words 120 --save
```

Sampling experiment, with the default model:

```bash
python creative_writer.py "Write an emotional poem about friendship" --temperature 0.9 --top-p 0.95 --presence-penalty 0.3 --frequency-penalty 0.2 --save
```

Reasoning experiment (run separately with a compatible model, if your API account supports it):

```bash
python creative_writer.py "Write a persuasive blog introduction about digital privacy" --model gpt-5-mini --reasoning-effort low --max-output-tokens 900 --save
```

Some model/parameter combinations are unsupported. The app warns when mixing reasoning and sampling controls, and the API returns a clear error if the selected model rejects a control. Use `--help` for all flags.

## Assignment requirements

1. **OpenAI API**: official `openai` Python SDK, `client.responses.create()`.
2. **User writing request**: positional argument or interactive input.
3. **Three different versions**: default `--versions 3` and varied stylistic instructions.
4. **Three independent API calls**: one `responses.create()` per loop iteration, with no `n`.
5. **Developer/system prompt**: `DEVELOPER_PROMPT` passed as `instructions`.
6. **Length controls**: `--max-words` plus optional hard API budget `--max-output-tokens` (token budget is not a strict word cap).
7. **Secret key**: `OPENAI_API_KEY` environment variable, never in source code.
8. **Error handling**: missing key, auth, rate limit, timeout, connection, unsupported parameter, API status.
9. **Experiment controls**: temperature, top-p, presence/frequency penalties and reasoning effort (model-dependent).
10. **Compare versions**: printed comparison includes word counts, unique-word ratios, repeated trigrams, latency, plus human scoring rubric for creativity, repetition, factual accuracy, style and audience usefulness. Reasoning comparison requires repeat runs with alternate effort settings.

## Screenshots to submit

- Screenshot 1: Terminal showing a writing request and 3 generated versions.
- Screenshot 2: Terminal or saved Markdown showing the comparison table.

On Mac, use **Command + Shift + 4**. Upload the project under a dedicated folder in your **group's** existing GitHub repository via a branch / pull request. Exclude API keys and `.env` files.

**Note:** Source code and syntax are prepared, but actual generated content, latency and model support cannot be verified without your own API key and account access. Review factual claims manually.
