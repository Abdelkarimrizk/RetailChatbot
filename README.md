<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#technology-stack-and-why-each-was-chosen">Technology Stack and Why Each was Chosen</a>
    </li>
    <li>
      <a href="#possible-improvements">Possible Improvements</a>
    </li>
    <li>
      <a href="#api-reference">API Reference</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installing-and-running-locally">Installing and Running Locally</a></li>
        <li><a href="#running-and-deploying-with-docker">Running and Deploying with Docker</a></li>
      </ul>
    </li>
    <li><a href="#demo">Demo</a></li>
    <li><a href="#test-it-yourself">Test it yourself</a></li>
    <li><a href="#references">References</a></li>
  </ol>
</details>

# Iris Retail Chatbot

<!-- ABOUT THE PROJECT -->
## About The Project

Iris is an AI chatbot created for a generic ecommerce store. It helps users with text-based and image-based product recommendations.

This project was built using Flask and React, and it is deployed using Docker on a private virtual server (Hetzner).

link: https://retailchatbot.cv/

**Key Features:**
- Answer general store/product questions
- Recommend products based on user text input.
- Find and match uploaded user images to similar product sold.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Technology Stack and Why Each was Chosen  -->
## Technology Stack and Why Each was Chosen

| Component | Technology | Why I Chose It              |
|-----------|------------|-----------------------------|
| Frontend  | React + Tailwind CSS | I have previous experience with react and tailwind through another<br> project I am currently working on. |
| Backend | Flask (Python) | Lightweight, flexible, and most straightforward to use given the timeframe. |
| AI Response | OpenAI GPT-4o mini | Fast, light, and one of the better customer facing models. |
| AI Logic | OpenAI GPT-4.1 nano | Extremely fast, efficient, and light, perfect for simple classification. |
| Text Embedding | OpenAI text-embedding-3-small | Optimized for storage and latency, helping embed text faster. |
| Image Embedding | HuggingFace Google ViT | Light and quick, allowing for almost immediate image embedding. |
| Deployment | Docker + Gunicorn | Docker helps make deployment simple and it allows for cross platform use, and Gunicorn helps the website handle traffic |
| Hosting | Hetzner | I already owned a server with enough ram and cpu power, allowing for more control and faster use.  |


<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Possible Improvements  -->
## Possible Improvements

There are a few features I would have liked to include, but unfortunately, I was not able to implement them within the time frame.

- **Text Streaming**: Streaming the response as soon as it started generating would have made the chatbot seem faster.
- **Image Responses**: Including image resposes with the replies would improve the user experience by allowing them to see what is recommended/found.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- API Reference -->
## API Reference

### `POST /api/chat`

**Request Sample:**

```json
 {
  "message": "Can you recommend a good monitor?",
  "image": "<optional image>",
  "history": [
    {"role": "user", "content": "What is your name?"},
    {"role": "assistant", "content": "My name is Iris. How can I assist you today?"}
  ]
}
```

**Response Sample:**

```json
{
  "reply": "Here are a few monitors you might like...",
  "history": [
    {"role": "user", "content": "What is your name?"},
    {"role": "assistant", "content": "My name is Iris. How can I assist you today?"}
    {"role": "user", "content": "Can you recommend a good monitor?"},
    {"role": "assistant", "content": "Here are a couple of monitors that I can recommend: ..."}
  ]
}
```


<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

These instructions will help you set up the project locally.

### Prerequisites

Make sure you have:
- python 3.10 or higher
-  Node.js 
-  An OpenAI API key
-  Docker setup and running

### Installing and Running Locally

1. Clone the repo:
   ```sh
   git clone https://github.com/Abdelkarimrizk/RetailChatbot.git
   ```
2. Enter the api folder
   ```sh
   cd react-with-flask/api
   ```
3. Set up a virtual environment:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
4. Install the requirments:
   ```sh
   pip install -r requirements.txt
   ```
5. Create the .env file and write:
   ```ini
   OPENAI_API=your_openai_api_key
   FLASK_APP=app.py
   FLASK_ENV=development
   ```
6. go back to the react-with-flask folder:
   ```sh
   cd ..
   ```
8. Run the frontend and backend on two separate terminals using:
   ```sh
   npm run dev
   ```
   and
   ```sh
   npm run api
   ```
### Running and Deploying with Docker

1. Make sure you are in react-with-flask
2. Build the Dockerfile:
   ```sh
   docker build -t iris-chatbot .
   ```
3. Start the website using Docker:
   ```sh
   docker run -d \
   --restart=always \
   --env-file api/.env \
   -p 8000:8000 \
   --name iris \
   iris-chatbot
   ```
   - -d: detached mode
   - --restart=always: auto restarts
   - --env-file: loads the env variable (openai api key)
   - -p 8000:8000 : maps the docker container port to the host port
   - --name: adds a name for the container
   - iris-chatbot: the docker image built in the previous step
4. Check if the website is running using both:
   ```sh
   docker ps
   ```
   and visiting http://vps-ip:8000
5. Stop the server:
   ```sh
   docker stop iris
   ```
6. Remove and rebuild:
   ```sh
   docker rm -f iris
   docker build -t iris-chatbot .
   ```
7. If you are having disk space issues, look into docker pruning.

### HTTPS Setup

If you own your own domain, you can follow these steps to enable https through Nginx and Certbot

1. install Nginx and Certbot
   ```sh
   sudo apt install nginx certbot python3-certbot-nginx
   ```
2. Create a new Nginx file:
   ```sh
   sudo nano /etc/nginx/sites-available/iris
   ```
   and paste (replacing yourdomain.com with your own domain):
   ```sh
   server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
   }
   ```
3. Enable the file:
   ```sh
   sudo ln -s /etc/nginx/sites-available/iris /etc/nginx/sites-enabled/
   ```
4. Reload Nginx:
   ```sh
   sudo nginx -t && sudo systemctl reload nginx
   ```
5. Run Certbot (replacing yourdomain.com with your own domain):
   ```sh
   sudo certbot --nginx -d yourdomain.com
   ```
6. Assuming that succeeds, you can now open your website with https://yourdomain.com


<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Demo -->
## Demo

Here are some examples of the bot in use: 

### Empty Page:
![image](https://github.com/user-attachments/assets/4276f66d-26a6-40ed-a005-164c592fd3b8)

### General Conversation and a Recommendation Request:
![image](https://github.com/user-attachments/assets/9573b755-4646-4f5b-9279-7120fdb2c7d1)

### Image Search:
![image](https://github.com/user-attachments/assets/54d92a0b-1743-4cd5-8b35-6b0813b49861)

### Follow Up Question:
![image](https://github.com/user-attachments/assets/733f15fb-8131-4406-a86b-98289faa8fdc)

<!-- Test it yourself -->
## Test it yourself

You can copy any of the following images onto your clipboard and paste it in https://retailchatbot.cv
(All images can be found in react-with-flask/api/agent/data/images)

![image](https://github.com/user-attachments/assets/32198ab4-a711-4ca3-9d2e-3df11f0e9c4f)

![image](https://github.com/user-attachments/assets/18d6a548-de63-4436-bb77-6e70873edc21)

![image](https://github.com/user-attachments/assets/df772a4e-425b-4d6c-8a3d-4090fc49e9b8)


<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- References -->
## References

- FakeStoreAPI.com for the mock data
- OpenAI.com for GPT-4o-mini, GPT-4.1-nano, and text-embedding-3-small
- HuggingFace for google/vit-base-patch16-224
- miguelgrinberg.com for the flask and react setup

<p align="right">(<a href="#readme-top">back to top</a>)</p>
