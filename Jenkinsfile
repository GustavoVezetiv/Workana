pipeline {
    agent any

    stages {
        stage('Preparar ambiente') {
            steps {
                echo '🔧 Instalando dependências'
                sh '''
                    python --version
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Rodar testes') {
            steps {
                echo '🧪 Rodando testes'
                sh 'python manage.py test'
            }
        }

        stage('Concluir') {
            steps {
                echo '✅ Pipeline concluído!'
            }
        }
    }
}
