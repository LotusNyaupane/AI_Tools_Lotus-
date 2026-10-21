# Creative Writer CLI – AI-Powered Content Generator

**Assignment:** #3 – Creative Writer CLI  
**Author:** Lotus Nyaupane  
**GitHub:** [LotusNyaupane](https://github.com/LotusNyaupane)  
**Original Group:** Dionysus  
**Group Members:** Udit Bhattarai, Lotus Nyaupane, Dipen Gaihre  
**Programming Language:** Python  
**AI Provider:** OpenAI  
**Default AI Model:** GPT-4.1 Mini  
**Development Environment:** Visual Studio Code

---

## 1. Project Introduction

Creative Writer CLI is an AI-powered command-line application developed using Python and the OpenAI API. I worked on this project as part of my AI API development assignment.

The main purpose of this project is to understand how we can use large language models in our own Python applications instead of only using AI through websites such as ChatGPT.

With this application, users can generate different types of creative content by entering a simple writing request. The application communicates with the OpenAI API, processes the request and displays the generated content directly in the terminal.

One of the main features of this project is that it generates three different versions of the same writing request. This helps users compare different writing styles and select the version they prefer.

The application is designed to be simple, flexible and easy to use for people who are familiar with basic terminal commands.

## 2. Project Objectives

The main objectives of this project are:

- To understand how to integrate the OpenAI API into a Python application.
- To learn how to send user prompts to a large language model.
- To generate different types of creative writing using AI.
- To understand how developer instructions influence the generated response.
- To generate multiple versions of the same writing request.
- To experiment with different AI parameters.
- To learn how to manage API keys securely.
- To understand API error handling and response processing.
- To gain practical experience developing a standalone AI application.

Through this project, I wanted to learn how an AI application works from the programming side, including how requests are sent, how responses are received and how the results are displayed to users.

## 3. Main Features

### 3.1 AI Content Generation

The application can generate different types of creative content, including:

- Poems and emotional writing
- Short stories and storytelling
- Song lyrics
- Marketing and advertising content
- Social media captions
- Slogans and taglines
- Blog posts and articles
- SEO-oriented content
- Humorous writing and memes

Users can enter their own writing topic, and the AI model generates content based on their instructions.

### 3.2 Three Different Writing Versions

One important feature of this application is the ability to generate three different versions of a writing request.

Instead of generating only one response, the application makes three separate API requests with different stylistic instructions.

For example, if the user requests a poem about friendship, the application can generate three different interpretations of the same topic.

This allows users to compare the results and choose the writing style they like the most.

The number of versions can also be changed using the `--versions` parameter.

### 3.3 Writing Customization

The application allows users to customize their writing requests using different command-line options.

Users can specify:

- The writing topic
- Content genre
- Target audience
- Maximum word count
- Number of generated versions
- AI model
- Sampling parameters

These options make the application more flexible for different writing tasks.

### 3.4 AI Parameter Experimentation

During development, I also explored different AI parameters and how they can affect the generated results.

**Temperature:** Controls how much variation the model may introduce in its responses.

**Top-p:** Controls token selection using nucleus sampling.

**Presence penalty:** Can encourage the model to introduce new concepts rather than repeatedly using the same ones.

**Frequency penalty:** Can help reduce repeated words and phrases.

**Reasoning effort:** Allows experimentation with reasoning settings on supported AI models.

Not every AI model supports all of these parameters. The application handles incompatible settings by providing warnings or reporting API errors.

### 3.5 Content Comparison

After generating the writing versions, the application provides information that helps users compare the outputs.

The comparison includes measurements such as:

- Total word count
- Unique-word ratio
- Repeated three-word sequences
- API response latency

These measurements help users understand differences between the generated versions.

The application also provides a human evaluation rubric for creativity, repetition, factual accuracy, writing style and usefulness for the intended audience.

### 3.6 Save Generated Content

The application supports saving generated content using the `--save` option.

This is useful when users want to keep their generated writing for future reference or comparison.

### 3.7 Error Handling

The application includes error handling for common API-related problems, such as:

- Missing API keys
- Invalid authentication
- API rate limits
- Network connection errors
- Request timeouts
- Unsupported model parameters
- Other API response errors

This makes it easier to identify problems while running the application.

---

## 4. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| OpenAI API | AI content generation |
| GPT-4.1 Mini | Default language model |
| OpenAI Python SDK | Communication with the API |
| VS Code | Writing and testing the code |
| Git | Version control |
| GitHub | Project hosting |
| Python virtual environment | Dependency isolation |

## 5. Project Structure

```text
Creative_Writer_CLI_OpenAI/
├── creative_writer.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

**creative_writer.py:** Contains the main application logic, API integration, writing instructions and command-line options.

**requirements.txt:** Contains the Python packages required to run the application.

**.env.example:** Provides an example of how an environment variable can be configured without exposing a real API key.

**.gitignore:** Prevents sensitive files, virtual environments and unnecessary generated files from being tracked by Git.

**README.md:** Contains the project description, installation instructions and usage information.

---

## 6. Installation and Setup

The following instructions explain how to run this project on macOS using VS Code.

### Step 1 – Clone the Repository

```bash
git clone https://github.com/LotusNyaupane/AI_Tools_Lotus-.git
```

Move to the Creative Writer CLI folder:

```bash
cd AI_Tools_Lotus-/creative_writer_cli/Creative_Writer_CLI_OpenAI
```

### Step 2 – Create a Virtual Environment

```bash
python3 -m venv .venv
```

Activate the environment:

```bash
source .venv/bin/activate
```

Using a virtual environment helps keep project dependencies separate from other Python projects.

### Step 3 – Install Required Packages

```bash
python -m pip install -r requirements.txt
```

This installs the packages needed to run the application.

### Step 4 – Configure the OpenAI API Key

To use the application, an OpenAI API key is required.

Create an API key from the official OpenAI platform:

https://platform.openai.com/api-keys

Set the API key in the terminal:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

Replace `your_api_key_here` with your actual API key.

**Important:** Never upload real API keys to GitHub or include them directly in Python source code.

OpenAI API usage may involve charges depending on the model and number of requests. A ChatGPT subscription does not automatically include OpenAI API credits.

---

## 7. How to Run the Application

### Example 1 – Interactive Mode

```bash
python creative_writer.py --save
```

This starts the application in interactive mode, allowing the user to enter a writing request.

### Example 2 – Generate a Poem

```bash
python creative_writer.py "Write an emotional poem about friendship"
```

The application sends the request to the AI model and generates three different versions by default.

### Example 3 – Generate Marketing Content

```bash
python creative_writer.py "Create a catchy marketing campaign for a local bakery" --genre "marketing material" --audience "students" --max-words 120 --save
```

In this example, the application generates marketing content for a specific audience while using a requested word limit.

### Example 4 – Experiment with AI Parameters

```bash
python creative_writer.py "Write an emotional poem about friendship" --temperature 0.9 --top-p 0.95 --presence-penalty 0.3 --frequency-penalty 0.2 --save
```

This command allows experimentation with different sampling parameters using a compatible model.

### Example 5 – Reasoning Model Experiment

```bash
python creative_writer.py "Write a persuasive blog introduction about digital privacy" --model gpt-5-mini --reasoning-effort low --max-output-tokens 900 --save
```

This example uses a reasoning-capable model, provided it is supported by the API account.

### Example 6 – View Available Commands

```bash
python creative_writer.py --help
```

This displays the available command-line arguments.

---

## 8. How the Application Works

The working process of Creative Writer CLI follows these steps:

1. The user enters a writing request through the terminal.
2. The application reads the prompt and command-line settings.
3. Python prepares the request using the configured developer instructions.
4. The application sends the request to the OpenAI API using `client.responses.create()`.
5. The AI model generates a response.
6. The application repeats the process to generate additional versions.
7. The generated writing is displayed in the terminal.
8. The application provides comparison information.
9. If the user enables the save option, the generated results are saved.

The application uses separate API calls rather than the `n` parameter to generate multiple versions.

## 9. What I Learned from This Project

Working on this assignment helped me understand how AI APIs can be integrated into real Python applications.

Before this project, I was mostly familiar with using AI tools through their existing interfaces. Through this assignment, I learned how to connect an AI model with Python and control its behavior through programming.

I also learned about API authentication, environment variables, prompt engineering and how different parameters can affect the generated output.

Another important part was understanding how to handle API errors. Sometimes a request may fail because of an invalid API key, network problems, rate limits or unsupported parameters.

This project also helped me improve my experience with Python, VS Code, Git and GitHub.

Overall, it was a useful practical assignment that gave me more confidence in developing AI-powered applications.

## 10. Challenges and Limitations

During this project, there were some important challenges and limitations to consider.

**API configuration:** The application requires a valid OpenAI API key and an active API account.

**Model compatibility:** Some parameters work with certain models but are not supported by others.

**API costs:** Generating multiple versions requires multiple API requests, which can increase usage costs.

**Content quality:** AI-generated writing may sometimes be repetitive, inaccurate or different from the expected style.

**Internet dependency:** The application cannot generate new AI content without connecting to the API.

**Command-line interface:** Users who are not familiar with terminal commands may find the application less convenient than a graphical application.

## 11. Future Improvements

In the future, I would like to improve this project by adding more features and making it easier to use.

Some possible improvements include:

- Creating a graphical interface using Streamlit.
- Supporting additional AI providers and models.
- Adding more writing genres and templates.
- Allowing users to edit and regenerate selected versions.
- Improving the content comparison system.
- Adding more export formats.
- Providing a history of previous writing requests.
- Creating a more user-friendly interface.

These improvements could make Creative Writer CLI more useful as a standalone AI writing application.

## 12. Conclusion

Creative Writer CLI is a Python application that demonstrates how the OpenAI API can be used for creative content generation.

Through this project, I gained practical experience with API integration, prompt customization, content generation, error handling and comparing AI-generated outputs.

The project also helped me understand how a command-line AI application can be developed and improved over time.

I plan to continue learning more about AI development and use the knowledge from this assignment in my future projects.

---

## Author and Project Information

**Author:** Lotus Nyaupane  
**GitHub Profile:** https://github.com/LotusNyaupane  
**Project Repository:** https://github.com/LotusNyaupane/AI_Tools_Lotus-  
**Original Assignment Group:** Dionysus  
**Group Members:** Udit Bhattarai, Lotus Nyaupane, Dipen Gaihre

*This project was developed for educational purposes as part of an AI API development assignment.*