# 🏠 Sistema de Gerenciamento de Imóveis

Este projeto é um sistema web completo desenvolvido com Django, voltado para o gerenciamento de **imóveis, locações, contratos, pagamentos, manutenções, visitas e proprietários**.

---

## 📚 Funcionalidades

- Cadastro e edição de:
  - Clientes
  - Imóveis (com upload de imagens)
  - Contratos de locação
  - Pagamentos
  - Funcionários
  - Solicitações de manutenção
  - Visitas agendadas
  - Proprietários
- Registro de locações com vínculo ao imóvel
- Liberação automática do imóvel após exclusão da locação
- Relatórios com filtros por:
  - Cliente
  - Tipo de imóvel
  - Status (locado ou não)
  - Intervalo de datas
  - Proprietário
- Tela de confirmação para exclusões
- Upload múltiplo de imagens dos imóveis
- Injeção de Dependência aplicada nas views
- Pronto para análise com SonarCloud e build com Jenkins
- Demais explicações estarão no Documento da aplicação 😁
---

## 🚀 Tecnologias utilizadas

- [Python 3.12](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Bootstrap 5](https://getbootstrap.com/)
- HTML5 + CSS3
- SQLite (padrão Django) 

---

## 📦 Instalação local

```bash
# Clone o repositório
git clone https://github.com/GustavoVezetiv/Workana.git
cd Workana

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Aplique as migrações
python manage.py migrate

# Rode o servidor local
python manage.py runserver



