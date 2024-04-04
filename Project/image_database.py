import sqlite3
import io

def initialize_database(database_name='image_database.db'):
    """
    Initializes the database connection. If the database exists, it will use it;
    otherwise, it will create a new one.

    Args:
        database_name (str): Name of the SQLite database file.

    Returns:
        sqlite3.Connection: Database connection object.
    """
    conn = sqlite3.connect(database_name)
    return conn

def store_image(conn, image, tags):
    """
    Stores an image and its corresponding tags in the database.

    Args:
        conn (sqlite3.Connection): Database connection object.
        image_data (bytes): Binary data of the image.
        tags (str): Comma-separated string of tags associated with the image.
    """
    image_bytes = io.BytesIO()
    image.save(image_bytes, format=image.format)
    image_data = image_bytes.getvalue()

    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS images
                 (id INTEGER PRIMARY KEY, image BLOB, tags TEXT)''')
    c.execute('INSERT INTO images (image, tags) VALUES (?, ?)', (sqlite3.Binary(image_data), tags))
    conn.commit()

def query_images(conn, tags):
    """
    Queries the database using the provided tags and returns the images.

    Args:
        conn (sqlite3.Connection): Database connection object.
        tags (str): Comma-separated string of tags to search for.

    Returns:
        list: List of image data retrieved from the database.
    """
    c = conn.cursor()
    c.execute('SELECT image FROM images WHERE tags LIKE ?', ('%' + tags + '%',))
    result = c.fetchall()
    return result

# Example usage:
# conn = initialize_database()
# image_data = open('image.jpg', 'rb').read()
# tags = 'nature, landscape, mountains'
# store_image(conn, image_data, tags)
# images = query_images(conn, 'landscape')
# for image in images:
#     display_image(image[0])
