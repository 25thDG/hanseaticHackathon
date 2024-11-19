FROM continuumio/miniconda3:main

WORKDIR /app

COPY environment.yml .
RUN conda env create -f environment.yml
SHELL ["conda", "run", "--no-capture-output", "-n", "container", "/bin/bash", "-c"]

COPY energy_prompt.jpg .
COPY final_prompt.py .
COPY stage_one.py .
COPY build-knowledge-base.py .
RUN python -u build-knowledge-base.py

COPY chatbot.py .
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "container", "streamlit", "run", "chatbot.py", "--server.address", "0.0.0.0"]

EXPOSE 8501
