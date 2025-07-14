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
- SQLite (padrão Django) ou PostgreSQL

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
```

---

## ✅ Testes automatizados

- Foram desenvolvidos **5 testes de interface com Katalon Studio** cobrindo os principais fluxos:
  - Cadastro de cliente
  - Cadastro de imóvel
  - Registro de locação
  - Exclusão de locação
  - Geração de relatório

Os arquivos estão disponíveis na pasta `/tests-katalon`.

---

## 🔧 Build automatizado com Jenkins

Um pipeline de build automatizado foi criado utilizando o Jenkins, com os seguintes estágios:

- Checkout do código
- Criação de ambiente virtual
- Instalação de dependências

---

## 📊 Análise de código com SonarCloud

O projeto está integrado com o [SonarCloud](https://sonarcloud.io/) para verificação de:

- Cobertura de testes
- Vulnerabilidades
- Bugs
- Code smells
- Dívida técnica

Arquivo de configuração: [`sonar-project.properties`](https://github.com/GustavoVezetiv/Workana/blob/main/SONARRELATORIO.pdf)

---

## 💡 Arquitetura do projeto

```bash
myapp/
├── models.py          # Modelos principais
├── forms.py           # Formulários Django
├── views.py           # Lógicas das páginas
├── urls.py            # Rotas do app
├── templates/         # HTMLs (com Bootstrap)
├── static/            # Arquivos estáticos
└── repositories/      # Repositórios injetáveis (Injeção de Dependência)
```

---

## 🧠 Padrões aplicados

- Injeção de Dependência nas views para facilitar testes e manutenção
- Separação de responsabilidades entre views, formulários e lógica de acesso a dados (repositórios)
- Views baseadas em função (FBV)

---

## 🤝 Contribuição

Contribuições são bem-vindas!  
Sinta-se à vontade para abrir **issues**, **pull requests** ou sugerir melhorias.

---

## 📄 Licença

Este projeto está sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.

---

## 👨‍💻 Autor

**Gustavo Vezetiv**  
[LinkedIn]([https://www.linkedin.com/in/gustavovezetiv](https://www.linkedin.com/in/gustavo-vezetiv-08416126b/)) | [GitHub](https://github.com/GustavoVezetiv)
