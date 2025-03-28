from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# caminho para o CSV
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, "data", "Relatorio_cadop.csv") # Localizacao do CSV na maquina

try:
    df = pd.read_csv(
        csv_path,
        delimiter=';',
        encoding='latin1',
        on_bad_lines='skip',
        dtype={'Registro_ANS': str, 'CNPJ': str, 'CEP': str, 'Telefone': str}
    )
    print(f"Dados carregados com {len(df)} registros")
except Exception as e:
    print(f"Erro ao carregar CSV: {e}")
    df = pd.DataFrame()

@app.route("/buscar", methods=["GET"])
def buscar_operadora():
    if df.empty:
        return jsonify({"success": False, "message": "Dados não disponíveis"}), 503

    termo = request.args.get("q", "").strip().lower()
    
    if not termo:
        return jsonify({"success": False, "message": "Parâmetro de busca 'q' é obrigatório"}), 400
    
    if len(termo) < 3:
        return jsonify({
            "success": False,
            "message": "Termo de busca deve ter pelo menos 3 caracteres"
        }), 400

    try:
        # Busca aprimorada
        mask = (
            df["Razao_Social"].str.lower().str.startswith(termo, na=False) |
            df["Nome_Fantasia"].str.lower().str.startswith(termo, na=False) |
            df["Razao_Social"].str.lower().str.contains(termo, na=False) |
            df["Nome_Fantasia"].str.lower().str.contains(termo, na=False)
        )
        
        resultados = df[mask].head(20)
        
        return jsonify({
            "success": True,
            "message": "Busca realizada com sucesso",
            "count": len(resultados),
            "results": resultados.fillna('').to_dict(orient='records')
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro na busca: {str(e)}"
        }), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)