pipeline {
    agent any
    triggers {
        pollSCM 'H/15 * * * *'
    }


    stages {
        
        stage('Checkout') {
            steps {
                echo 'Checking out the git repository...'
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[url: 'https://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@github.com/nackc8/cicd-grp--leeroy.git']])
            }
        }

        stage('Creating venv') {
            steps {
                echo "Installing dependencies..."
                sh '''
                cd backend && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
                '''
            }
        }

        stage('Build') {
            steps {
                script {
                    def containerExists = sh(script: 'docker ps -a | grep api >/dev/null', returnStatus: true) == 0

                    if (containerExists) {
                        sh 'docker stop api || true'
                        sh 'docker rm api || true'
                    }

                    sh 'docker build -t api -f Docker/Dockerfile.backend .'
                }
            }
        }

        stage('Run Container') {
            steps {
                echo "Running the script...."
                sh '''
                docker run -d -p 5000:5000 --name api api
                '''
            }
        }       
        stage('Run Pytest') {
            steps {
                echo "Running Pytest..."
                sh '''
                source ./backend/venv/bin/activate && pytest backend/
                '''
            }
        }

        stage('Run Pylint') {
            steps {
                echo "Running Pylint..."
                sh '''
                source ./backend/venv/bin/activate && pylint --fail-under 8 backend/pingurl/ --rcfile=backend/pyproject.toml
                '''
            }
        }
    }
}
