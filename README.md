# TalentScout Chatbot — AI-Powered Hiring Assistant
Url : https://chatbothiring.streamlit.app/
TalentScout is a Streamlit-based chatbot application designed to assist with technical hiring processes. It helps recruiters and hiring managers conduct structured interviews by generating technical questions based on candidate profiles and facilitating conversation management.

## 🚀 Features

- **Candidate Profile Management**: Capture and store candidate information including skills, experience, and contact details
- **AI-Powered Question Generation**: Automatically generates technical questions using Google GenAI based on candidate's tech stack
- **Conversation Management**: Structured chat interface with session persistence
- **Input Validation**: Validates email addresses, phone numbers, and required fields
- **Responsive Design**: Clean, professional UI built with Streamlit

## 📋 Prerequisites

- Python 3.8+
- pip (Python package manager)
- Google Generative AI API key

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <your-repository-url>
   cd talentscout_chatbot
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   GOOGLE_API_KEY=your_google_genai_api_key_here
   ```

## 🔧 Configuration

### Environment Variables
- `GOOGLE_API_KEY`: Your Google Generative AI API key (required for question generation)

### Project Structure
```
talentscout_chatbot/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables (gitignored)
├── talentscout/          # Core application modules
│   ├── __init__.py
│   ├── conversation.py   # Conversation management
│   ├── llm_client.py     # Google GenAI integration
│   ├── prompts.py        # Prompt templates and text generation
│   └── utils.py          # Utility functions and validation
└── README.md
```

## 🚀 Usage

1. **Start the application**
   ```bash
   streamlit run app.py
   ```

2. **Fill candidate details** in the sidebar before starting the conversation
   - Full Name (required)
   - Email (required, validated)
   - Phone (required, validated)
   - Years of Experience
   - Desired Position(s)
   - Current Location
   - Tech Stack (comma-separated, required)

3. **Interact with the chatbot**
   - Type messages to have a conversation
   - Use "generate questions" to create technical questions based on the candidate's tech stack
   - Type "done" to end the conversation

4. **Review generated questions**
   - Questions are organized by technology in expandable sections
   - Copy questions for use in interviews

## 🧩 Modules

### `app.py`
Main Streamlit application with UI components and interaction logic.

### `talentscout/conversation.py`
Manages conversation state, message history, and session initialization.

### `talentscout/llm_client.py`
Handles communication with Google GenAI for question generation with fallback mechanisms.

### `talentscout/prompts.py`
Contains prompt templates, greeting messages, and text generation functions.

### `talentscout/utils.py`
Utility functions for input validation, tech stack parsing, and data processing.

## 🔒 Input Validation

- **Email Validation**: Uses email-validator library for proper email format validation
- **Phone Validation**: Validates phone numbers contain only digits
- **Required Fields**: Ensures essential candidate information is provided
- **Tech Stack Parsing**: Converts comma-separated strings into clean lists

## 🚨 Error Handling

The application includes robust error handling:
- Fallback question generation if LLM API calls fail
- Input validation with clear error messages
- Session state management to prevent crashes
- Graceful degradation when external services are unavailable

## 📊 Session State

The application maintains:
- Candidate information
- Conversation history
- Generated technical questions
- Conversation active status

## 🧪 Testing

To test the application:
1. Start the Streamlit server
2. Fill in valid candidate information
3. Test various conversation flows
4. Verify question generation works
5. Test input validation with invalid data

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section below
2. Review the code documentation
3. Create an issue in the repository

## 🔍 Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure `GOOGLE_API_KEY` is set in your `.env` file
2. **Import Errors**: Verify all dependencies are installed with `pip install -r requirements.txt`
3. **Streamlit Issues**: Check that Streamlit is properly installed and updated

### Getting API Key

1. Visit [Google AI Studio](https://makersuite.google.com/)
2. Create an account and generate an API key
3. Add the key to your `.env` file

## 📈 Future Enhancements

- [ ] Database integration for candidate storage
- [ ] Export functionality for interview notes
- [ ] Multi-language support
- [ ] Advanced analytics and reporting
- [ ] Integration with ATS systems
- [ ] Custom question templates
- [ ] Interview scoring system
