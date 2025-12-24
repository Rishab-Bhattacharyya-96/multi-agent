from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

def get_book_recommendations(genre:str, tool_context: ToolContext) -> dict:
    """Return a mock book recommendation for a given genre."""
    print(f"--- Tool: get_book_recommendations called with genre: {genre} ---")

    genre_key = genre.lower()

    books = {
        'fantasy': {
            'title': 'The Hobbit',
            'author': 'J.R.R. Tolkien',
            'description': 'A fantasy novel about the adventures of Bilbo Baggins.'
        },
        'science fiction': {
            'title': 'Dune',
            'author': 'Frank Herbert',
            'description': 'A science fiction novel set in a distant future amidst a huge interstellar empire.'
        },
        'mystery': {
            'title': 'The Hound of the Baskervilles',
            'author': 'Arthur Conan Doyle',
            'description': 'A mystery novel featuring Sherlock Holmes.'
        },
        'romance': {
            'title': 'Pride and Prejudice',
            'author': 'Jane Austen',
            'description': 'A classic romance novel about manners and matrimonial machinations.'
        },
        'non-fiction': {
            'title': 'Sapiens: A Brief History of Humankind',
            'author': 'Yuval Noah Harari',
            'description': 'A non-fiction book exploring the history of humankind.'
        }
    }

    result = books.get(genre_key, {
        'title': 'Unknown Genre',
        'author': 'N/A',
        'description': 'No recommendations available for this genre.'
    })

    tool_context.state['last_book_genre'] = genre_key

    return {
        'status': 'success',
        'book': result,
        'genre': genre
    }

book_recommender = Agent(
    model='gemini-2.5-flash',
    name='book_recommender',
    description='Recommends books based on user preferences.',
    instruction="""
    You are a helpful book recommender assistant.

    When the user asks for a book recommendation:
    1. If they specify a genre (e.g., fantasy, science fiction, mystery, romance, non-fiction) call get_book_recommendations with the specified genre.
    2. If they do not specify a genre, as which genre they prefer.
    3. Format your response to include:
         - Title
         - Author
         - Description

    Example response:
    "Here's a great sci-fi recommendation for you:

    *Dune* by Frank Herbert.
    Why: A science fiction novel set in a distant future amidst a huge interstellar empire."

    If the user asks for anything unrelated to book recommendations,
    delegate the task to the manager agent.
    """,
    tools=[get_book_recommendations],

)
