#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Run migrations (if needed)
# alembic upgrade head

# Start the server
uvicorn main:app --host 0.0.0.0 --port 8000
