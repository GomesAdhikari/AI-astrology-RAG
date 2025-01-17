# AI Astrology Web App

A powerful web app that provides horoscope analysis based on planetary positions, compares birth charts of couples, and answers extravagant astrological queries using AI-powered features. This app leverages modular coding, making it scalable and easy to maintain.

## Features

- **Horoscope Generation**: Generate horoscope analysis based on planetary positions at the time of birth.
- **Couple Birth Chart Comparison**: Compare the birth charts of two individuals to determine compatibility.
- **Astro AI Chat**: Ask any extravagant queries and get personalized astrological answers using the Gemini API.
- **Astrology for Vedic**: Access a PDF version of "Astrology for Vedic" through the Astrobook holder.
- **Modular Codebase**: Clean and efficient modular coding with separate components for different functionalities.

## Tech Stack

- **Backend**: Python
- **Frontend**: HTML, CSS, JavaScript
- **API**: Gemini API
- **Libraries**: FAISS (for indexing and retrieval), Flask (for web app functionality)
- **Data Source**: PDF of "Astrology for Vedic" for the astrology book

## File Organization

- **Astrobook holder**: Contains the PDF file of "Astrology for Vedic."
- **FAISS Index**: Four files used for indexing and query handling.
  - `chat.py`: Handles chat queries.
  - `get_astrology_pi.py`: Retrieves astrology information.
  - `get_geo_details.py`: Fetches geographic details.
  - `get_horoscope.py`: Retrieves horoscope based on birth date and planetary positions.
- **Static Folder**: Contains CSS and images used in the app.
- **Templates Folder**: Includes HTML templates for various pages such as birth chart, dashboard, and horoscope views.
  - `base.html`: Base template for all pages.
  - `birth_chart.html`: Displays birth chart details.
  - `chat.html`: Chat interface for the Astro AI.
  - `compare.html`: Compares the birth charts of two people.
  - `horoscope.html`: Displays the generated horoscope.
  - `dashboard.html`: Main dashboard page.
  - `welcome.html`: Welcome page for users.
- **setup.py**: Setup file for initializing the environment.
- **exp.ipynb**: Jupyter notebook for exploration.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/ai-astrology-web-app.git
    ```

2. Navigate to the project directory:

    ```bash
    cd ai-astrology-web-app
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the app:

    ```bash
    python setup.py
    ```

5. Access the web app by navigating to `http://localhost:5000` in your browser.

## Folder Structure

```bash
.
├── Astrobook holder
│   └── astrology_for_vedic.pdf
├── FAISS Index
│   ├── chat.py
│   ├── get_astrology_pi.py
│   ├── get_geo_details.py
│   └── get_horoscope.py
├── static
│   ├── css
│   │   └── style.css
│   └── images
├── templates
│   ├── base.html
│   ├── birth_chart.html
│   ├── chat.html
│   ├── compare.html
│   ├── horoscope.html
│   ├── dashboard.html
│   └── welcome.html
├── setup.py
└── exp.ipynb
