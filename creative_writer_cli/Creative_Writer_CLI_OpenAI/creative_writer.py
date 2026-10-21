"""Assignment 3: OpenAI-powered Creative Writer CLI."""
import argparse
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

from openai import OpenAI, APIConnectionError, APITimeoutError, AuthenticationError, BadRequestError, RateLimitError, APIStatusError

GENRES = ['marketing material', 'slogan', 'meme', 'poem', 'song lyrics', 'blog post', 'SEO article', 'short story', 'other']
STYLES = [
    'Clear, audience-focused and polished',
    'Playful, surprising, memorable imagery',
    'Emotional, vivid, original storytelling',
]
DEVELOPER_PROMPT = """You are an expert professional creative writer. Fulfill the user's requested genre and audience with a distinctive voice, strong structure, and original language. Follow length requirements. Do not invent verified facts, citations, testimonials, endorsements, statistics or sources. If factual claims cannot be verified, qualify or omit them. For SEO writing use keywords, synonyms and semantically related terms naturally; never stuff keywords or repeat phrases mechanically. If writing lyrics, create original lyrics rather than copying known works. Give only the finished writing, with a brief title if appropriate."""


def parse_args(argv=None):
    p = argparse.ArgumentParser(description='Generate three independent OpenAI creative-writing versions and compare them.')
    p.add_argument('request', nargs='?', help='Writing request (asked interactively if omitted).')
    p.add_argument('--genre', choices=GENRES, help='Content type; optional.')
    p.add_argument('--audience', default='general readers', help='Intended readers.')
    p.add_argument('--max-words', type=int, default=180, help='Maximum words per version (default 180).')
    p.add_argument('--max-output-tokens', type=int, default=None, help='API output-token cap; optional. Word cap is prompted separately.')
    p.add_argument('--model', default='gpt-4.1-mini', help='OpenAI model ID (default gpt-4.1-mini).')
    p.add_argument('--temperature', type=float, help='Sampling temperature, if model supports it (0 to 2).')
    p.add_argument('--top-p', type=float, help='Nucleus sampling, if supported (0 to 1).')
    p.add_argument('--presence-penalty', type=float, help='Presence penalty, if supported (-2 to 2).')
    p.add_argument('--frequency-penalty', type=float, help='Frequency penalty, if supported (-2 to 2).')
    p.add_argument('--reasoning-effort', choices=['none', 'minimal', 'low', 'medium', 'high', 'xhigh'], help='Reasoning effort, if supported by the model.')
    p.add_argument('--versions', type=int, default=3, help='Independent requests (default 3).')
    p.add_argument('--save', action='store_true', help='Save versions and comparison to a Markdown file.')
    return p.parse_args(argv)


def validate(a):
    if not 1 <= a.max_words <= 3000:
        raise ValueError('--max-words must be between 1 and 3000')
    if a.max_output_tokens is not None and a.max_output_tokens < 16:
        raise ValueError('--max-output-tokens must be at least 16')
    if not 1 <= a.versions <= 10:
        raise ValueError('--versions must be between 1 and 10')
    for field, low, high in [('temperature', 0, 2), ('top_p', 0, 1), ('presence_penalty', -2, 2), ('frequency_penalty', -2, 2)]:
        value = getattr(a, field)
        if value is not None and not low <= value <= high:
            raise ValueError(f'--{field.replace("_", "-")} must be between {low} and {high}')


def input_request(a):
    if not a.request:
        print('\n=== CREATIVE WRITER CLI ===\nGenres: ' + ', '.join(GENRES))
        a.request = input('What do you want to write? ').strip()
        if not a.genre:
            chosen = input('Genre (Enter for auto): ').strip().lower()
            if chosen:
                if chosen not in GENRES:
                    raise ValueError('Unknown genre; choose a listed genre.')
                a.genre = chosen
        audience = input(f'Audience (Enter for {a.audience}): ').strip()
        if audience:
            a.audience = audience
    if not a.request.strip():
        raise ValueError('A non-empty writing request is required.')


def options_for_model(a):
    # Do not send unsupported sampling controls to reasoning-model families.
    is_reasoning = a.model.lower().startswith(('gpt-5', 'o1', 'o3', 'o4'))
    sampling = dict(temperature=a.temperature, top_p=a.top_p,
                    presence_penalty=a.presence_penalty, frequency_penalty=a.frequency_penalty)
    supplied_sampling = {k: v for k, v in sampling.items() if v is not None}
    if is_reasoning and supplied_sampling:
        raise ValueError('Sampling controls may not be supported on this reasoning model. Remove temperature/top-p/penalties or use --model gpt-4.1-mini. Exact support varies by model.')
    if not is_reasoning and a.reasoning_effort is not None:
        raise ValueError('Reasoning effort is not supported by this default non-reasoning model. Try --model gpt-5-mini --reasoning-effort low (model support varies).')
    params = supplied_sampling
    if a.reasoning_effort:
        params['reasoning'] = {'effort': a.reasoning_effort}
    return params


