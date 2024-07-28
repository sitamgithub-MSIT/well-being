# Well-Being

This project aims to reduce neonatal and under-5 mortality rates by the year 2030 through information dissemination and raising awareness. It utilizes an Artificial Conversational Entity powered by the Gemini API.

## Project Structure

The project is structured as follows:

- `assets`: This directory contains the output responses screenshots.

- `src`: This directory contains the source code for the project.

  - `chat.py`: This file contains the code for the chat updating the conversation history.
  - `config.py`: This file contains the model configuration settings for the project.
  - `llm_response.py`: This file contains the code for the language model response.
  - `prompt.py`: This file contains the system prompt for the project.
  - `utils.py`: This file contains utility functions for the project.

- `app.py`: This file contains the code for the Gradio application.
- `.env.example`: This file contains the environment variables required for the project.
- `requirements.txt`: This file contains the required dependencies for the project.
- `README.md`: This file contains the project documentation.
- `LICENSE`: This file contains the project license.

## Tech Stack

- Python: Python is used as the primary programming language for this project.
- Gemini API: These APIs provide advanced natural language processing and computer vision capabilities.
- Gradio: Gradio is used for building interactive UIs for the chat interface.
- Hugging Face Spaces: Hugging Face spaces is used for collaborative development and deployment of the gradio application.

## Getting Started

To get started with this project, follow the steps below:

1. Clone the repository: `git clone https://github.com/sitamgithub-MSIT/well-being.git`
2. Create a virtual environment: `python -m venv tutorial-env`
3. Activate the virtual environment: `tutorial-env\Scripts\activate`
4. Install the required dependencies: `pip install -r requirements.txt`
5. Run the Gradio application: `python app.py`

Now, open up your local host and you should see the web application running. For more information, refer to the Gradio documentation [here](https://www.gradio.app/docs/interface). Also, a live version of the application can be found [here](https://sitammeur-well-being.hf.space/).

## Usage

Once the application is up and running, you can interact with the conversational entity through the provided UI. It can answer questions, provide information, and raise awareness about neonatal and under-5 mortality.

## Contributing

Contributions are welcome! If you would like to contribute to this project, please raise an issue to discuss the changes you would like to make. Once the changes are approved, you can create a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any inquiries or feedback, please contact the project team at their GitHub profiles: [Sitam](https://github.com/sitamgithub-MSIT), [Aharna](https://github.com/aharna), [Avirup](https://github.com/avirupnandi1).

Happy coding! 🚀
