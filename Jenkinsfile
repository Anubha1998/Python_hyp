pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                // This step checks out your Python repository from version control (e.g., Git)
                checkout([$class: 'GitSCM', branches: [[name: 'main']], userRemoteConfigs: [[url: 'https://github.com/Anubha1998/Python_hyp.git']]])
            }
        }
        
        stage('Setup') {
            steps {
                // Set up any necessary environment (e.g., virtual environment)
                sh 'python -m venv venv'
                sh 'source venv/bin/activate'
                sh 'pip install -r requirements.txt'
            }
        }
        
        stage('Test') {
            steps {
                // Run your Python tests here
                sh 'python -m tests/JiraPython.py''
            }
        }
    }
    
    post {
        always {
            // Cleanup steps, if needed
            sh 'deactivate' // Deactivate the virtual environment
        }
        success {
            // Actions to take if the pipeline succeeds
        }
        failure {
            // Actions to take if the pipeline fails
        }
    }
}
