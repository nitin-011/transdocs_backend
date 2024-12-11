from flask_babel import Babel, _

babel = Babel()

# Supported languages
LANGUAGES = {
    'en': 'English',
    'fr': 'French',
}

def init_babel(app):
    app.config['BABEL_DEFAULT_LOCALE'] = 'en'
    app.config['BABEL_SUPPORTED_LOCALES'] = list(LANGUAGES.keys())
    babel.init_app(app)


def get_locale():
    # Default to 'en' if no language is set
    return 'en'

def get_translation(language_code):
    if language_code in LANGUAGES:
        return f"Language switched to {LANGUAGES[language_code]}"
    return "Invalid language selection"