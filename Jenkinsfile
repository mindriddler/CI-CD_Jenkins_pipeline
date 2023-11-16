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
        
        stage('Run Pytest') {
            steps {
                echo "Installing dependencies..."
                sh '''
                source ../venv/backend/venv/bin/activate && cd backend && pytest .
                '''
            }
        }


        stage('Run Pylint') {
            steps {
                echo "Running the script..."
                sh '''
                source ../venv/backend/venv/bin/activate && cd backend && pylint --fail-under 8 pingurl/
                '''
            }
        }


        stage('Build') {
            steps {
                script {
                    echo 'Deploying...'

                    try {
                        sh '''
                        docker build -t api -f Docker/Dockerfile.backend .
                        '''
                    } catch (Exception e) {
                        currentBuild.result = 'FAILURE!!!!!'
                        error("Failed to build Docker image: ${e.message}")
                    }
                }
            }
        }
    }
}
