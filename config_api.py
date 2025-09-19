"""This module loads the environment varibales necessary to run the project with
the models from OpenAI and when using LangSmith tracing.
Not necessary to run the project locally.

Functions:
- load_env(): Loads environment variables.

Exceptions:
- ImportError: Raised if environment variables are missing.
"""

__file__ = "config_api.py"
__version__ = "0.1"
__author__ = "Martin Brossard"
__copyright__ = "Copyright (C) 2025 Martin Brossard"
__license__ = "MIT"

import os
import getpass
from dotenv import load_dotenv


def load_env():
    """Load environment variables, if not available ask for user input."""
    try:
        # load environment variables from .env file
        load_dotenv()

    except ImportError:
        pass

    # LangSmith
    os.environ["LANGSMITH_TRACING"] = "true"

    if not os.environ.get("LANGSMITH_API_KEY"):
        os.environ["LANGSMITH_API_KEY"] = getpass.getpass(
            "Enter your LangSmith API key: "
        )

    if "LANGSMITH_PROJECT" not in os.environ:
        os.environ["LANGSMITH_PROJECT"] = getpass.getpass(
            "Enter your LangSmith Project Name: "
        )
        if not os.environ.get("LANGSMITH_PROJECT"):
            os.environ["LANGSMITH_PROJECT"] = "default"

    # OpenAI
    if not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"]= getpass.getpass(
            "Enter API key for OpenAI: "
            )
