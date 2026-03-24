# Agropreneur.ai Backend

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Train ML Models:
   ```bash
   python app/ml/train_models.py
   ```

3. Run Server:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
