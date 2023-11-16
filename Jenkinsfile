pipeline {
    triggers {
        pollSCM '*/15 * * * *'
    }


    stages {

        stage('Step 1 - Change the name') {
            steps {
                echo "Installing dependencies..."
                sh '''
                echo "Needs some code here"
                '''
            }
        }


        stage('Step 2 - Change the name') {
            steps {
                echo "Running the script..."
                sh '''
                echo "Needs some code here"
                '''
            }
        }


        stage('Step 3 - Change the name') {
            steps {
                echo 'Deploying...'
                sh '''
                echo "Deploying to production environment"
                '''
            }
        }

    }
}