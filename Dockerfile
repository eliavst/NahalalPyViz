FROM python:3.7-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
        libproj-dev proj-data proj-bin \
        libgeos-dev \
        # libgdal-dev \
        # libspatialindex-dev  \
        cython \
        g++
 
# Create the environment:
COPY requirements.txt .
RUN pip install shapely cartopy --no-binary shapely --no-binary cartopy
RUN pip install -r requirements.txt

# Make RUN commands use the new environment:
# Make sure the environment is activated:
RUN echo "Make sure geoviews is installed:"
RUN python -c "import geoviews"

# The code to run when container is started:
COPY run.py .
COPY bin bin/
COPY data data/




# EXPOSE 5006 
# EXPOSE 80

VOLUME /app
EXPOSE 5006

# CMD ["bokeh", "serve", "run.py", "--address", "0.0.0.0"]

CMD ["bokeh", "serve", "run.py"]
#ENTRYPOINT ["conda", "run", "-n", "pyviz37"]
# ENTRYPOINT ["conda", "run", "-n", "pyviz37", "python", "runpy2.py"]
#ENTRYPOINT ["conda", "run", "-n", "pyviz37", "bokeh", "serve", "run.py", "--address", "0.0.0.0"]
