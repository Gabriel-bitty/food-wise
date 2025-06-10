# Food Wise

```bash - powershell - prompt

# Criar o .venv para nao ter conflitos
python -m venv .venv

# .venv para não ter conflitos com sua máquina

.venv\Scripts\activate

# Instalar as dependencias do Python
pip install -r requirements.txt

# Executar o Backend
cd src/food-wise-backend
npm install
npm start

# Para o Frontend
cd ../../
streamlit run src/app.py
```

## Dependencies

### Frontend (Python)
- Streamlit >= 1.28.0
- Requests >= 2.31.0
