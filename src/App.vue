<template>
  <div class="container">
    <h1>Busca de Operadoras de Saúde</h1>
    <div class="search-box">
      <input
        v-model="termo"
        @input="onSearchInput"
        placeholder="Digite o nome da operadora..."
        class="search-input"
      />
      <div v-if="loading" class="loading">Buscando...</div>
      <div v-if="error" class="error-message">{{ error }}</div>
    </div>

    <div v-if="operadoras.length > 0" class="results-container">
      <h2>Resultados ({{ operadoras.length }})</h2>
      <div class="operadora-card" v-for="op in operadoras" :key="op.Registro_ANS">
        <h3>{{ op.Nome_Fantasia || op.Razao_Social }}</h3>
        <div class="operadora-details">
          <p v-if="op.Registro_ANS"><strong>Registro ANS:</strong> {{ op.Registro_ANS }}</p>
          <p v-if="op.CNPJ"><strong>CNPJ:</strong> {{ formatCNPJ(op.CNPJ) }}</p>
          <p v-if="op.Modalidade"><strong>Modalidade:</strong> {{ op.Modalidade }}</p>
          <p v-if="op.Cidade || op.UF">
            <strong>Localização:</strong> 
            {{ [op.Cidade, op.UF].filter(Boolean).join(' - ') }}
          </p>
        </div>
      </div>
    </div>

    <div v-else-if="termo.length >= 3 && !loading" class="no-results">
      Nenhuma operadora encontrada para "{{ termo }}"
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { debounce } from 'lodash';

export default {
  data() {
    return {
      termo: '',
      operadoras: [],
      loading: false,
      error: null
    };
  },
  methods: {
    onSearchInput: debounce(function() {
      if (this.termo.length >= 3) {
        this.buscarOperadoras();
      } else {
        this.operadoras = [];
      }
    }, 500),
    
    async buscarOperadoras() {
      this.loading = true;
      this.error = null;
      try {
        const response = await axios.get(`http://localhost:5000/buscar`, {
          params: { q: this.termo }
        });
        
        if (response.data.success) {
          this.operadoras = response.data.results;
        } else {
          this.error = response.data.message;
          this.operadoras = [];
        }
      } catch (err) {
        console.error("Erro na busca:", err);
        this.error = "Erro ao buscar operadoras. Tente novamente.";
        this.operadoras = [];
      } finally {
        this.loading = false;
      }
    },
    
    formatCNPJ(cnpj) {
      return cnpj.replace(/^(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})$/, '$1.$2.$3/$4-$5');
    }
  }
};
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  font-family: 'Arial', sans-serif;
}

h1 {
  color: #2c3e50;
  text-align: center;
  margin-bottom: 30px;
}

.search-box {
  margin-bottom: 30px;
}

.search-input {
  width: 100%;
  padding: 12px 15px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: all 0.3s;
}

.search-input:focus {
  outline: none;
  border-color: #42b983;
  box-shadow: 0 2px 8px rgba(66, 185, 131, 0.2);
}

.loading {
  margin-top: 10px;
  color: #42b983;
}

.error-message {
  margin-top: 10px;
  color: #e74c3c;
}

.results-container {
  margin-top: 20px;
}

.operadora-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 15px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  transition: transform 0.2s;
}

.operadora-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.operadora-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}

.operadora-header h3 {
  margin: 0;
  color: #2c3e50;
}

.badge {
  background: #42b983;
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
}

.operadora-details p {
  margin: 5px 0;
  color: #555;
}

.no-results {
  text-align: center;
  padding: 20px;
  color: #7f8c8d;
  font-style: italic;
}

@media (max-width: 600px) {
  .container {
    padding: 10px;
  }
  
  .operadora-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .badge {
    margin-top: 5px;
  }
}
</style>