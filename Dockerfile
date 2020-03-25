FROM continuumio/miniconda3

WORKDIR /app

# Create the environment:
COPY environment.yml .
RUN conda env create -f environment.yml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "pyviz37", "/bin/bash", "-c"]

# Make sure the environment is activated:
RUN echo "Make sure geoviews is installed:"
RUN python -c "import geoviews"

# The code to run when container is started:
COPY run.py .
COPY bin bin/
COPY data data/
COPY runpy2.py .

CMD ["bokeh", "serve", "run.py", "--address", "0.0.0.0"]
#ENTRYPOINT ["conda", "run", "-n", "pyviz37"]
# ENTRYPOINT ["conda", "run", "-n", "pyviz37", "python", "runpy2.py"]
#ENTRYPOINT ["conda", "run", "-n", "pyviz37", "bokeh", "serve", "run.py", "--address", "0.0.0.0"]
