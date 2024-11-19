FROM git.mylab.th-luebeck.de:4181/hackathon/base-images/hhack-base:2024

WORKDIR /app

ADD chatbot.py .
CMD ["streamlit", "run", "chatbot.py", "--server.address", "0.0.0.0"]

EXPOSE 8501