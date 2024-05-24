# tempoChat

tempoChat is a real-time chat application built with Django, Django Channels, Redis, and PostgreSQL. The application supports user authentication, real-time messaging, and conversation management. Docker and Docker Compose are used to containerize the application for easy set.

## Features

- User signup and login
- Real-time messaging with WebSocket
- Conversation management
- Redis for message persistence
- PostgreSQL for user management and conversation metadata
- Bootstrap for styling

## Prerequisites

- Python >= 3.11.*
- Docker
- Docker Compose

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/gbolly/tempoChat.git
    cd tempoChat
    ```

## Configuration

### Environment Variables

The following environment variables are used in the `docker-compose.yml` file:

- Create a `.env` file in the root of the project and set the required environment variables:

    ```bash
    export SECRET_KEY=<your-secret-key>
    export DJANGO_SETTINGS_MODULE="tempoChat.settings"
    ```
    The SECRET_KEY has a default value in case you decide not to generate a new one. However, this is not encouraged as it is less secured.
    
    > **__NOTE__**: You can generate and copy a secret key(`SECRET_KEY`) for the django app by opening a django shell `python manage.py shell` and running;

    ```python
    from django.core.management.utils import get_random_secret_key  
    get_random_secret_key()
    ```
    if you get a permission denied build.sh, make it executable on your local by running;
    ```bash
    chmod +x build.sh
    ```
    Then rebuild the docker image.

## Usage

### Running the Application

Start the application with Docker Compose:

```bash
docker-compose up --build
```

The application will be available at `http://localhost:8000`.

### Chatting
- You need to create at least 2 users to start a chat. So, ensure you register 2 or more different users
- After logging in, you will be able to see other users and start a conversation.
- Open a conversation to start real-time chatting.

### Log Files
The project is setup with 3 log files which are located in the root directory of the project. They are;
- api.log: All the logs of API calls made can be found here.
- debug.log: For debug level bulogs.gs
- info.log: for info level logs.

### Test
To run unit test, run;

```bash
python manage.py test
```

### API Throttling
Rate limits occurs at 10calls/min. The server then gets disconnected when this happens.
You will have to wait 10 seconds for the connection to come up.

#### Implemention Details
Throttling implementation leverages Django cache to store message count for a user. When a message is received, a check is done against the last time the cache was accessed. If it is less than a minute, the cached message count is then used to check if the use has sent up to 10 messages. When this is true, the channel is disconnected and a message is sent to the client.

The client after receiving a 4001 code, also closes its socket and refreshes the page after 10 seconds to reconnect and start chatting again.


### Live
Visit [tempochat](https://tempochat.onrender.com/chat/) to access the project or follow the docker setup steps to test locally.