def assess_versions(results):
    if len(results) < 2:
        return 'Fewer than two successful versions: manual comparison unavailable.'
    lines = ['## Comparison (simple local measures; assess quality manually)',
             '| Version | Words | Unique-word ratio | Repeated 3-word phrases | Latency (s) |',
             '|---|---:|---:|---:|---:|']
    for i, (txt, seconds) in enumerate(results, 1):
        words = re.findall(r"\b[\w'-]+\b", txt.lower())
        trigrams = [tuple(words[j:j + 3]) for j in range(len(words) - 2)]
        repeats = len(trigrams) - len(set(trigrams))
        uniqueness = len(set(words)) / len(words) if words else 0
        lines.append(f'| {i} | {len(words)} | {uniqueness:.2f} | {repeats} | {seconds:.2f} |')
    lines += ['', '### Human evaluation (fill after reading all versions)',
              '| Criterion | Version 1 | Version 2 | Version 3 |',
              '|---|---|---|---|',
              *[f'| {metric} | /5 | /5 | /5 |' for metric in ['Creativity', 'Repetition (5 = least)', 'Factual accuracy', 'Writing style', 'Audience usefulness']],
              '', 'Describe differences, check any factual claims with reliable sources, and identify your preferred version.',
              'A reasoning-effort effect requires additional runs with a compatible model at different reasoning settings.']
    return '\n'.join(lines)


def run(a):
    validate(a)
    input_request(a)
    model_controls = options_for_model(a)
    if not os.getenv('OPENAI_API_KEY'):
        raise ValueError('OPENAI_API_KEY is missing. Set it as an environment variable; see README.md.')
    client = OpenAI(timeout=45.0, max_retries=1)
    results = []
    print(f'\nModel: {a.model} | Separate calls: {a.versions} | Max words/version: {a.max_words}')
    if model_controls:
        print(f'Controls: {model_controls}')
    print('Note: word count is an instruction, not a hard API limit. max_output_tokens is an API cap.\n')
    for idx in range(a.versions):
        angle = STYLES[idx % len(STYLES)]
        user_prompt = (f'Writing request: {a.request}\nGenre: {a.genre or "infer from request"}\n'
                       f'Target audience: {a.audience}\nMaximum length: {a.max_words} words. '
                       f'Writing angle for this independent version: {angle}. '
                       'Do not exceed the word limit. For SEO, use synonyms and related terms naturally.')
        print(f'Generating version {idx + 1}/{a.versions} ...')
        try:
            started = time.perf_counter()
            kwargs = dict(model=a.model, instructions=DEVELOPER_PROMPT,
                          input=user_prompt, **model_controls)
            if a.max_output_tokens is not None:
                kwargs['max_output_tokens'] = a.max_output_tokens
            response = client.responses.create(**kwargs)  # Each loop makes a NEW API request; no n parameter.
            seconds = time.perf_counter() - started
            output = (response.output_text or '').strip()
            if not output:
                print('No text returned (output-token cap may be too low). Skipping this version.\n', file=sys.stderr)
                continue
            results.append((output, seconds))
            print(f'\n{"=" * 15} VERSION {idx + 1} ({seconds:.2f}s) {"=" * 15}\n{output}\n')
        except AuthenticationError:
            print('Authentication failed: verify OPENAI_API_KEY.', file=sys.stderr)
            break
        except RateLimitError:
            print('Rate limit or API quota/billing issue. Check your OpenAI platform usage and billing.', file=sys.stderr)
            break
        except (APIConnectionError, APITimeoutError):
            print(f'Network/timeout problem on version {idx + 1}; continuing.', file=sys.stderr)
        except BadRequestError as exc:
            print(f'Unsupported model/parameter or bad request: {exc.message}', file=sys.stderr)
            print('Try the default model without extra controls, or choose compatible controls.', file=sys.stderr)
            break
        except APIStatusError as exc:
            print(f'OpenAI service error (HTTP {exc.status_code}); continuing.', file=sys.stderr)
    if not results:
        print('No versions generated. Check the errors above.', file=sys.stderr)
        return 1
    comparison = assess_versions(results)
    print(comparison)
    if a.save:
        output_dir = Path('outputs')
        output_dir.mkdir(exist_ok=True)
        path = output_dir / f'creative_writer_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
        details = (f'# Creative Writer CLI\n\nRequest: {a.request}\n\n'
                   f'Model: {a.model}\nAudience: {a.audience}\nGenre: {a.genre or "auto"}\n'
                   f'Max words: {a.max_words}\nControls: {model_controls}\n\n')
        path.write_text(details + '\n\n'.join(f'## Version {i}\n\n{txt}' for i, (txt, _) in enumerate(results, 1)) + '\n\n' + comparison + '\n', encoding='utf-8')
        print(f'\nSaved to: {path}')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(run(parse_args()))
    except (ValueError, KeyboardInterrupt) as exc:
        print(f'\nStopped: {exc}', file=sys.stderr)
        sys.exit(1)
